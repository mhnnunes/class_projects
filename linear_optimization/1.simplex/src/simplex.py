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

import sys  # System functions
import numpy as np  # Matrix functions
from ioutils import IOUtils


class Simplex(object):

    def setMode(self, mode):
        """Set the mode of simplex algorithm chosen by the user.
        Arguments:
            mode {string} -- Has to be one of ["primal", "dual"],
            otherwise an exception is raised.
        Raises:
            Exception -- Invalid simplex mode.
        """
        if mode in ["primal", "dual"]:
            self.mode = mode
        else:
            raise Exception

    def getMode(self):
        """Returns the mode of the simplex algorithm chosen by the user.
        Returns:
            [string] -- [Type of simplex algorithm chosen. Can be one of
            ["primal", "dual"]]
        """
        return self.mode

    def __primal_simplex(self, LP, mode):
        """ Naive implementation of the (Primal) Simplex Algorithm in python
        Pre-conditions:
            . A numpy matrix (n-dimensional array), containing the tableau for
            the LP, in canonical form, with the following properties:
                - There is at least one element smaller than 0 in the first row
                (representing a positive element in the original vector c);
                - There are no negative elements in the last column
                (no negative elements in b);
                - There is an inital feasible base of columns.
            . The dimensions for this tableau
        Post-conditions:
            . A numpy matrix containing the resulting tableau after n
            iterations of the algorithm.
            . A summarized result in the form ["optimal", "unlimited"]
        Arguments:
            LP {LinearProgramming} -- A LinearProgramming class object
            containing information about the LP,
            as well as the tableau in canonical form with an initial feasible
            base
            mode {string} -- A string defining the mode of execution, can be
            one of ["1", "2"]
        """

        tableau = LP.getTableau()
        rows, columns = tableau.shape
        # Get c vector
        c = tableau[0, LP.orig_rows - 1:columns]
        # Reference to IO
        io_handler = IOUtils()
        # io_handler.openOutputFile()
        while True:
            # Print the tableau on each iteration on mode 2
            if mode == "2":
                string = "{"
                for row in np.vsplit(tableau, rows):
                    string += io_handler.formatOutputString(row[0]) + ","
                string += "}\n"
                io_handler.writeOutput(string)

            # Find index of first negative element in c
            for i in xrange(LP.orig_rows - 1, columns):
                if tableau[0, i] < 0.0:
                    break

            if i == (columns - 1):
                # No negative elements were found in c
                LP.setResult("optimal")
                return

            # Get the pivot column
            pivotcolumn = tableau[:, i]

            # Get b column
            bcolumn = tableau[:, columns - 1]

            # Find pivot on the column with a negative c element
            smallestratio = float("inf")
            srindex = -1
            for i in xrange(1, rows):
                if pivotcolumn[i] > 0.0:
                    # pivoted element must be GREATER THAN zero!
                    # Divide the element on the b column by the element
                    # on the pivot column
                    if (bcolumn[i] / pivotcolumn[i]) < smallestratio:
                        # Bland rule, since division can't return
                        # negative values
                        # Stop at first zero!
                        # Save the smallest ratio index
                        smallestratio = (bcolumn[i] / pivotcolumn[i])
                        srindex = i

            if srindex == -1:  # Column has no values > 0, unlimited LP
                LP.setResult("unlimited")
                return
            # Gaussian elimination: divide pivot row by pivot,
            # zero every other element in column

            # Divide pivot row by pivot
            tableau[srindex, :] /= pivotcolumn[srindex]

            # Zero other elements in column
            for i in xrange(0, rows):

                if i != srindex:
                    tableau[i, :] = tableau[i, :] - (pivotcolumn[i] *
                                                     tableau[srindex, :])

    def __dual_simplex(self, LP, mode):
        """ A naive implementation of the (Dual) Simplex algorithm in python.
        Pre-conditions:
            . A numpy matrix (n-dimensional array), containing the tableau
            for the LP, in canonical form, with the following properties:
                - There are no negative elements in the first row of the
                tableau (meaning there are no positive elements in the vector
                c on the original LP);
                - There is at least one negative element in the last columnn
                of the tableau (at least one negative entry in vector b);
                - There is an inital feasible base of columns.
            . The dimensions for this tableau
        Post-conditions:
            . A numpy matrix containing the resulting tableau after n
            iterations of the algorithm.
            . A summarized result in the form ["optimal", "unlimited"]
        Arguments:
            LP {LinearProgramming} --
            A LinearProgramming class object containing information about
            the LP, as well as the tableau in canonical form,
            with an initial feasible base
            mode {string} -- A string defining the mode of execution,
            can be one of ["1", "2"]
        """
        tableau = LP.getTableau()
        rows, columns = tableau.shape
        # Get matrix elements
        b = tableau[:, columns - 1]
        c = tableau[0, :]
        # Reference to IO
        io_handler = IOUtils()
        while True:
            # Print the tableau on each iteration on mode 2
            if mode == "2":
                string = "{"
                for row in np.vsplit(tableau, rows):
                    string += io_handler.formatOutputString(row[0]) + ","
                string += "}\n"
                io_handler.writeOutput(string)

            # Pick the first negative element in b
            # (ignoring first element [0], obj. value)
            firstnegativeb = -1
            for i in xrange(1, rows):
                if b[i] < 0.0:
                    firstnegativeb = i
                    break

            if firstnegativeb == -1:
                LP.setResult("optimal")
                return

            # Get pivot row
            pivotrow = tableau[firstnegativeb, :columns - 1]

            # Look for the negative entry which minimizes cj/Aij
            smallestratio = float("inf")
            srindex = -1
            for i in xrange(LP.orig_rows - 1, columns - 1):
                if pivotrow[i] < 0.0 and c[i] >= 0:  # Sanity check
                    if((c[i] / (pivotrow[i] * -1)) < smallestratio):
                        # Bland rule(?), get first entry
                        # (smallest index) minimizing the ratio
                        smallestratio = c[i] / pivotrow[i]
                        srindex = i
            # Sanity check!
            if srindex == -1:
                # print "smallestratio not found"
                LP.setResult("unlimited")  # ??????
                return

            # Gaussian elimination on that column!
            # Multiply that row by -1
            tableau[firstnegativeb, :] *= -1
            # Divide it by the pivot value
            tableau[firstnegativeb, :] /= (pivotrow[srindex])
            # Zero other enntries in the column
            for i in xrange(0, rows):
                if not i == firstnegativeb:
                    tableau[i, :] -= tableau[i, srindex] * \
                        tableau[firstnegativeb, :]

    def run(self, LP, mode):
        """ Run the appropriate simplex method, depending on the mode
        chosen by the user.
        Calls the __primal_simplex method if the choice is mode "primal",
        and calls the __dual_simplex method if the choice is mode "dual".
        Arguments:
            LP {LinearProgramming} --
            A LinearProgramming class object containing information
            about the LP, as well as the tableau in canonical form,
            with an initial feasible base
            mode {string} -- A string defining the mode of execution,
            can be one of ["1", "2"]
        """
        if self.mode == "primal":
            self.__primal_simplex(LP, mode)
        elif self.mode == "dual":
            self.__dual_simplex(LP, mode)
        else:
            print "ERROR: unrecognized simplex mode."
            sys.exit(-1)
