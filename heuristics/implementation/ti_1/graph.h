
#include<vector>

#ifndef GRAPH_H
#define GRAPH_H

class Edge{
public:
    int v; //destination
    int flow;
    int capacity;
    double weight;
    int rev; // reverse edge
    Edge(int dt, int fl, int cap, double weight, int r);
};


// Residual Graph
class Graph{
    int nvertices;
    int nedges;
    std::vector<int> level;
    std::vector< std::vector<Edge> > adj;
public: 
    Graph(int size);
    Graph();
    void addEdge(int u, int v, int cap, double weight);
    void printGraph(); //debug method
    double TSPConstructive();
};

#endif