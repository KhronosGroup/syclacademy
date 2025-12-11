/*
 SYCL Academy (c)

 SYCL Academy is licensed under a Creative Commons
 Attribution-ShareAlike 4.0 International License.

 You should have received a copy of the license along with this
 work.  If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
*/

#include <benchmark.h>
#include <image_conv.h>

#include <algorithm>
#include <iostream>

#include <sycl/sycl.hpp>

#include "../helpers.hpp"

class image_convolution;

inline constexpr util::filter_type filterType = util::filter_type::blur;
inline constexpr int filterWidth = 11;
inline constexpr int halo = filterWidth / 2;

int main() {
  constexpr auto inputImageFile = "../Images/dogs.png";
  constexpr auto outputImageFile = "../Images/blurred_dogs.png";

  auto inputImage = util::read_image(inputImageFile, halo);

  auto outputImage = util::allocate_image(
      inputImage.width(), inputImage.height(), inputImage.channels());

  auto filter = util::generate_filter(util::filter_type::blur, filterWidth);

  try {
    sycl::queue myQueue{sycl::default_selector_v};

    std::cout << "Running on "
              << myQueue.get_device().get_info<sycl::info::device::name>()
              << "\n";

    auto inputImgWidth = inputImage.width();
    auto inputImgHeight = inputImage.height();
    auto channels = inputImage.channels();
    auto filterWidth = filter.width();
    auto halo = filter.half_width();

    auto globalRange = sycl::range(inputImgHeight, inputImgWidth);
    auto localRange = sycl::range(16, 16);
    auto ndRange = sycl::nd_range(globalRange, localRange);

    auto inBufRange =
        sycl::range(inputImgHeight + (halo * 2), inputImgWidth + (halo * 2)) *
        sycl::range(1, channels);
    auto outBufRange =
        sycl::range(inputImgHeight, inputImgWidth) * sycl::range(1, channels);
    auto filterRange = filterWidth * sycl::range(1, channels);
    auto scratchpadRange = localRange + sycl::range(halo * 2, halo * 2);

    {
      auto inBuf = sycl::buffer{inputImage.data(), inBufRange};
      auto outBuf = sycl::buffer<float, 2>{outBufRange};
      auto filterBuf = sycl::buffer{filter.data(), filterRange};
      outBuf.set_final_data(outputImage.data());

      auto inBufVec = inBuf.reinterpret<sycl::float4>(inBufRange /
                                                      sycl::range(1, channels));
      auto outBufVec = outBuf.reinterpret<sycl::float4>(
          outBufRange / sycl::range(1, channels));
      auto filterBufVec = filterBuf.reinterpret<sycl::float4>(
          filterRange / sycl::range(1, channels));

      util::benchmark(
          [&] {
            myQueue.submit([&](sycl::handler& cgh) {
              sycl::accessor inputAcc{inBufVec, cgh, sycl::read_only};
              sycl::accessor outputAcc{outBufVec, cgh, sycl::write_only};
              sycl::accessor filterAcc{filterBufVec, cgh, sycl::read_only};

              auto scratchpad =
                  sycl::local_accessor<sycl::float4, 2>(scratchpadRange, cgh);

              cgh.parallel_for<image_convolution>(
                  ndRange, [=](sycl::nd_item<2> item) {
                    auto globalId = item.get_global_id();
                    auto groupId = item.get_group().get_group_id();
                    auto localId = item.get_local_id();
                    auto globalGroupOffset = groupId * localRange;

                    for (auto i = localId[0]; i < scratchpadRange[0];
                         i += localRange[0]) {
                      for (auto j = localId[1]; j < scratchpadRange[1];
                           j += localRange[1]) {
                        scratchpad[i][j] =
                            inputAcc[globalGroupOffset + sycl::range(i, j)];
                      }
                    }

                    sycl::group_barrier(item.get_group());

                    auto sum = sycl::float4{0.0f, 0.0f, 0.0f, 0.0f};

                    for (int r = 0; r < filterWidth; ++r) {
                      for (int c = 0; c < filterWidth; ++c) {
                        auto idx = sycl::range(r, c);
                        sum += scratchpad[localId + idx] * filterAcc[idx];
                      }
                    }

                    outputAcc[globalId] = sum;
                  });
            });

            myQueue.wait_and_throw();
          },
          100, "image convolution (tiled)");
    }
  } catch (const sycl::exception& e) {
    std::cout << "Exception caught: " << e.what() << std::endl;
  }

  util::write_image(outputImage, outputImageFile);

  SYCLACADEMY_ASSERT(true);
}
