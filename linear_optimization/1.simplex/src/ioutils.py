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
import numpy as np


class IOUtils:
    """Class implementing IO functionalities
    Variables:
        out {file} -- Output file
    """

    class __IOUtils:
        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not IOUtils.instance:
            IOUtils.instance = IOUtils.__IOUtils()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def readInput(self, filename):
        # If filename is invalid, open will throw an error
        try:
            rw_input = []
            # Read lines
            for line in open(filename, 'r').readlines():
                # Remove \n in order to make things work in processinputstring
                rw_input.append(line.replace('\n', ''))
            return rw_input
        except IOError as e:
            print e
            sys.exit(-1)
        except Exception as e:
            print e
            sys.exit(-1)

    def writeOutput(self, line):
        """Write an output line to a previously opened output file.
        Arguments:
            line {string} -- A formatted line, which will be written to the
            output file.
        """
        try:
            with open("saida.txt", "a") as f:
                f.write(line)
        except IOError as e:
            print e
            sys.exit(-1)
        except Exception as e:
            print e
            sys.exit(-1)

    def formatOutputString(self, numbers):
        """Formats a line into the format expected in the output.
        Arguments:
            numbers {numbers list} -- a list of numbers which will be
            formatted for the output.
        Returns:
            string -- the final formatted string
        """
        arrstr = np.array_str(numbers, precision=5)
        sub1 = arrstr.replace("[ ", "{")
        sub2 = sub1.replace("]", "}")
        sub3 = re.sub(" +", ", ", sub2)
        return re.sub("{, +", "{", re.sub(", +}", "}", sub3))
