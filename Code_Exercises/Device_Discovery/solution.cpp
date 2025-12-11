/*
 SYCL Academy (c)

 SYCL Academy is licensed under a Creative Commons
 Attribution-ShareAlike 4.0 International License.

 You should have received a copy of the license along with this
 work.  If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
*/

#include <sycl/sycl.hpp>

#include "../helpers.hpp"

class scalar_add;

// Function device selector
int intel_gpu_selector1(const sycl::device& dev) {
  if (dev.has(sycl::aspect::gpu)) {
    auto vendorName = dev.get_info<sycl::info::device::vendor>();
    if (vendorName.find("Intel") != std::string::npos) {
      return 1;
    }
  }
  // Fall back to other devices if desired device not available
  // (return -1 instead to fail instead)
  return 0;
}

// Lambda device_selector
auto intel_gpu_selector2 = [](const sycl::device& dev) {
  if (dev.has(sycl::aspect::gpu)) {
    auto vendorName = dev.get_info<sycl::info::device::vendor>();
    if (vendorName.find("Intel") != std::string::npos) {
      return 1;
    }
  }
  // Fall back to other devices if desired device not available
  // (return -1 instead to fail instead)
  return 0;
};

int main() {
  int a = 18, b = 24, r = 0;

  try {
    auto defaultQueue1 = sycl::queue{intel_gpu_selector1};
    auto defaultQueue2 = sycl::queue{intel_gpu_selector2};

    std::cout << "Chosen device: "
              << defaultQueue1.get_device().get_info<sycl::info::device::name>()
              << std::endl;

    {
      auto bufA = sycl::buffer{&a, sycl::range{1}};
      auto bufB = sycl::buffer{&b, sycl::range{1}};
      auto bufR = sycl::buffer{&r, sycl::range{1}};

      defaultQueue1
          .submit([&](sycl::handler& cgh) {
            auto accA = sycl::accessor{bufA, cgh, sycl::read_only};
            auto accB = sycl::accessor{bufB, cgh, sycl::read_only};
            auto accR = sycl::accessor{bufR, cgh, sycl::write_only};

            cgh.single_task<scalar_add>([=]() { accR[0] = accA[0] + accB[0]; });
          })
          .wait();
    }

    defaultQueue1.throw_asynchronous();
  } catch (const sycl::exception& e) {
    std::cout << "Exception caught: " << e.what() << std::endl;
  }

  SYCLACADEMY_ASSERT_EQUAL(r, 42);
}
