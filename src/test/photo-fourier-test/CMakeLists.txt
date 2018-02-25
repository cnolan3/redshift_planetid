file(GLOB SRCS *.cpp)

add_executable(test-photo-fourier ${SRCS})

target_link_libraries(test-photo-fourier
	photo-fourier
	libgtest
	libgmock
)

add_test(NAME test-photo-fourier
		 COMMAND test-photo-fourier)
