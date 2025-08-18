// FixedSalinityCPP_f32.cpp
// pybind11 backend (float32 strict)
// APIs:
//   compute_resources_constant(...)
//   compute_resources_sine(...)
//   compute_resources_timeseries(...)
// Returns: np.ndarray(shape=(n_plants,), dtype=float32)

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <cmath>
#include <random>
#include <string>
#include <stdexcept>
#include <limits>
#include <algorithm>

namespace py = pybind11;

// ---------- helpers ----------
inline void check_lengths_match(py::ssize_t n, const py::buffer_info& a, const char* name){
    if (a.ndim != 1) throw std::runtime_error(std::string(name) + " must be 1D");
    if (a.shape[0] != n) throw std::runtime_error(std::string(name) + " length mismatch");
}

inline void check_bc_unit(float left, float right){
    // same rule as Python code: salinity in kg/kg, must not exceed 1
    if (left > 1.0f || right > 1.0f){
        throw std::runtime_error("Salinity over 1000 ppt. Are you sure salinity is kg/kg (not ppt)?");
    }
}

struct RNG {
    std::mt19937_64 eng;
    bool enabled{false};
    explicit RNG(long long seed){
        if (seed >= 0){
            eng.seed(static_cast<uint64_t>(seed));
            enabled = true;
        } else {
            std::random_device rd;
            eng.seed(((uint64_t)rd() << 32) ^ (uint64_t)rd());
            enabled = true;
        }
    }
    RNG() = default;
};

// spatial linear interpolation along x
inline void spatial_salinity_1d(float min_x, float max_x,
                                float left_bc, float right_bc,
                                const float* plant_x, py::ssize_t n,
                                std::vector<float>& sal_out){
    const float L = max_x - min_x;
    if (L == 0.0f){
        const float m = 0.5f * (left_bc + right_bc);
        for (py::ssize_t i=0;i<n;++i) sal_out[i] = m;
        return;
    }
    const float slope = (right_bc - left_bc) / L;
    for (py::ssize_t i=0;i<n;++i){
        sal_out[i] = (plant_x[i] - min_x) * slope + left_bc;
    }
}

// optional stochastic distribution
inline void apply_distribution(const std::string& distribution_type,
                               float deviation, bool relative,
                               float left_bc, float right_bc,
                               std::vector<float>& sal,
                               RNG* prng){
    if (distribution_type.empty()) return;
    if (!prng || !prng->enabled) return;

    if (distribution_type == "uniform"){
        std::uniform_real_distribution<float> U(left_bc, right_bc);
        for (auto& v : sal){
            v = U(prng->eng);
            if (v < 0.0f) v = 0.0f;
        }
        return;
    }

    if (distribution_type == "normal" || distribution_type == "normal_relative"){
        for (auto& v : sal){
            float sigma = deviation;
            if (distribution_type == "normal_relative" || relative){
                sigma = v * deviation;
            }
            std::normal_distribution<float> N(v, sigma);
            v = N(prng->eng);
            if (v < 0.0f) v = 0.0f;
        }
        return;
    }

    throw std::runtime_error("Unknown distribution_type: " + distribution_type);
}

// core formula (float32)
inline void compute_resources_core(
    const float* /*plant_x*/, py::ssize_t n_plants,
    const int8_t* r_salinity_code,     // 1=bettina, 2=forman
    const float* h_stem, const float* r_crown, const float* psi_leaf,   // bettina
    const float* salt_effect_d, const float* salt_effect_ui,             // forman
    const std::vector<float>& salinity_plant,
    std::vector<float>& out_resources
){
    std::fill(out_resources.begin(), out_resources.end(), 0.0f);

    // Bettina
    for (py::ssize_t i=0;i<n_plants;++i){
        if (r_salinity_code[i] == 1){
            // psi_zero = psi_leaf + (2*r_crown + h_stem) * 9810
            const float psi_zero = psi_leaf[i] + (2.0f * r_crown[i] + h_stem[i]) * 9810.0f;
            const float psi_sali = psi_zero + 85000000.0f * salinity_plant[i];
            out_resources[i] = psi_sali / psi_zero; // keep IEEE behavior for zero/NaN same as NumPy
        }
    }

    // Forman
    for (py::ssize_t i=0;i<n_plants;++i){
        if (r_salinity_code[i] == 2){
            // expo = d * (ui - sal_kgkg * 1e3)  -> ppt
            const float expo = salt_effect_d[i] * (salt_effect_ui[i] - salinity_plant[i] * 1000.0f);
            const float v = 1.0f / (1.0f + std::expf(expo));
            out_resources[i] = v;
        }
    }
}

