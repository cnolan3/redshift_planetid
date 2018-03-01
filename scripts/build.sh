#!/bin/bash

mkdir -p ../src/build/
cd ../src/build
cmake -G "Unix Makefiles" ..
make
