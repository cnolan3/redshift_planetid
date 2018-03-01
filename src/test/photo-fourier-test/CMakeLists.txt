file(GLOB SRCS *.cpp)

FIND_PACKAGE( OpenMP)
  if(OPENMP_FOUND)
     message("OPENMP FOUND")
     set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
     set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS} -Ofast")
     set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
  endif()

add_executable(photo-fourier-test ${SRCS})

target_link_libraries(photo-fourier-test
	photo-fourier
    utils
	libgtest
	libgmock
)

add_test(photo-fourier-test photo-fourier-test)
