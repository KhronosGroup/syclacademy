# SYCL Academy

![SYCL Academy](sycl_academy_black.png#gh-light-mode-only "SYCL Academy")
![SYCL Academy](sycl_academy_white.png#gh-dark-mode-only "SYCL Academy")

This repository provides materials that can be used for teaching SYCL. The
materials are provided using the "Creative Commons Attribution Share Alike 4.0
International" license.

## What is SYCL?

If you're not familiar with SYCL or would like some further resources for
learning about SYCL below are a list of useful resources:

*  Read a description of SYCL on the [Khronos website SYCL page](https://www.khronos.org/sycl/).
*  Go to the Khronos website to find [a list of SYCL resources](https://www.khronos.org/sycl/resources).
*  Check out the [SYCL 2020 reference guide](https://www.khronos.org/registry/SYCL/).
*  Browse SYCL news, blog posts, videos, projects and more on the [sycl.tech community website](https://sycl.tech/)
*  Get a list of the [available SYCL implementations](https://sycl.tech/#get-sycl)

### How to use the Materials

To use these materials simply clone this repository including the required submodules.

```
git clone --recursive https://github.com/KhronosGroup/syclacademy.git
```

The lectures are written in reveal.js, and can be found in `Lesson_Materials`,
in the sub-directory for each topic. To view them simply open the `index.html`
file in your browser. Your browser will have a "Full Screen" mode that can be
used to run the presentation, use the right and left cursors to move forward and
backward in the presentation.

The exercises can be found in `Code_Exercises` in the sub-directory for each
topic. Each exercise has a markdown document instructing what to do in the
exercise, a source file to start with and a solution file to provide an
example implementation to compare against.

## Contributing to SYCL Academy

Contributions to the materials are very gratefully received and this can be done
by submitting a Pull Request with any changes. If you can, follow the
instructions [here](https://revealjs.com/pdf-export/) to generate a pdf file for
any lecture slides you change. Please limit the scope of each
Pull Request so that they can be reviewed and merged in a timely manner.

### List of Contributors

Codeplay Software Ltd., Heidelberg University, Intel, Xilinx and University of Bristol.

## Supporting Organizations

Abertay University, Universidad de Concepcion, TU Dresden, University of
Edinburgh, Federal University of Sao Carlos, University of Glasgow, Heriot Watt
University, Universitat Innsbruck, Universidad de Málaga, University of Salerno
and University of the West of Scotland.

## Lesson Curriculum

The SYCL Academy curriculum is divided up into a number of short lessons
consisting of slides for presenting the material and a more detailed write-up,
each accompanied by a tutorial for getting hands on experience with the subject
matter.

Each of the lessons are designed to be self contained modules in order to
support both academic and training style teaching environments.

A playlist of video content is [also available][video-playlist]. Though note that these
slides and exercises may have changed since these videos were created so they
may not match completely.

| Lesson | Title | Slides | Exercise | Source | Solution |
|--------|-------|--------|----------|--------|----------|
| 01 | What is SYCL | [slides][lesson-1-slides] | [exercise][lesson-1-exercise] | [source][lesson-1-source] | [solution][lesson-1-solution] |
| 02 | Enqueueing a Kernel | [slides][lesson-2-slides] | [exercise][lesson-2-exercise] | [source][lesson-2-source] | [solution][lesson-2-solution] |
| 03 | Managing Data | [slides][lesson-3-slides] | [exercise][lesson-3-exercise] | [source][lesson-3-source] | [solution][lesson-3-solution] |
| 04 | Handling Errors | [slides][lesson-4-slides] | [exercise][lesson-4-exercise] | [source][lesson-4-source] | [solution][lesson-4-solution] |
| 05 | Device Discovery | [slides][lesson-5-slides] | [exercise][lesson-5-exercise] | [source][lesson-5-source] | [solution][lesson-5-solution] |
| 06 | Data Parallelism | [slides][lesson-6-slides] | [exercise][lesson-6-exercise] | [source][lesson-6-source] | [solution][lesson-6-solution] |
| 07 | Introduction to USM | [slides][lesson-7-slides] | [exercise][lesson-7-exercise] | [source][lesson-7-source] | [solution][lesson-7-solution] |
| 08 | Using USM | [slides][lesson-8-slides] | [exercise][lesson-8-exercise] | [source][lesson-8-source] | [solution][lesson-8-solution] |
| 09 | Asynchronous Execution | [slides][lesson-9-slides] | [exercise][lesson-9-exercise] | [source][lesson-9-source] | [solution][lesson-9-solution] |
| 10 | Data and Dependencies | [slides][lesson-10-slides] | [exercise][lesson-10-exercise] | [source][lesson-10-source] | [solution][lesson-10-solution] |
| 11 | In Order Queue | [slides][lesson-11-slides] | [exercise][lesson-11-exercise] | [source][lesson-11-source] | [solution][lesson-11-solution] |
| 12 | Advanced Data Flow | [slides][lesson-12-slides] | [exercise][lesson-12-exercise] | [source][lesson-12-source] | [solution][lesson-12-solution] |
| 13 | Multiple Devices | [slides][lesson-13-slides] | [exercise][lesson-13-exercise] | [source][lesson-13-source] | [solution][lesson-13-solution] |
| 14 | Image Convolution | [slides][lesson-14-slides] | [exercise][lesson-14-exercise] | [source][lesson-14-source] | [solution][lesson-14-solution] |
| 15 | Coalesced Global Memory | [slides][lesson-15-slides] | [exercise][lesson-15-exercise] | [source][lesson-15-source] | [solution][lesson-15-solution] |
| 16 | Vectors | [slides][lesson-16-slides] | [exercise][lesson-16-exercise] | [source][lesson-16-source] | [solution][lesson-16-solution] |
| 17 | Local Memory Tiling | [slides][lesson-17-slides] | [exercise][lesson-17-exercise] | [source][lesson-17-source] | [solution][lesson-17-solution] |
| 18 | Further Optimisations | [slides][lesson-18-slides] | [exercise][lesson-18-exercise] | [source][lesson-18-source] | [solution][lesson-18-solution] |
| 19 | Matrix Transpose | [slides][lesson-19-slides] | [exercise][lesson-19-exercise] | [source][lesson-19-source] | [solution][lesson-19-solution] |
| 20 | More SYCL Features | [slides][lesson-20-slides] | [exercise][lesson-20-exercise] | [source][lesson-20-source] | [solution][lesson-20-solution] |
| 21 | Functors | [slides][lesson-21-slides] | [exercise][lesson-21-exercise] | [source][lesson-21-source] | [solution][lesson-21-solution] |

### oneMath

The lessons in this table work with oneAPI, but might not work with other
SYCL implementations.

| Lesson | Title | Slides | Exercise | Source | Solution |
|--------|-------|--------|----------|--------|----------|
| 22 | OneMath GEMM | [slides][lesson-22-slides] | [execise][lesson-22-exercise] | [source][lesson-22-source] | [solution][lesson-22-solution] |

## Building the Exercises

The exercises can be built for DPC++ and AdaptiveCpp.

### Supported Platforms

Below is a list of the supported platforms and devices for each SYCL implementations,
please check this before deciding which SYCL implementation to use.
Make sure to also install the specified version to ensure that you can build
all of the exercises.

| Implementation | Supported Platforms | Supported Devices | Required Version |
|----------------|---------------------|-------------------|------------------|
| DPC++ | [Intel DevCloud](#connecting-to-devcloud-via-ssh) <br> Windows 10 Visual Studio 2019 (64bit) <br> Red Hat Enterprise Linux 8, CentOS 8<br> Ubtuntu 18.04 LTS, 20.04 LTS (64bit)<br> Refer to [System Requirements][oneAPI-system-requirements] for more details | Intel CPU (OpenCL) <br> Intel GPU (OpenCL) <br> Intel FPGA (OpenCL) <br> Nvidia GPU (CUDA)* | 2021.4	|
| AdaptiveCpp | Any Linux | CPU (OpenMP) <br> AMD GPU (ROCm)*** <br> NVIDIA GPU (CUDA)<br> Intel GPU (Level Zero)<br> Intel CPU, GPU (OpenCL) | 23.10.0 from Nov 1, 2023 or newer |

\* Supported in open source project only

\*\* See [here][rocm-gpus] for the official list of GPUs supported by AMD for
ROCm. We do not recommend using GPUs earlier than gfx9 (Vega 10 and Vega 20
chips).

### Install SYCL implementations

First you'll need to install your chosen SYCL implementation and any
dependencies they require.

#### Installing DPC++

To set up DPC++ follow the [getting started instructions][dpcpp-getting-started].

You can also use a [Docker* image][docker-container-oneapi].

If you are using the [Intel DevCloud][intel-devcloud] then the latest version of DPC++ will
already be installed and available in the path.

#### Installing AdaptiveCpp

You will need a AdaptiveCpp (formerly hipSYCL) build from September 2021 or newer. Refer to the [AdaptiveCpp installation instructions][adaptivecpp-installing] for details on how to install AdaptiveCpp.

### Pre-requisites

Before building the exercises you'll need:

* One of the platforms in the support matrix above, depending on which SYCL
implementation you are wishing to build for.
* A C++17 or above tool-chain.
* An appropriate build system for the platform you are targeting (CMake, Ninja,
Make, Visual Studio).

### Configuring using CMake

Clone this repository, there are some additional dependencies configured as git
sub-modules so make sure to clone those as well. Then simply invoke CMake as
follows:

```
mkdir build

cd build

cmake ../ -G<cmake_generator> -A<cmake_arch> -D<sycl_implementation>=ON
```

For `<cmake_generator>` / `<cmake_arch>` we recommend:

* Visual Studio 16 2019 / x64 (Windows)
* Ninja / NA (Windows or Linux)
* Make / NA (Linux) i.e. "-GUnix Makefiles"

For `sycl_implementation` this can be one of:

* `SYCL_ACADEMY_USE_ADAPTIVECPP`
* `SYCL_ACADEMY_USE_DPCPP`

You can also specify the additional optional options:

```
-DSYCL_ACADEMY_INSTALL_ROOT=<path_to_sycl_impl_install_root>
```

For `<path_to_sycl_impl_install_root>` we recommend you specify the path to the
root directory of your SYCL implementation installation, though this may not
always be required.

```
-DSYCL_ACADEMY_ENABLE_SOLUTIONS=ON
```

This will enable building the solutions for each exercise as well as the source
files. This is disabled by default.

```
-DCMAKE_BUILD_TYPE=Release
```

The build configuration for all exercises defaults to a debug build if this option is not specified.

#### Additional cmake arguments for DPC++

```
-DCMAKE_C_COMPILER=icx -DCMAKE_CXX_COMPILER=icpx
```

This SYCL Academy CMake configuration uses the Intel oneAPI IntelSYCL CMake module package to assist it in its configuration. These command line arguments must be used to initiate this configuration correctly.

`-DSYCL_TRIPLE` can be used to specify a DPC++ compatible SYCL triple. Possible
values include:

* `amdgcn-amd-amdhsa` - For AMD devices
* `nvptx64-nvidia-cuda` - For CUDA devices
* `spir64_gen` - For Intel GPUs
* `native_cpu` - For native CPU SYCL device (dependent on DPCPP version)

`-DSYCL_ARCH` can also be used to specify a device arch. This CMake opt is
necessary for AMD. Possible values include:

* `gfx90a` - For AMD MI200
* `sm_80` - For NVIDIA A100
* `pvc` - For Intel PVC

It may also be necessary to manually specify the install location of the CUDA or
ROCM SDK, if this is found in a non-standard location. The flags:

`-DROCM_DIR` and `-DCUDA_DIR` can be used to specify the install dir of the ROCM
or CUDA SDKs, respectively.

##### DPC++ for AMD CMake example

```
  cmake .. -GNinja -DSYCL_ACADEMY_USE_DPCPP=ON -DSYCL_ACADEMY_ENABLE_SOLUTIONS=ON -DCMAKE_C_COMPILER=icx -DCMAKE_CXX_COMPILER=icpx _DSYCL_TRIPLE=amdgcn-amd-amdhsa -DSYCL_ARCH=gfx90a -DROCM_DIR=/opt/rocm/5.4.3
```

##### DPC++ for CUDA CMake example

```
  cmake .. -GNinja -DSYCL_ACADEMY_USE_DPCPP=ON -DSYCL_ACADEMY_ENABLE_SOLUTIONS=ON -DCMAKE_C_COMPILER=icx -DCMAKE_CXX_COMPILER=icpx _DSYCL_TRIPLE=nvptx64-nvidia-cuda -DSYCL_ARCH=sm_61 -DCUDA_DIR=/usr/local/cuda/11.2/
```

#### Additional cmake arguments for AdaptiveCpp

Sufficiently new (>= 24.02.0), full installations of AdaptiveCpp do not require specifying compilation targets.
In this case, targets may still be provided optionally. 

For older AdaptiveCpp versions, CMake will require you to specify the compilation targets using `-DACPP_TARGETS=<target specification>`. 

`<target specification>` is a list of compilation flows to enable and devices to target, for example
`-DACPP_TARGETS="omp;generic"` compiles for CPUs using OpenMP and GPUs using the generic single-pass compiler.

If your AdaptiveCpp installation does not force a compilation target to be provided, but it was built with the generic single-pass compiler disabled (it is enabled by default in all AdaptiveCpp installations built against LLVM >= 14), it is compiling for a default set of targets provided at installation time. If you cannot run the binary on the hardware of your choice, this default set may not be the right one for your hardware and you may have to specify the right targets explicitly.

Available compilation flows are:
* `omp` - OpenMP CPU backend
* `generic` - Generic single-pass compiler. Generates a binary that runs on host CPU, AMD, NVIDIA and Intel GPUs using runtime compilation
* `cuda` - CUDA backend for NVIDIA GPUs. Requires specification of targets of the form sm_XY, e.g. sm_70 for Volta, sm_60 for Pascal. E.g: `cuda:sm_70`.
* `hip`  - HIP backend for AMD GPUs. Requires specification of targets of the form gfxXYZ, e.g. gfx906 for Vega 20, gfx900 for Vega 10. E.g.: `hip:gfx906`.

When in doubt, use `-DACPP_TARGETS=generic` as it compiles the fastest, usually generates the fastest binaries, and generates portable binaries.

#### CMake usage example

Invoking CMake from the command line example usage:
```
  cmake .. "-GUnix Makefiles" -DSYCL_ACADEMY_USE_DPCPP=ON -DSYCL_ACADEMY_ENABLE_SOLUTIONS=ON -DCMAKE_C_COMPILER=icx -DCMAKE_CXX_COMPILER=icpx
```

### Getting started with compiling DPC++

First you have to ensure that your environment is configured to use DPC++ (note
if you are using the Intel DevCloud then you don't need to do this step).

On Linux simply call the `setvars.sh` which is available in `/opt/intel/oneapi`
for sudo or root users and ~/intel/oneapi/ when installed as a normal user.

For root or sudo installations:
`source /opt/intel/oneapi/setvars.sh`

For normal user installations:
`source ~/intel/oneapi/setvars.sh`

On Windows the script is located in  `<dpc++_install_root>\setvars.bat`

Where `<dpc++_install_root>` is wherever the `oneAPI` directory is installed.

Once that's done you can invoke the DPC++ compiler as follows:

`icpx -fsycl -o a.out source.cpp`

Where `<syclacademy_root>` is the path to the root directory of where you cloned
this repository. Note that on Windows you need to add the option /EHsc to avoid exception handling error.

The CMake configuration can also be used to build the exercises, see the section **Configuring using CMake** above.

## Working on the Exercises
Once you have a working SYCL compiler, you are ready to start writing some SYCL code. To find the first exercise:
```
cd Code_Exercises/Compiling_with_SYCL/
```
And read the README.md for further instructions.

Each exercise directory contains:
* ```README.md```, which contains instructions of how to complete a given exercise, as well as directions for compilation.
* ```source.cpp```, a placeholder file where your code implementation should be written.
* ```solution.cpp```, where a solution has been implemented in advance.

Once you have completed any given exercise make sure to compare your implementation against the corresponding ```solution.cpp```.

## Online Interactive Tutorial

Hosted by tech.io, this [SYCL Introduction](https://tech.io/playgrounds/48226/introduction-to-sycl/introduction-to-sycl-2) tutorial introduces the concepts of SYCL. The website also provides the ability to compile and execute SYCL code from your web browser.

## Connecting to DevCloud via SSH

* Start by creating an [Intel DevCloud account][intel-devcloud] account if you do not already have one and login in.
* Initialize the SSH configuration by clicking on [Automated Configuration](https://devcloud.intel.com/oneapi/documentation/connect-with-ssh-linux-macos/) and follow the instructions to setup the SSH configuration file.
* SSH into DevCloud (```ssh devcloud```)

## Connect to DevCloud via Jupyter Notebooks

* Start by creating an [Intel DevCloud account][intel-devcloud] account if you do not already have one and login in.
* Go to [training](https://console.cloud.intel.com/training) and click on ```Launch JupyterLab´´´
* In the ```Jupiter Notebook``` select *File->New->Terminal*

You are now ready to start with the first [lesson][lesson-1-slides]. Enjoy !

## Building the Exercises for DPC++

* Execute the following command to download SYCLAcademy:
```sh
git clone --recursive https://github.com/codeplaysoftware/syclacademy.git

```
* If you are using **DevCloud via ssh**, run:
 ```sh
 module load cmake
 ```

* To create the code_exercises directory structure with the Makefiles:
```sh
cd syclacademy
mkdir build
cd build
cmake ../ "-GUnix Makefiles" -DSYCL_ACADEMY_USE_DPCPP=ON -DSYCL_ACADEMY_ENABLE_SOLUTIONS=ON -DCMAKE_C_COMPILER=icx -DCMAKE_CXX_COMPILER=icpx
```


[dpcpp-getting-started]: https://software.intel.com/content/www/us/en/develop/articles/installation-guide-for-intel-oneapi-toolkits.html
[intel-devcloud]: https://consumer.intel.com/intelcorpb2c.onmicrosoft.com/B2C_1A_UnifiedLogin_SISU_CML_SAML/generic/login?entityId=www.intel.com&ui_locales=en
[docker-container-oneapi]: https://software.intel.com/content/www/us/en/develop/documentation/get-started-with-intel-oneapi-base-linux/top/using-containers.html
[oneAPI-system-requirements]: https://software.intel.com/content/www/us/en/develop/articles/intel-oneapi-base-toolkit-system-requirements.html

[adaptivecpp-installing]: https://github.com/AdaptiveCpp/AdaptiveCpp/blob/develop/doc/installing.md
[rocm-gpus]: https://github.com/RadeonOpenCompute/ROCm#supported-gpus
[spack]: https://github.com/spack/spack

[video-playlist]: https://youtube.com/playlist?list=PLCssnq0MpRdM-IUAYtNSPYck6u3oz7OZQ

[lesson-1-slides]: ./Lesson_Materials/What_is_SYCL/
[lesson-1-exercise]: ./Code_Exercises/What_is_SYCL/README.md
[lesson-1-source]:   ./Code_Exercises/What_is_SYCL/source.cpp
[lesson-1-solution]: ./Code_Exercises/What_is_SYCL/solution.cpp

[lesson-2-slides]: ./Lesson_Materials/Enqueueing_a_Kernel/
[lesson-2-exercise]: ./Code_Exercises/Enqueueing_a_Kernel/README.md
[lesson-2-source]:   ./Code_Exercises/Enqueueing_a_Kernel/source.cpp
[lesson-2-solution]: ./Code_Exercises/Enqueueing_a_Kernel/solution.cpp

[lesson-3-slides]: ./Lesson_Materials/Managing_Data/
[lesson-3-exercise]: ./Code_Exercises/Managing_Data/README.md
[lesson-3-source]:   ./Code_Exercises/Managing_Data/source.cpp
[lesson-3-solution]: ./Code_Exercises/Managing_Data/solution.cpp

[lesson-4-slides]: ./Lesson_Materials/Handling_Errors/
[lesson-4-exercise]: ./Code_Exercises/Handling_Errors/README.md
[lesson-4-source]:   ./Code_Exercises/Handling_Errors/source.cpp
[lesson-4-solution]: ./Code_Exercises/Handling_Errors/solution.cpp

[lesson-5-slides]: ./Lesson_Materials/Device_Discovery/
[lesson-5-exercise]: ./Code_Exercises/Device_Discovery/README.md
[lesson-5-source]:   ./Code_Exercises/Device_Discovery/source.cpp
[lesson-5-solution]: ./Code_Exercises/Device_Discovery/solution.cpp

[lesson-6-slides]: ./Lesson_Materials/Data_Parallelism/
[lesson-6-exercise]: ./Code_Exercises/Data_Parallelism/README.md
[lesson-6-source]:   ./Code_Exercises/Data_Parallelism/source.cpp
[lesson-6-solution]: ./Code_Exercises/Data_Parallelism/solution.cpp

[lesson-7-slides]: ./Lesson_Materials/Introduction_to_USM/
[lesson-7-exercise]: ./Code_Exercises/Introduction_to_USM/README.md
[lesson-7-source]:   ./Code_Exercises/Introduction_to_USM/source.cpp
[lesson-7-solution]: ./Code_Exercises/Introduction_to_USM/solution.cpp

[lesson-8-slides]: ./Lesson_Materials/Using_USM/
[lesson-8-exercise]: ./Code_Exercises/Using_USM/README.md
[lesson-8-source]:   ./Code_Exercises/Using_USM/source.cpp
[lesson-8-solution]: ./Code_Exercises/Using_USM/solution.cpp

[lesson-9-slides]: ./Lesson_Materials/Asynchronous_Execution/
[lesson-9-exercise]: ./Code_Exercises/Asynchronous_Execution/README.md
[lesson-9-source]:   ./Code_Exercises/Asynchronous_Execution/source.cpp
[lesson-9-solution]: ./Code_Exercises/Asynchronous_Execution/solution.cpp

[lesson-10-slides]: ./Lesson_Materials/Data_and_Dependencies/
[lesson-10-exercise]: ./Code_Exercises/Data_and_Dependencies/README.md
[lesson-10-source]:   ./Code_Exercises/Data_and_Dependencies/source.cpp
[lesson-10-solution]: ./Code_Exercises/Data_and_Dependencies/solution.cpp

[lesson-11-slides]: ./Lesson_Materials/In_Order_Queue/
[lesson-11-exercise]: ./Code_Exercises/In_Order_Queue/README.md
[lesson-11-source]:   ./Code_Exercises/In_Order_Queue/source_vector_add.cpp
[lesson-11-solution]: ./Code_Exercises/In_Order_Queue/solution_vector_add.cpp

[lesson-12-slides]: ./Lesson_Materials/Advanced_Data_Flow/
[lesson-12-exercise]: ./Code_Exercises/Advanced_Data_Flow/README.md
[lesson-12-source]:   ./Code_Exercises/Advanced_Data_Flow/source.cpp
[lesson-12-solution]: ./Code_Exercises/Advanced_Data_Flow/solution.cpp

[lesson-13-slides]: ./Lesson_Materials/Multiple_Devices/
[lesson-13-exercise]: ./Code_Exercises/Multiple_Devices/README.md
[lesson-13-source]:   ./Code_Exercises/Multiple_Devices/source.cpp
[lesson-13-solution]: ./Code_Exercises/Multiple_Devices/solution.cpp

[lesson-14-slides]: ./Lesson_Materials/Image_Convolution/
[lesson-14-exercise]: ./Code_Exercises/Image_Convolution/README.md
[lesson-14-source]:   ./Code_Exercises/Image_Convolution/source.cpp
[lesson-14-solution]: ./Code_Exercises/Image_Convolution/reference.cpp

[lesson-15-slides]: ./Lesson_Materials/Coalesced_Global_Memory/
[lesson-15-exercise]: ./Code_Exercises/Coalesced_Global_Memory/README.md
[lesson-15-source]:   ./Code_Exercises/Coalesced_Global_Memory/source.cpp
[lesson-15-solution]: ./Code_Exercises/Coalesced_Global_Memory/solution.cpp

[lesson-16-slides]: ./Lesson_Materials/Vectors/
[lesson-16-exercise]: ./Code_Exercises/Vectors/README.md
[lesson-16-source]:   ./Code_Exercises/Vectors/source.cpp
[lesson-16-solution]: ./Code_Exercises/Vectors/solution.cpp

[lesson-17-slides]: ./Lesson_Materials/Local_Memory_Tiling/
[lesson-17-exercise]: ./Code_Exercises/Local_Memory_Tiling/README.md
[lesson-17-source]:   ./Code_Exercises/Local_Memory_Tiling/source.cpp
[lesson-17-solution]: ./Code_Exercises/Local_Memory_Tiling/solution.cpp

[lesson-18-slides]: ./Lesson_Materials/Work_Group_Sizes/
[lesson-18-exercise]: ./Code_Exercises/Work_Group_Sizes/README.md
[lesson-18-source]:   ./Code_Exercises/Work_Group_Sizes/source.cpp
[lesson-18-solution]: ./Code_Exercises/Work_Group_Sizes/solution.cpp

[lesson-19-slides]: ./Lesson_Materials/Matrix_Transpose/
[lesson-19-exercise]: ./Code_Exercises/Matrix_Transpose/README.md
[lesson-19-source]:   ./Code_Exercises/Matrix_Transpose/source.cpp
[lesson-19-solution]: ./Code_Exercises/Matrix_Transpose/solution.cpp

[lesson-20-slides]: ./Lesson_Materials/More_SYCL_Features/
[lesson-20-exercise]: ./Code_Exercises/More_SYCL_Features/README.md
[lesson-20-source]:   ./Code_Exercises/More_SYCL_Features/source.cpp
[lesson-20-solution]: ./Code_Exercises/More_SYCL_Features/solution.cpp

[lesson-21-slides]: ./Lesson_Materials/Fast_Track/
[lesson-21-exercise]: ./Code_Exercises/Functors/README.md
[lesson-21-source]:   ./Code_Exercises/Functors/source.cpp
[lesson-21-solution]: ./Code_Exercises/Functors/solution.cpp

[lesson-22-slides]: ./Lesson_Materials/oneMath_gemm/
[lesson-22-exercise]: ./Code_Exercises/oneMath_gemm/README.md
[lesson-22-source]:   ./Code_Exercises/oneMath_gemm/source.cpp
[lesson-22-solution]: ./Code_Exercises/oneMath_gemm/solution.cpp
