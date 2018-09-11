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

import argparse
from model import Model
from IOUtils import IOUtils


def main(args):
    print 'entrou na main'
    io = IOUtils()
    io.openOutFile(args.out)
    training_data = io.readInput(args.train)
    testing_data = io.readInput(args.test)
    model = Model(args)
    model.train(training_data, io)
    model.test(testing_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Symbolic Regressor using \
                                     Genetic Programming')
    parser.add_argument('--train', action='store', type=str, required=True,
                        help='Name of training dataset')
    parser.add_argument('--test', action='store', type=str, required=True,
                        help='Name of testing dataset')
    parser.add_argument('-o', '--out', action='store', type=str, required=True,
                        help='Name of output file')
    parser.add_argument('-e', '--elitism', action='store_true', default=True,
                        help='Choose wether the algorithm uses elitism or not')
    parser.add_argument('--seed', action='store', type=float, default=1,
                        help='Seed for random number generator')
    parser.add_argument('--max-depth', action='store', type=int, default=7,
                        help='Select the maximum depth of the tree')
    parser.add_argument('--pop-size', action='store', type=int, default=50,
                        help='Select the size of the population')
    parser.add_argument('--prob-cross', action='store', type=float,
                        default=0.9,
                        help='Select the maximum depth of the tree')
    parser.add_argument('--prob-mut', action='store', type=float, default=0.05,
                        help='Select the maximum depth of the tree')
    parser.add_argument('--tour-size', action='store', type=int, default=2,
                        help='Select the maximum depth of the tree')
    parser.add_argument('--gen', action='store', type=int, default=50,
                        help='Select the number of generations the program \
                        must compute')
    args = parser.parse_args()
    main(args)
