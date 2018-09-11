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

import sys
import copy
import random
from math import sin
from math import cos
from math import log
from math import sqrt
from chromo import Chromossome


class GeneticProgramming(object):
    """ Class containing the implementation of a Genetic Programming.
    """

    def __init__(self, nvariables, max_depth, pop_size, tour_size,
                 prob_cross, prob_mut, seed):
        # Set seed for reproducibility
        random.seed(seed)
        self.terminals = []
        self.binary = []
        self.unary = []
        self.constants = []
        self.max_depth = max_depth
        self.pop_size = pop_size
        self.nvariables = nvariables
        self.tour_size = tour_size
        self.prob_cross = prob_cross
        self.prob_mut = prob_mut
        self.MAX_CHROMO_SIZE = (2 ** (self.max_depth + 1) - 1)
        self.__initialize_sets()

    def __initialize_sets(self):
        for i in xrange(self.nvariables):
            self.terminals.append('X' + str(i))
        self.binary = ['+', '-', '*', '/', 'pow']
        self.unary = ['sin', 'cos', 'log', 'sqrt']
        self.constants = [float(i) / 10 for i in xrange(-50, 50)]

    def __get_terminal(self, index):
        """ Returns a terminal from the terminals list, extracted at the
        given index.

        Arguments:
            index {int} -- index for the terminals list.

        Returns:
            [string] -- terminal.
        """
        return self.terminals[index] if index < len(self.terminals) else \
            self.constants[index % len(self.constants)]

    def __get_function(self, index):
        """ Returns a function from the functions list, extracted at the
        given index.

        Arguments:
            index {int} -- index for the function list.

        Returns:
            [string] -- function.
        """
        func = self.binary + self.unary
        return func[index]

    def getRandomProbability(self):
        return random.random()

    def generate_random_expression(self, max_depth, method):
        """ Recursively generate a random expression, and return a Chromossome
        object containing it.

        Arguments:
            max_depth {int} -- indicates the maximum depth a tree can reach,
            decreases at each recursive call
            method {str} -- name of the method being used

        Returns:
            [Chromossome] -- Chromossome object describing the espression
        """
        # Generate an equal chance of choosing between (terminal & functions)
        # or a constant
        # chosen_set = random.randint(1, 2)
        arg1 = None
        arg2 = None
        index = random.randint(0, (len(self.terminals) + len(self.constants) +
                                   len(self.binary) + len(self.unary)) - 1)
        if max_depth == 0 or (method == 'grow' and
                                        index < (len(self.terminals) +
                                                 len(self.constants))):
            # When max_depth == 0, it means we're initializing the leaves
            # of the trees, so terminals (variables or constants)
            # have to be chosen.
            # Also, when the initialization method is grow, consider the
            # possibility of a function being chosen
            expr = self.__get_terminal(index % (len(self.terminals) +
                                                len(self.constants)))
        else:
            # If initialization method is 'full', choose only functions,
            # until max_depth of 0 is reached. When the method is set
            # to 'grow', this part will only be executed when the randomly
            # generated index is larger than the terminals set's length,
            # meaning a function has been chosen.
            expr = self.__get_function(index % (len(self.binary) +
                                                len(self.unary)))
            arg1 = self.generate_random_expression(max_depth - 1, method)
            if expr not in self.unary:
                arg2 = self.generate_random_expression(max_depth - 1,
                                                       method)

        return Chromossome(expr, arg1, arg2)

    def gen_population_ramped_half_half(self):
        """ Generate a population using the Ramped Hald and Half method.

        This function generates a population using the Ramped Half and Half
        method, that is, half of the population is generated using the 'grow'
        method, and the other half is generated using the 'full method'.

        Returns:
            [list(Chromossome)] -- list of Chromossome objects, representing a
            population.
        """
        population = []
        half = self.pop_size / 2
        for count in xrange(half):
            # Calculate the module of the counter so it generates an (almost)
            # equal number of elements at each depth
            population.append(self.generate_random_expression(
                count % self.max_depth, 'full'))
            population.append(self.generate_random_expression(
                count % self.max_depth, 'grow'))
        return population

    def chromossome_str(self, chromo):
        """ Format the chromossome's content into string

        This function formats the chromossome's content into a string by
        performing an InOrder traversal in the tree.

        Arguments:
            chromo {Chromossome} -- Chromossome object, represented as a binary
            tree.

        Returns:
            [str] -- returns a string containing a representation of the
            chromossome.
        """
        if chromo is not None:
            return '( ' + str(chromo) + self.chromossome_str(chromo.getLeft())\
                + ' ' + self.chromossome_str(chromo.getRight()) + ' )'
        else:
            return ""

    def eval_chromossome(self, chromo, x):
        """ Evaluate the chromossome given the input array x.

        Evaluate the given chromossome on the input array x. Returns the value
        obtained in the evaluation.

        Arguments:
            chromo {Chromossome} -- Chromossome object representing the
            function
            x {numpy.array(float)} -- array of input values

        Returns:
            [float] -- result of the evaluation
        """
        if str(chromo) in (self.binary + self.unary):
            # node is a function
            if str(chromo) == '+':
                return self.eval_chromossome(chromo.getLeft(), x) +\
                    self.eval_chromossome(chromo.getRight(), x)
            elif str(chromo) == '-':
                return self.eval_chromossome(chromo.getLeft(), x) -\
                    self.eval_chromossome(chromo.getRight(), x)
            elif str(chromo) == '*':
                return self.eval_chromossome(chromo.getLeft(), x) *\
                    self.eval_chromossome(chromo.getRight(), x)
            elif str(chromo) == '/':
                # Protected division: returns zero when dividing by zero.
                num = self.eval_chromossome(chromo.getLeft(), x)
                den = self.eval_chromossome(chromo.getRight(), x)
                return 0 if den == 0 else num / den
            elif str(chromo) == 'sin':
                return sin(self.eval_chromossome(chromo.getLeft(), x))
            elif str(chromo) == 'cos':
                return cos(self.eval_chromossome(chromo.getLeft(), x))
            elif str(chromo) == 'log':
                num = self.eval_chromossome(chromo.getLeft(), x)
                return log(num) if num > 0 else 0
            elif str(chromo) == 'pow':
                left = self.eval_chromossome(chromo.getLeft(), x)
                right = self.eval_chromossome(chromo.getRight(), x)
                return left ** right
            elif str(chromo) == 'sqrt':
                num = self.eval_chromossome(chromo.getLeft(), x)
                return sqrt(num) if num > 0 else 0
        elif str(chromo) in self.terminals:
            # node is a variable
            index = int(str(chromo)[1])
            return x[index]
        else:
            # node is a constant
            return float(str(chromo))

    def calculate_fitness(self, population, rw_input):
        """ Given a population and an input stream, calculate the fitness of
        the chromossomes in the population

        Arguments:
            population {list(Chromossome)} -- list of Chromossome objects,
            representing the population
            rw_input {numpy.array} -- input containing the values in which the
            chromossomes will be evaluated

        Returns:
            [list(float)] -- list of floating point numbers reporting the
            population's fitness
        """
        rows = len(rw_input)
        fitness = []
        for elem in population:
            # print self.chromossome_str(elem)
            sq_dif_sum = 0
            for row in rw_input:
                try:
                    result = self.eval_chromossome(elem, row)
                    # Square of difference between the result of the evaluation
                    # using the chromossome and the expected value on the input
                    sq_dif_sum += (result - row[-1]) ** 2
                except Exception:
                    sq_dif_sum = sys.maxint
            # Calculate error and append to list, the fitness
            # Penalize chromossomes that are larger than a full tree
            # with the maximum depth
            if self.get_chromossome_size(elem) > self.MAX_CHROMO_SIZE:
                el_fit = sys.maxint
            else:
                el_fit = sqrt(sq_dif_sum / rows)
            fitness.append(el_fit if el_fit < sys.maxint else sys.maxint)
        return fitness

    def tournament_selection(self, population, fitness):
        """ Realize a tournament selection among the population

        Realize a tournament selection among the population, returns the index
        of the chromossome who won the tournament.

        Arguments:
            population {list(Chromossome)} -- list of Chromossome objects
            representing the population

            fitness {list(int)} -- list of integers representing the chromos_
            some's fitness

        Returns:
            [int] -- index of the chromossome who won the tournament
        """

        chosen = []
        # Choose random chromossomes from population
        for i in xrange(self.tour_size):
            chosen.append(random.randint(0, (self.pop_size - 1)))
        best = 0
        fbest = float('inf')
        # Get best chromossome from chosen set
        for i in chosen:
            if fitness[i] <= fbest:
                best = i
                fbest = fitness[best]

        return best

    def crossover(self, parent1, parent2):
        """ Generate two children through the recombination of randomly
        selected parents' genes

        This function randomly selects two of the parents' genes (points in the
        parents' tree) and swaps them, generating two children through this
        operation.

        Arguments:
            parent1 {Chromossome} -- Chromossome object representing parent #1
            parent2 {Chromossome} -- Chromossome object representing parent #2

        Returns:
            (Chromossome,Chromossome) -- tuple of Chromossome representing the
            two children generated in the operation
        """
        # Select crossover point on parent 1
        size = self.get_chromossome_size(parent1)
        rand1 = random.randint(0, (size - 1))
        # Select crossover point on parent 2
        size = self.get_chromossome_size(parent2)
        rand2 = random.randint(0, (size - 1))

        # Make copy of parents
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)

        # Get points of trade
        point1 = self.search_node(child1, rand1)
        point2 = self.search_node(child2, rand2)

        if child1 == point1:
            child1 = point2
        else:
            self.substitute(child1, point1, point2)

        if child2 == point2:
            child2 = point1
        else:
            self.substitute(child2, point2, point1)

        return child1, child2

    def mutation(self, parent):
        """ Mutation: replace a subtree of a parent, with a randomly generated
        tree.
        Arguments:
            parent {Chromossome} -- Chromossome to be mutated
        Returns:
            chile {Chromossome} -- Mutated chromossome.
        """

        # Make copy of parent
        child = copy.deepcopy(parent)

        # Get mutation point
        size = self.get_chromossome_size(parent)
        rand = random.randint(0, (size - 1))
        point = self.search_node(child, rand)

        # Choose a random symbol from the set of terminals and functions
        # to replace the current one
        new_node = random.choice(self.terminals + self.binary + self.unary)
        if 'X' in new_node:
            # node is terminal
            point.setSymbol(new_node)
            point.setLeft(None)
            point.setRight(None)
        else:
            # node is function
            point.setSymbol(new_node)
            point.setLeft(self.generate_random_expression(
                random.randint(2, self.max_depth / 2), 'full'))
            if new_node not in self.unary:
                point.setRight(self.generate_random_expression(
                    random.randint(2, self.max_depth / 2), 'full'))

        return child

    def substitute(self, chromo, trading_point, new_node):
        """ Recursively replace a subtree in a chromossome.
        Arguments:
            chromo {Chromossome} -- chromosomme that will be modified
            trading_point {Chromossome} -- pointer to subtree that will
            be replaced
            new_node {Chromossome} -- new subtree
        """
        if chromo is not None:
            if chromo.getLeft() == trading_point:
                chromo.left = new_node
                return
            else:
                self.substitute(chromo.getLeft(), trading_point, new_node)

            if chromo.getRight() == trading_point:
                chromo.right = new_node
                return
            else:
                self.substitute(chromo.getRight(), trading_point, new_node)
        else:
            return

    def search_node(self, chromo, node):
        # Iterative function for inorder tree traversal
        # Set current to root of binary tree
        curr_gene = chromo
        s = []
        # initialize stack
        done = 0
        count = 0
        while not done:
            # Reach the left most Node of the current Node
            if curr_gene is not None:
                # Place pointer to a tree node on the stack
                # before traversing the node's left subtree
                s.append(curr_gene)
                curr_gene = curr_gene.getLeft()
            # BackTrack from the empty subtree and visit the Node
            # at the top of the stack; however, if the stack is
            # empty you are done
            else:
                if len(s) > 0:
                    curr_gene = s.pop()
                    if count == node:
                        done = 1
                        return curr_gene
                    # We have visited the node and its left
                    # subtree. Now, it's right subtree's turn
                    curr_gene = curr_gene.getRight()
                    count += 1
                else:
                    done = 1

    def get_chromossome_size(self, chromo):
        if chromo is None:
            return 0
        else:
            return self.get_chromossome_size(chromo.getLeft()) +\
                1 + self.get_chromossome_size(chromo.getRight())
