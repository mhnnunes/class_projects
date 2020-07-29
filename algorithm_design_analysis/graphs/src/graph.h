
// Copyright 2019 Matheus Nunes <mhnnunes@dcc.ufmg.br>
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

#ifndef GRAPH_H
#define GRAPH_H

#include <unordered_map>
#include <vector>
#include <queue>

#define endl '\n'

#define UNVISITED 0
#define VISITED 1

enum CC_type { tree, path, bipartite, cycle };

struct Node
{
    std::vector<unsigned int> adj;
    long long int position;
    // position holds:
    //     node depth, when node is in a tree
    //     node absolute position when node is in a cycle or path
    //     node partition when node is in bipartite graph
    unsigned int CC; // connected component that the node is in
    Node(): position(0), CC(0) {}
};

struct CC
{
    std::vector<int> nodes_in_cc;
    int nvertices;
    int maxdegree; // maximum degree of nodes in this CC
    long long int mintime; // sum of minimum distances between swaps in this CC
    int number_of_arcs;
    int start_node;
    CC_type type;
    CC(): nvertices(0), maxdegree(0), mintime(0LL), number_of_arcs(0), start_node(0){}
};

class Graph{
    std::vector< Node > nodes;
    std::vector<std::vector<int>> parent;
    // char is only 1 byte long
    std::vector<char> visited; // use char to save memory
    int nvertex;
public:
    Graph(int size);
    void addEdge(int u, int v);
    unsigned int getNodeCC(int i){ return nodes[i].CC; };
    unsigned int getDist(int a, int b, const CC &cc_data);
    void print();
    int lca(int u, int v);
    std::vector< CC > findConnectedComponents();
    void precomputeSparseMatrix(std::vector<int> &nodes_in_cc);

    // polymorphic DFS
    void dfsVisit(int u, int v, int node_index);
    void dfsVisit(const int &v, CC &cc_data, const int &CC_index);
    // unsigned int dfsVisit(const int &u, const int &v, const int &depth);
    // end of DFS
    void preProcessConnectedComponents(std::vector< CC > &CCs);
    void findRootforMinimumHeight(const CC &cc, std::vector<int> &roots);
};

#endif