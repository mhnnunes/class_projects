
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

#include <iostream>
#include <algorithm> 
#include <cmath>

#include "graph.h"

Graph::Graph(int size)
{
    nodes.resize(size);
    visited.assign(size, UNVISITED);
    parent.assign(size, std::vector<int>(18, 0));
    nvertex = size;
}

void Graph::addEdge(int u, int v)
{
    nodes[u].adj.push_back(v);
    nodes[v].adj.push_back(u); // reverse edge
}

void Graph::print()
{
    for (int i = 0; i < (int) nodes.size(); i++)
    {
        // print vertex and cc index
        std::cout << "(" << i  << ", " << nodes[i].CC <<    ") " ;
    }
    std::cout << endl;
}


std::vector< CC > Graph::findConnectedComponents()
{
    std::vector< CC > CCs;
    for (int i = 0; i < nvertex; i++)
    {
        if(visited[i] == UNVISITED)
        {
            // Initialize CC data
            CC cc_data;
            cc_data.nvertices = 0;
            cc_data.maxdegree = 0;
            cc_data.mintime = 0;
            cc_data.number_of_arcs = 0;
            // Start DFS
            dfsVisit(i, cc_data, (int) CCs.size());
            cc_data.number_of_arcs /= 2; // divide by two to avoid
                                         // counting each edge twice
            CCs.push_back(cc_data);
        }
    }
    return CCs;
}

void Graph::preProcessConnectedComponents(std::vector< CC > &CCs)
{
    int start_node = -1;
    visited.assign(nvertex, 0); // reset visited indicator
    for (int i = 0; i < (int) CCs.size(); i++)
    {
        start_node = -1;
        switch(CCs[i].type)
        {
            case path:
                // start DFS from start node (node with degree = 1)
                // first node position = 0
                dfsVisit(CCs[i].start_node, CCs[i].start_node, 0);
                break;
            case cycle:
                start_node = CCs[i].nodes_in_cc[0];
                // start DFS from start node
                // first node position = 0
                dfsVisit(start_node, start_node, 0);
                break;
            case bipartite:
                // take an arbitrary node
                start_node =  CCs[i].nodes_in_cc[0];
                // mark this node as in one partition
                nodes[start_node].position = 0;
                // mark this node as visited
                visited[start_node] = 1;
                // mark nodes adjacent to the current node as nodes
                // in the other partition
                for(int i = 0; i < (int) nodes[start_node].adj.size(); i++)
                { // nodes in the other partition 
                    visited[nodes[start_node].adj[i]] = 1;
                    nodes[nodes[start_node].adj[i]].position = 1;
                }
                // the unmarked nodes will be in the same partition as start node
                for(auto &node : CCs[i].nodes_in_cc) // nodes in same partition
                {
                    if(!visited[node])
                    {
                        nodes[node].position = 0;
                        visited[node] = 1;
                    }
                }
                break;
            case tree:
                // take an arbitrary node
                
                start_node =  CCs[i].nodes_in_cc[0];
                // this node will be the root node
                // other nodes wil have a position equal to their level
                dfsVisit(start_node, start_node, 0);
                precomputeSparseMatrix(CCs[i].nodes_in_cc);
                break;
        }
    }
}


// =============================
// The code below was adapted from: 
// https://www.geeksforgeeks.org/lca-for-general-or-n-ary-trees-sparse-matrix-dp-approach-onlogn-ologn/

void Graph::precomputeSparseMatrix(std::vector<int> &nodes_in_cc) 
{
    long int level = log10((long int) nodes_in_cc.size()) + 1;

    for (int i=1; i<level; i++) 
    { 
        for (auto &node : nodes_in_cc) 
        { 
            if (parent[node][i-1] != -1) // compute 2^jth parent for each node
                parent[node][i] = 
                    parent[parent[node][i-1]][i-1]; 
        } 
    } 
}


int Graph::lca(int u, int v)
{
    if (nodes[v].position < nodes[u].position) 
        std::swap(u, v); 
  
    int diff = nodes[v].position - nodes[u].position;
  
    // Step 1 of the pseudocode 
    for (int i=0; i < (int) parent[v].size(); i++) 
        if ((diff>>i)&1)
            v = parent[v][i]; 
  
    // now depth[u] == depth[v] 
    if (u == v) 
        return u; 
  
    // Step 2 of the pseudocode 
    for (int i = ((int) parent[v].size())-1; i>=0; i--) 
        if (parent[u][i] != parent[v][i]) 
        { 
            u = parent[u][i]; 
            v = parent[v][i]; 
        } 
  
    return parent[u][0]; 
}

// End of adapted code
// =============================

// call this when determining nodes' positions in path and cycle 
void Graph::dfsVisit(int u, int v, int node_index)
{ //polymorphic method
    // Mark the current node as visited
    visited[v] = VISITED;
    // Save node position inside of CC
    nodes[v].position = node_index;

    // Save v's parent
    parent[v][0] = u;
    for(auto &node : nodes[v].adj)
    {
        if(visited[node] == UNVISITED)
        {
            dfsVisit(v, node, node_index + 1); 
        } 
    }
}

// call this when recognizing ships
void Graph::dfsVisit(const int &v, CC &cc_data, const int &CC_index)
{ //polymorphic method
    // Count maximum vertex degree
    cc_data.maxdegree = std::max((int) nodes[v].adj.size(),
        cc_data.maxdegree);
    cc_data.nvertices++;
    // Mark the current node as visited
    visited[v] = VISITED;
    nodes[v].CC = CC_index;
    cc_data.nodes_in_cc.push_back(v);

    if((int) nodes[v].adj.size() == 1) cc_data.start_node = v;
    for(auto &node : nodes[v].adj)
    {
        if(visited[node] == UNVISITED)
        {
            dfsVisit(node, cc_data, CC_index); 
        } 
        cc_data.number_of_arcs++;
    }
}

unsigned int Graph::getDist(int a, int b, const CC &cc_data)
{
    int l; 
    int n;
    long long int ans = 0;
    switch(cc_data.type)
    {
        case path:
            ans = std::abs(nodes[a].position - nodes[b].position);
            break;
        case cycle:
            l = nodes[a].position - nodes[b].position;
            n = (int) cc_data.nodes_in_cc.size();
            ans = std::min(std::abs(l), std::abs(n - std::abs(l)));
            break;
        case bipartite:
            // if nodes are in the same partition: dist == 2
            // else dist == 1
            ans = (nodes[a].position == nodes[b].position)? 2 : 1;
            break;
        case tree:
            int LCA = lca(a, b);
            if(LCA == a)
            {
                ans = std::abs(nodes[a].position - nodes[b].position);
            }
            else if(LCA == b)
            {
                ans = std::abs(nodes[b].position - nodes[a].position);
            }
            else
            {
                ans = std::abs( std::abs(nodes[LCA].position - nodes[a].position) + 
                    std::abs(nodes[LCA].position - nodes[b].position) );
            }
            break;
    }
    return ans;
}
