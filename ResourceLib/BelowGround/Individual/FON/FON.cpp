// ResourceLib/BelowGround/Individual/FON/FON.cpp
//
// Pybind11 C++ core for the Field of Neighborhood (FON) below-ground
// competition model (Berger & Hildenbrandt 2000, Eq. 7).
//
// Key optimizations over the Python path:
// - Grid spatial indexing: only cells within FON radius are visited.
// - No 3D tensor allocation.
// - Deterministic OpenMP parallelization over contiguous plant ranges.
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

namespace {

struct PlantWindow {
    int col_lo;
    int col_hi;
    int row_lo;
    int row_hi;
};

struct ContributionBuffer {
    std::vector<int> cells;
    std::vector<double> heights;
};

struct FONWorkspace {
    std::vector<double> fon_radius;
    std::vector<double> cc;
    std::vector<double> total_fon;
    std::vector<PlantWindow> windows;
    std::vector<std::uint64_t> cumulative_work;
    std::vector<int> boundaries;
    std::vector<ContributionBuffer> contributions;
    std::vector<std::size_t> contribution_begin;
    std::vector<std::size_t> contribution_end;
};

FONWorkspace& get_workspace() {
    static thread_local FONWorkspace workspace;
    return workspace;
}

}  // namespace

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

    const double* px = xe.data();
    const double* py_ = ye.data();
    const double* pr = r_stem.data();
    const double* paa = aa.data();
    const double* pbb = bb.data();
    const double* pfmin = fmin.data();
    const double* pphi = phi.data();
    const double* pgx = grid_x.data();
    const double* pgy = grid_y.data();

    // Reuse internal storage across calls. pybind11 keeps the GIL held for this
    // function, and thread-local storage also isolates independent callers.
    FONWorkspace& workspace = get_workspace();
    std::vector<double>& fon_radius = workspace.fon_radius;
    std::vector<double>& cc = workspace.cc;
    std::vector<double>& total_fon = workspace.total_fon;
    std::vector<PlantWindow>& windows = workspace.windows;
    std::vector<std::uint64_t>& cumulative_work = workspace.cumulative_work;
    std::vector<int>& boundaries = workspace.boundaries;
    std::vector<ContributionBuffer>& contributions = workspace.contributions;
    std::vector<std::size_t>& contribution_begin = workspace.contribution_begin;
    std::vector<std::size_t>& contribution_end = workspace.contribution_end;

    // Grid geometry (uniform spacing, derived from grid arrays)
    const double x_origin = pgx[0];                    // first col center
    const double y_origin = pgy[0];                     // first row center
    const double x_step = (gx > 1) ? (pgx[1] - pgx[0]) : lx;
    const double y_step = (gy > 1) ? (pgy[gx] - pgy[0]) : ly;

    // Storage for per-plant FON parameters
    fon_radius.resize(n_plants);
    cc.resize(n_plants);

    // Per-cell total FON height
    total_fon.assign(grid_size, 0.0);

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

    // floor/ceil deliberately produces a conservative spatial window. Trim
    // only edge rows and columns that the original Euclidean-distance test
    // would reject even when the other distance component is zero. This
    // reduces grid traversal without changing the order or arithmetic of any
    // retained cell.
    auto trim_window = [&](double x, double y, double radius, PlantWindow& window) {
        auto column_outside = [&](int col) {
            const int ci = periodic ? ((col % gx + gx) % gx) : col;
            double dx = pgx[ci] - x;
            if (periodic) dx -= lx * std::round(dx / lx);
            return std::sqrt(dx * dx) > radius;
        };
        auto row_outside = [&](int row) {
            const int r = periodic ? ((row % gy + gy) % gy) : row;
            double dy = pgy[r * gx] - y;
            if (periodic) dy -= ly * std::round(dy / ly);
            return std::sqrt(dy * dy) > radius;
        };

        while (window.col_lo <= window.col_hi && column_outside(window.col_lo)) {
            ++window.col_lo;
        }
        while (window.col_lo <= window.col_hi && column_outside(window.col_hi)) {
            --window.col_hi;
        }
        while (window.row_lo <= window.row_hi && row_outside(window.row_lo)) {
            ++window.row_lo;
        }
        while (window.row_lo <= window.row_hi && row_outside(window.row_hi)) {
            --window.row_hi;
        }
    };

    // Storage for spatial windows and their approximate cumulative work.
    windows.resize(n_plants);
    cumulative_work.resize(n_plants + 1);

    int thread_count = 1;
