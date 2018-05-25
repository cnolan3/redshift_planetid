/**
 * @file    gen_data.cpp
 *
 * @brief   generate test training data for planetId neural net
 *
 * @author  Connor Nolan
**/

#include <iostream>
#include <fstream>
#include <cmath>
#include <cstdlib>
#include <ctime>

#define WAVES 3

using namespace std;

float rand_float(float min, float max);

/**
 * main
**/
int main(int argc, char* argv[]) {

    if(argc < 4) {
        cerr << "Usage: num_data_points data_file labels_file" << endl;
        exit(1);
    }

    srand(time(NULL));

    int n = atoi(argv[1]); // number of data points
    float freq[WAVES], mag[WAVES], phase[WAVES], val[WAVES], totVal;
    float time = 0; // time in seconds
    ofstream train_out(argv[3]);
    ofstream data_out(argv[2]);

    // set noise wave frequencies, magnitudes and phase angles
    for(int i = 0; i < WAVES - 1; i++) {
        freq[i] = rand_float(1.0, 10.0);
        mag[i] = rand_float(1.0, 5.0);
        phase[i] = rand_float(0.0, 2 * M_PI);
    }

    // set transit frequency, magnitude and phase angle
    freq[WAVES - 1] = rand_float(2.0, 7.0);
    mag[WAVES - 1] = rand_float(1.0, 2.0);
    phase[WAVES - 1] = rand_float(0.0, 2 * M_PI);

    // generate data and write to files
    for(int i = 0; i < n; i++) {
        int transit;
        float tmp_val;

        // generate noise wave values
        totVal = 0;
        for(int j = 0; j < WAVES - 1; j++) {
            val[j] = mag[j] * sin((time * freq[j]) + phase[j]);
            totVal += val[j];
        }
        
        // generate tranit wave value
        tmp_val = sin((time * freq[WAVES - 1]) + phase[WAVES - 1]);
        val[WAVES - 1] = mag[WAVES - 1] * tmp_val;

        // if transit wave is below threshhold, add to output value
        // and set transit flag
        if(tmp_val <= -0.8) {
            totVal += val[WAVES - 1];
            transit = 1;
        }
        else
            transit = 0;

        // output to files
        data_out << time << "," << totVal << endl;
        train_out << transit << endl;

        // increment time
        time += rand_float(0.1, 1);
    }

    return 0;
}

/**
 * generate random float
 *
 * @param    min minimum value
 * @param    max maximum value
 *
 * @return   random float between min and max
**/
float rand_float(float min, float max) {
    float random = ((float) rand() / (float)RAND_MAX);

    float range = max - min;
    return (random * range) + min;
}
