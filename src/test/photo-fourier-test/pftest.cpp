#include "pftest.h"
#include "photo-fourier/photo-fourier.h"
#include "utils/fileops.h"
#include <cmath>
#include <complex>
#include <iostream>

pftest::pftest() {

}

void pftest::SetUp() {

}

void pftest::TearDown() {

}

TEST(pftest, fourierPD1) {
    struct photoData pd;

    pd.size = 100;
    pd.minTime = -(3 * M_PI);
    pd.maxTime = (3 * M_PI);
    pd.times = new double[100];
    pd.photo = new std::complex<double>[100];
    for(int i = 0; i < 100; i++) {
        pd.times[i] = ((6 * M_PI) * ((double)i / 100)) - (3 * M_PI);
        pd.photo[i] = sin(pd.times[i]);
    }

    double* out = fourierPD(pd, 100);

    EXPECT_GE(out[1], 1);
    EXPECT_LT(out[0], 1);
}

TEST(pftest, fourierPD2) {
    struct photoData pd;

    pd.size = 100;
    pd.minTime = -(3 * M_PI);
    pd.maxTime = (3 * M_PI);
    pd.times = new double[100];
    pd.photo = new std::complex<double>[100];
    for(int i = 0; i < 100; i++) {
        pd.times[i] = ((6 * M_PI) * ((double)i / 100)) - (3 * M_PI);
        pd.photo[i] = sin(pd.times[i]) + sin(3 * pd.times[i]);
    }

    double* out = fourierPD(pd, 100);

    EXPECT_GE(out[1], 1);
    EXPECT_GE(out[3], 1);
    EXPECT_LT(out[0], 1);
}
