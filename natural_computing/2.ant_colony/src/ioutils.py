#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv  # Reading .csv files
import numpy as np  # Matrix functions


class Singleton(type):
    """ This class implements the Singleton design pattern
    Variables:
        _instances {dict} -- contains the single instance of the class
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class IOUtils:
    """Class implementing IO functionalities.

    Vairables:
        out {file} -- Output file
    """
    __metaclass__ = Singleton

    def read_input(self, filename):
        # If filename is invalid, open will throw an error
        try:
            rw_input = []
            for row in open(filename, 'rb'):
                rw_input.append(list(map(float, row.split())))

            return rw_input[0][0], rw_input[0][1], \
                np.array(rw_input[1:]).astype(np.float32)
        except IOError as e:
            print(e)
            sys.exit(-1)
        except Exception as e:
            print(e)
            sys.exit(-1)

    def openOutFile(self, filename):
        try:
            self.output = csv.writer(open(filename, 'wb'))
        except IOError as e:
            print(e)
            sys.exit(-1)
        except Exception as e:
            print(e)
            sys.exit(-1)

    def writeOutput(self, line):
        """Write an output line to a previously opened output file.
        Arguments:
            line {string} -- A formatted line, which will be written
            to the output file.
        """
        try:
            self.output.writerow(line)
        except IOError as e:
            print(e)
            sys.exit(-1)
        except Exception as e:
            print(e)
            sys.exit(-1)
