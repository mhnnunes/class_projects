#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def build_distance_matrix(points):
    rows, columns = points.shape
    # Initialize empty matrix containing the initial pheromone value in every
    # position
    edges = np.zeros((rows, rows))
    for row in range(rows):
        # Fill up matrix storing distances between all points
        for column in range(rows):
            edges[row][column] = np.linalg.norm(points[row] - points[column])
    return edges


class AntColony(object):

    def __init__(self, npoints, nmedians, nants, alpha, beta, ro):
        self.npoints = npoints
        self.nmedians = nmedians
        self.alpha = alpha
        self.beta = beta
        self.ro = ro
        self.NUMBER_OF_ANTS = \
            int(nants) if not nants == -1 else int(self.npoints -
                                                   self.nmedians)
        self.INITIAL_PHEROMONE = 0.5
        self.MIN_PHEROMONE = 0.001
        self.MAX_PHEROMONE = 0.999
        self.pheromone = np.ones(npoints, dtype=np.float32) * \
            self.INITIAL_PHEROMONE

    def init_solution(self):
        self.clients = np.array(list(range(self.npoints)))
        self.medians = np.empty(self.nmedians, dtype=np.int)
        self.assign_matrix = np.zeros((self.npoints, self.npoints))

    def gap(self, capacities, demands, distance_matrix):
        """ General assignment problem
        Assigns clients to medians until the capacity of the median is
        fullfiled.
        Arguments:
            capacities {numpy.ndarray} -- array containing node capacities
            demands {numpy.ndarray} -- array containing node demands
            distance_matrix {numpy.ndarray} -- matrix containing node distances
        """

        # Build ordered clients array
        # Get matrix containing (clients on rows) x (medians on columns)
        dists = distance_matrix[self.clients][:, self.medians]
        # np.amin gets the nearest median to each client (smallest element on
        # each row), then np.argsort sorts the array and returns sorted indexes
        cli_dists = np.argsort(np.amin(dists, axis=1))
        # ordered_clients then gets a list of clients, ordered by the ones clo-
        # sest to their respective median
        ordered_clients = self.clients[cli_dists]
        for client in ordered_clients:
            # Obtain ordered medians and indexes
            dists = distance_matrix[client][self.medians]
            sorted_indexes = np.argsort(dists)
            ordered_medians = self.medians[sorted_indexes]
            # Create a separate array for the capacities, for safety
            ordered_capacities = capacities[sorted_indexes]
            # For each median in ordered medians
            for median_index, median in enumerate(ordered_medians):
                if (ordered_capacities[median_index] - demands[client]) >= 0:
                    self.assign_matrix[client, median] = 1
                    ordered_capacities[median_index] -= demands[client]
                    break

    def transition(self, node, densities):
        # EXCLUDE ALREADY ALLOCATED MEDIANS
        self.clients = np.setdiff1d(np.array(range(self.npoints)),
                                    self.medians)
        # DEFINE PROBABILITY FOR EACH NODE
        probabilities = (self.pheromone[self.clients] ** self.alpha) * \
                        (densities[self.clients] ** self.beta)
        sum_probs = np.sum(probabilities)
        transition_probabilities = probabilities / sum_probs if sum_probs > 0 \
            else 0
        # RANDOMLY CHOOSE NODE BASED ON PROBABILITY
        self.medians[node] = \
            np.random.choice(self.clients, p=transition_probabilities)

    def build_solution(self, densities, capacities, demands, distance_matrix):
        self.init_solution()
        # CHOOSE P medians based on transition probability
        for median in range(self.nmedians):
            self.transition(median, densities)
        # Assign nodes to chosen median
        self.clients = np.setdiff1d(np.array(range(self.npoints)),
                                    self.medians)
        self.gap(capacities, demands, distance_matrix)

    def iterate(self, densities, capacities, demands, distance_matrix):
        Fbest = float('inf')
        Fworst = 0.0
        for ant in range(self.NUMBER_OF_ANTS):
            self.build_solution(densities, capacities, demands,
                                distance_matrix)
            result = self.eval(distance_matrix)
            if result < Fbest:
                Fbest = result
                best_solution = {}
                best_solution['value'] = result
                best_solution['clients'] = self.clients
                best_solution['medians'] = self.medians
                best_solution['assign_matrix'] = self.assign_matrix
            if result > Fworst:
                Fworst = result
                worst_solution = {}
                worst_solution['value'] = result
                worst_solution['clients'] = self.clients
                worst_solution['medians'] = self.medians
                worst_solution['assign_matrix'] = self.assign_matrix
        return Fbest, Fworst, best_solution, worst_solution

    def update_pheromone(self, local_best, global_best, local_worst):
        all_medians = np.unique(np.concatenate((local_best['medians'],
                                global_best['medians']), 0))
        delta = 1 - ((local_best['value'] - global_best['value']) /
                     (local_worst['value'] - local_best['value']))

        self.pheromone[all_medians] += self.ro * \
            (delta - self.pheromone[all_medians])
        self.pheromone = np.clip(self.pheromone, self.MIN_PHEROMONE,
                                 self.MAX_PHEROMONE)
        # Stagnation control
        s = np.sum(self.pheromone)
        stagnation = self.ro * self.MAX_PHEROMONE + \
            (self.npoints - self.nmedians) * self.MIN_PHEROMONE
        if round(s, 2) == round(stagnation, 2):
            self.pheromone.fill(self.INITIAL_PHEROMONE)

    def eval(self, distance_matrix):
        return np.sum(self.assign_matrix * distance_matrix)


class P_Medians(object):

    def __init__(self, npoints, nmedians):
        self.npoints = int(npoints)
        self.nmedians = int(nmedians)

    def allocate(self, median, ordered_nodes):
        all_nodes = 0
        sum_distance = 0
        capacity = self.capacities[median]
        for node in ordered_nodes:
            node_demand = self.demands[node]
            if node_demand < capacity:
                capacity -= node_demand
                all_nodes += 1
                sum_distance += self.distance_matrix[node][median]
        return all_nodes, sum_distance

    def get_points_density(self):
        densities = np.zeros(self.npoints)
        for node_index in range(self.npoints):
            ordered_nodes = np.argsort(self.distance_matrix[node_index, :])
            all_nodes, sum_distance = self.allocate(node_index, ordered_nodes)
            densities[node_index] = all_nodes / sum_distance
        return densities

    def optimize(self, seed, points, iterations, nants, alpha, beta, ro):
        np.random.seed(seed)
        self.capacities = points[:, 2]
        self.demands = points[:, 3]
        self.distance_matrix = build_distance_matrix(points[:, 0:2])
        self.densities = self.get_points_density()
        ant_colony = AntColony(self.npoints, self.nmedians, nants, alpha,
                               beta, ro)
        FGbest = float('inf')
        FGworst = 0.0
        Gbest = {}
        Gworst = {}
        for iteration in range(iterations):
            Fbest, Fworst, best, worst = \
                ant_colony.iterate(self.densities,
                                   self.capacities,
                                   self.demands,
                                   self.distance_matrix)
            if Fbest < FGbest:
                # If local best is better than global best, save local best as
                # new global best
                FGbest = Fbest
                Gbest = best
            if Fworst > FGworst:
                # If local worst is worse than global worst, save local worst
                # as new global worst
                FGworst = Fworst
                Gworst = worst
            print(str(iteration) + ',' + str(Fbest) + ',' + str(FGbest) + ',' +
                  str(Fworst) + ',' + str(FGworst))
            # UPDATE PHEROMONES!!
            ant_colony.update_pheromone(best, Gbest, worst)
