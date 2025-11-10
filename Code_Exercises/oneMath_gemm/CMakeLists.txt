#[[
  SYCL Academy (c)

  SYCL Academy is licensed under a Creative Commons Attribution-ShareAlike 4.0
  International License.

  You should have received a copy of the license along with this work.  If not,
  see <http://creativecommons.org/licenses/by-sa/4.0/>.
]]

find_package(oneMath QUIET)
if (NOT oneMath_FOUND)
  message(STATUS "oneMath not found: disabling oneMath_gemm target")
  return()
endif()

add_sycl_executable(oneMath_gemm source_onemath_usm_gemm)
add_sycl_executable(oneMath_gemm source_onemath_buffer_gemm)

target_link_libraries(oneMath_gemm_source_onemath_usm_gemm PUBLIC ONEMATH::onemath)
target_link_libraries(oneMath_gemm_source_onemath_buffer_gemm PUBLIC ONEMATH::onemath)
if(SYCL_ACADEMY_ENABLE_SOLUTIONS)
  add_sycl_executable(oneMath_gemm solution_onemath_usm_gemm)
  add_sycl_executable(oneMath_gemm solution_onemath_buffer_gemm)

  target_link_libraries(oneMath_gemm_solution_onemath_usm_gemm PUBLIC ONEMATH::onemath)
  target_link_libraries(oneMath_gemm_solution_onemath_buffer_gemm PUBLIC ONEMATH::onemath)
endif()
