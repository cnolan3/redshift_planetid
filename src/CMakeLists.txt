cmake_minimum_required(VERSION 2.8)

project("redshift_planetid")

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

add_subdirectory(photo-fourier)
add_subdirectory(test)

add_executable(planetid main.cpp)
target_link_libraries(planetid photo-fourier)
