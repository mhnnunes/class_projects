#!/usr/bin/env python3
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

import argparse
from ioutils import IOUtils
from antsystem import P_Medians


def main(filename, args):
    io_utils = IOUtils()
    npoints, nmedians, points = io_utils.read_input(filename)
    pmedians = P_Medians(npoints, nmedians)
    pmedians.optimize(args.seed, points, args.iterations, args.ants,
                      args.alpha, args.beta, args.ro)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Capacitated p-Medians \
                                     Problem using Ant Colony Optimization')
    parser.add_argument('-a', '--alpha', action='store', type=float,
                        default=3.0, help='Alpha for the transition \
                        probability')
    parser.add_argument('-b', '--beta', action='store', type=float,
                        default=1.0, help='Beta for the transition \
                        probability')
    parser.add_argument('-p', '--ro', action='store', type=float,
                        default=0.5, help='Ro - pheromone decay rate')
    parser.add_argument('-i', '--iterations', action='store', type=int,
                        default=10, help='Maximum number of iterations for \
                        the Optimization process')
    parser.add_argument('-an', '--ants', action='store', type=int,
                        default=10, help='Number of ants in the Colony')
    parser.add_argument('-s', '--seed', action='store', type=int,
                        default=1, help='Random seed')
    parser.add_argument('filename', action='store', type=str,
                        help='Name of input file')
    args = parser.parse_args()
    filename = args.filename
    main(filename, args)
