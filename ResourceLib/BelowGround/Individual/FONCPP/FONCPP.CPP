// FONCPP.cpp  (window + support-bitmask; float32 strict; python-aligned; deterministic-safe)
// - PASS1: 在窗口内计算 v，累加 fon_total、sum/area，并把 (v>0) 记到位图（每株一张，1bit/像元）
// - PASS2: 使用 PASS1 生成的位图求 sum_total_on_support（不再重算 v）
// - deterministic=true  单线程顺序，位级可复现
// - deterministic=false 并行：按“每株外层 + 窗口内网格”并发；对 fon_total 用 atomic（与原版一致）
//
// 注：若要更贴近 NumPy 的数值稳健性，可把 hypotf32 换成 std::hypotf（会略慢）。

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>
#include <vector>
#include <limits>
#include <algorithm>
#include <cstdint>

#ifdef _OPENMP
  #include <omp.h>
#endif

namespace py = pybind11;

// ---- float32 helpers --------------------------------------------------------
inline float expf32(float x){ return std::expf(x); }
inline float logf32(float x){ return std::logf(x); }
inline float powf32(float a, float b){ return std::powf(a,b); }
// 若希望更贴近 np.hypot，可改为：return std::hypotf(x, y);
inline float hypotf32(float x, float y){
#ifdef FON_USE_STD_HYPOT
  return std::hypotf(x, y);
#else
  return std::sqrt(x*x + y*y);
#endif
}


// ---- 轴窗口（非严格单调支持） ------------------------------------------------
inline void find_index_window(const std::vector<float>& axis, float lo, float hi, int& i0, int& i1){
    const int n = (int)axis.size();
    if (n == 0){ i0=0; i1=-1; return; }

    bool nondec = true, noninc = true;
    for (int k=0; k<n-1; ++k){
        if (axis[k+1] < axis[k]) nondec = false;
        if (axis[k+1] > axis[k]) noninc = false;
    }

    auto lb_inc = [&](float v){ int L=0,R=n; while(L<R){ int M=(L+R)>>1; if(axis[M] >= v) R=M; else L=M+1; } return L; };
    auto ub_inc = [&](float v){ int L=0,R=n; while(L<R){ int M=(L+R)>>1; if(axis[M] > v) R=M; else L=M+1; } return L; };
    auto lb_dec = [&](float v){ int L=0,R=n; while(L<R){ int M=(L+R)>>1; if(axis[M] <= v) R=M; else L=M+1; } return L; };
    auto ub_dec = [&](float v){ int L=0,R=n; while(L<R){ int M=(L+R)>>1; if(axis[M] < v) R=M; else L=M+1; } return L; };

    int a0=0, a1=-1;
    if (nondec){ a0 = lb_inc(lo); a1 = ub_inc(hi) - 1; }
    else if (noninc){ a0 = lb_dec(lo); a1 = ub_dec(hi) - 1; }
    else {
        int L=0, R=n-1;
        while(L<n && axis[L] < std::min(lo,hi)) ++L;
        while(R>=0 && axis[R] > std::max(lo,hi)) --R;
        a0=L; a1=R;
    }

    if (a0 < 0) a0 = 0;
    if (a1 >= n) a1 = n-1;
    if (a0 > a1){ i0=0; i1=-1; return; }
    i0=a0; i1=a1;
}

