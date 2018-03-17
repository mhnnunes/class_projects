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
from simplex import Simplex
from ioutils import IOUtils


class LinearProgramming(object):
    """Stores a Linear Programming and perform operations in it.
    Variables:
        LP {numpy.ndarray} -- N-dimensional numpy aray containing the LP
        feasible {bool} -- boolean flag indicating if the LP is feasible or not
        tableau {numpy.ndarray} -- N-dimensional numpy array containing the
        tableau in which the Simplex method must be run
        result {string} -- One of ["optimal", "unlimited"]
    """

    def setLP(self, LP):
        """Sets the LP variable as the numpy.ndarray received as argument
        Arguments:
            LP {numpy.ndarray} -- Linear Programming supplied to the main
            program
        """
        self.LP = LP
        self.orig_rows, self.orig_columns = self.LP.shape

    def getLP(self):
        """Returns the LP stored
        Returns:
            numpy.ndarray -- Linear Programming as a numpy N-dimensional array
        """
        return self.LP

    def setFeasible(self, feasible):
        """Set the LP as feasible or not
        Arguments:
            feasible {bool} -- Flag indicating if the LP is feasible or not
        """
        self.feasible = feasible

    def isFeasible(self):
        """Gets information about the feasibility of the LP
        Returns:
            bool -- True if the LP is feasible, False otherwise
        """
        return self.feasible

    def getTableau(self):
        """Returns the tableau of the LP
        Returns:
            numpy.ndarray -- numpy N-dimensional array containing the tableau
            of the LP
        """
        return self.tableau

    def setResult(self, result):
        """Sets the result of the LP. If something nasty happens and the
        result is not as expected, exit the system
        Arguments:
            result {string} -- One of ["optimal", "unlimited"]
        """
        if result in ["optimal", "unlimited"]:
            self.result = result
        else:
            print "ERROR: Unrecognized LP result."
            sys.exit(-1)

    def makeExtendedCanonicalTableau(self):
        """Build the extended tableau for the LP, in canonical form, and sets
        the class variable tableau.
        """
        rows, columns = self.LP.shape
        # Separate LP's elements
        ct = self.LP[0, :columns - 1]
        # Multiply c by -1, in order to make tableau
        ct = list(map(lambda x: -x, ct))
        b = self.LP[:, columns - 1]
        A = self.LP[1:rows, 0:columns - 1]
        self.setFeasible(True)
        # Create identity matrix, that will be appended to the LP's tableau
        auxIdentity = np.identity(rows - 1)

        # Concatenate A matrix and auxiliary identity matrix
        AauxIdentity = np.concatenate((A, auxIdentity), axis=1)

        # Make a new C vector, containig zeros in the positions in which the
        # identity matrix will be appended
        newc = np.concatenate((np.array([ct]),
                               np.array([np.zeros(rows - 1)])), axis=1)

        # Join A and auxiliary Identity matrix with new C vector
        # NEW FORM:
        # |    c   |
        # | A auxId|
        CAauxId = np.concatenate((newc, AauxIdentity), axis=0)

        extIdentity = \
            np.concatenate((np.array(
                            [np.zeros(rows - 1)]),
                            auxIdentity),
                           axis=0)
        # Concatenate the elements that compose the auxiliar
        # LP's tableau:
        # |           c           |
        # | extId | A | auxId | B |
        auxLP = \
            np.concatenate((extIdentity,
                            np.concatenate((CAauxId,
                                            np.transpose([b])),
                                           axis=1)),
                           axis=1)

        self.tableau = auxLP

    def makeAuxCanonicalTableau(self):
        """Build the extended tableau for the auxiliary LP to the original LP
        provided, in canonical form, and sets the class variable tableau
        """
        rows, columns = self.LP.shape
        # Get each LP element
        ct = self.LP[0, :columns - 1]
        b = self.LP[:, columns - 1]
        A = self.LP[1:rows, 0:columns - 1]

        # Create identity matrix, that will be appended to the LP's tableau
        # This identity matrix represents the slack variables, added due to
        # the unequalities
        slackIdentity = np.identity(rows - 1)
        slackIdentity = np.concatenate((np.array([np.zeros(rows - 1)]),
                                       slackIdentity),
                                       axis=0)

        Aandzeros = np.concatenate((np.array([np.zeros(columns - 1)]), A),
                                   axis=0)
        OpAandZeros = np.concatenate((slackIdentity, Aandzeros), axis=1)

        Azerosslack = np.concatenate((OpAandZeros, slackIdentity), axis=1)

        # For each negative entry in vector b, multiply that row by -1
        for i in xrange(1, rows):
            if b[i] < 0:
                Azerosslack[i, :] *= -1
                b[i] *= -1

        # Create identity matrix, that will be appended to the LP's tableau
        auxIdentity = np.identity(rows - 1)
        ones = np.array([np.ones(rows - 1)])
        auxIdentity = np.concatenate((ones, auxIdentity), axis=0)

        # Concatenate everything to create helper tableau
        Aslackhelper = np.concatenate((Azerosslack, auxIdentity), axis=1)
        tableau = np.concatenate((Aslackhelper, np.transpose([b])), axis=1)

        rows, columns = tableau.shape

        # Make canonical form (zeros above the initial feasible base)
        for i in xrange(1, rows):
            tableau[0, :] -= tableau[i, :]

        self.tableau = tableau

    def makeTableauFromAux(self):
        """Build the extended tableau from the auxiliary's LP tableau,
        in canonical form, and set the class variable tableau.
        """
        rows, columns = self.tableau.shape
        # Sanity check
        if self.isFeasible() and self.tableau[0, columns - 1] == 0.0:
            opMatrix = self.tableau[:, 0:self.orig_rows - 1]
            origc = self.LP[0, :self.orig_columns - 1]

            # Ignoring aux part
            AandC = self.tableau[:, self.orig_rows - 1:self.orig_rows +
                                 self.orig_columns]
            # Get the indexes of the columns that are the new base
            r, c = AandC.shape
            base = {}
            for i in xrange(0, c):
                if AandC[0, i] == 0 and \
                   reduce(lambda x, y: x + y, AandC[:, i]) == 1:

                    for j in xrange(1, r):
                        if AandC[j, i] == 1:
                            base[i] = j

            # Add the original c vector to the matrix
            AandC[0, 0:self.orig_columns - 1] = origc * -1
            # Adjust the new matrix to contain zeros over the base
            # (Canonical form)
            for k, v in base.iteritems():
                AandC[0, :] -= AandC[v, :] * AandC[0, k]

            b = self.tableau[:, columns - 1]

            # Concatenate opMatrix and new A and C
            opAandC = np.concatenate((opMatrix, AandC), axis=1)
            # Concatenate with vector b
            self.tableau = np.concatenate((opAandC, np.transpose([b])), axis=1)
        else:
            print "ERROR: Something went wrong, building tableau from aux LP."
            sys.exit(-1)

    def checkFeasibility(self):
        """Check the feasibility of the LP provided, and
        sets the class variable 'feasible'
        """
        # Make tableau
        orig_rows, orig_columns = self.LP.shape

        b = self.LP[:, orig_columns - 1]
        negativeB = list(filter(lambda x: x < 0, b))

        if negativeB:
            self.makeAuxCanonicalTableau()
            rows, columns = self.tableau.shape
            s = Simplex()
            s.setMode("primal")
            s.run(self, mode="1")
            if self.tableau[0, columns - 1] < 0.0:
                # Objective value of auxiliary LP <0: Unfeasible LP!!
                self.setFeasible(False)
                return
            else:
                self.setFeasible(True)
                self.makeTableauFromAux()
                return
        else:
            self.setFeasible(True)

    def printResult(self):
        """Summarizes and prints the result of the LP
        """
        # Get shape of tableau
        # Rows, columns contain the value from extended tableau I | A | I | b
        rows, columns = self.tableau.shape
        # Local tableau ignoring the extended part
        tableau = self.tableau[:, self.orig_rows - 1:columns]
        # Update rows, columns variables to keep values from the current
        # local tableau
        rows, columns = tableau.shape
        slack = self.orig_columns - columns - 1
        io_handler = IOUtils()
        # io_handler.openOutputFile()
        if not self.isFeasible():
            certUnf = np.array(self.tableau[0, 0:self.orig_rows - 1])
            io_handler.writeOutput("PL inviável, aqui está um certificado: " +
                                   io_handler.formatOutputString(certUnf))
        elif self.result == "optimal":
            c = tableau[0, 0:slack]
            x = []
            for i in xrange(0, columns + slack):
                if c[i] > 0:
                    # sanity check, if c element was < 0 in here,
                    # there would be an error
                    x.append(0)
                else:
                    for j in xrange(1, rows):
                        # Transform zeros into ones on the column,
                        # everything else into zero
                        # Sum this up, should be equal to number of rows -1
                        # This 1 is the 1 found:> meaning the rest of the
                        # column is zero
                        sumones = reduce(lambda x, y: x + y,
                                         map(lambda x: 1 if x == 0 else 0,
                                             tableau[:, i]))
                        if tableau[j, i] == 1 and sumones == rows - 1:
                            x.append(tableau[j, columns - 1])

            certOpt = np.array(self.tableau[0, 0:self.orig_rows - 1])
            io_handler.writeOutput("Solução ótima x = " +
                                   io_handler.formatOutputString(np.array(x)) +
                                   " com valor objetivo " +
                                   str(tableau[0, columns - 1]) +
                                   " e solução dual y = " +
                                   io_handler.formatOutputString(certOpt))
            # print "optimal PL"
        elif self.result == "unlimited":
            # Split the tableau into a list of columns
            cols = np.hsplit(tableau, columns)
            # Get the columns in which the vector c contains a negative
            # element (problematic/negative column)
            negcol = [c for c in cols if c[0] < 0]
            # Get the ones positions in the columns in which the
            # vector c is equal to 0
            ones = [i for col in cols for i in xrange(0, rows)
                    if col[0] == 0 and col[i] == 1]
            cert = []
            # index for the "ones" list, which has to be indexed sequentially
            j = 0
            # flags the first negative column (problematic column)
            flag = False
            # Run through all the columns
            for i in xrange(0, columns - 1):
                # For the columns in the base (vector c == 0)
                if cols[i][0] == 0:
                    # Get the corresponding element in the negative column
                    item = np.ndarray.item(negcol[0][ones[j]])
                    if item < 0:
                        cert.append(float(item * -1))
                    else:  # Avoid the -0 case
                        cert.append(float(item))
                    j += 1  # count the columnss
                elif cols[i][0] < 0:
                    if not flag:
                        cert.append(1.0)  # Set one for the problematic column
                        flag = True
                    else:  # Set zero for the other elements
                        cert.append(0.0)
                else:
                    cert.append(0.0)

            cert = np.array(cert)
            io_handler.writeOutput("PL ilimitada, aqui está um certificado: " +
                                   io_handler.formatOutputString(cert))
        else:
            print "ERROR: printing LP result. Unrecognized LP result."
            sys.exit(-1)
