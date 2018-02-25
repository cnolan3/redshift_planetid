#include "pftest.h"
#include "photo-fourier/plus.h"

pftest::pftest() {

}

void pftest::SetUp() {

}

void pftest::TearDown() {

}

TEST(pftest, oneplusone) {
    EXPECT_EQ(add_two(1, 1), 2);
}
