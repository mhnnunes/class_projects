

#include <iostream>
#include <cstdlib>

#include "io.h"
#include "graph.h"
#include "algorithm.h"

using namespace std;


int main(int argc, char* argv[]){
	std::vector< pdd >  cities;
    bool att = false;
	readInput(cities, att);
    // cout << "ATT: " << att<< endl;
    cout << heuristics_ConstructiveTSP(cities, att) << endl;
}