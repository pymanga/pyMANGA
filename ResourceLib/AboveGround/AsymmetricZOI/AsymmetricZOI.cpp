// ResourceLib/AboveGround/AsymmetricZOI/AsymmetricZOI.cpp
//
// Summary
// -------
// Pybind11 C++ core for the Asymmetric Zone of Influence (ZOI) above-ground
// competition model. For each grid cell, the tallest competing plant "wins"
// according to a crown height profile.
//
// Important
// ---------
// This C++ module mirrors the Python AsymmetricZOI logic, including support for
// cylindrical above-ground plant geometry. For cylinder geometries, the plant
// height is constant within the above-ground radius:
//
//     height = h_stem
//
// For non-cylinder geometries, the legacy crown logic is used:
//
//     curved crown: height = h_stem + sqrt(4 * r_ag^2 - distance^2)
//     flat crown  : height = h_stem + 2 * r_ag
//
// The per-plant aboveground resource factor is computed as:
//
//     wins / crown_area
//
// Notes
// -----
// - Inputs are provided as NumPy arrays from Python.
// - All internal computation uses double precision to match the Python path.
// - OpenMP parallelizes the loop over grid cells for each plant if available.
// - n_threads is now used if > 0; otherwise all available processors are used.
//
// Safety / Validation
// -------------------
// - Consistency checks for array sizes and grid shapes.
// - Detects oversize grids for 32-bit indexing safety.
// - Throws on NaN in the final result to surface unexpected conditions.

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <vector>
#include <cmath>
#include <cstdint>
#include <stdexcept>
#include <limits>
#include <sstream>
#include <algorithm>
#include <climits>

namespace py = pybind11;

#ifdef _OPENMP
  #include <omp.h>
#endif


