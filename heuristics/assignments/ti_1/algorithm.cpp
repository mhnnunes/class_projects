
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
#include "algorithm.h"
#define INF 0x3f3f3f3f
#define x first
#define y second

typedef long double lld;
typedef std::pair<double, int> pdi; 

double euc_2d(pdd city1, pdd city2){
	// Euclidean distance
    return round(sqrt(pow((city1.x - city2.x), 2) +
                      pow((city1.y - city2.y), 2)));
}

double att_dist(pdd city1, pdd city2){
	// ATT distance, as specified in the TSP input pdf
    return ceil(sqrt((pow((city1.x - city2.x), 2) +
                pow((city1.y - city2.y), 2)) / 10.0));
}


double heuristics_ConstructiveTSP(std::vector<pdd> &cities, bool att){
	// Greedy heuristic for constructing a TSP path in a complete graph

    int cur = 0;
    double dist;
    int ncities = (int) cities.size();
    int nvisited = 0;
    lld totalcost = 0.0;
    pdi nearest_neighbor;
    std::vector<bool> visited(ncities, false);

    visited[cur] = 1; // Mark current city as visited
    nvisited++;

    while(nvisited < ncities){ // Iterate through all cities: O(n)
        nearest_neighbor.first = INF;
        for (int i = 0; i < ncities; ++i){ // Iterate through all cities: O(n)
            if(!visited[i] && i != cur){ // Only calculate distance to unvisited cities
                dist = (att)? att_dist(cities[cur], cities[i]) : euc_2d(cities[cur], cities[i]);
                if(dist < nearest_neighbor.first){
                    nearest_neighbor.first = dist;
                    nearest_neighbor.second = i;
                }
            }
        }
        // Take out closest city:
        totalcost += nearest_neighbor.first;
        cur = nearest_neighbor.second;
        visited[cur] = 1; // Mark current city as visited
        nvisited++;
    }
    // Add edge from last city to first
    int i = 0;
    dist = (att)? att_dist(cities[cur], cities[i]) : euc_2d(cities[cur], cities[i]);
    totalcost += dist;
    return totalcost;
}