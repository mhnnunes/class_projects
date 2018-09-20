
// Copyright 2018 Matheus Nunes <mhnnunes@dcc.ufmg.br>
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

#include <iostream>

#include "../lib/io.h"
#include "algorithm.h"

using namespace std;

int main(int argc, char* argv[]){
    bool att = false;
    
    vector< pdd >  cities;

    readInput(cities, att);

    int ncities = (int) cities.size();
    vector< int > tour(ncities+1);

    // cout << heuristics_ConstructiveTSP(cities, tour, ncities, att) << endl;
    lld cost = heuristics_VND_TSP(cities, tour, ncities, att);
    cout << cost << endl;
    print_tour(tour, cities);
    cost = search_2Opt_TSP(cities, tour, cost, ncities, att);
    cout<< "Cost after search 2opt: " << endl;
    cout << cost << endl;
    print_tour(tour, cities);
    // std::vector<int> new_tour(tour.begin(), tour.end());
    // swap_2Opt(new_tour, 0, 5, att);
    // swap_2Opt(tour, 0, 5, att);
    // print_tour(new_tour, cities);
    // cout << calculate_tour_cost(new_tour, cities, att) << endl;
    // print_tour(tour, cities);
}
