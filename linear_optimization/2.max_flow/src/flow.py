#!/usr/bin/env python

# Copyright 2017 Matheus Nunes <mhnnunes@dcc.ufmg.br>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-

import itertools
import numpy as np  # Matrix functions
from IOUtils import IOUtils


class MaxFlow(object):
    """ Find Maximum Flow in a directed graph.

    The class MaxFlow contains implementations of algorithms designed to find
    the Maximum Flow in a flow network (directed graph).
    """
    @classmethod
    def fordFulkerson(cls, graph, source, sink):
        # Find augmenting path
        # This path is stored in the 'parent' list
        io = IOUtils()
        ok, path = graph.DFS(source, sink)
        max_flow = 0
        while ok:
            # Find smallest capacity in path
            path_capacity = graph.findSmallestCapacityinPath(source, sink,
                                                             path)
            # Increase maximum flow
            max_flow += path_capacity
            # Update edge values
            path_edges = graph.updateFlows(source, sink, path, path_capacity)
            # Print arc flows and capacities
            used_arcs, flows = graph.getPathInfo(path_edges)
            io.writeOutput(str(used_arcs) + '\n')
            io.writeOutput(str(flows) + '\n')
            io.writeOutput(str(graph.getCapacities()) + '\n')
            io.writeOutput('\n')
            # Find new augmenting path
            ok, path = graph.DFS(source, sink)

        io.writeOutput(str(max_flow) + '\n')

    @classmethod
    def findMinimumCut(cls, graph, source):
        io = IOUtils()
        graph_status = graph.BFS(source)
        # Find reachable and unreachable vertexes from source
        reachable = [index for index, vertex in enumerate(graph_status)
                     if vertex]
        print 'reachable', reachable
        unreachable = [index for index, vertex in enumerate(graph_status)
                       if not vertex]
        print 'unreachable', unreachable
        for elem in itertools.product(reachable, unreachable):
            print elem
        print graph.getArcs()
        # The edges between the reachable and unreachable vertexes describe
        # the cut
        min_cut = []
        for i in itertools.product(reachable, unreachable):
            if i in graph.getArcs():
                min_cut.append(i)
        # Transform it into a list of 0s and 1s
        min_cut_arr = [1 if arc in min_cut else 0 for arc in graph.getArcs()]
        print min_cut_arr
        io.writeOutput(str(np.array(min_cut_arr).astype(np.int32)) + '\n')
