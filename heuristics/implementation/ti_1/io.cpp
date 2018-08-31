

#include <string>
#include <vector>
#include <sstream>
#include <utility>
#include <iostream>

#include "io.h"

#define OPENING_LINES 6

void readInput(std::vector<pdd>  &cities, bool &att){
    // Read 6 opening lines
    int ncities = 0;
    std::string raw_input;
    std::string line_type;
    std::string ewt;
    for (int i = 0; i < OPENING_LINES; ++i)
    {
        std::getline(std::cin, raw_input);
        std::stringstream ss(raw_input);
        ss >> line_type;
        if(line_type == "DIMENSION:"){
            ss >> ncities;
        }
        if(line_type == "EDGE_WEIGHT_TYPE:"){
            ss >> ewt;
            if(ewt == "ATT") att = true;
        }
    }
    double id, x, y;
    for (int i = 0; i < ncities; ++i)
    {
        // Read city coords
        std::cin >> id >> x >> y;
        cities.push_back(std::make_pair(x, y));
    }
}