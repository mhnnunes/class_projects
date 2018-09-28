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

    def __reassing_clusters(self, centers_indexes, npoints):
        # Initially all points are in cluster 0
        clusters = np.zeros(npoints)
        for point in range(npoints):
            # Get distances from point to the centers, in the order:
            # [dist_to_center_0, dist_to_center_1, ...]
            distance_to_centers = self.distances[point, centers_indexes]
            # Get index of smallest distance
            closest_center = np.argmin(distance_to_centers)
            # Assign the point to the cluster with center on smallest distance
            clusters[point] = centers_indexes[closest_center]
        return clusters

    def lloyd_heuristic(self, threshold=10):
        # If the 'distances' variable does not exist, make ir
        if not hasattr(self, 'distances'):
            self.calculate_distance_between_pairs()

        npoints = self.data.shape[0]
        # Initially all points are in cluster 0
        self.clusters = np.zeros(npoints)
        # Define k initial clusters randomly
        #    - Choose k points randomly
        # Choose k indexes from data
        centers_indexes = np.random.randint(npoints, size=self.k)
        # Use centers to index distance matrix, then sort
        self.clusters = self.__reassing_clusters(centers_indexes, npoints)

        # Number of points that changed cluster from one iteration to another
        changed_cluster_prev = 1
        changed_cluster_cur = 0
        # Mark the number of iterations in which the number of points that
        # have changed cluster is the same from the last iteration
        nochange = 0
        iteration = 1
        while nochange < threshold:
            print("Iteration:: ", iteration)
            new_centers_indexes = []
            changed_cluster_cur = 0
            for center in centers_indexes:
                # Get indexes of points assigned to center
                points_in_cluster = np.where(self.clusters == center)[0]
                # Calculate centroid
                centroid = np.mean(self.data[points_in_cluster, :], axis=0)
                # print(centroid)
                # Get closest point to centroid
                closest_point_index = \
                    np.argmin(euclidean_distances(X=heu.data,
                                                  Y=centroid.reshape(1, -1)))
                new_centers_indexes.append(closest_point_index)
            # end for loop
            centers_indexes = np.array(new_centers_indexes)
            # Reassign points to new clusters
            cur_clusters = self.__reassing_clusters(centers_indexes, npoints)
            # Count how many points changed clusters
            changed_cluster_cur = \
                np.count_nonzero(self.clusters - cur_clusters)
            # No change since last iteration
            if changed_cluster_cur == changed_cluster_prev:
                nochange += 1
            # Save current clusters
            self.clusters = cur_clusters
            # Save current number of points that changed cluster
            changed_cluster_prev = changed_cluster_cur
            iteration += 1
            print(changed_cluster_cur, ' points changes cluster')
        # Repeat until convergence (points stop changing clusters)
        return self.clusters


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
    heu = KMeans(data.values, 1, 5)
    c = heu.lloyd_heuristic()
    print(c)