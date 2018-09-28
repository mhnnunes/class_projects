#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
from sys import argv
from io_utils import read_input
from sklearn.metrics.pairwise import euclidean_distances


class KMeans(object):
    """ This class implements several heuristics for the
    Euclidean Minimum Sum-of-Squares Clustering (MSCC) problem.
    This problem is also commonly known as K-Means.
    """

    def __init__(self, data, seed, k):
        self.k = k
        # Data will be passed as a numpy 2D array
        self.data = data
        self.seed = seed
        # Set random generator seed
        np.random.seed(self.seed)

    def calculate_distance_between_pairs(self):
        self.distances = euclidean_distances(self.data)

    def lloyd_heuristic(self):
        # Define k initial clusters randomly
        #    - Choose k points randomly
        # Choose k indexes from data
        nrows = self.data.shape[0]
        # Initially all points are in cluster 0
        clusters = np.zeros(nrows)
        indexes = np.random.randint(nrows, size=self.k)
        centers = self.data[indexes, :]  # Grab k centers from data
        # Use centers to index distance matrix, then sort
        for point in range(nrows):
            distance_to_centers = self.distances[point, centers]
            # get smaller
            closest_center = np.argmin(distance_to_centers)
            clusters[point] = closest_center

        # Calculate centroid of each cluster
        for center in centers:
            # Get indexes of points assigned to center
            points_in_cluster = np.where(clusters == center)[0]
            # Calculate centroid
            centroid = np.mean(self.data[points_in_cluster, :])
            # Get closest point to centroid
            
        # Assign points to closest centroid
        # Repeat until convergence (points stop changing clusters)


if __name__ == "__main__":
    filename = argv[1]
    data = read_input(filename)
    # pre-process data
    # pre-processing breast cancer data
    data = data.drop('id', axis=1)
    data = data.drop('Unnamed: 32', axis=1)
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
    print(data)
    print(data.values)
    heu = KMeans(data.values, 1, 2)
    heu.lloyd_heuristic()
