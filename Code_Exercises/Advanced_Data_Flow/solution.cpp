/*
 SYCL Academy (c)

 SYCL Academy is licensed under a Creative Commons
 Attribution-ShareAlike 4.0 International License.

 You should have received a copy of the license along with this
 work.  If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
*/

#include <sycl/sycl.hpp>

#include "../helpers.hpp"

class kernel_a_1;
class kernel_b_1;
class kernel_a_2;
class kernel_b_2;

int usm_selector(const sycl::device& dev) {
  if (dev.has(sycl::aspect::usm_device_allocations)) {
    if (dev.has(sycl::aspect::gpu)) return 2;
    return 1;
  }
  return -1;
}

// Prefers same devices as usm_selector, but does
// not strictly require them.
int prefer_usm_gpu_selector(const sycl::device& dev) {
  if (dev.has(sycl::aspect::usm_device_allocations)) {
    if (dev.has(sycl::aspect::gpu)) return 2;
    return 1;
  }
  return 0;
}

void test_buffer() {
  constexpr size_t dataSize = 1024;

  float in[dataSize], out[dataSize];
  for (int i = 0; i < dataSize; ++i) {
    in[i] = static_cast<float>(i);
    out[i] = 0.0f;
  }

  try {
    auto gpuQueue = sycl::queue{prefer_usm_gpu_selector};

    auto bufIn = sycl::buffer{in, sycl::range{dataSize}};
    auto bufInt = sycl::buffer<float>{sycl::range{dataSize}};
    auto bufOut = sycl::buffer<float>{sycl::range{dataSize}};

    bufIn.set_final_data(nullptr);
    bufOut.set_final_data(out);

    gpuQueue.submit([&](sycl::handler& cgh) {
      sycl::accessor accIn{bufIn, cgh, sycl::read_only};
      sycl::accessor accOut{bufInt, cgh, sycl::write_only};

      cgh.parallel_for<kernel_a_1>(sycl::range{dataSize}, [=](sycl::id<1> idx) {
        accOut[idx] = accIn[idx] * 8.0f;
      });
    });

    gpuQueue.submit([&](sycl::handler& cgh) {
      sycl::accessor accIn{bufInt, cgh, sycl::read_only};
      sycl::accessor accOut{bufOut, cgh, sycl::write_only};

      cgh.parallel_for<kernel_b_1>(sycl::range{dataSize}, [=](sycl::id<1> idx) {
        accOut[idx] = accIn[idx] / 2.0f;
      });
    });

    gpuQueue.wait_and_throw();
  } catch (const sycl::exception& e) {
    std::cout << "Exception caught: " << e.what() << std::endl;
  }

  SYCLACADEMY_ASSERT_EQUAL(out, [](size_t i) { return i * 4.0f; });
}

void test_usm() {
  constexpr size_t dataSize = 1024;

  float in[dataSize], out[dataSize];
  for (int i = 0; i < dataSize; ++i) {
    in[i] = static_cast<float>(i);
    out[i] = 0.0f;
  }

  try {
    auto usmQueue = sycl::queue{usm_selector};

    auto devicePtrIn = sycl::malloc_device<float>(dataSize, usmQueue);
    auto devicePtrInt = sycl::malloc_device<float>(dataSize, usmQueue);
    auto devicePtrOut = sycl::malloc_device<float>(dataSize, usmQueue);

    auto e1 = usmQueue.memcpy(devicePtrIn, in, sizeof(float) * dataSize);

    auto e2 = usmQueue.parallel_for<kernel_a_2>(
        sycl::range{dataSize}, e1, [=](sycl::id<1> idx) {
          auto globalId = idx[0];
          devicePtrInt[globalId] = devicePtrIn[globalId] * 8.0f;
        });

    auto e3 = usmQueue.parallel_for<kernel_b_2>(
        sycl::range{dataSize}, e2, [=](sycl::id<1> idx) {
          auto globalId = idx[0];
          devicePtrOut[globalId] = devicePtrInt[globalId] / 2.0f;
        });

    usmQueue
        .submit([&](sycl::handler& cgh) {
          cgh.depends_on(e3);
          cgh.memcpy(out, devicePtrOut, sizeof(float) * dataSize);
        })
        .wait();

    sycl::free(devicePtrIn, usmQueue);
    sycl::free(devicePtrInt, usmQueue);
    sycl::free(devicePtrOut, usmQueue);

    usmQueue.throw_asynchronous();
  } catch (const sycl::exception& e) {
    std::cout << "Exception caught: " << e.what() << std::endl;
  }

  SYCLACADEMY_ASSERT_EQUAL(out, [](size_t i) { return i * 4.0f; });
}

int main() {
  test_usm();
  test_buffer();
}
