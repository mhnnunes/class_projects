
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

void recognizeShips(std::vector<CC> &CCs)
{
    int path_count = 0, cycle_count = 0, bipartite_count = 0, tree_count = 0;
    for (int i = 0; i < (int) CCs.size(); i++)
    {
        // Decision tree to classify CCs
        CCs[i].mintime = 0LL;
        if(CCs[i].maxdegree <= 2) // path or cycle
        {
            if(CCs[i].number_of_arcs == CCs[i].nvertices) // cycle
            {
                cycle_count++;
                CCs[i].type = cycle;
            }
            else // path
            {
                path_count++;
                CCs[i].type = path;
            }
        }
        else // tree or bipartite
        {
            if(CCs[i].number_of_arcs == CCs[i].nvertices - 1) // tree
            {
                tree_count++;
                CCs[i].type = tree;
            }
            else // bipartite
            {
                bipartite_count++;
                CCs[i].type = bipartite;
            }
        }
    }
    std::cout << path_count << " " << tree_count << " " <<
        bipartite_count  << " " << cycle_count << endl;
}

void calculateAdvantageTime(Graph &g, const std::vector<int> &swaps,
    std::vector<CC> &CCs)
{
    unsigned int minDist = UINT_MAX;
    for(int i = 0; i < (int) swaps.size(); i++)
    {
        if(swaps[i] != i) // only count when distance is not 0
        { // not swapping node with itself
            // Check nodes CC
            int node_cc = g.getNodeCC(i);
            // std::cerr << node_cc << endl;
            CCs[node_cc].mintime += g.getDist(i, swaps[i], CCs[node_cc]);
        }
    }
    for(auto &cc : CCs)
    {
        cc.mintime /= 2;
        if((cc.mintime) < minDist) minDist = cc.mintime;
    }
    std::cout << minDist << endl;
}