// ================= front-ends =================

// 1) constant boundaries
py::array_t<float> compute_resources_constant(
    py::array_t<float,  py::array::c_style | py::array::forcecast> plant_x,
    py::array_t<int8_t, py::array::c_style | py::array::forcecast> r_salinity_code,
    py::array_t<float,  py::array::c_style | py::array::forcecast> h_stem,
    py::array_t<float,  py::array::c_style | py::array::forcecast> r_crown,
    py::array_t<float,  py::array::c_style | py::array::forcecast> psi_leaf,
    py::array_t<float,  py::array::c_style | py::array::forcecast> salt_effect_d,
    py::array_t<float,  py::array::c_style | py::array::forcecast> salt_effect_ui,
    float min_x, float max_x,
    float left_bc, float right_bc,
    std::string distribution_type = "",
    float deviation = 0.0f,
    bool relative = false,
    py::object seed = py::none()
){
    auto bx  = plant_x.request();
    auto br  = r_salinity_code.request();
    const py::ssize_t n = bx.shape[0];

    check_lengths_match(n, br, "r_salinity_code");
    auto bhs = h_stem.request();        check_lengths_match(n, bhs, "h_stem");
    auto brc = r_crown.request();       check_lengths_match(n, brc, "r_crown");
    auto bpl = psi_leaf.request();      check_lengths_match(n, bpl, "psi_leaf");
    auto bsd = salt_effect_d.request(); check_lengths_match(n, bsd, "salt_effect_d");
    auto bsU = salt_effect_ui.request();check_lengths_match(n, bsU, "salt_effect_ui");

    const float* px  = static_cast<float*>(bx.ptr);
    const int8_t* rc = static_cast<int8_t*>(br.ptr);
    const float* hs  = static_cast<float*>(bhs.ptr);
    const float* rcw = static_cast<float*>(brc.ptr);
    const float* pl  = static_cast<float*>(bpl.ptr);
    const float* sd  = static_cast<float*>(bsd.ptr);
    const float* su  = static_cast<float*>(bsU.ptr);

    check_bc_unit(left_bc, right_bc);

    std::vector<float> sal(n);
    spatial_salinity_1d(min_x, max_x, left_bc, right_bc, px, n, sal);

    std::unique_ptr<RNG> prng;
    if (!distribution_type.empty() || !seed.is_none()){
        long long s = -1;
        if (!seed.is_none()) s = py::cast<long long>(seed);
        prng.reset(new RNG(s));
        apply_distribution(distribution_type, deviation, relative, left_bc, right_bc, sal, prng.get());
    }

    py::array_t<float> out(n);
    auto bo = out.request();
    auto* outp = static_cast<float*>(bo.ptr);
    std::vector<float> res(n);
    compute_resources_core(px, n, rc, hs, rcw, pl, sd, su, sal, res);
    std::copy(res.begin(), res.end(), outp);
    return out;
}

