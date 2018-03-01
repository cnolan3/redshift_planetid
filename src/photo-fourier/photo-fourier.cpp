/**
 * @file    photo-fourier.cpp
 *
 * @author  Connor Nolan
**/
#include "photo-fourier.h"
#include "../include/finufft/finufft.h"

#include <complex>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>

using namespace std;

double* fourierPD(photoData &pd, int bins) {
    double acc = 1e-9;      // desired accuracy
    nufft_opts opts; finufft_default_opts(opts);
    opts.modeord = 1;
    complex<double> I = complex<double>(0.0,1.0);  // the imaginary unit

    // allocate output array for the Fourier modes:
    complex<double>* F = (complex<double>*)malloc(sizeof(complex<double>)*bins);
    double* out = new double[bins];

    // call the NUFFT (with iflag=+1):
    int ier = finufft1d1(pd.size, pd.times, pd.photo, +1, acc, bins, F, opts);

    for (int i = 0; i < bins; ++i) {
        out[i] = (2 * abs(F[i])) / pd.size;
    }

    return out;
}
