# SYCL Academy

## Coalesced Global Memory
---

In this exercise you will learn how to apply row-major and column-major when
linearizing the global id in order to compare the performance difference due to
coalesced global memory access.

---

### 1.) Evaluate global memory access

Now that you have a working image convolution kernel you should evaluate whether the
global memory access patterns in your kernel are coalesced.

SYCL buffer & accessor objects can be multi-dimensional, and in this image convolution
example 2d buffer/accessors are used which are operated on in the kernel using a
`sycl::id<2>` 2d index. This operation will
[calculate](https://registry.khronos.org/SYCL/specs/sycl-2020/html/sycl-2020.html#sec:multi-dim-linearization)
the linear address in memory based on the size of the dimensions.

Try inverting the dimensions used in the 2d index and compare the execution time.

## Build and execution hints

From the syclacademy directory
```sh
cd build/Code_Exercises/Coalesced_Global_Memory
```
and execute:
* ```make Coalesced_Global_Memory_source``` - to build source.cpp
* ```make Coalesced_Global_Memory_solution``` - to build the solution provided
* ```make``` - to build both

Alternatively from a terminal at the command line:
```sh
icpx -fsycl -o Coalesced_Global_Memory_source -I../../Utilities/include/ -I../../External/stb ../Code_Exercises/Coalesced_Global_Memory/source.cpp
```

In Intel DevCloud, to run computational applications, you will submit jobs to a queue for execution on compute nodes,
especially some features like longer walltime and multi-node computation is only available through the job queue.
Please refer to the [guide][devcloud-job-submission].

So wrap the binary into a script `job_submission`
```sh
#!/bin/bash
./Coalesced_Global_Memory_source
```
and run:
```sh
qsub -l nodes=1:gpu:ppn=2 -d . job_submission
```

The stdout will be stored in ```job_submission.o<job id>``` and stderr in ```job_submission.e<job id>```.

For DPC++:
Using CMake to configure then build the exercise:
```sh
mkdir build
cd build
cmake .. "-GUnix Makefiles" -DSYCL_ACADEMY_USE_DPCPP=ON -DSYCL_ACADEMY_ENABLE_SOLUTIONS=OFF -DCMAKE_C_COMPILER=icx -DCMAKE_CXX_COMPILER=icpx
make Coalesced_Global_Memory_source
```
Alternatively from a terminal at the command line:
```sh
icpx -fsycl -o Coalesced_Global_Memory_source ../Code_Exercises/Coalesced_Global_Memory/source.cpp
./Coalesced_Global_Memory_source
```

For AdaptiveCpp:
```sh
# <target specification> is a list of backends and devices to target, for example
# "generic" compiles for CPUs and GPUs using the generic single-pass compiler.
# When in doubt, use "generic" as it usually generates the fastest binaries.
#
# Recent, full installations of AdaptiveCpp may not need targets to be provided,
# compiling for "generic" by default.
cmake -DSYCL_ACADEMY_USE_ADAPTIVECPP=ON -DSYCL_ACADEMY_INSTALL_ROOT=/insert/path/to/adaptivecpp -DACPP_TARGETS="<target specification>" ..
make Coalesced_Global_Memory_source
```
alternatively, without CMake:
```sh
cd Code_Exercises/Coalesced_Global_Memory
/path/to/adaptivecpp/bin/acpp -o Coalesced_Global_Memory_source --acpp-targets="<target specification>" source.cpp
./Coalesced_Global_Memory_source
```