#ifdef _OPENMP
    // The deterministic partition assumes the requested team size is used.
    // Disabling dynamic teams does not override OMP_NUM_THREADS.
    omp_set_dynamic(0);
    thread_count = (n_threads > 0) ? n_threads : omp_get_max_threads();
    thread_count = std::max(1, std::min(thread_count, n_plants));
#else
    (void)n_threads;
#endif

    auto set_boundaries = [&](int count) {
        boundaries.assign(count + 1, 0);
        boundaries[count] = n_plants;
        if (cumulative_work[n_plants] == 0) {
            for (int t = 1; t < count; ++t) {
                boundaries[t] = static_cast<int>(
                    static_cast<std::int64_t>(n_plants) * t / count);
            }
        } else {
            for (int t = 1; t < count; ++t) {
                const std::uint64_t target = cumulative_work[n_plants] * t / count;
                boundaries[t] = static_cast<int>(
                    std::lower_bound(cumulative_work.begin(), cumulative_work.end(), target)
                    - cumulative_work.begin());
            }
        }
    };
    auto prepare_boundaries = [&]() {
        cumulative_work[0] = 0;
        for (int i = 0; i < n_plants; ++i) {
            const PlantWindow& window = windows[i];
            const std::uint64_t cols = static_cast<std::uint64_t>(
                std::max(0, window.col_hi - window.col_lo + 1));
            const std::uint64_t rows = static_cast<std::uint64_t>(
                std::max(0, window.row_hi - window.row_lo + 1));
            cumulative_work[i + 1] = cumulative_work[i] + rows * cols;
        }
        set_boundaries(thread_count);
    };
    const int requested_thread_count = thread_count;

    // Small teams do not amortize an additional OpenMP work-sharing barrier.
    // Keep their preprocessing on the optimized serial path.
    if (requested_thread_count < 4) {
        for (int i = 0; i < n_plants; ++i) {
            fon_radius[i] = paa[i] * std::pow(pr[i], pbb[i]);
            cc[i] = -std::log(pfmin[i]) / (fon_radius[i] - pr[i]);

            auto [col_lo, col_hi] = index_range(
                px[i], x_origin, x_step, gx, fon_radius[i], periodic);
            auto [row_lo, row_hi] = index_range(
                py_[i], y_origin, y_step, gy, fon_radius[i], periodic);
            windows[i] = {col_lo, col_hi, row_lo, row_hi};
            trim_window(px[i], py_[i], fon_radius[i], windows[i]);
        }
        prepare_boundaries();
    }

    if (contributions.size() < static_cast<std::size_t>(thread_count)) {
        contributions.resize(thread_count);
    }
    for (int tid = 0; tid < thread_count; ++tid) {
        contributions[tid].cells.clear();
        contributions[tid].heights.clear();
    }
    contribution_begin.resize(n_plants);
    contribution_end.resize(n_plants);
    py::array_t<double> out(n_plants);
    double* output = out.mutable_data();

    // Keep preprocessing and both computational passes in one OpenMP region to
    // avoid repeatedly creating and synchronizing a thread team for this
    // short-running kernel.
#ifdef _OPENMP
    #pragma omp parallel num_threads(requested_thread_count)
