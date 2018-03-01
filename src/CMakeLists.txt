cmake_minimum_required(VERSION 2.8)

enable_testing()

project("redshift_planetid")

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

add_subdirectory(photo-fourier)
add_subdirectory(utils)
add_subdirectory(test)

set(CMAKE_BUILD_TYPE Debug)

FIND_PACKAGE( OpenMP)
  if(OPENMP_FOUND)
     message("OPENMP FOUND")
     set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
     set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS} -Ofast")
     set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
  endif()

add_executable(planetid main.cpp)
target_link_libraries(planetid photo-fourier utils)
