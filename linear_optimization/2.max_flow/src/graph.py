
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

import numpy as np


class Graph(object):
    def __init__(self, nvertexes, narcs, costs, N):
        self.nvertexes = nvertexes
        self.narcs = narcs
        self.capacities = np.array(costs).astype(np.int32)
        inc_graph = np.array(N).astype(np.int32)
        self.__buildGraph(inc_graph)
        self.adj_graph = np.array(self.adj_graph).astype(np.int32)
        self.__buildOrigArcs(inc_graph)
        self.initializeFlows()

    def getSourceSink(self):
        return 0, self.nvertexes - 1

    def getCapacities(self):
        return self.capacities

    def getArcs(self):
        return self.orig_arcs

    def initializeFlows(self):
        self.arc_flow = {arc: 0 for arc in self.orig_arcs}

    def getFlows(self):
        return [self.arc_flow[edge] for edge in self.orig_arcs]

    def getPathInfo(self, path_arcs):
        used_edges_list = [1 if arc in path_arcs else 0 for arc in
                           self.orig_arcs]
        return np.array(used_edges_list).astype(np.int32), \
            np.array(self.getFlows()).astype(np.int32)

    def __buildOrigArcs(self, inc_graph):
        """ Builds a list containing the original edges of the graph (stored
        as tuples of vertexes).

        Arguments:
            inc_graph {matrix} -- incidency matrix describing the graph
        """
        self.orig_arcs = []
        for index, edge in enumerate(np.hsplit(inc_graph, self.narcs)):
            orig_vertex = int(np.where(edge == -1)[0])
            dest_vertex = int(np.where(edge == 1)[0])
            self.orig_arcs.append((orig_vertex, dest_vertex))

    def __buildGraph(self, inc_graph):
        """ Build the adjaceny matrix for the graph (which is initially
        specified as an incidency matrix).

        Arguments:
            inc_graph {matrix} -- incidency matrix (edge by vertex) for the
            graph.
        """
        self.adj_graph = []
        for index, vertex in enumerate(np.vsplit(inc_graph, self.nvertexes)):
            adj = [0] * self.nvertexes
            outgoing_edges = np.where(inc_graph[index, :] == -1)[0]
            if outgoing_edges.size > 0:
                for i, incoming_edge in enumerate(np.hsplit(
                        inc_graph[:, outgoing_edges], outgoing_edges.size)):
                    adjacent_vertex = int(np.where(incoming_edge == 1)[0])
                    adj[adjacent_vertex] = self.capacities[outgoing_edges[i]]
            self.adj_graph.append(adj)

    def BFS(self, s):
        """ Performs a breadth first search in the graph.

        Returns an array of boolean elements, marking the visited (reachable
        from source) nodes.

        Arguments:
            s {node} -- source node (start of search)

        Returns:
            visited {list(nodes)} -- list of visited (reachable from source)
            nodes.
        """
        # Mark all the vertices as not visited
        visited = [False] * self.nvertexes

        # Create a queue for BFS
        queue = []

        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

        while queue:

            # Dequeue a vertex from queue and print it
            s = queue.pop(0)

            # Get all adjacent vertices of the dequeued
            # vertex s. If a adjacent has not been visited,
            # then mark it visited and enqueue it
            outgoing_edges = np.where(self.adj_graph[s] != 0)[0]
            for neighbour in outgoing_edges:
                if visited[neighbour] is False:
                    queue.append(neighbour)
                    visited[neighbour] = True
        return visited

    def DFS(self, s, t):
        """ Performs a depth first search in the graph, returning a path from
        vertex 's' to vertex 't', if any is found.

        Arguments:
            s {node} -- source node
            t {node} -- destination node

        Returns:
            bool -- True if there is a path between s and t
            parent {path} -- path taken from s to t
        """
        stack = []
        parent = [-1] * self.nvertexes
        visited = [False] * self.nvertexes
        stack.append((s, s))
        while stack:
            curr = stack.pop()
            prev = curr[0]
            curr = curr[1]
            if not visited[curr]:
                parent[curr] = prev
                visited[curr] = True
                outgoing_edges = np.where(self.adj_graph[curr] != 0)[0]
                for neighbour in outgoing_edges:
                    stack.append((curr, neighbour))
            if curr == t:
                return True, parent
        return False, parent

    def findSmallestCapacityinPath(self, source, sink, parent):
        """ Iterates on a given path, finding the smallest edge capacity
        (bottleneck) in the path.

        Arguments:
            source {node} -- start of the path
            sink {node} -- end of the path
            parent {path} -- list storing the path

        Returns:
            cp {int} -- smallest edge capacity in path
        """
        curr = sink
        cp = float('Inf')
        while(curr != source):
            prev = parent[curr]
            cp = min(cp, self.adj_graph[prev][curr])
            curr = prev

        return cp

    def updateFlows(self, source, sink, parent, path_capacity):
        """ Given a path, and a smallest capacity, update the flow value on
        each edge in the path.

        Arguments:
            source {node} -- start of path
            sink {node} -- end of path
            parent {path} -- path between nodes
            path_capacity {int} -- value of the smallest capacity

        Returns:
            path_edges {list} -- list describing which of the original graph
            edges were used in the path
        """
        path_edges = []
        curr = sink
        while(curr != source):
            prev = parent[curr]
            path_edges.append((prev, curr))
            self.adj_graph[prev][curr] -= path_capacity
            self.adj_graph[curr][prev] += path_capacity
            if (prev, curr) in self.orig_arcs:
                self.arc_flow[(prev, curr)] += path_capacity
            curr = prev

        return path_edges