// ---- 主计算 -----------------------------------------------------------------
py::array_t<float> compute_fon_resources(
    py::array_t<float, py::array::c_style | py::array::forcecast> grid_x,
    py::array_t<float, py::array::c_style | py::array::forcecast> grid_y,
    py::array_t<float, py::array::c_style | py::array::forcecast> plant_x,
    py::array_t<float, py::array::c_style | py::array::forcecast> plant_y,
    py::array_t<float, py::array::c_style | py::array::forcecast> r_stem,
    float aa, float bb, float fmin, int threads=0, bool deterministic=true
){
    // --- shape 检查
    auto bx = grid_x.request(), by = grid_y.request();
    if (bx.ndim!=2 || by.ndim!=2) throw std::runtime_error("grid_x and grid_y must be 2D.");
    if (bx.shape[0]!=by.shape[0] || bx.shape[1]!=by.shape[1]) throw std::runtime_error("grid_x and grid_y shape mismatch.");
    const int nx=(int)bx.shape[0], ny=(int)bx.shape[1], grid_size=nx*ny;

    auto bpx = plant_x.request(), bpy = plant_y.request(), brs = r_stem.request();
    if (bpx.ndim!=1 || bpy.ndim!=1 || brs.ndim!=1) throw std::runtime_error("plant arrays must be 1D.");
    if (!(bpx.shape[0]==bpy.shape[0] && bpx.shape[0]==brs.shape[0])) throw std::runtime_error("plant array lengths differ.");
    const int n_plants = (int)bpx.shape[0];

    const float* gx = static_cast<float*>(bx.ptr);
    const float* gy = static_cast<float*>(by.ptr);
    const float* px = static_cast<float*>(bpx.ptr);
    const float* py_ = static_cast<float*>(bpy.ptr);
    const float* rs = static_cast<float*>(brs.ptr);

#ifdef _OPENMP
    if (threads>0) omp_set_num_threads(threads);
#endif

    auto out = py::array_t<float>(n_plants);
    float* resources = static_cast<float*>(out.request().ptr);
    if (n_plants==0) return out;

    // 抽取轴（meshgrid('ij') 假设）
    std::vector<float> xs(nx), ys(ny);
    for (int i=0;i<nx;++i) xs[i] = gx[i*ny + 0];
    for (int j=0;j<ny;++j) ys[j] = gy[0*ny + j];

    // 全局累计场、每株的 sum 与 area
    std::vector<float> fon_total(grid_size, 0.f);
    std::vector<float> fon_sums(n_plants, 0.f);
    std::vector<int>   fon_areas(n_plants, 0);

    // 支持域位图（每株一张，1bit/像元）
    const size_t stride_bytes = ( (size_t)grid_size + 7u ) >> 3; // ceil(N/8)
    std::vector<uint8_t> support_bits( (size_t)n_plants * stride_bytes, 0 );

    auto set_bit = [&](int plant, int idx){
        size_t off = (size_t)plant * stride_bytes + ((size_t)idx >> 3);
        uint8_t mask = (uint8_t)(1u << (idx & 7));
        support_bits[off] |= mask;
    };
    auto test_bit = [&](int plant, int idx)->bool{
        size_t off = (size_t)plant * stride_bytes + ((size_t)idx >> 3);
        uint8_t mask = (uint8_t)(1u << (idx & 7));
        return (support_bits[off] & mask) != 0;
    };

    // 预计算每株的 R, R2 与 c（float32 严格；与 Python 一致）
    std::vector<float> R(n_plants), R2(n_plants), cc(n_plants);
    for (int i=0;i<n_plants;++i){
        const float ri = rs[i];
        const float Ri = aa * powf32(ri, bb);
        R[i]  = Ri;
        R2[i] = Ri * Ri;
        const float denom = (Ri - ri);
        if (denom == 0.0f){
            cc[i] = std::numeric_limits<float>::infinity(); // 特判：d<=r → v=1，else v=0
        }else{
            cc[i] = -logf32(fmin) / denom;
        }
    }

    // ---- PASS 1：窗口内计算 v、累加 fon_total，并记录支持域位图 -------------------
    if (deterministic){
        for (int i=0;i<n_plants;++i){
            const float xi=px[i], yi=py_[i], ri=rs[i];
            const float Ri = R[i], R2i = R2[i], ci = cc[i];

            int i0,i1,j0,j1;
            find_index_window(xs, xi-Ri, xi+Ri, i0, i1);
            find_index_window(ys, yi-Ri, yi+Ri, j0, j1);
            if (i1<0 || j1<0){ fon_sums[i]=0.f; fon_areas[i]=0; continue; }

            // +1 安全边界（半格）
            if (i0>0) --i0; if (i1<nx-1) ++i1;
            if (j0>0) --j0; if (j1<ny-1) ++j1;

            float local_sum=0.f; int local_area=0;
            for (int ii=i0; ii<=i1; ++ii){
                const float ddx = xs[ii]-xi;
                const int base = ii*ny;
                for (int jj=j0; jj<=j1; ++jj){
                    const float ddy = ys[jj]-yi;
                    const float d2  = ddx*ddx + ddy*ddy;
                    if (d2 > R2i) continue;             // 圆掩膜：在半径外直接跳过
                    float v;
                    if (std::isinf(ci)) {
                        v = (d2 <= ri*ri) ? 1.f : 0.f;  // denom==0 的极限（与 Python 等价）
                    } else {
                        const float d = std::sqrt(d2);  // 仅在圆内才开方
                        v = expf32(-ci * (d - ri));
                        if (v > 1.f)   v = 1.f;
                        if (v < fmin)  v = 0.f;        // 严格 "<"
                    }
                    if (v>0.f){
                        const int idx = base + jj;
                        fon_total[idx] += v;            // 串行顺序累加（可复现）
                        set_bit(i, idx);
                        local_sum += v;
                        ++local_area;
                    }
                }
            }
            fon_sums[i]=local_sum; fon_areas[i]=local_area;
        }
    }else{
        #pragma omp parallel for schedule(dynamic)
        for (int i=0;i<n_plants;++i){
            const float xi=px[i], yi=py_[i], ri=rs[i];
            const float Ri = R[i], R2i = R2[i], ci = cc[i];

            int i0,i1,j0,j1;
            find_index_window(xs, xi-Ri, xi+Ri, i0, i1);
            find_index_window(ys, yi-Ri, yi+Ri, j0, j1);
            if (i1<0 || j1<0){ fon_sums[i]=0.f; fon_areas[i]=0; continue; }

            if (i0>0) --i0; if (i1<nx-1) ++i1;
            if (j0>0) --j0; if (j1<ny-1) ++j1;

            float local_sum=0.f; int local_area=0;
            for (int ii=i0; ii<=i1; ++ii){
                const float ddx = xs[ii]-xi;
                const int base = ii*ny;
                for (int jj=j0; jj<=j1; ++jj){
                    const float ddy = ys[jj]-yi;
                    const float d2  = ddx*ddx + ddy*ddy;
                    if (d2 > R2i) continue;
                    float v;
                    if (std::isinf(ci)) {
                        v = (d2 <= ri*ri) ? 1.f : 0.f;
                    } else {
                        const float d = std::sqrt(d2);
                        v = expf32(-ci * (d - ri));
                        if (v > 1.f)   v = 1.f;
                        if (v < fmin)  v = 0.f;
                    }
                    if (v>0.f){
                        const int idx = base + jj;
                        #ifdef _OPENMP
                        #pragma omp atomic
                        #endif
                        fon_total[idx] += v;            // 原子加，避免竞态
                        set_bit(i, idx);                // 每株独立位图分片，无冲突
                        local_sum += v;
                        ++local_area;
                    }
                }
            }
            fon_sums[i]=local_sum; fon_areas[i]=local_area;
        }
    }

    // total_sum = sum(fon_total)
    float total_sum=0.f;
    if (deterministic){
        for (int idx=0; idx<grid_size; ++idx) total_sum += fon_total[idx];
    }else{
        #pragma omp parallel for reduction(+:total_sum) schedule(static)
        for (int idx=0; idx<grid_size; ++idx) total_sum += fon_total[idx];
    }

    // ---- PASS 2：用位图（与 PASS1 相同判定）求 sum_total_on_support ----------
    #pragma omp parallel for schedule(dynamic) if(!deterministic)
    for (int i=0;i<n_plants;++i){
        const int area = fon_areas[i];
        if (area==0){ resources[i]=1.f; continue; }

        const float xi=px[i], yi=py_[i], ri=rs[i];
        const float Ri = R[i];

        int i0,i1,j0,j1;
        find_index_window(xs, xi-Ri, xi+Ri, i0, i1);
        find_index_window(ys, yi-Ri, yi+Ri, j0, j1);
        if (i0>0) --i0; if (i1<nx-1) ++i1;
        if (j0>0) --j0; if (j1<ny-1) ++j1;

        float sum_total_on_support = 0.f;
        if (i1>=0 && j1>=0){
            for (int ii=i0; ii<=i1; ++ii){
                const int base = ii*ny;
                for (int jj=j0; jj<=j1; ++jj){
                    const int idx = base + jj;
                    if (test_bit(i, idx)){
                        sum_total_on_support += fon_total[idx];
                    }
                }
            }
        }

        const float impact = sum_total_on_support - fon_sums[i];
        float stress = impact / static_cast<float>(area);
        if (std::isnan(stress)) stress = 0.f;
        float res = 1.f - 2.f*stress;
        if (res < 0.f) res = 0.f;
        resources[i] = res;
    }

    return out;
}

// ---- pybind -----------------------------------------------------------------
PYBIND11_MODULE(foncpp, m){
    m.doc() = "C++ HPC backend for FONHPC (belowground): window(+circle) + support-bitmask; float32 strict; deterministic matches Python.";
    m.def("compute_fon_resources", &compute_fon_resources,
          py::arg("grid_x"), py::arg("grid_y"),
          py::arg("plant_x"), py::arg("plant_y"), py::arg("r_stem"),
          py::arg("aa"), py::arg("bb"), py::arg("fmin"),
          py::arg("threads")=0, py::arg("deterministic")=true);
}