// 2) sine boundaries
py::array_t<float> compute_resources_sine(
    py::array_t<float,  py::array::c_style | py::array::forcecast> plant_x,
    py::array_t<int8_t, py::array::c_style | py::array::forcecast> r_salinity_code,
    py::array_t<float,  py::array::c_style | py::array::forcecast> h_stem,
    py::array_t<float,  py::array::c_style | py::array::forcecast> r_crown,
    py::array_t<float,  py::array::c_style | py::array::forcecast> psi_leaf,
    py::array_t<float,  py::array::c_style | py::array::forcecast> salt_effect_d,
    py::array_t<float,  py::array::c_style | py::array::forcecast> salt_effect_ui,
    float min_x, float max_x,
    float t_ini, float amplitude, float stretch, float offset, float noise,
    float left_bc_base, float right_bc_base,
    std::string distribution_type = "",
    float deviation = 0.0f,
    bool relative = false,
    py::object seed = py::none()
){
    float s0 = amplitude * std::sinf(t_ini / stretch + offset);
    std::unique_ptr<RNG> prng;
    float left  = s0 + left_bc_base;
    float right = s0 + right_bc_base;

    if (!seed.is_none() || noise > 0.0f || !distribution_type.empty()){
        long long s = -1;
        if (!seed.is_none()) s = py::cast<long long>(seed);
        prng.reset(new RNG(s));
        if (noise > 0.0f){
            std::normal_distribution<float> Nl(left,  noise);
            std::normal_distribution<float> Nr(right, noise);
            left  = Nl(prng->eng);
            right = Nr(prng->eng);
            if (left  < 0.0f) left  = 0.0f;
            if (right < 0.0f) right = 0.0f;
        }
    }

    check_bc_unit(left, right);

    auto bx  = plant_x.request();
    auto br  = r_salinity_code.request();
    const py::ssize_t n = bx.shape[0];

    auto bhs = h_stem.request();        check_lengths_match(n, bhs, "h_stem");
    auto brc = r_crown.request();       check_lengths_match(n, brc, "r_crown");
    auto bpl = psi_leaf.request();      check_lengths_match(n, bpl, "psi_leaf");
    auto bsd = salt_effect_d.request(); check_lengths_match(n, bsd, "salt_effect_d");
    auto bsU = salt_effect_ui.request();check_lengths_match(n, bsU, "salt_effect_ui");

    const float* px  = static_cast<float*>(bx.ptr);
    const int8_t* rc = static_cast<int8_t*>(br.ptr);
    const float* hs  = static_cast<float*>(bhs.ptr);
    const float* rcw = static_cast<float*>(brc.ptr);
    const float* pl  = static_cast<float*>(bpl.ptr);
    const float* sd  = static_cast<float*>(bsd.ptr);
    const float* su  = static_cast<float*>(bsU.ptr);

    std::vector<float> sal(n);
    spatial_salinity_1d(min_x, max_x, left, right, px, n, sal);

    if (!distribution_type.empty()){
        if (!prng) prng.reset(new RNG(-1));
        apply_distribution(distribution_type, deviation, relative, left, right, sal, prng.get());
    }

    py::array_t<float> out(n);
    auto bo = out.request();
    auto* outp = static_cast<float*>(bo.ptr);
    std::vector<float> res(n);
    compute_resources_core(px, n, rc, hs, rcw, pl, sd, su, sal, res);
    std::copy(res.begin(), res.end(), outp);
    return out;
}

