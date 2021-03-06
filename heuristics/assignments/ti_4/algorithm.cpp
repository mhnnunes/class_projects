
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

using namespace std;

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

void makeDistMatrix(vector< pdd > &cities,
                    vector< vector< double> > &distMatrix,
                    int ncities, bool att){
    for(int i = 0; i < ncities - 1; i++){
        distMatrix[i][i] = 0.0;
        for (int j = i + 1; j < ncities; j++){
            distMatrix[i][j] = calculateDist(cities[i], cities[j], att);
            distMatrix[j][i] = distMatrix[i][j];
        }
    }
}

lld calculate_tour_cost(std::vector<int> &tour,
                        vector< vector< double> > &distMatrix){
    lld totalcost = 0.0;
    for (int i = 0; i < ((int) tour.size()) - 1; i++){ // O(n)
        totalcost += distMatrix[tour[i]][tour[i+1]];
    }
    return totalcost;
}

lld heuristics_ConstructiveTSP(vector< vector< double> > &distMatrix,
                               std::vector<int> &tour,
                               int ncities){
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
                dist = distMatrix[cur][i];
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
    dist = distMatrix[cur][i];
    tour[nvisited] = i;
    totalcost += dist;
    return totalcost;
}

void print_tour(std::vector<int> tour){
    std::cout << "PRINTING TOUR" << std::endl;
    std::cout << "city -> nextcity" << std::endl;
    for(auto &it: tour){
        std::cout << it << "-> " ;
    }
    std::cout << std::endl;
}

lld heuristics_VND_TSP(vector< vector< double> > &distMatrix,
                       std::vector<int> &tour,
                       int ncities){
    lld curcost = 0.0;
    lld bestcost = 0.0;
    int nneighborhoods = 2; // Number of neighborhoods for local search
    int noimprovement = 0;

    // Generate initial solution using the constructive heuristic
    bestcost = heuristics_ConstructiveTSP(distMatrix, tour, ncities);
    // Tour will be stored in the tour variable
    int l = 0;
    while(l < nneighborhoods && noimprovement < 10){
        // Search for improvement on neighborhood l
        //     - neighborhood 0: 2Opt
        //     - neighborhood 1: 3Opt
        if(l == 0){
            curcost = search_2Opt_TSP(distMatrix, tour, bestcost, ncities);
            if(curcost < bestcost){
                // If cost of new solution is better than cost of current solution
                // Store new solution
                bestcost = curcost;
                noimprovement = 0;
                // Go back to first neighborhood
                l = 0;
            }else { // Otherwise next neighborhood
                noimprovement++;
                l = 1;
            }
        }
        if(l == 1){
            curcost = search_3Opt_TSP(distMatrix, tour, bestcost, ncities);
            if(curcost < bestcost){
                // If cost of new solution is better than cost of current solution
                // Store new solution
                bestcost = curcost;
                noimprovement = 0;
                // Go back to first neighborhood
                l = 0;
            }else { // Otherwise next neighborhood
                noimprovement++;
                l = 1;
            }
        }

    }
    return bestcost;
}

void reverse_path(std::vector<int> &tour, int i, int k){
    int swapaux = 0;
    int ncities = ((int) tour.size()) - 1;
    if(k < i) swap(i, k);
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
        swap(tour[index], tour[revindex]);
    }
}

lld search_2Opt_TSP(vector< vector< double> > &distMatrix,
                    std::vector<int> &tour,
                    lld initialcost,
                    int ncities){
    lld bestcost = initialcost;
    lld curcost = 0.0;
    for (int i = 0; i < ncities - 1; i++){
        for (int k = i + 1; k < ncities; k++){
            // Swap nodes i and k in tour
            std::vector<int> new_tour(tour.begin(), tour.end());
            // Calculate new tour distance
            reverse_path(new_tour, i, k);
            curcost = calculate_tour_cost(new_tour, distMatrix);
            // If new distance < best distance: replace
            if(curcost < bestcost){
                bestcost = curcost;
                tour = new_tour;
            }
        }
    }
    return bestcost;
}


