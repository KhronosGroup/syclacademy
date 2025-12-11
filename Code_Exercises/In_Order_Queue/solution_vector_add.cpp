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
class kernel_c_1;
class kernel_d_1;
class kernel_a_2;
class kernel_b_2;
class kernel_c_2;
class kernel_d_2;

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

  float inA[dataSize], inB[dataSize], inC[dataSize], out[dataSize];
  for (int i = 0; i < dataSize; ++i) {
    inA[i] = static_cast<float>(i);
    inB[i] = static_cast<float>(i);
    inC[i] = static_cast<float>(i);
    out[i] = 0.0f;
  }

  try {
    auto inOrderQueue = sycl::queue{prefer_usm_gpu_selector,
                                    {sycl::property::queue::in_order{}}};

    auto bufInA = sycl::buffer{inA, sycl::range{dataSize}};
    auto bufInB = sycl::buffer{inB, sycl::range{dataSize}};
    auto bufInC = sycl::buffer{inC, sycl::range{dataSize}};
    auto bufOut = sycl::buffer{out, sycl::range{dataSize}};

    inOrderQueue.submit([&](sycl::handler& cgh) {
      sycl::accessor accInA{bufInA, cgh, sycl::read_write};

      cgh.parallel_for<kernel_a_1>(
          sycl::range{dataSize}, [=](sycl::id<1> idx) { accInA[idx] *= 2.0f; });
    });

    inOrderQueue.submit([&](sycl::handler& cgh) {
      sycl::accessor accIn{bufInA, cgh, sycl::read_only};
      sycl::accessor accOut{bufInB, cgh, sycl::read_write};

      cgh.parallel_for<kernel_b_1>(sycl::range{dataSize}, [=](sycl::id<1> idx) {
        accOut[idx] += accIn[idx];
      });
    });

    inOrderQueue.submit([&](sycl::handler& cgh) {
      sycl::accessor accInA{bufInA, cgh, sycl::read_only};
      sycl::accessor accInC{bufInC, cgh, sycl::read_write};

      cgh.parallel_for<kernel_c_1>(sycl::range{dataSize}, [=](sycl::id<1> idx) {
        accInC[idx] -= accInA[idx];
      });
    });

    inOrderQueue.submit([&](sycl::handler& cgh) {
      sycl::accessor accInB{bufInB, cgh, sycl::read_only};
      sycl::accessor accInC{bufInC, cgh, sycl::read_only};
      sycl::accessor accOut{bufOut, cgh, sycl::write_only};

      cgh.parallel_for<kernel_d_1>(sycl::range{dataSize}, [=](sycl::id<1> idx) {
        accOut[idx] = accInB[idx] + accInC[idx];
      });
    });

    inOrderQueue.wait_and_throw();
  } catch (const sycl::exception& e) {
    std::cout << "Exception caught: " << e.what() << std::endl;
  }

  SYCLACADEMY_ASSERT_EQUAL(out, [](size_t i) { return i * 2.0f; });
}

void test_usm() {
  constexpr size_t dataSize = 1024;

  float inA[dataSize], inB[dataSize], inC[dataSize], out[dataSize];
  for (int i = 0; i < dataSize; ++i) {
    inA[i] = static_cast<float>(i);
    inB[i] = static_cast<float>(i);
    inC[i] = static_cast<float>(i);
    out[i] = 0.0f;
  }

  try {
    auto inOrderQueue =
        sycl::queue{usm_selector, {sycl::property::queue::in_order{}}};

    auto devicePtrInA = sycl::malloc_device<float>(dataSize, inOrderQueue);
    auto devicePtrInB = sycl::malloc_device<float>(dataSize, inOrderQueue);
    auto devicePtrInC = sycl::malloc_device<float>(dataSize, inOrderQueue);
    auto devicePtrOut = sycl::malloc_device<float>(dataSize, inOrderQueue);

    inOrderQueue.memcpy(devicePtrInA, inA, sizeof(float) * dataSize);
    inOrderQueue.memcpy(devicePtrInB, inB, sizeof(float) * dataSize);
    inOrderQueue.memcpy(devicePtrInC, inC, sizeof(float) * dataSize);
    inOrderQueue.memcpy(devicePtrOut, out, sizeof(float) * dataSize);

    inOrderQueue.parallel_for<kernel_a_2>(
        sycl::range{dataSize}, [=](sycl::id<1> idx) {
          auto globalId = idx[0];
          devicePtrInA[globalId] = devicePtrInA[globalId] * 2.0f;
        });

    inOrderQueue.parallel_for<kernel_b_2>(
        sycl::range{dataSize}, [=](sycl::id<1> idx) {
          auto globalId = idx[0];
          devicePtrInB[globalId] += devicePtrInA[globalId];
        });

    inOrderQueue.parallel_for<kernel_c_2>(
        sycl::range{dataSize}, [=](sycl::id<1> idx) {
          auto globalId = idx[0];
          devicePtrInC[globalId] -= devicePtrInA[globalId];
        });

    inOrderQueue.parallel_for<kernel_d_2>(
        sycl::range{dataSize}, [=](sycl::id<1> idx) {
          auto globalId = idx[0];
          devicePtrOut[globalId] =
              devicePtrInB[globalId] + devicePtrInC[globalId];
        });

    inOrderQueue.memcpy(inA, devicePtrInA, sizeof(float) * dataSize);
    inOrderQueue.memcpy(inB, devicePtrInB, sizeof(float) * dataSize);
    inOrderQueue.memcpy(inC, devicePtrInC, sizeof(float) * dataSize);
    inOrderQueue.memcpy(out, devicePtrOut, sizeof(float) * dataSize);

    inOrderQueue.wait_and_throw();

    sycl::free(devicePtrInA, inOrderQueue);
    sycl::free(devicePtrInB, inOrderQueue);
    sycl::free(devicePtrInC, inOrderQueue);
    sycl::free(devicePtrOut, inOrderQueue);

  } catch (const sycl::exception& e) {
    std::cout << "Exception caught: " << e.what() << std::endl;
  }

  SYCLACADEMY_ASSERT_EQUAL(out, [](size_t i) { return i * 2.0f; });
}

int main() {
  test_buffer();
  test_usm();
}
