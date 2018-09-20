
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

double calculateDist(pdd city1, pdd city2, bool att){
    return (att)? att_dist(city1, city2) :
                  euc_2d(city1, city2);
}

lld calculate_tour_cost(std::vector<int> &tour, std::vector<pdd> &cities,
                        bool att){
    lld totalcost = 0.0;
    for (int i = 0; i < ((int) tour.size()) - 1; i++){
        totalcost += calculateDist(cities[tour[i]], cities[tour[i+1]], att);
    }
    return totalcost;
}

lld heuristics_ConstructiveTSP(std::vector<pdd> &cities,
                               std::vector<int> &tour,
                               int ncities, bool att){
	// Greedy heuristic for constructing a TSP path in a complete graph
    int cur = 0;
    double dist;
    int nvisited = 0;
    lld totalcost = 0.0;
    pdi nearest_neighbor;
    std::vector<bool> visited(ncities, false);

    visited[cur] = 1; // Mark current city as visited
    tour[0] = cur; // Add the first city to tour
    nvisited++;

    while(nvisited < ncities){ // Iterate through all cities: O(n)
        nearest_neighbor.first = INF;
        for (int i = 0; i < ncities; ++i){ // Iterate through all cities: O(n)
            // Only calculate distance to unvisited cities
            if(!visited[i] && i != cur){
                // Calculate distance between cities: O(1)
                dist = calculateDist(cities[cur], cities[i], att);
                if(dist < nearest_neighbor.first){
                    nearest_neighbor.first = dist;
                    nearest_neighbor.second = i;
                }
            }
        }
        // Add closest city to tour
        tour[nvisited] = nearest_neighbor.second;
        // Add its cost to the total
        totalcost += nearest_neighbor.first;
        cur = nearest_neighbor.second;
        visited[cur] = 1; // Mark current city as visited
        nvisited++;
    }
    // Add edge from last city to first
    int i = 0;
    dist = calculateDist(cities[cur], cities[i], att);
    tour[nvisited] = i;
    totalcost += dist;
    return totalcost;
}

void print_tour(std::vector<int> tour, std::vector<pdd> &cities){
    std::cout << "PRINTING TOUR" << std::endl;
    std::cout << "city -> nextcity" << std::endl;
    for(auto &it: tour){
        std::cout << it << "-> " ;
    }
    std::cout << std::endl;
}

lld heuristics_VND_TSP(std::vector<pdd> &cities,
                       std::vector<int> &tour,
                       int ncities, bool att){
    // lld curcost = 0.0;
    lld bestcost = 0.0;
    // int nneighborhoods = 2; // Number of neighborhoods for local search

    // Generate initial solution using the constructive heuristic
    bestcost = heuristics_ConstructiveTSP(cities, tour, ncities, att);
    // Tour will be stored in the tour variable
    // int l = 0;
    // while(l < nneighborhoods){
    //     // Search for improvement on neighborhood l
    //     //     - neighborhood 0: 2Opt
    //     //     - neighborhood 1: 3Opt
    //     // If cost of new solution is better than cost of current solution
    //     // Store new solution
    //     // Go back to first neighborhood
    //     // Otherwise next neighborhood

    // }
    return bestcost;
}

void swap_2Opt(std::vector<int> &tour,
               int i, int k, bool att){
    int swapaux = 0;
    int ncities = ((int) tour.size()) - 1;
    // Special case when i = 0: swapping tour beginning
    if(i == 0){
        swapaux = tour[i];
        tour[i] = tour[k];
        tour[ncities] = tour[k];
        tour[k] = swapaux;
        // Replace first
        i++;
        k--;
    }
    for (int index = i, revindex = k; index < revindex; index++, revindex--){
        // Swap cities
        swapaux = tour[index];
        tour[index] = tour[revindex];
        tour[revindex] = swapaux;
    }
}

lld search_2Opt_TSP(std::vector<pdd> &cities,
                    std::vector<int> &tour,
                    lld initialcost,
                    int ncities, bool att){
    lld bestcost = initialcost;
    lld curcost = 0.0;
    for (int i = 0; i < ncities - 1; i++){
        for (int k = i + 1; k < ncities; k++){
            // Swap nodes i and k in tour
            std::vector<int> new_tour(tour.begin(), tour.end());
            // Calculate new tour distance
            swap_2Opt(new_tour, i, k, att);
            curcost = calculate_tour_cost(new_tour, cities, att);
            // If new distance < best distance: replace
            if(curcost < bestcost){
                bestcost = curcost;
                tour = new_tour;
            }
        }
    }
    return bestcost;
}