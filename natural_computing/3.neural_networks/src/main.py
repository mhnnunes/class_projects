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
import numpy as np
from time import time
from os import getcwd
from nn import NeuralNet
from os.path import join
from os.path import split
from keras.utils import np_utils


def convert_categorical(vector):
    """ convert integers to dummy variables (i.e. one hot encoded)
    Arguments:
        vector {numpy.array} -- array of integers
    Returns:
        {numpy.array} -- array of arrays, containing an encoding
        of the integers
    """
    return np_utils.to_categorical(vector)


def kfold_cross_validation(X, K, randomise=False):
    """
    Generates K (training, validation) pairs from the items in X.

    Each pair is a partition of X, where validation is an iterable
    of length len(X)/K. So each training iterable is of length (K-1)*len(X)/K.

    If randomise is true, a copy of X is shuffled before partitioning,
    otherwise its order is preserved in training and validation.
    """
    if randomise:
        np.random.shuffle(X)
    for k in range(K):
        size = len(X)
        # Build a list of integers, with a step of K, from the start number
        validation_indexes = np.arange(start=k, stop=size, step=K)
        # Get training set index, from the difference between the whole
        # collection of indexes, and the validation indexes
        indexes = np.setdiff1d(np.arange(size), validation_indexes)
        yield indexes, validation_indexes


def to_numerical(var, dic):
    """ Convert classes string array to float array, using a dictionary
    containing the mapping.
    Arguments:
        var {[str]} -- array of (string) classes
        dic {dict} -- mapping from string to float
    Returns:
        classes {[float]} -- array of classes mapped to float
    """
    for loc, num in dic.items():
        var[np.where(var == loc)] = num
    return np.array(var, dtype=float)


def build_fullpath(filename):
    return join(split(getcwd())[0], 'datasets', filename)


def read_input(filename):
    fullpath = build_fullpath(filename)
    return np.loadtxt(fullpath, dtype=object, delimiter=';')


def main(filename, args):
    # fix random seed for reproducibility
    np.random.seed(args.seed)
    classes_dict = {
        'CYT': 0,
        'MIT': 1,
        'EXC': 2,
        'ME1': 3,
        'ME2': 4,
        'ME3': 5,
        'NUC': 6
    }
    matrix = read_input(filename)
    classes = matrix[:, -1]
    nclasses = len(classes_dict.keys())
    X = np.array(matrix[:, :-1], dtype=float)
    examples, attributes = X.shape
    # One hot encoding
    Y = convert_categorical(to_numerical(classes, classes_dict))
    net = NeuralNet(args.hidden, args.neurons, nclasses, attributes,
                    args.activation, args.epochs, args.batch,
                    args.learning_rate, args.decay, args.seed)
    # Separate train and validation data
    indexes_X = np.arange(examples)
    train_epochs = []
    valid_epochs = []
    times = []
    # 3-Fold Cross Validation
    for train, valid in kfold_cross_validation(indexes_X, 3, True):
        net.create_model()
        init = time()
        train_err, valid_err = net.fit_model(X, Y, train, valid)
        end = time()
        times.append(end - init)
        train_epochs.append(train_err)
        valid_epochs.append(valid_err)
    mean_time = np.mean(np.array(times), axis=0)
    mean_folds = np.mean(np.dstack((train_epochs[0],
                                    train_epochs[1],
                                    train_epochs[2])),
                         axis=2)
    mean_folds_test = np.mean(np.dstack((valid_epochs[0],
                                         valid_epochs[1],
                                         valid_epochs[2])),
                              axis=2)
    np.savetxt(join(args.outfile,
                    'train_' +
                    str(args.seed) + '.csv'), mean_folds,
               delimiter=',',
               fmt='%6f')
    with open(join(args.outfile, 'time_train_' +
                   str(args.seed) + '.csv'), 'w') as f:
        f.write('%6f' % mean_time)
    np.savetxt(join(args.outfile,
                    'test_' +
                    str(args.seed) + '.csv'), mean_folds_test,
               delimiter=',',
               fmt='%6f')


if __name__ == '__main__':
    parser = \
        argparse.ArgumentParser(description='Protein Location Classifier\
                                using Neural Networks')
    parser.add_argument('-n', '--neurons', action='store', type=int,
                        default=8, help='Number of neurons in each hidden \
                        layer')
    parser.add_argument('--hidden', action='store', type=int,
                        default=1, help='Number of hidden layers in the  \
                        network')
    parser.add_argument('-a', '--activation', action='store', type=str,
                        choices=[
                            'relu',
                            'sigmoid',
                            'softmax'
                        ],
                        default='relu', help='Activation function for the \
                        neurons')
    parser.add_argument('-e', '--epochs', action='store', type=int,
                        default=100, help='Number of epochs for \
                        the Network')
    parser.add_argument('-b', '--batch', action='store', type=int,
                        default=10, help='Batch size for the Training step')
    parser.add_argument('-lr', '--learning-rate', action='store', type=float,
                        default=0.01, help='Net\'s Learning rate')
    parser.add_argument('-d', '--decay', action='store', type=float,
                        default=0.00005, help='Decay factor for the learning \
                        rate')
    parser.add_argument('-s', '--seed', action='store', type=int,
                        default=1, help='Random seed')
    parser.add_argument('filename', action='store', type=str,
                        help='Name of input file')
    parser.add_argument('outfile', action='store', type=str,
                        help='Name of output file')
    args = parser.parse_args()
    filename = args.filename
    main(filename, args)
