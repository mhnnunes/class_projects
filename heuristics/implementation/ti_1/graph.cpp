

#include <iostream>

#include "graph.h"


Edge::Edge(int dt, int fl, int cap, double weight, int r){
    this->v = dt;
    this->flow = fl;
    this->capacity = cap;
    this->weight = weight;
    this->rev = r;
}

Graph::Graph(int size){
    this->nvertices = size;
    this->adj.resize(size);
}

Graph::Graph(){
    nvertices = 0;
}

void Graph::addEdge(int u, int v, double weight){
    // Forward edge : 0 flow and C capacity
    // Edge a(v, 0, cap, weight, adj[v].size());

    // // Back edge : 0 flow and 0 capacity
    // Edge b(u, 0, cap, weight, adj[u].size());

    // this->adj[u].push_back(a);
    // this->adj[v].push_back(b); // reverse edge
    this->adj[u].insert(std::make_pair(weight, v)); // O(log n)
    this->adj[v].insert(std::make_pair(weight, u)); // O(log n)
    this->nedges+=2;
}

void Graph::deleteEdge(int u, city_it c){
    // Delete city v from u's adj list 
    // (calling erase on a set using an iterator
    //  has a complexity of an amortized constant)
    this->adj[u].erase(c); // O(1)
}

void Graph::printGraph(){
	for (int i = 0; i < nvertices; ++i)
	{
		std::cout << "U:" << i << "  ";
		for (auto &neighbor: adj[i])
		{
			std::cout << "V:" << neighbor.second << "," << neighbor.first << "  ";
		}
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
	}
}

city_it Graph::getNearestCity(int city){
	return adj[city].begin();
}

double Graph::getPathCost(int u, int v){
	// auto &next_city = adj[u].find(v);
	return 42;
}