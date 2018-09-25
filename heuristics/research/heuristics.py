#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# import pandas as pd
from sys import argv
from io import read_input


class KMeans(object):

    def __init__(self, data):
        self.data = data

    def lloyd_heuristic(self):
        # Define k initial clusters randomly
        # Calculate centroid of each cluster
        # Assign points to closest centroid
        # Repeat until convergence (points stop changing clusters)
        pass


if __name__ == "__main__":
    filename = argv[1]
    data = read_input(filename)
