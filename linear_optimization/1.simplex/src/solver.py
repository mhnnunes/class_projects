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

import re
import sys
import argparse
import numpy as np
from ioutils import IOUtils
from simplex import Simplex
from lp import LinearProgramming


class Main(object):
    """Main program class.

    Variables:
        rw_input {string} -- Raw string received as input.
        io_handler {IOUtils} -- Handles IO functionalities.
        lp {LinearProgramming} -- Stores information and perform operations
        on the Linear Programming supplied.
        s {Simplex} -- Runs the Simplex algorithm in the LP supplied
        mode {string} -- Sets the mode in which the program will be executed,
        can be one of ["1", "2"]
    """
    def __init__(self, filename):
        self.io_handler = IOUtils()
        self.rw_input = self.io_handler.readInput(filename)
        self.lp = LinearProgramming()
        self.s = Simplex()

    def processInputString(self):
        """Processes the given input string, setting class variables as needed
        Returns:
            bool -- Success or fail flag.
        """
        try:
            # File should be 4 lines long on mode 1 and 5 lines long on mode 2
            if len(self.rw_input) not in [4, 5]:
                print "ERROR: Wrong number of lines in input file."
                raise Exception

            # Get (and save) program mode
            mode = self.rw_input[0].split(" ")
            self.mode = mode[1]
            if self.mode == "1":
                rows = self.rw_input[1]
                self.s.setMode("primal")
                matrix = self.rw_input[3]
            elif self.mode == "2":
                simplex_mode = self.rw_input[1]
                # Set the mode for the simplex
                if simplex_mode == "D":
                    self.s.setMode("dual")
                elif simplex_mode == "P":
                    self.s.setMode("primal")
                else:
                    print "ERROR: unrecognized simplex mode"
                    raise Exception
                rows = self.rw_input[2]
                matrix = self.rw_input[4]
            else:
                print "ERROR: Unrecognized program mode."
                raise Exception

            # Remove extra curly bracket from borders
            matrix = matrix.replace('{{', '{')
            matrix = matrix.replace('}}', '}')
            # Extract numbers from curly brackets
            # Returns a list of string elements, containing numbers
            # separated by a comma (,)
            matched = re.findall(r'{(.*?)}', matrix)

            # For each element in list, this element will be a string,
            # representing a list of numbers separated by a comma
            # Split the string by comma to get string numbers,
            # then convert to float
            matrix_rows = [map(float, m.split(',')) for m in matched]
            # Each row will now be a list of float numbers
            nrows_a = len(matrix_rows) - 1
            if not int(rows) == nrows_a:
                # Throw error if matrix contains
                # more rows than expected
                print "ERROR: Matrix has more rows than expected."
                raise Exception
            # Transform the rows list into a numpy array (matrix)
            self.lp.setLP(np.array(matrix_rows))
            return True
        except Exception as e:
            print e
            return False

    def run(self):
        """Main program method. Runs the expected functionalities on
        the Linear Programming model supplied
        """
        ok = self.processInputString()
        if ok:
            if self.mode == "1":
                # We're not sure if the LP is feasible if the mode is 1
                # Check feasibility
                self.lp.checkFeasibility()

                if not self.lp.isFeasible():
                    # Print the result and exit
                    self.lp.printResult()
                    return

            self.lp.makeExtendedCanonicalTableau()
            # Run simplex (polymorphic call)
            self.s.run(self.lp, self.mode)
            # Print results
            self.lp.printResult()
        else:
            print "Error reading input"
            sys.exit(-1)


if __name__ == '__main__':
    parser = \
        argparse.ArgumentParser(description='Linear Programming Solving \
                                             via the Simplex Algorithm')
    parser.add_argument('filename', help="Name of input file")

    args = parser.parse_args()

    main = Main(args.filename)
    main.run()
