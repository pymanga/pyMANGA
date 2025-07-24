# Description
stable version!
Stable version updated after local testing on July 24.
Read the md file of benchmarks. Refer to the test xml. We welcome more complex and extreme tests.

The High-Performance Computing related code modules follow five main optimization logic:
1. Parallelized Single-Tree Height Matrix Computation
joblib.Parallel and delayed are used to parallelize _compute_single_tree.
The number of parallel threads (n_jobs) is dynamically adjusted based on the number of CPU cores via _determine_n_jobs.
By default, the number of threads is capped at 10 to avoid scheduling overhead on personal computers (this restriction does not apply to HPC environments).
2. Batch Processing
Batch processing is employed to reduce memory peaks. The number of trees processed in each batch is inversely adjusted based on the grid resolution (grid_size) via _determine_batch_size:
Larger grids result in fewer trees being processed per batch, thereby reducing memory usage and preventing memory spikes. The default batch size cap is 8000 trees (this can be adjusted based on resolution and plant count).
After each batch is completed, results are gradually merged into canopy_height and highest_plant, rather than allocating a global height matrix for each tree.
3. Avoid Frequent Boolean Array Allocation
To reduce memory allocation overhead, mask_buffer is pre-allocated and updated in place using np.copyto with the where parameter.
4. Efficient Wins Statistics
np.bincount is used to directly count the number of wins for each tree in highest_plant, significantly reducing computational complexity.
5. Memory Optimization
np.zeros_like(grid_x) is used instead of np.zeros(grid_x.shape) to reduce shape inference overhead.
canopy_height and highest_plant are updated in place where necessary, avoiding multiple full matrix allocations.
1.  float64 or float32 ？
Using float32 instead of float64 reduces memory usage by approximately 30% (based on my simple tests with a 100 ha scenario). However, this also leads to accumulated numerical errors. In my current tests, the accumulated deviation appears after the sixth decimal place. （Changing float is dangerous. It is recommended to use float64.）


(I do not recommend excessive optimization, as personal computers are not well-suited for HPC-style optimization. It can significantly impact the computer’s lifespan and requires high hardware specifications. Therefore, I suggest considering high-performance computing as an optional approach for simulations. I have rewritten these modules mainly because my computational demands are exceptionally high. The need for optimization depends on the pyMANGA team. If the team considers such modules useful, we can continue to move forward with further work.)

# Usage

```xml

<aboveground>
    <type>AsymmetricZOIHighPerformanceComputing</type>
    <domain>
        <x_1>0</x_1>
        <y_1>0</y_1>
        <x_2>500</x_2>
        <y_2>200</y_2>
        <x_resolution>4000</x_resolution>
        <y_resolution>800</y_resolution>
    </domain>
</aboveground>
```

# Environmental Requirements

```bash
conda install -c conda-forge numpy joblib multiprocessing
```

# Testing Method
Run the following project files separately to do long time simulation compare:
Benchmarks\HighPerformanceComputing\xml\Original1HA.xml
Benchmarks\HighPerformanceComputing\xml\AsymmetricZOIHighPerformanceComputing1HA.xml
Benchmarks\HighPerformanceComputing\xml\AsymmetricZOIFixedSalinityHighPerformanceComputing1HA.xml

Run the following project files separately to do huge resolution simulation compare:
Benchmarks\HighPerformanceComputing\xml\Original10HA.xml   
Benchmarks\HighPerformanceComputing\xml\AsymmetricZOIHighPerformanceComputing10HA.xml
Benchmarks\HighPerformanceComputing\xml\AsymmetricZOIFixedSalinityHighPerformanceComputing10HA.xml

Run the following project files separately to do double resolution simulation compare:
Benchmarks\HighPerformanceComputing\xml\ZOISaltFeedbackBucket1HA.xml
Benchmarks\HighPerformanceComputing\xml\AsymmetricZOISaltFeedbackBucketHighPerformanceComputing1HA.xml  
(This is the large updateoptimized version from ZOISaltFeedbackBucket, in my tests, it is about 10 times faster than the original ZOISaltFeedbackBucket)

If you want, Please try 100HA (cpu will die) :)

Compare the runtime of a single time step. After the simulation, compare the output results.

# How to Improve Performance
As mentioned in the Description section, any of the five points could become a bottleneck for the simulation.
Further HPC optimization requires a thorough review and potential refactoring of all code modules.
Again: I do not recommend excessive optimization, as personal computers are not well-suited for HPC-style optimization. It can significantly impact the computer’s lifespan and requires high hardware specifications. Therefore, I suggest considering high-performance computing as an optional approach for simulations. I have rewritten these modules mainly because my computational demands are exceptionally high.


# Notes：
On personal computers, memory limitations are the primary bottleneck. When multiple CPU cores simultaneously perform large memory operations, CPU performance may degrade, often triggering memory warnings.
Therefore, the above optimizations are best suited for HPC environments, which typically provide terabytes of memory and hundreds or even thousands of CPU cores.

To prevent memory explosions and "computational efficiency traps," I have set upper limits on the number of cores and trees processed per batch within the optimized modules. This ensures stable performance.

The "computational efficiency trap" represents a trade-off: Using too many CPU cores simultaneously can increase memory consumption, which may lead to reduced performance or even exceeding memory limits.

# Dangerous
The calibration of FixedSalinityHighPerformanceComputing is not yet complete, and the result differences are likely caused by float. To reduce memory usage on my local machine, I implemented the module using float32.(fixed)