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

from sets import Set
from statistics import Stats
from genetic import GeneticProgramming


class Model(object):

    def __init__(self, args):
        self.args = args

    def train(self, rw_input, io):
        max_depth = self.args.max_depth
        pop_size = self.args.pop_size
        prob_cross = self.args.prob_cross
        prob_mut = self.args.prob_mut
        tour_size = self.args.tour_size
        generations = self.args.gen
        elitism = self.args.elitism
        nvariables = len(rw_input[0]) - 1
        seed = self.args.seed
        stats = Stats()
        self.gp = GeneticProgramming(nvariables, max_depth, pop_size,
                                     tour_size, prob_cross, prob_mut, seed)
        self.population = self.gp.gen_population_ramped_half_half()
        self.fitness = self.gp.calculate_fitness(self.population, rw_input)

        for gen in xrange(generations):
            # Get Statistics of generation
            stats.setGeneration(gen)
            stats.setAVG(sum(self.fitness) / pop_size)
            stats.setBest(min(self.fitness))
            stats.setWorst(max(self.fitness))
            unique = Set(self.gp.chromossome_str(chromo) for chromo in
                         self.population)
            stats.setRepeated(pop_size - len(unique))
            self.best = self.population[self.fitness.index(min(self.fitness))]

            # Write stats from last generation to file
            io.writeOutput(stats.summarize())
            stats.clean()
            # Renew population
            new_population = []
            new_fitness = []

            # Elitism
            if elitism:
                new_population.append(self.best)
                new_fitness.append(min(self.fitness))

            # While population has not been entirely renewed
            while len(new_population) < pop_size:
                try:
                    # Get probability for each operator
                    prob = self.gp.getRandomProbability()

                    # Selection (choosing first parent)
                    parent1 = self.gp.tournament_selection(self.population,
                                                           self.fitness)
                    if prob <= prob_cross:
                        # Selection (choosing second parent for crossover)
                        parent2 = self.gp.tournament_selection(self.population,
                                                               self.fitness)
                        # Crossover
                        child1, child2 = self.gp.crossover(
                            self.population[parent1], self.population[parent2])

                        # Get stats about children
                        avg_parents_fitness = (self.fitness[parent1] +
                                               self.fitness[parent2]) / 2
                        childrens_fitness = self.gp.calculate_fitness(
                            [child1, child2], rw_input)
                        for fit in childrens_fitness:
                            if fit > avg_parents_fitness:
                                stats.incBTB()
                            elif fit < avg_parents_fitness:
                                stats.incWTB()

                        # Save children
                        new_population.append(child1)
                        new_fitness.append(childrens_fitness[0])
                        if len(new_population) < pop_size:
                            new_population.append(child2)
                            new_fitness.append(childrens_fitness[1])
                    elif prob <= (prob_cross + prob_mut):
                        # Mutation
                        child1 = self.gp.mutation(self.population[parent1])
                        # Calculate child's fitness
                        childrens_fitness = self.gp.calculate_fitness(
                            [child1], rw_input)
                        # Save child (and it's fitness)

                        new_fitness.append(childrens_fitness[0])
                        new_population.append(child1)
                except Exception:
                    # If anything goes wrong in the above code, just ignore
                    # the whole attempt and try again
                    pass
            # End of population renewal loop

            self.population = new_population
            self.fitness = new_fitness
            print 'best chromo', self.gp.chromossome_str(self.best)
        # End of evolutionary loop (generations)

    def test(self, test_data):
        fitness = self.gp.calculate_fitness([self.best], test_data)
        print 'TESTING ERROR>  ', fitness
