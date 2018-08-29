#include<iostream>
// #include<vector>
#include<cstdlib>
#include<cmath>
#include "io.h"
#include "graph.h"

using namespace std;


double euc_2d(pdd city1, pdd city2){
	return sqrt(pow((city1.first - city2.first), 2) + pow((city1.second - city2.second), 2));
}

int main(int argc, char* argv[]){
	std::vector< pdd >  cities;
	readInput(cities);
	for(auto &city : cities)
	{
        std::cout << "X: " << city.first << "  Y: " << city.second << std::endl;
    }

    // Make graph
    Graph graph(cities.size());
    for (int i = 0; i < (int) cities.size(); i++)
    {
    	for (int j = i; j < (int) cities.size(); j++)
    	{
    		if(i != j)
    		{ // Avoid adding loops
    			double dist = euc_2d(cities[i], cities[j]);
    			cout << "dist bet x:" << i << " and y:" << j << "  " << dist << endl;
    			graph.addEdge(i, j, 0, dist);
    			// graph.addEdge(j, i, dist); // Two way edge, undirected graph
    		}
    	}
    }

    graph.printGraph();
}