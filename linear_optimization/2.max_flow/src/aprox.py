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

import argparse  # Argument parsing
import numpy as np  # Matrix functions
from IOUtils import IOUtils


class IntegerProgramming(object):
    def __init__(self, nelements, nsets, costs, A):
        print "IN IP INIT"
        self.c = np.array(costs).astype(np.float64)
        print 'costs', self.c
        # PRIMAL VARIABLES (sets)
        self.y = np.zeros(nsets, dtype=np.int32)
        print 'y', self.y
        # DUAL VARIABLES (elements)
        self.x = np.zeros(nelements, dtype=np.float64)
        print 'x', self.x
        # A MATRIX (for primal, TRANSPOSE FOR DUAL)
        self.A = np.array(A).astype(np.int32)
        self.b = np.ones(nelements, dtype=np.int32)
        # self.A = self.A[:, :-1]
        print 'primal A revisited:'
        print self.A
        print 'primal b', self.b
        self.Atranspose = np.transpose(self.A)
        print 'Atranspose'
        print self.Atranspose

    def solve(self):
        nelements, nsets = self.A.shape
        # Array (initially full of zeros) that will record
        # which vertexes were included in the solution
        covered_vertexes = np.zeros(nelements, dtype=np.int32)

        # While not all elements have been included, keep working
        while not np.sum(covered_vertexes) == nelements:
            print '================= ITERATION STARTS ================'
            # Find first zero (uncovered) element in covered elements array
            print 'covered vertexes before zeros', covered_vertexes
            zeros = np.where(covered_vertexes == 0)[0]
            print 'zeros', zeros
            if not zeros.size == 0:
                i = zeros[0]
            else:
                i = 0

            print 'i', i
            # Variable i will be the index of the first uncovered element
            # Get restrictions in which this element is one (ON DUAL)
            restrictions_indexes = np.where(self.Atranspose[:, i] == 1)[0]
            print 'ones', restrictions_indexes
            # Find out how much I can raise the value of variable i
            # Multiply A transpose by x
            dot_product = np.dot(self.Atranspose, self.x)
            print 'dot', dot_product
            # Subtract the resulting value from the cost vector
            # (obtain new costs)
            taken_amt = self.c - dot_product
            print 'taken_amt'
            print taken_amt
            # The new value for the variable will be the smalles value it can
            # assume, given the restrictions
            new_x_value = np.min(taken_amt[restrictions_indexes])
            # Get the index of the restriction in which this value was found
            argmin = np.argmin(taken_amt[restrictions_indexes])
            # Get the restriction
            selected_restriction = \
                self.Atranspose[restrictions_indexes[argmin], :]
            print 'selected restriction', selected_restriction

            print 'min', new_x_value
            # Update vector x with the new value
            self.x[i] = new_x_value
            # Include vertices covered by the restriction (set) in the covered
            # vertexes array
            covered_vertexes = np.array([a | b for (a, b) in
                                        zip(covered_vertexes,
                                            selected_restriction)])
            print 'covered:', covered_vertexes
            print 'new x:', self.x
            self.y[restrictions_indexes[argmin]] = 1
            print 'y', self.y


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
            nelements = int(self.rw_input[0])
            nsets = int(self.rw_input[1])
            costs = self.rw_input[2].split(' ')
            if not len(costs) == nsets:
                print 'ERROR: Number of actual elements in costs vector is \
                smaller than declared.'
                raise Exception

            costs = list(map(int, costs))
            if not len(self.rw_input[3:]) == nelements:
                print 'ERROR: Number of rows in N matrix is different from \
                the declared value.'
                print 'Matrix length (in rows):', len(self.rw_input[3:])
                raise Exception

            A = []
            i = 0
            for line in self.rw_input[3:]:
                if not len(line.split(' ')) == nsets:
                    print 'ERROR: Number of elements (' + \
                        str(len(line.split(' '))) + \
                        ') in row ' + str(i) + \
                        ' of A matrix does not agree with' +\
                        ' number of declared sets (' + str(nsets) + ')'
                    raise Exception
                else:
                    A.append(list(map(int, line.split(' '))))
                    i += 1

            self.IP = IntegerProgramming(nelements, nsets, costs, A)
            return True
        except Exception as e:
            print e
            return False

    def main(self):
        ok = self.processInputString()
        if ok:
            self.IP.solve()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Integer Programming \
                                     solution to the Set Cover problem.')
    parser.add_argument('filename', help="Name of input file")

    args = parser.parse_args()

    m = Main(args.filename)
    m.main()
