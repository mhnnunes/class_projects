

#include <iostream>
#include "algorithm.h"
#define MAXCITIES 2000000

typedef long double lld;

typedef std::set< std::pair<double, int> > sdi;

double euc_2d(pdd city1, pdd city2){
    return sqrt(pow((city1.first - city2.first), 2) +
                pow((city1.second - city2.second), 2));
}

double att_dist(pdd city1, pdd city2){
    return ceil(sqrt((pow((city1.first - city2.first), 2) +
                pow((city1.second - city2.second), 2)) / 10.0));
}


double heuristics_ConstructiveTSP(std::vector<pdd> &cities, bool att){
    int cur = 0;
    lld totalcost = 0.0;
    int ncities = (int) cities.size();
    int nvisited = 0;
    std::vector<bool> visited(ncities, false);

    // visited.reset(); // In the beggining no cities have been visited
    visited[cur] = 1; // Mark current city as visited
    nvisited++;
    // std::cout << "BEFORE LOOP    ncities: " << ncities << "   nvis: " << nvisited << std::endl;
    while(nvisited < ncities){
        // std::cout << "Including city: " << cur << std::endl;
        // std::cout << "visited: " << visited << std::endl;
        sdi not_visited_cities;
        for (int i = 0; i < ncities; ++i)
        { // Iterate through all cities: O(n)
            if(!visited[i] && i != cur){ // Only calculate distance to unvisited cities
                double dist = (att)? att_dist(cities[cur], cities[i]) : euc_2d(cities[cur], cities[i]);
                // std::cout << "dist: " << dist << std::endl;
                not_visited_cities.insert(std::make_pair(dist, i)); // insert on set O(1)
            }
        }
        // Take out closest city:
        auto nearest_neighbor = not_visited_cities.begin();
        totalcost += nearest_neighbor->first;
        cur = nearest_neighbor->second;
        // std::cout << "Smallest distance city is: " << cur << "  with distance: "<< nearest_neighbor->first << std::endl;
        visited[cur] = 1; // Mark current city as visited
        nvisited++;
    }

    // Add edge from last city to first
    int i = 0;
    double dist = (att)? att_dist(cities[cur], cities[i]) : euc_2d(cities[cur], cities[i]);
    totalcost += dist;
    return totalcost;
}