#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from graph import Graph
from flow import MaxFlow
from IOUtils import IOUtils
import argparse  # Argument parsing


class Main(object):

    def __init__(self, filename):
        self.io_handler = IOUtils()
        self.rw_input = self.io_handler.readInput(filename)

    def processInputString(self):
        """Processes the given input string, setting class variables as needed.
        Returns:
            bool -- Success or fail flag.
        """
        try:
            nvertexes = int(self.rw_input[0])
            narcs = int(self.rw_input[1])

            capacities = self.rw_input[2].split()
            if not len(capacities) == narcs:
                print 'ERROR: Number of actual elements in costs vector is \
                smaller than declared.'
                raise Exception

            if not len(self.rw_input[3:]) == nvertexes:
                print 'ERROR: Number of rows in N matrix is different from the\
                 declared value.'
                print 'Matrix length (in rows):', len(self.rw_input[3:])
                raise Exception

            A = []
            i = 0
            for line in self.rw_input[3:]:
                if not len(line.split()) == narcs:
                    print 'ERROR: Number of elements (' + \
                        str(len(line.split())) + \
                        ') in row ' + str(i) + \
                        ' of A matrix does not agree with' + \
                        ' number of declared sets (' + str(narcs) + ')'
                    print 'line:', line
                    raise Exception
                else:
                    A.append(list(map(int, line.split())))
                    i += 1

            self.graph = Graph(nvertexes, narcs, capacities, A)
            return True
        except Exception as e:
            print e
            return False

    def main(self):
        self.processInputString()

        source, sink = self.graph.getSourceSink()

        MaxFlow.fordFulkerson(self.graph, source, sink)
        MaxFlow.findMinimumCut(self.graph, source)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ford Fulkerson's algorithm \
        for finding the Maximum Flow in a graph.")
    parser.add_argument('filename', help="Name of input file")

    args = parser.parse_args()

    m = Main(args.filename)
    # m.processInputString()
    m.main()