// compute_aboveground_resources
// Parameters
//   xe, ye       : 1D (n_plants) arrays of plant positions
//   h_stem       : 1D (n_plants) stem/base heights or cylinder heights
//   r_ag         : 1D (n_plants) above-ground/crown radii
//   is_cylinder  : 1D (n_plants) bool array;
//                  true  -> cylindrical saltmarsh geometry, height = h_stem
//                  false -> legacy crown geometry
//   grid_x/y     : 2D coordinate arrays for the grid
//   curved_crown : if true, curved crown profile h + sqrt(4 r^2 - d^2);
//                  else flat h + 2r
//   mesh_size    : grid mesh size used for minimum-radius handling
//   n_threads    : OpenMP thread count; -1 -> auto
// Returns
//   1D (n_plants) float64 array with per-plant aboveground resource factor
py::array_t<double> compute_aboveground_resources(
    py::array_t<double, py::array::c_style | py::array::forcecast> xe,
    py::array_t<double, py::array::c_style | py::array::forcecast> ye,
    py::array_t<double, py::array::c_style | py::array::forcecast> h_stem,
    py::array_t<double, py::array::c_style | py::array::forcecast> r_ag,
    py::array_t<bool,   py::array::c_style | py::array::forcecast> is_cylinder,
    py::array_t<double, py::array::c_style | py::array::forcecast> grid_x,
    py::array_t<double, py::array::c_style | py::array::forcecast> grid_y,
    bool curved_crown,
    double mesh_size,
    int n_threads /* -1 -> auto */
) {
    // Basic input validation & grid bookkeeping
    const int n_plants = static_cast<int>(xe.size());

    if (
        ye.size() != xe.size() ||
        h_stem.size() != xe.size() ||
        r_ag.size() != xe.size() ||
        is_cylinder.size() != xe.size()
    ) {
        throw std::invalid_argument(
            "xe, ye, h_stem, r_ag, and is_cylinder must have same length"
        );
    }

    if (grid_x.ndim() != 2 || grid_y.ndim() != 2) {
        throw std::invalid_argument("grid_x and grid_y must be 2D");
    }

    if (
        grid_x.shape(0) != grid_y.shape(0) ||
        grid_x.shape(1) != grid_y.shape(1)
    ) {
        throw std::invalid_argument("grid_x and grid_y must have same shape");
    }

    const int gy = static_cast<int>(grid_x.shape(0));
    const int gx = static_cast<int>(grid_x.shape(1));

    if (gy <= 0 || gx <= 0 || static_cast<long long>(gy) * static_cast<long long>(gx) > INT32_MAX) {
        throw std::runtime_error("grid too large for 32-bit indexing");
    }

    const int grid_size = gy * gx;

#ifdef _OPENMP
    omp_set_dynamic(0);
    if (n_threads > 0) {
        omp_set_num_threads(n_threads);
    } else {
        omp_set_num_threads(omp_get_num_procs());
    }
#endif

    // Raw pointers for tight loops
    const double* px = xe.data();
    const double* py_ = ye.data();
    const double* ph = h_stem.data();
    const double* pr = r_ag.data();
    const bool* pcyl = is_cylinder.data();

    const double* pgx = grid_x.data();
    const double* pgy = grid_y.data();

    // Derive actual grid spacings from the grid arrays
    const double x_step = (gx > 1) ? (pgx[1] - pgx[0]) : mesh_size;
    const double y_step = (gy > 1) ? (pgy[gx] - pgy[0]) : mesh_size;

    // Grid origin: first cell center
    const double origin_x = pgx[0];
    const double origin_y = pgy[0];

    // Working buffers
    // canopy     : tallest crown/cylinder height found for each grid cell
    // winner     : index of plant currently owning the cell, -1 = none
    // crown_area : per-plant number of grid cells within its footprint
    // wins       : per-plant number of cells where this plant is tallest
    std::vector<double> canopy(grid_size, 0.0);
    std::vector<int32_t> winner(grid_size, -1);
    std::vector<double> crown_area(n_plants, 0.0);
    std::vector<double> wins(n_plants, 0.0);

    // Main loop: for each plant, update canopy winners over its crown/cylinder footprint
    for (int i = 0; i < n_plants; ++i) {
        double x = px[i];
        double y = py_[i];
        double h = ph[i];
        double r = pr[i];
        bool cylinder = pcyl[i];

        // Per-plant minimum distance to nearest grid cell center.
        // Mirrors Python:
        //     min_distance = np.min(distance)
        //     if crown_radius < min_distance: crown_radius = min_distance
        int ix = std::clamp(
            static_cast<int>(std::round((x - origin_x) / x_step)),
            0,
            gx - 1
        );

        int iy = std::clamp(
            static_cast<int>(std::round((y - origin_y) / y_step)),
            0,
            gy - 1
        );

        double ndx = pgx[iy * gx + ix] - x;
        double ndy = pgy[iy * gx + ix] - y;
        double min_dist = std::sqrt(ndx * ndx + ndy * ndy);

        if (r < min_dist) {
            r = min_dist;
        }

        const double r2 = r * r;
        int local = 0;

        // Iterate all grid cells; compare using sqrt(d2) to match Python.
        // Python:
        //     bools = crown_radius >= distance
#ifdef _OPENMP
        #pragma omp parallel for schedule(static) reduction(+:local)
#endif
        for (int idx = 0; idx < grid_size; ++idx) {
            double dx = pgx[idx] - x;
            double dy = pgy[idx] - y;
            double d2 = dx * dx + dy * dy;
            double dist = std::sqrt(d2);

            if (r >= dist) {
                double cell_h;

                // This is the important transferred AZOI change:
                // For cylindrical above-ground geometry, height is constant.
                if (cylinder) {
                    cell_h = h;
                } else if (curved_crown) {
                    cell_h = h + std::sqrt(std::max(0.0, 4.0 * r2 - d2));
                } else {
                    cell_h = h + 2.0 * r;
                }

                // Strict tie-break matches Python:
                // indices = np.where(np.less(canopy_height, my_height))
                if (cell_h > canopy[idx]) {
                    canopy[idx] = cell_h;
                    winner[idx] = i;
                }

                local += 1;
            }
        }

        crown_area[i] = static_cast<double>(local);
    }

    // Accumulate wins per plant from the winner map
    for (int idx = 0; idx < grid_size; ++idx) {
        int w = winner[idx];
        if (w >= 0) {
            wins[w] += 1.0;
        }
    }

    // Normalize to get per-plant resource factor; NaN guard
    py::array_t<double> out(n_plants);
    auto o = out.mutable_unchecked<1>();

    for (int i = 0; i < n_plants; ++i) {
        double denom = crown_area[i];

        o(i) = (denom > 0.0)
            ? (wins[i] / denom)
            : std::numeric_limits<double>::quiet_NaN();

        if (o(i) != o(i)) {
            throw std::runtime_error(
                "NaN detected in aboveground_resources for plants at index: " +
                std::to_string(i)
            );
        }
    }

    return out;
}


// pybind11 module declaration
// Exposes the function compute_aboveground_resources to Python.
PYBIND11_MODULE(asymzoi, m) {
    m.doc() = "Asymmetric ZOI CPP core matching Python AsymmetricZOI logic";

    m.def(
        "compute_aboveground_resources",
        &compute_aboveground_resources,
        py::arg("xe"),
        py::arg("ye"),
        py::arg("h_stem"),
        py::arg("r_ag"),
        py::arg("is_cylinder"),
        py::arg("grid_x"),
        py::arg("grid_y"),
        py::arg("curved_crown"),
        py::arg("mesh_size"),
        py::arg("n_threads") = -1
    );
}
