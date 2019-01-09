
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

    lld cost = heuristics_VND_TSP(cities, tour, ncities, att);
    cout << cost << endl;
    // print_tour(tour, cities);
}
