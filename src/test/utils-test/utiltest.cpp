#include "utiltest.h"
#include "utils/fileops.h"

utiltest::utiltest() {

}

void utiltest::SetUp() {

}

void utiltest::TearDown() {

}

TEST(utiltest, normalize1) {
    struct photoData pd;

    pd.size = 4;
    pd.times = new double[4];
    pd.minTime = 0;
    pd.maxTime = 3;

    for(int i = 0; i < 4; i++) {
        pd.times[i] = i;
    }

    normalize(pd, -1, 1);

    EXPECT_EQ(pd.times[0], -1);
    EXPECT_EQ(pd.times[3], 1);
}

TEST(utiltest, normalize2) {
    struct photoData pd;

    pd.size = 4;
    pd.times = new double[4];
    pd.minTime = 0;
    pd.maxTime = 3;

    for(int i = 0; i < 4; i++) {
        pd.times[i] = i;
    }

    normalize(pd, 0, 5);

    EXPECT_EQ(pd.times[0], 0);
    EXPECT_EQ(pd.times[3], 5);
}
