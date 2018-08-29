#include<iostream>
#include <string>
#include<sstream>
#include<vector>
#include<utility> 
#include<cstdio>
#include "io.h"
#include "graph.h"

using namespace std;

#define OPENING_LINES 6

void readInput(std::vector<pdd>  &cities){
    // Read 6 opening lines
    int ncities = 0;
    std::string raw_input;
    std::string line_type;
    for (int i = 0; i < OPENING_LINES; ++i)
    {
        std::getline(std::cin, raw_input);
        std::stringstream ss(raw_input);
        ss >> line_type;
        // cout << "Line type: " << line_type << endl;
        // cout << raw_input << endl;
        if(line_type == "DIMENSION:"){
            ss >> ncities;
            std::cout << "ncities: " << ncities << std::endl;
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