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
  const char* inputImageFile = "../Images/dogs.png";
  const char* outputImageFile = "../Images/blurred_dogs.png";

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

    auto globalRange = sycl::range(inputImgWidth, inputImgHeight);
    auto localRange = sycl::range(1, 32);
    auto ndRange = sycl::nd_range(globalRange, localRange);

    auto inBufRange =
        sycl::range(inputImgHeight + (halo * 2), inputImgWidth + (halo * 2)) *
        sycl::range(1, channels);
    auto outBufRange =
        sycl::range(inputImgHeight, inputImgWidth) * sycl::range(1, channels);
    auto filterRange = filterWidth * sycl::range(1, channels);

    {
      auto inBuf = sycl::buffer{inputImage.data(), inBufRange};
      auto outBuf = sycl::buffer<float, 2>{outBufRange};
      auto filterBuf = sycl::buffer{filter.data(), filterRange};
      outBuf.set_final_data(outputImage.data());

      util::benchmark(
          [&]() {
            myQueue.submit([&](sycl::handler& cgh) {
              sycl::accessor inputAcc{inBuf, cgh, sycl::read_only};
              sycl::accessor outputAcc{outBuf, cgh, sycl::write_only};
              sycl::accessor filterAcc{filterBuf, cgh, sycl::read_only};

              cgh.parallel_for<image_convolution>(
                  ndRange, [=](sycl::nd_item<2> item) {
                    auto globalId = item.get_global_id();

                    auto channelsStride = sycl::range(1, channels);
                    auto haloOffset = sycl::id(halo, halo);
                    auto src = (globalId + haloOffset) * channelsStride;
                    auto dest = globalId * channelsStride;

                    float sum[4] = {0.0f, 0.0f, 0.0f, 0.0f};

                    for (int r = 0; r < filterWidth; ++r) {
                      for (int c = 0; c < filterWidth; ++c) {
                        auto srcOffset =
                            sycl::id(src[0] + (r - halo),
                                     src[1] + ((c - halo) * channels));
                        auto filterOffset = sycl::id(r, c * channels);

                        for (int i = 0; i < 4; ++i) {
                          auto channelOffset = sycl::id(0, i);
                          sum[i] += inputAcc[srcOffset + channelOffset] *
                                    filterAcc[filterOffset + channelOffset];
                        }
                      }
                    }

                    for (size_t i = 0; i < 4; ++i) {
                      outputAcc[dest + sycl::id{0, i}] = sum[i];
                    }
                  });
            });

            myQueue.wait_and_throw();
          },
          100, "image convolution (coalesced)");
    }
  } catch (const sycl::exception& e) {
    std::cout << "Exception caught: " << e.what() << std::endl;
  }

  util::write_image(outputImage, outputImageFile);

  SYCLACADEMY_ASSERT(true);
}