lld search_3Opt_TSP(vector< vector< double> > &distMatrix,
                    std::vector<int> &tour,
                    lld initialcost,
                    int ncities){
    lld bestcost = initialcost;
    lld curcost = 0.0;
    for (int i = 0; i < ncities - 2; i++){
        for (int j = i + 1; j < ncities - 1; j++){
            for (int k = j + 1; k < ncities; k++){
                // Make swapping combinations
                // Consider a path like:
                // A - i - i+1 - B - j - j+1 - C - k - k+1 - A
                // Segment A is between k and i-1 [k, i)
                // Segment B is between i and j-1 [i ,j)
                // Segment C is between j and k-1 [j, k)
                // First try: Reverse A, which equals reverse BC
                // Make new tour
                std::vector<int> new_tour(tour.begin(), tour.end());
                reverse_path(new_tour, i, k-1); // Revert BC
                curcost = calculate_tour_cost(new_tour, distMatrix);
                // If new distance < best distance: replace
                if(curcost < bestcost){
                    bestcost = curcost;
                    tour = new_tour;
                    // return bestcost; // First improving
                }
                // Second try: Reverse C
                new_tour.assign(tour.begin(), tour.end());
                reverse_path(new_tour, j, k-1); // Revert C
                curcost = calculate_tour_cost(new_tour, distMatrix);
                // If new distance < best distance: replace
                if(curcost < bestcost){
                    bestcost = curcost;
                    tour = new_tour;
                    // return bestcost; // First improving
                }
                // Third try: Reverse B
                new_tour.assign(tour.begin(), tour.end());
                reverse_path(new_tour, i, j-1); // Revert B
                curcost = calculate_tour_cost(new_tour, distMatrix);
                // If new distance < best distance: replace
                if(curcost < bestcost){
                    bestcost = curcost;
                    tour = new_tour;
                    // return bestcost; // First improving
                }
                // Fourth try: Reverse A, then revert B, which means
                // revert BC then revert B
                new_tour.assign(tour.begin(), tour.end());
                reverse_path(new_tour, i, k-1); // Revert BC
                reverse_path(new_tour, i, j-1); // Revert B
                curcost = calculate_tour_cost(new_tour, distMatrix);
                // If new distance < best distance: replace
                if(curcost < bestcost){
                    bestcost = curcost;
                    tour = new_tour;
                    // return bestcost; // First improving
                }

                // Fifth try: Reverse A, then revert C, which means
                // revert BC then revert C
                new_tour.assign(tour.begin(), tour.end());
                reverse_path(new_tour, i, k-1); // Revert BC
                reverse_path(new_tour, j, k-1); // Revert C
                curcost = calculate_tour_cost(new_tour, distMatrix);
                // If new distance < best distance: replace
                if(curcost < bestcost){
                    bestcost = curcost;
                    tour = new_tour;
                    // return bestcost; // First improving
                }

                // Sixth try: Reverse B, then revert C
                new_tour.assign(tour.begin(), tour.end());
                reverse_path(new_tour, i, j-1); // Revert B
                reverse_path(new_tour, j, k-1); // Revert C
                curcost = calculate_tour_cost(new_tour, distMatrix);
                // If new distance < best distance: replace
                if(curcost < bestcost){
                    bestcost = curcost;
                    tour = new_tour;
                    // return bestcost; // First improving
                }

                // Seventh try: Reverse A, then B, then C
                // which means: revert BC, then B, then C
                new_tour.assign(tour.begin(), tour.end());
                reverse_path(new_tour, i, k-1); // Revert BC
                reverse_path(new_tour, i, j-1); // Revert B
                reverse_path(new_tour, j, k-1); // Revert C
                curcost = calculate_tour_cost(new_tour, distMatrix);
                // If new distance < best distance: replace
                if(curcost < bestcost){
                    bestcost = curcost;
                    tour = new_tour;
                    // return bestcost; // First improving
                }                
            }
        }
    }
    return bestcost;
}

void add_tour_to_tabu(std::vector<int> &new_tour,
                      std::vector< std::vector< pii > > &tabulist,
                      int ncities, int &tabu_solution){
    // Add first city
    tabulist[tabu_solution][new_tour[0]] = pii(new_tour[ncities - 1],
                                               new_tour[1]);
    // Add last city
    tabulist[tabu_solution][new_tour[ncities - 1]] = pii(new_tour[ncities - 2],
                                                         new_tour[0]);
    for (int i = 1; i < ncities - 1; ++i){
        tabulist[tabu_solution][new_tour[i]] = pii(new_tour[i - 1],
                                                   new_tour[i + 1]);
    }
    tabu_solution += 1;
    tabu_solution %= 10;
}

void print_tabu_list(std::vector< std::vector< pii > > &tabulist,
                     int ncities){
    std::cout << "PRINTING TABU LIST" << std::endl;
    std::cout << "city -> (prevcity, nextcity)" << std::endl;
    for (int i = 0; i < (int) tabulist.size(); i++){
        std::cout << "Position: " << i << std::endl;
        for (int j = 0; j < ncities; j++){
            std::cout << j << "-> (" << tabulist[i][j].first << ',' << tabulist[i][j].second << ")  ";
        }
        std::cout << std::endl;
    }
}

bool tour_in_tabu_list(std::vector<int> &tour,
                       std::vector< std::vector< pii > > &tabulist,
                       int ncities){
    bool present = false;
    for(int i = 0; i < (int) tabulist.size(); i++){
        // Check solution
        present = false;
        // Check first and last position, if equal to tour on tabulist,
        // check middle of tour        
        if( ( tabulist[i][tour[0]] == pii(tour[ncities-1], tour[1]) ) && 
            ( tabulist[i][tour[ncities-1]] == pii(tour[ncities-2], tour[0]) )){
            // std::cout << "found first and last of tour  " << std::endl;
            present = true;
            for (int j = 1; j < ncities - 1; j++){
                if(tabulist[i][tour[j]] != pii(tour[j-1], tour[j+1])){
                    present = false;
                    break;
                }
            }
            if(present) return present;
        }
    }
    return false;
}

