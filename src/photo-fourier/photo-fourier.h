/**
 * @file    photo-fourier.h
 *
 * @brief   fourier transform functions for photometry data.
 *
 * Originally, the intention was to use the fourier transform to
 * decompose the stellar photometry data collected from images into
 * basic sine waves, and to use the frequency and phase angle of those
 * waves as input into a neural network trained to identify possible
 * planets. This method proved to be overly complex and unreliable,
 * and given the time constraints of this project it was abandoned for
 * a simpler approach.
 *
 * @author  Connor Nolan
**/
#ifndef __PHOTO_FOURIER_H__
#define __PHOTO_FOURIER_H__

#include "utils/fileops.h"

/**
 * get fourier transform of photometry data
 *
 * @param    pd photometry data structure
 * @param    bins number of frequency bins
**/
double* fourierPD(photoData &pd, int bins);

#endif
