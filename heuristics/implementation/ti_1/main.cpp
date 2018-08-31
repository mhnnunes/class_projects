

#include <iostream>
#include <cstdlib>

#include "io.h"
#include "algorithm.h"

using namespace std;


int main(int argc, char* argv[]){
    bool att = false;
    std::vector< pdd >  cities;
    
    readInput(cities, att);

    cout << heuristics_ConstructiveTSP(cities, att) << endl;
}