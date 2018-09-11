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


class Stats(object):

    def __init__(self):
        self.clean()

    def clean(self):
        self.generation = 0
        self.avg_fitness = 0.0
        self.best_fitness = 0.0
        self.worst_fitness = 0.0
        self.repeated_chromo = 0.0
        self.better_than_before = 0
        self.worse_than_before = 0

    def setGeneration(self, generation):
        self.generation = generation

    def setAVG(self, avg):
        self.avg_fitness = avg

    def setBest(self, best):
        self.best_fitness = best

    def setWorst(self, worst):
        self.worst_fitness = worst

    def setRepeated(self, repeated):
        self.repeated_chromo = repeated

    def incBTB(self):
        self.better_than_before += 1

    def incWTB(self):
        self.worse_than_before += 1

    def summarize(self):
        return [self.generation, self.avg_fitness, self.best_fitness,
                self.worst_fitness, self.repeated_chromo,
                self.better_than_before, self.worse_than_before]
