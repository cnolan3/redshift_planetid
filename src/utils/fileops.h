/**
 * @file    fileops.h
 *
 * @brief   utility file operations dealing with photometry data
 *
 * @author  Connor Nolan
**/
#ifndef __FILEOPS_H__
#define __FILEOPS_H__

#include <iostream>
#include <complex>
#include <vector>

/**
 * photometry data structure
**/
struct photoData {
    /// data point times
    double* times;
    /// data photometric values
    std::complex<double>* photo;
    /// lowest time value
    double minTime;
    /// greatest time value
    double maxTime;
    /// number of data points
    int size;
};

/**
 * print photoData structure
 *
 * @param    pd photoData structure
**/
void printPD(struct photoData &pd, std::ostream& os);

/**
 * get photometry data from nasa archive file
 *
 * @param    filename
 *
 * @return   phtotoData struct
**/
std::vector<struct photoData> readNasaArchive(const char* filename);

/**
 * normalize data times between min and max
 *
 * @param    pd photometry data
 * @param    min minimum time value
 * @param    max maximum time value
**/
void normalize(struct photoData &pd, double min, double max);

#endif