lld heuristics_Tabu_Search_TSP(vector< vector< double> > &distMatrix,
                               std::vector<int> &tour,
                               int ncities){
    lld curcost = 0.0;
    lld bestcost = 0.0;
    int noimprovement = 0;
    int tabu_solution = 0; // Keep track of how many solutions are in the tabu list
    int MAX_ITERATIONS_WITH_NO_IMPROVEMENT = 10;
    std::vector< std::vector< pii > > tabulist(10, std::vector< pii >(ncities, pii(0, 0)));
    // Generate initial solution using the constructive heuristic
    bestcost = heuristics_ConstructiveTSP(distMatrix, tour, ncities);
    // Add solution to tabu list
    add_tour_to_tabu(tour, tabulist, ncities, tabu_solution);
    
    while(noimprovement < MAX_ITERATIONS_WITH_NO_IMPROVEMENT){
        std::vector<int> new_tour(tour.begin(), tour.end());
        // Search 2-Opt neghborhood for solution with fitness higher
        // than the current solution
        curcost = search_2Opt_TSP(distMatrix, new_tour, bestcost, ncities);
        if(!tour_in_tabu_list(new_tour, tabulist, ncities) && (curcost < bestcost) ){
            add_tour_to_tabu(tour, tabulist, ncities, tabu_solution);
            tour = new_tour;
            bestcost = curcost;
            noimprovement = 0;
        }else noimprovement++;
    }
    return bestcost;
}


lld heuristics_Greedy_Randomized_TSP(std::vector< std::vector< double> > &distMatrix,
                                     std::vector<int> &tour,
                                     double alpha,
                                     int ncities){
    // Greedy randomized heuristic for constructing a TSP path in a complete graph
    int randi;
    int cur = 0;
    int nvisited = 0;
    lld totalcost = 0.0;
    double maxcost, mincost, threshold;
    std::vector<int> rcl;
    std::vector<bool> visited(ncities, false);
    srand( 12345 ); // Initialize random seed

    // Pick initial node at random
    int firstcity = rand() % ncities;
    cur = firstcity;
    visited[cur] = 1; // Mark current city as visited
    tour[0] = cur; // Add the first city to tour
    nvisited++;


    while(nvisited < ncities){ // Iterate through all cities: O(n)

        // Build RCL
        rcl.resize(0);
        // Set maxcost and mincost
        mincost = (double) INF;
        maxcost = 0.0;
        for (int i = 0; i < ncities; ++i){ // Iterate through all cities: O(n)
            if(!visited[i] && distMatrix[cur][i] < mincost)
                mincost = distMatrix[cur][i];
            if(!visited[i] && distMatrix[cur][i] > maxcost)
                maxcost = distMatrix[cur][i];
        }
        threshold = mincost + alpha*(maxcost - mincost);
        for (int i = 0; i < ncities; i++){ // Iterate through all cities: O(n)
            // Only calculate distance to unvisited cities
            if(!visited[i] && i != cur){
                if(distMatrix[cur][i] <= threshold) rcl.push_back(i);
            }
        }
        randi = rand() % ((int) rcl.size());
        // Add closest city to tour
        tour[nvisited] = rcl[randi];
        // Add its cost to the total
        totalcost += distMatrix[cur][rcl[randi]];
        cur = rcl[randi];
        visited[cur] = 1; // Mark current city as visited
        nvisited++;
    }
    // Add edge from last city to first
    int i = firstcity;
    tour[nvisited] = i;
    totalcost += distMatrix[cur][i];
    return totalcost;
}


lld heuristics_GRASP_TSP(vector< vector< double> > &distMatrix,
                         std::vector<int> &tour,
                         int ncities){
    lld curcost_greedy = 0.0;
    lld curcost_local = 0.0;
    lld bestcost = 0.0;
    
    int noimprovement = 0;
    int MAX_ITERATIONS_WITH_NO_IMPROVEMENT = 500;
    double alpha = 0.001;
    // Generate initial solution using the constructive heuristic
    bestcost = heuristics_Greedy_Randomized_TSP(distMatrix, tour, alpha,
                                                 ncities);
    while(noimprovement < MAX_ITERATIONS_WITH_NO_IMPROVEMENT){
        std::vector<int> new_tour(tour.begin(), tour.end());
        curcost_greedy = heuristics_Greedy_Randomized_TSP(distMatrix,
                                                          new_tour,
                                                          alpha,
                                                          ncities);
        // Search 2-Opt neghborhood for solution with fitness higher
        // than the current solution
        curcost_local = search_2Opt_TSP(distMatrix, new_tour, curcost_greedy,
                                        ncities);
        if(curcost_local < bestcost){
            tour = new_tour;
            bestcost = curcost_local;
            noimprovement = 0;
        }
        else noimprovement++;
    }
    return bestcost;
}