
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
#include "algorithm.h"

#define _ ios_base::sync_with_stdio(0);cin.tie(0);

using namespace std;


int main(int argc, char *argv[])
{ _
    int vertices, edges;
    int u, v;
    cin >> vertices >> edges;
    Graph graph = Graph(vertices);

    for (int i = 0; i < edges; i++)
    {
    	cin >> u >> v;
    	// vertices are 1-based on input
    	// insert them in graph as 0-based	
    	graph.addEdge(u-1, v-1);
    }

    std::vector<int> swaps(vertices, -1);
    for(int i = 0; i < vertices; i++)
    {
        // Read swaps
        cin >> u >> v;
        // Swap u with v
        swaps[--u] = --v;
    }

    std::vector<CC> CCs = graph.findConnectedComponents();
    recognizeShips(CCs);

    graph.preProcessConnectedComponents(CCs);

    calculateAdvantageTime(graph, swaps, CCs);
    return 0;
}