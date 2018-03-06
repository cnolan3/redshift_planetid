/**
 * @file    fileops.cpp
 *
 * @author  Connor Nolan
**/
#include "fileops.h"

#include <utility>
#include <fstream>
#include <limits>
#include <cmath>

using std::vector;
using std::pair;
using std::cerr;
using std::cout;
using std::endl;
using std::ifstream;
using std::ostream;

void printPD(struct photoData &pd, ostream &os) {
    for(int i = 0; i < pd.size; i++) {
        os << i << ": " << pd.times[i] << " " << pd.photo[i] << endl;
    }
}

vector<struct photoData> readNasaArchive(const char* filename) {
    vector<struct photoData> pdList;
    vector<vector<pair<double, double> > > data;
    
    ifstream in(filename);

    if(!in.is_open()) {
        cerr << "file " << filename << " could not be opened." << endl;
        return pdList;
    }

	// go to line 4 of file
    // adapted from stack overflow https://stackoverflow.com/questions/5207550/in-c-is-there-a-way-to-go-to-a-specific-line-in-a-text-file
	in.seekg(std::ios::beg);
    for(int i = 0; i < 3; ++i){
        in.ignore(std::numeric_limits<std::streamsize>::max(),'\n');
    }

	while(!in.eof()) {
        unsigned int setNum;
        double time;
        double val;

		in >> setNum;
		in >> time;
		in >> val;

        while(setNum >= data.size()) {
            vector<pair<double, double> > v;
            data.push_back(v);
        }

		pair<double, double> p;
		p.first = time;
		p.second = val;

		data[setNum].push_back(p);	

        in.ignore();
	}

    for(unsigned int j = 0; j < data.size(); j++) {
        struct photoData* pd = new struct photoData;
        pd->size = data[j].size() - 1;
        pd->times = new double[pd->size];
        pd->photo = new std::complex<double>[pd->size];
        pd->minTime = data[j][0].first;
        pd->maxTime = data[j][0].first;

        for(int i = 0; i < pd->size; i++) {
            pd->times[i] = data[j][i].first;
            pd->photo[i] = data[j][i].second;

            if(pd->times[i] < pd->minTime)
                pd->minTime = pd->times[i];

            if(pd->times[i] > pd->maxTime)
                pd->maxTime = pd->times[i];
        }

        pdList.push_back(*pd);
    }

    return pdList;
}

void normalize(struct photoData &pd, double min, double max) {
    for(int i = 0; i < pd.size; i++) {
        pd.times[i] = ((max - min) * ((pd.times[i] - pd.minTime) / (pd.maxTime - pd.minTime))) + min;
    }
}
