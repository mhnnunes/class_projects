

#include <set>
#include <vector>
#include <bitset>
#include <utility>
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

typedef std::pair<double, int> city;
typedef std::set < city >::iterator city_it;

// Residual Graph
class Graph{
    int nvertices;
    int nedges;
    std::vector< std::set< city > > adj;
public:
    Graph(int size);
    Graph();
    void addEdge(int u, int v, int cap, double weight);
    void addEdge(int u, int v, double weight);
    void deleteEdge(int u, city_it c);
    void printGraph(); //debug method
    int getSize(){ return this->nvertices; }
    city_it getNearestCity(int city);
    double getPathCost(int u, int v);
};


#endif