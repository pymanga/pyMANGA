// ResourceLib/AboveGround/AsymmetricZOICPP/AsymmetricZOICPP.cpp
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

py::array_t<float> compute_aboveground_resources(
    py::array_t<float, py::array::c_style | py::array::forcecast> xe,
    py::array_t<float, py::array::c_style | py::array::forcecast> ye,
    py::array_t<float, py::array::c_style | py::array::forcecast> h_stem,
    py::array_t<float, py::array::c_style | py::array::forcecast> r_ag,
    py::array_t<float, py::array::c_style | py::array::forcecast> grid_x,
    py::array_t<float, py::array::c_style | py::array::forcecast> grid_y,
    bool curved_crown, float mesh_size, int n_threads /* -1 -> auto */) {

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
    { int th = omp_get_max_threads(); int use = std::max(1, th/2);
      if (use>48) use=48; if (n_threads>0) use=n_threads; omp_set_num_threads(use); }
#endif

    const float min_r_ag = mesh_size * (float)(1.0/std::sqrt(2.0));

    const float* px=xe.data(); const float* py_=ye.data();
    const float* ph=h_stem.data(); const float* pr=r_ag.data();
    const float* pgx=grid_x.data(); const float* pgy=grid_y.data();

    std::vector<float> canopy(grid_size, 0.0f);
    std::vector<int32_t> winner(grid_size, -1);
    std::vector<float> crown_area(n_plants, 0.0f);
    std::vector<float> wins(n_plants, 0.0f);

    for (int i=0;i<n_plants;++i){
        float x=px[i], y=py_[i], h=ph[i], r=pr[i];
        if (r<min_r_ag) r=mesh_size;
        const float r2=r*r;
        int local=0;

        #ifdef _OPENMP
        #pragma omp parallel for schedule(static) reduction(+:local)
        #endif
        for (int idx=0; idx<grid_size; ++idx){
            float dx = pgx[idx]-x, dy = pgy[idx]-y;
            float d2 = dx*dx + dy*dy;
            if (d2<=r2){
                float cell_h = curved_crown
                    ? (h + std::sqrt(std::max(0.0f, 4.0f*r2 - d2)))
                    : (h + 2.0f*r);
                if (cell_h > canopy[idx]){ // strict ">" tie rule
                    canopy[idx] = cell_h;
                    winner[idx] = i;
                }
                local += 1;
            }
        }
        crown_area[i] = (float)local;
    }

    for (int idx=0; idx<grid_size; ++idx){
        int w=winner[idx]; if (w>=0) wins[w]+=1.0f;
    }

    py::array_t<float> out(n_plants);
    auto o = out.mutable_unchecked<1>();
    for (int i=0;i<n_plants;++i){
        float denom=crown_area[i];
        o(i) = (denom>0.0f) ? (wins[i]/denom) : std::numeric_limits<float>::quiet_NaN();
        if (o(i)!=o(i)) // NaN
            throw std::runtime_error("NaN detected in aboveground_resources for plants at indices: ["+std::to_string(i)+"]");
    }
    return out;
}

PYBIND11_MODULE(asymzoicpp, m){
    m.doc() = "Asymmetric ZOI HPC core (keeps Python API unchanged)";
    m.def("compute_aboveground_resources", &compute_aboveground_resources,
          py::arg("xe"), py::arg("ye"), py::arg("h_stem"), py::arg("r_ag"),
          py::arg("grid_x"), py::arg("grid_y"),
          py::arg("curved_crown"), py::arg("mesh_size"),
          py::arg("n_threads") = -1);
}
