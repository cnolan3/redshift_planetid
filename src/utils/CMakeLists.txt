file(GLOB SRCS *.cpp)
add_library(utils ${SRCS})
target_link_libraries(utils m)