// 3) time-series boundaries (A: shape Nx3 [t,left,right], dtype float32 acceptable)
py::array_t<float> compute_resources_timeseries(
    py::array_t<float,  py::array::c_style | py::array::forcecast> plant_x,
    py::array_t<int8_t, py::array::c_style | py::array::forcecast> r_salinity_code,
    py::array_t<float,  py::array::c_style | py::array::forcecast> h_stem,
    py::array_t<float,  py::array::c_style | py::array::forcecast> r_crown,
    py::array_t<float,  py::array::c_style | py::array::forcecast> psi_leaf,
    py::array_t<float,  py::array::c_style | py::array::forcecast> salt_effect_d,
    py::array_t<float,  py::array::c_style | py::array::forcecast> salt_effect_ui,
    float min_x, float max_x,
    py::array_t<float,  py::array::c_style | py::array::forcecast> sal_over_t, // (N,3)
    float t_ini,
    std::string distribution_type = "",
    float deviation = 0.0f,
    bool relative = false,
    py::object seed = py::none()
){
    auto bt = sal_over_t.request();
    if (bt.ndim != 2 || bt.shape[1] != 3){
        throw std::runtime_error("sal_over_t must be shape (N,3) with columns [t, left, right]");
    }
    const py::ssize_t T = bt.shape[0];
    const float* rows = static_cast<float*>(bt.ptr);

    float left = 0.0f, right = 0.0f;
    bool found_exact = false;
    for (py::ssize_t i=0;i<T;i++){
        const float ti = rows[i*3 + 0];
        if (ti == t_ini){
            left  = rows[i*3 + 1];
            right = rows[i*3 + 2];
            found_exact = true;
            break;
        }
    }
    if (!found_exact){
        py::ssize_t ib = -1, ia = -1;
        for (py::ssize_t i=0;i<T;i++){
            const float ti = rows[i*3+0];
            if (ti < t_ini) ib = i;
            if (ti > t_ini){ ia = i; break; }
        }
        if (ib>=0 && ia>=0){
            const float tb = rows[ib*3+0], ta = rows[ia*3+0];
            const float lb = rows[ib*3+1], la = rows[ia*3+1];
            const float rb = rows[ib*3+2], ra = rows[ia*3+2];
            const float w  = (t_ini - tb) / (ta - tb);
            left  = lb + w*(la - lb);
            right = rb + w*(ra - rb);
        }else if (T>0){
            if (t_ini < rows[0*3+0]){ left=rows[0*3+1];  right=rows[0*3+2]; }
            else { left=rows[(T-1)*3+1]; right=rows[(T-1)*3+2]; }
        }
    }

    check_bc_unit(left, right);

    auto bx  = plant_x.request();
    auto br  = r_salinity_code.request();
    const py::ssize_t n = bx.shape[0];

    auto bhs = h_stem.request();        check_lengths_match(n, bhs, "h_stem");
    auto brc = r_crown.request();       check_lengths_match(n, brc, "r_crown");
    auto bpl = psi_leaf.request();      check_lengths_match(n, bpl, "psi_leaf");
    auto bsd = salt_effect_d.request(); check_lengths_match(n, bsd, "salt_effect_d");
    auto bsU = salt_effect_ui.request();check_lengths_match(n, bsU, "salt_effect_ui");

    const float* px  = static_cast<float*>(bx.ptr);
    const int8_t* rc = static_cast<int8_t*>(br.ptr);
    const float* hs  = static_cast<float*>(bhs.ptr);
    const float* rcw = static_cast<float*>(brc.ptr);
    const float* pl  = static_cast<float*>(bpl.ptr);
    const float* sd  = static_cast<float*>(bsd.ptr);
    const float* su  = static_cast<float*>(bsU.ptr);

    std::vector<float> sal(n);
    spatial_salinity_1d(min_x, max_x, left, right, px, n, sal);

    std::unique_ptr<RNG> prng;
    if (!distribution_type.empty() || !seed.is_none()){
        long long s = -1;
        if (!seed.is_none()) s = py::cast<long long>(seed);
        prng.reset(new RNG(s));
        apply_distribution(distribution_type, deviation, relative, left, right, sal, prng.get());
    }

    py::array_t<float> out(n);
    auto bo = out.request();
    auto* outp = static_cast<float*>(bo.ptr);
    std::vector<float> res(n);
    compute_resources_core(px, n, rc, hs, rcw, pl, sd, su, sal, res);
    std::copy(res.begin(), res.end(), outp);
    return out;
}

PYBIND11_MODULE(fixedsalcpp, m){
    m.doc() = "C++ float32 backend for FixedSalinity (pyMANGA).";
    m.def("compute_resources_constant",   &compute_resources_constant,
          py::arg("plant_x"),
          py::arg("r_salinity_code"),
          py::arg("h_stem"),
          py::arg("r_crown"),
          py::arg("psi_leaf"),
          py::arg("salt_effect_d"),
          py::arg("salt_effect_ui"),
          py::arg("min_x"), py::arg("max_x"),
          py::arg("left_bc"), py::arg("right_bc"),
          py::arg("distribution_type")="", py::arg("deviation")=0.0f,
          py::arg("relative")=false, py::arg("seed")=py::none());

    m.def("compute_resources_sine",       &compute_resources_sine,
          py::arg("plant_x"),
          py::arg("r_salinity_code"),
          py::arg("h_stem"),
          py::arg("r_crown"),
          py::arg("psi_leaf"),
          py::arg("salt_effect_d"),
          py::arg("salt_effect_ui"),
          py::arg("min_x"), py::arg("max_x"),
          py::arg("t_ini"), py::arg("amplitude"), py::arg("stretch"), py::arg("offset"), py::arg("noise"),
          py::arg("left_bc_base"), py::arg("right_bc_base"),
          py::arg("distribution_type")="", py::arg("deviation")=0.0f,
          py::arg("relative")=false, py::arg("seed")=py::none());

    m.def("compute_resources_timeseries", &compute_resources_timeseries,
          py::arg("plant_x"),
          py::arg("r_salinity_code"),
          py::arg("h_stem"),
          py::arg("r_crown"),
          py::arg("psi_leaf"),
          py::arg("salt_effect_d"),
          py::arg("salt_effect_ui"),
          py::arg("min_x"), py::arg("max_x"),
          py::arg("sal_over_t"),
          py::arg("t_ini"),
          py::arg("distribution_type")="", py::arg("deviation")=0.0f,
          py::arg("relative")=false, py::arg("seed")=py::none());
}
