file(GLOB SRCS *.cpp)

add_executable(utils-test ${SRCS})

target_link_libraries(utils-test
    utils
	libgtest
	libgmock
)

add_test(utils-test utils-test)
