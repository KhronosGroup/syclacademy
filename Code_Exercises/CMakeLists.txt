#[[
  SYCL Academy (c)

  SYCL Academy is licensed under a Creative Commons Attribution-ShareAlike 4.0
  International License.

  You should have received a copy of the license along with this work.  If not,
  see <http://creativecommons.org/licenses/by-sa/4.0/>.
]]

# CMake function to build ab AdaptiveCpp configuration and create executable binaries
# from AdaptiveCpp libraries.
function( add_sycl_executable_adaptivecpp prefix source )
  set(TARGET_NAME "${prefix}_${source}")
  add_executable("${TARGET_NAME}" "${source}.cpp")
  add_sycl_to_target(TARGET ${TARGET_NAME} SOURCES "${source}.cpp")

  target_include_directories("${prefix}_${source}" PRIVATE
    ${PROJECT_SOURCE_DIR}/Utilities/include
    ${PROJECT_SOURCE_DIR}/External/stb)
  target_link_libraries("${prefix}_${source}" PRIVATE Threads::Threads)
  set_target_properties("${prefix}_${source}" PROPERTIES CXX_STANDARD 17 CXX_STANDARD_REQUIRED ON)
endfunction()

# CMake function to build a DPC++ configuration and create executable binaries
# from oneAPI libraries.
function( add_sycl_executable_dpcpp prefix source )
  set(TARGET_NAME "${prefix}_${source}")

  add_executable(${TARGET_NAME} "${source}.cpp")
  # This function is from IntelSYCL cmake module
  add_sycl_to_target(TARGET ${TARGET_NAME} SOURCES "${source}.cpp")
  target_include_directories(${TARGET_NAME} PUBLIC "${CMAKE_SOURCE_DIR}/External/stb")
  target_include_directories(${TARGET_NAME} PUBLIC "${CMAKE_SOURCE_DIR}/Utilities/include")
endfunction()

function( add_sycl_executable prefix source )
  if (SYCL_ACADEMY_USE_DPCPP)
    add_sycl_executable_dpcpp(${prefix} ${source})
  endif()
  if (SYCL_ACADEMY_USE_ADAPTIVECPP)
    add_sycl_executable_adaptivecpp(${prefix} ${source})
  endif()
endfunction()



add_subdirectory(What_is_SYCL)
add_subdirectory(Enqueueing_a_Kernel)
add_subdirectory(Managing_Data)
add_subdirectory(Handling_Errors)
add_subdirectory(Device_Discovery)
add_subdirectory(Data_Parallelism)
add_subdirectory(Introduction_to_USM)
add_subdirectory(Using_USM)
add_subdirectory(Asynchronous_Execution)
add_subdirectory(Data_and_Dependencies)
add_subdirectory(In_Order_Queue)
add_subdirectory(Advanced_Data_Flow)
add_subdirectory(Multiple_Devices)
add_subdirectory(Image_Convolution)
add_subdirectory(Coalesced_Global_Memory)
add_subdirectory(Vectors)
add_subdirectory(Local_Memory_Tiling)
add_subdirectory(Work_Group_Sizes)
add_subdirectory(Matrix_Transpose)
add_subdirectory(Functors)
add_subdirectory(oneMath_gemm)
add_subdirectory(More_SYCL_Features)
