// ResourceLib/AboveGround/AsymmetricZOI/AsymmetricZOI.cpp
//
// Summary
// -------
// Pybind11 C++ core for the Asymmetric Zone of Influence (ZOI) above-ground
// competition model. For each grid cell, the tallest competing plant "wins"
// according to a crown height profile (curved or flat). The per-plant
// aboveground resource factor is computed as: wins / crown_area.
//
// Notes
// -----
// - Inputs are provided as NumPy arrays (float32 recommended) from Python.
// - OpenMP (if available) parallelizes the loop over grid cells for each plant.
// - Current code sets OpenMP threads to all available processors; the function
//   signature includes `n_threads` but it is NOT used here. If you want to
//   control threads via Python/XML, wire `n_threads` into omp_set_num_threads().
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
namespace py = pybind11;

#ifdef _OPENMP
  #include <omp.h>
#endif

// compute_aboveground_resources
// Parameters
//   xe, ye      : 1D (n_plants) arrays of plant positions
//   h_stem      : 1D (n_plants) stem/base heights
//   r_ag        : 1D (n_plants) crown radii
//   grid_x/y    : 2D (gy x gx) coordinate arrays for the grid
//   curved_crown: if true, curved crown profile h + sqrt(4 r^2 - d^2); else flat h + 2r
//   mesh_size   : grid mesh size used for minimum-radius handling
// Returns
//   1D (n_plants) float array with per-plant aboveground resource factor ∈ [0, 1]
py::array_t<float> compute_aboveground_resources(
    py::array_t<float, py::array::c_style | py::array::forcecast> xe,
    py::array_t<float, py::array::c_style | py::array::forcecast> ye,
    py::array_t<float, py::array::c_style | py::array::forcecast> h_stem,
    py::array_t<float, py::array::c_style | py::array::forcecast> r_ag,
    py::array_t<float, py::array::c_style | py::array::forcecast> grid_x,
    py::array_t<float, py::array::c_style | py::array::forcecast> grid_y,
    bool curved_crown, float mesh_size, int n_threads /* -1 -> auto, currently unused */) {

    // Basic input validation & grid bookkeeping
    const int n_plants = (int)xe.size();
    if (ye.size()!=xe.size() || h_stem.size()!=xe.size() || r_ag.size()!=xe.size())
        throw std::invalid_argument("xe, ye, h_stem, r_ag must have same length");
    if (grid_x.ndim()!=2 || grid_y.ndim()!=2)
        throw std::invalid_argument("grid_x and grid_y must be 2D");
    if (grid_x.shape(0)!=grid_y.shape(0) || grid_x.shape(1)!=grid_y.shape(1))
        throw std::invalid_argument("grid_x and grid_y must have same shape");

    const int gy = (int)grid_x.shape(0), gx = (int)grid_x.shape(1);
    if (gy<=0 || gx<=0 || (long long)gy*(long long)gx > INT32_MAX)
        throw std::runtime_error("grid too large for 32-bit indexing");
    const int grid_size = gy*gx;

#ifdef _OPENMP
    omp_set_dynamic(0);
    omp_set_num_threads(omp_get_num_procs());
#endif

    // Precompute minimum allowed crown radius from mesh size
    const float min_r_ag = mesh_size * (float)(1.0/std::sqrt(2.0));

    // Raw pointers for tight loops
    const float* px=xe.data(); const float* py_=ye.data();
    const float* ph=h_stem.data(); const float* pr=r_ag.data();
    const float* pgx=grid_x.data(); const float* pgy=grid_y.data();

    // Working buffers 
    // canopy : tallest crown height found for each grid cell
    // winner : index of plant currently owning (winning) the cell, -1 = none
    // crown_area : per-plant number of grid cells within its crown footprint
    // wins   : per-plant number of cells where this plant is the tallest
    std::vector<float>   canopy(grid_size, 0.0f);
    std::vector<int32_t> winner(grid_size, -1);
    std::vector<float>   crown_area(n_plants, 0.0f);
    std::vector<float>   wins(n_plants, 0.0f);

    // Main loop: for each plant, update canopy winners over its crown
    for (int i=0;i<n_plants;++i){
        float x=px[i], y=py_[i], h=ph[i], r=pr[i];
        if (r<min_r_ag) r=mesh_size;            // enforce minimum crown radius
        const float r2=r*r;
        int local=0;                             // cells covered by this plant's crown

        // Iterate all grid cells; if within radius, compute cell crown height.
        // Strict '>' tie rule: later plants only win if strictly taller.
#ifdef _OPENMP
        #pragma omp parallel for schedule(static) reduction(+:local)
#endif
        for (int idx=0; idx<grid_size; ++idx){
            float dx = pgx[idx]-x, dy = pgy[idx]-y;
            float d2 = dx*dx + dy*dy;
            if (d2<=r2){
                float cell_h = curved_crown
                    ? (h + std::sqrt(std::max(0.0f, 4.0f*r2 - d2)))  // curved dome
                    : (h + 2.0f*r);                                 // flat top
                if (cell_h > canopy[idx]){                          // strict tie-break
                    canopy[idx] = cell_h;
                    winner[idx] = i;
                }
                local += 1;                                         // crown footprint cell
            }
        }
        crown_area[i] = (float)local;
    }

    // Accumulate wins per plant from the winner map 
    for (int idx=0; idx<grid_size; ++idx){
        int w=winner[idx]; if (w>=0) wins[w]+=1.0f;
    }

    // Normalize to get per-plant resource factor; NaN guard 
    py::array_t<float> out(n_plants);
    auto o = out.mutable_unchecked<1>();
    for (int i=0;i<n_plants;++i){
        float denom=crown_area[i];
        o(i) = (denom>0.0f) ? (wins[i]/denom) : std::numeric_limits<float>::quiet_NaN();
        if (o(i)!=o(i)) // NaN
            throw std::runtime_error(
                "NaN detected in aboveground_resources for plants at indices: ["+
                std::to_string(i)+"]"
            );
    }
    return out;
}


// pybind11 module declaration
// Exposes the function `compute_aboveground_resources` to Python as:
PYBIND11_MODULE(asymzoi, m){
    m.doc() = "Asymmetric ZOI CPP core (keeps Python API unchanged)";
    m.def("compute_aboveground_resources", &compute_aboveground_resources,
          py::arg("xe"), py::arg("ye"), py::arg("h_stem"), py::arg("r_ag"),
          py::arg("grid_x"), py::arg("grid_y"),
          py::arg("curved_crown"), py::arg("mesh_size"),
          py::arg("n_threads") = -1);  // currently ignored inside the function
}
