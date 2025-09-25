# SYCL Academy

## Compiling with SYCL

---

For this first exercise you simply need to install a SYCL implementation and the SYCL
Academy dependencies and then verify your installation by comping a source file
for SYCL.


### 1.) Installing a SYCL implementation

To install a SYCL implementation, follow the instructions in the README.md of the SYCL
Academy repository.

### 2.) Verifying your environment

Depending on the SYCL implementation used, the steps to verify your environment might vary.

#### When using AdaptiveCpp

With AdaptiveCpp, you can skip this step. If you suspect later that your environment might not be set up correctly, you can run `acpp-info -l` in the `bin`  directory of your AdaptiveCpp installation. It will then print the backends and devices that it sees, for example:
```
$ acpp-info -l
=================Backend information===================
Loaded backend 0: OpenCL
  Found device: Intel(R) UHD Graphics 620 [0x5917]
  Found device: ComputeAorta x86_64
  Found device: Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz
Loaded backend 1: OpenMP
  Found device: hipSYCL OpenMP host device
Loaded backend 2: CUDA
  Found device: NVIDIA GeForce MX150
Loaded backend 3: Level Zero
  Found device: Intel(R) UHD Graphics 620 [0x5917]
```

### If you're using DevCloud via SSH

If you have not already installed SYCLAcademy, follow this [guide](../../README.md#connecting-to-devcloud-via-ssh) to perform the installation.

Go to the What_is_SYCL directory:
From the syclacademy directory
```
cd build/Code_Exercises/What_is_SYCL
```
and continue to [4](#4-include-the-sycl-header-file)

### 3.) Configuring the exercise project

Once you have confirmed your environment is setup and available you are ready to
compile your first SYCL application from source code.

First fetch the tutorial samples from GitHub.

Clone this repository ensuring that you include sub-modules.

```sh
git clone --recursive https://github.com/khronosgroup/syclacademy.git
mkdir build
cd build
```

### 4.) Include the SYCL header file

Then open the source file for this exercise and include the SYCL header file
`"sycl/sycl.hpp"`.

Make sure before you do this you define `SYCL_LANGUAGE_VERSION` to `2020`, to
enable support for the SYCL 2020 interface.

Once that is done build your source file with your chosen build system.

### 5.) Compile and run

Once you've done that simply build the exercise with your chosen build system
and invoke the executable.

#### Build And Execution Hints

If you are using DevCloud via SSH:

If you haven't done so already, follow this [guide](../../README.md#building-the-exercises-for-dpc++) to build the exercise directory structure.

From the syclacademy directory
```
cd build/Code_Exercises/What_is_SYCL
```
and execute:
* ```make What_is_SYCL_source```   - to build source.cpp
* ```make What_is_SYCL_solution``` - to build the solution provided
* ```make``` - to build both

In Intel DevCloud, to run computational applications, you will submit jobs to a queue for execution on compute nodes,
especially some features like longer walltime and multi-node computation is only available through the job queue.
Please refer to the [guide][devcloud-job-submission].

So wrap the binary into a script `job_submission`
```
#!/bin/bash
./What_is_SYCL_source
```
and run:
```sh
qsub -l nodes=1:gpu:ppn=2 -d . job_submission
```

The stdout will be stored in ```job_submission.o<job id>``` and stderr in ```job_submission.e<job id>```.

Using CMake to configure then build the exercise:
```sh
mkdir build
cd build
cmake .. "-GUnix Makefiles" -DSYCL_ACADEMY_USE_DPCPP=ON
  -DSYCL_ACADEMY_ENABLE_SOLUTIONS=OFF -DCMAKE_C_COMPILER=icx -DCMAKE_CXX_COMPILER=icpx
make What_is_SYCL_source
```
Alternatively from a terminal at the command line:
```sh
icpx -fsycl -o What_is_SYCL_source ../Code_Exercises/What_is_SYCL/source.cpp
./What_is_SYCL_source
```

For AdaptiveCpp:
```sh
# <target specification> is a list of backends and devices to target, for example
# "generic" compiles for CPUs and GPUs using the generic single-pass compiler.
# When in doubt, use "generic" as it usually generates the fastest binaries.
#
# Recent, full installations of AdaptiveCpp may not need targets to be provided,
# compiling for "generic" by default.
cmake -DSYCL_ACADEMY_USE_ADAPTIVECPP=ON -DSYCL_ACADEMY_INSTALL_ROOT=/insert/path/to/AdaptiveCpp -DACPP_TARGETS="<target specification>" ..
make What_is_SYCL_source
```
alternatively, without CMake:
```sh
cd Code_Exercises/What_is_SYCL
/path/to/AdaptiveCpp/bin/acpp -o What_is_SYCL_source --acpp-targets="<target specification>" source.cpp
./What_is_SYCL_source
```


[devcloud-job-submission]: https://devcloud.intel.com/oneapi/documentation/job-submission/
