#include "photo-fourier/photo-fourier.h"
#include "utils/fileops.h"

#include <iostream>
#include <cmath>
#include <vector>

using namespace std;

int main(int argc, char* argv[]) {
    vector<struct photoData> pdList;
    vector<double*> out;
    int bins = 10;

    pdList = readNasaArchive(argv[1]);

    for(int i = 0; i < pdList.size(); i++) {
        normalize(pdList[i], -(3 * M_PI), (3 * M_PI));

        double* tmp;
        tmp = fourierPD(pdList[i], bins);
        out.push_back(tmp);
    }

    for(int i = 0; i < bins; i++) {
        cout << i << ": " << out[0][i] << " " << out[1][i] << " " << out[1][i] - out[0][i] << endl;;
    }

    return 0;
}
