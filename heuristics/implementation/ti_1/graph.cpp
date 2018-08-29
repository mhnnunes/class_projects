#include<iostream>
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

void Graph::addEdge(int u, int v, int cap, double weight){
	// Forward edge : 0 flow and C capacity
    Edge a(v, 0, cap, weight, adj[v].size());

    // Back edge : 0 flow and 0 capacity
    Edge b(u, 0, cap, weight, adj[u].size());

    this->adj[u].push_back(a);
    this->adj[v].push_back(b); // reverse edge
    this->nedges+=2;
}

void Graph::printGraph(){
	for (int i = 0; i < nvertices; ++i)
	{
		std::cout << "U:" << i << "  ";
		for (auto &neighbor: adj[i])
		{
			std::cout << "V:" << neighbor.v << "," << neighbor.weight << "  ";
		}
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
	}
}