#endif
    {
#ifdef _OPENMP
        // Record the actual team size if an implementation supplies a smaller
        // team than requested (for example because OMP_THREAD_LIMIT is set).
        #pragma omp single
        {
            const int actual_thread_count = omp_get_num_threads();
            if (actual_thread_count != thread_count) {
                thread_count = actual_thread_count;
                if (requested_thread_count < 4) {
                    set_boundaries(thread_count);
                }
            }
        }
        const int tid = omp_get_thread_num();
#else
        const int tid = 0;
#endif

        if (requested_thread_count >= 4) {
            // Precompute independent per-plant parameters and spatial windows
            // in parallel. Each plant performs the same floating-point
            // operations as the serial implementation.
#ifdef _OPENMP
            #pragma omp for schedule(static)
#endif
            for (int i = 0; i < n_plants; ++i) {
                fon_radius[i] = paa[i] * std::pow(pr[i], pbb[i]);
                cc[i] = -std::log(pfmin[i]) / (fon_radius[i] - pr[i]);

                auto [col_lo, col_hi] = index_range(
                    px[i], x_origin, x_step, gx, fon_radius[i], periodic);
                auto [row_lo, row_hi] = index_range(
                    py_[i], y_origin, y_step, gy, fon_radius[i], periodic);
                windows[i] = {col_lo, col_hi, row_lo, row_hi};
                trim_window(px[i], py_[i], fon_radius[i], windows[i]);
            }

            // Contiguous, work-balanced ranges let the deterministic merge
            // retain exactly the original plant order.
#ifdef _OPENMP
            #pragma omp single
#endif
            {
                prepare_boundaries();
            }
        }

        // Pass 1a evaluates plant contributions in parallel. Each thread owns
        // a contiguous plant range and a private buffer, so there are no shared
        // writes and no atomics. Contributions remain ordered by plant, row,
        // and column exactly as in the original serial loop.
        ContributionBuffer& buffer = contributions[tid];
        const int plant_begin = boundaries[tid];
        const int plant_end = boundaries[tid + 1];
        const std::uint64_t candidate_work =
            cumulative_work[plant_end] - cumulative_work[plant_begin];
        if (candidate_work <= buffer.cells.max_size() &&
            candidate_work <= buffer.heights.max_size()) {
            const std::size_t capacity = static_cast<std::size_t>(candidate_work);
            buffer.cells.reserve(capacity);
            buffer.heights.reserve(capacity);
        }

        for (int i = plant_begin; i < plant_end; ++i) {
            contribution_begin[i] = buffer.cells.size();

            const double x = px[i], y = py_[i];
            const double rs = pr[i], fr = fon_radius[i], c = cc[i], fm = pfmin[i];
            const PlantWindow& window = windows[i];

            for (int row = window.row_lo; row <= window.row_hi; ++row) {
                const int r = periodic ? ((row % gy + gy) % gy) : row;
                const double gy_val = pgy[r * gx];
                double dy = gy_val - y;
                if (periodic) dy -= ly * std::round(dy / ly);

                for (int col = window.col_lo; col <= window.col_hi; ++col) {
                    const int ci = periodic ? ((col % gx + gx) % gx) : col;
                    const double gx_val = pgx[ci];
                    double dx = gx_val - x;
                    if (periodic) dx -= lx * std::round(dx / lx);

                    const double dist = std::sqrt(dx * dx + dy * dy);
                    if (dist > fr) continue;

                    double h = std::exp(-c * (dist - rs));
                    if (h > 1.0) h = 1.0;
                    if (h < fm) continue;

                    buffer.cells.push_back(r * gx + ci);
                    buffer.heights.push_back(h);
                }
            }
            contribution_end[i] = buffer.cells.size();
        }

        // Pass 1b merges private buffers in their original plant order.
        // Keeping this inexpensive addition step in a single thread preserves
        // the serial floating-point summation order for every grid cell. The
        // implicit barrier after omp single makes total_fon visible to Pass 2.
#ifdef _OPENMP
        #pragma omp barrier
        #pragma omp single
#endif
        {
            for (int merge_tid = 0; merge_tid < thread_count; ++merge_tid) {
                const ContributionBuffer& merge_buffer = contributions[merge_tid];
                for (std::size_t j = 0; j < merge_buffer.cells.size(); ++j) {
                    total_fon[merge_buffer.cells[j]] += merge_buffer.heights[j];
                }
            }
        }

        // Pass 2 computes each plant's resource limitation in parallel. The
        // stored contributions avoid recalculating distance and exp(), while
        // each plant retains its original cell traversal and accumulation
        // order. Threads write to disjoint output elements.
        for (int i = boundaries[tid]; i < boundaries[tid + 1]; ++i) {
            double local_impact = 0.0;
            for (std::size_t j = contribution_begin[i]; j < contribution_end[i]; ++j) {
                local_impact += total_fon[buffer.cells[j]] - buffer.heights[j];
            }
            const double area = static_cast<double>(
                contribution_end[i] - contribution_begin[i]);
            if (area > 0.0) {
                const double stress = local_impact / area;
                const double rl = 1.0 - pphi[i] * stress;
                output[i] = (rl < 0.0) ? 0.0 : rl;
            } else {
                output[i] = 1.0;
            }
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
