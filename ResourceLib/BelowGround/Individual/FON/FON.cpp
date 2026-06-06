// ResourceLib/BelowGround/Individual/FON/FON.cpp
//
// Pybind11 C++ core for the Field of Neighborhood (FON) below-ground
// competition model (Berger & Hildenbrandt 2000, Eq. 7).
//
// Key optimizations over the Python path:
// - Grid spatial indexing: only cells within FON radius are visited.
// - No 3D tensor allocation.
// - OpenMP parallelization.
// - PBC via minimum image convention with wrapped index ranges.

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <vector>
#include <cmath>
#include <cstdint>
#include <stdexcept>
#include <algorithm>
namespace py = pybind11;

#ifdef _OPENMP
  #include <omp.h>
#endif

py::array_t<double> compute_belowground_resources(
    py::array_t<double, py::array::c_style | py::array::forcecast> xe,
    py::array_t<double, py::array::c_style | py::array::forcecast> ye,
    py::array_t<double, py::array::c_style | py::array::forcecast> r_stem,
    py::array_t<double, py::array::c_style | py::array::forcecast> aa,
    py::array_t<double, py::array::c_style | py::array::forcecast> bb,
    py::array_t<double, py::array::c_style | py::array::forcecast> fmin,
    py::array_t<double, py::array::c_style | py::array::forcecast> phi,
    py::array_t<double, py::array::c_style | py::array::forcecast> grid_x,
    py::array_t<double, py::array::c_style | py::array::forcecast> grid_y,
    bool periodic, double lx, double ly,
    int n_threads) {

    const int n_plants = (int)xe.size();
    if (ye.size() != n_plants || r_stem.size() != n_plants ||
        aa.size() != n_plants || bb.size() != n_plants ||
        fmin.size() != n_plants || phi.size() != n_plants)
        throw std::invalid_argument("All plant arrays must have same length");
    if (grid_x.ndim() != 2 || grid_y.ndim() != 2)
        throw std::invalid_argument("grid_x and grid_y must be 2D");
    if (grid_x.shape(0) != grid_y.shape(0) || grid_x.shape(1) != grid_y.shape(1))
        throw std::invalid_argument("grid_x and grid_y must have the same shape");

    const int gy = (int)grid_x.shape(0), gx = (int)grid_x.shape(1);
    const int grid_size = gy * gx;

    if (n_plants == 0) return py::array_t<double>(0);

#ifdef _OPENMP
    omp_set_dynamic(0);
    if (n_threads > 0) omp_set_num_threads(n_threads);
    else omp_set_num_threads(omp_get_num_procs());
#endif

    const double* px = xe.data();
    const double* py_ = ye.data();
    const double* pr = r_stem.data();
    const double* paa = aa.data();
    const double* pbb = bb.data();
    const double* pfmin = fmin.data();
    const double* pphi = phi.data();
    const double* pgx = grid_x.data();
    const double* pgy = grid_y.data();

    // Grid geometry (uniform spacing, derived from grid arrays)
    const double x_origin = pgx[0];                    // first col center
    const double y_origin = pgy[0];                     // first row center
    const double x_step = (gx > 1) ? (pgx[1] - pgx[0]) : lx;
    const double y_step = (gy > 1) ? (pgy[gx] - pgy[0]) : ly;

    // Precompute per-plant FON parameters
    std::vector<double> fon_radius(n_plants);
    std::vector<double> cc(n_plants);
    for (int i = 0; i < n_plants; ++i) {
        fon_radius[i] = paa[i] * std::pow(pr[i], pbb[i]);
        cc[i] = -std::log(pfmin[i]) / (fon_radius[i] - pr[i]);
    }

    // Per-cell total FON height
    std::vector<double> total_fon(grid_size, 0.0);

    // Helper lambda: compute col/row index range for a plant's FON radius
    // Returns (min_idx, max_idx) in grid index space. May exceed [0, n) for PBC.
    auto index_range = [](double pos, double origin, double step, int n, double radius, bool pbc)
        -> std::pair<int, int> {
        int lo = (int)std::floor((pos - radius - origin) / step);
        int hi = (int)std::ceil((pos + radius - origin) / step);
        if (!pbc) {
            lo = std::max(lo, 0);
            hi = std::min(hi, n - 1);
        } else if (hi - lo >= n) {
            hi = lo + n - 1;
        }
        return {lo, hi};
    };

    // Pass 1: accumulate total FON field (spatial indexed)
    for (int i = 0; i < n_plants; ++i) {
        double x = px[i], y = py_[i];
        double rs = pr[i], fr = fon_radius[i], c = cc[i], fm = pfmin[i];

        auto [col_lo, col_hi] = index_range(x, x_origin, x_step, gx, fr, periodic);
        auto [row_lo, row_hi] = index_range(y, y_origin, y_step, gy, fr, periodic);

        for (int row = row_lo; row <= row_hi; ++row) {
            int r = periodic ? ((row % gy + gy) % gy) : row;
            double gy_val = pgy[r * gx];
            double dy = gy_val - y;
            if (periodic) dy -= ly * std::round(dy / ly);

            for (int col = col_lo; col <= col_hi; ++col) {
                int ci = periodic ? ((col % gx + gx) % gx) : col;
                double gx_val = pgx[ci];
                double dx = gx_val - x;
                if (periodic) dx -= lx * std::round(dx / lx);

                double dist = std::sqrt(dx * dx + dy * dy);
                if (dist > fr) continue;

                double h = std::exp(-c * (dist - rs));
                if (h > 1.0) h = 1.0;
                if (h < fm) continue;

                total_fon[r * gx + ci] += h;
            }
        }
    }

    // Pass 2: for each plant, compute FON area and impact (spatial indexed)
    std::vector<double> fon_area(n_plants, 0.0);
    std::vector<double> fon_impact(n_plants, 0.0);

    for (int i = 0; i < n_plants; ++i) {
        double x = px[i], y = py_[i];
        double rs = pr[i], fr = fon_radius[i], c = cc[i], fm = pfmin[i];

        auto [col_lo, col_hi] = index_range(x, x_origin, x_step, gx, fr, periodic);
        auto [row_lo, row_hi] = index_range(y, y_origin, y_step, gy, fr, periodic);

        double local_area = 0.0, local_impact = 0.0;

        for (int row = row_lo; row <= row_hi; ++row) {
            int r = periodic ? ((row % gy + gy) % gy) : row;
            double gy_val = pgy[r * gx];
            double dy = gy_val - y;
            if (periodic) dy -= ly * std::round(dy / ly);

            for (int col = col_lo; col <= col_hi; ++col) {
                int ci = periodic ? ((col % gx + gx) % gx) : col;
                double gx_val = pgx[ci];
                double dx = gx_val - x;
                if (periodic) dx -= lx * std::round(dx / lx);

                double dist = std::sqrt(dx * dx + dy * dy);
                if (dist > fr) continue;

                double h = std::exp(-c * (dist - rs));
                if (h > 1.0) h = 1.0;
                if (h < fm) continue;

                local_area += 1.0;
                local_impact += (total_fon[r * gx + ci] - h);
            }
        }

        fon_area[i] = local_area;
        fon_impact[i] = local_impact;
    }

    // Compute resource limitation: 1 - phi * (impact / area)
    py::array_t<double> out(n_plants);
    auto o = out.mutable_unchecked<1>();
    for (int i = 0; i < n_plants; ++i) {
        double area = fon_area[i];
        if (area > 0.0) {
            double stress = fon_impact[i] / area;
            double rl = 1.0 - pphi[i] * stress;
            o(i) = (rl < 0.0) ? 0.0 : rl;
        } else {
            o(i) = 1.0;
        }
    }
    return out;
}

PYBIND11_MODULE(fonzoi, m) {
    m.doc() = "FON (Field of Neighborhood) CPP core with spatial indexing + PBC";
    m.def("compute_belowground_resources", &compute_belowground_resources,
          py::arg("xe"), py::arg("ye"), py::arg("r_stem"),
          py::arg("aa"), py::arg("bb"), py::arg("fmin"), py::arg("phi"),
          py::arg("grid_x"), py::arg("grid_y"),
          py::arg("periodic"), py::arg("lx"), py::arg("ly"),
          py::arg("n_threads") = -1);
}
