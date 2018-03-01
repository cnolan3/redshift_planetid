file(GLOB SRCS *.cpp)
add_library(photo-fourier ${SRCS})
target_link_libraries(photo-fourier utils ${CMAKE_SOURCE_DIR}/lib/libfinufft.a fftw3 fftw3_threads m)
