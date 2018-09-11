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


class Chromossome(object):
    """ Representation of a Chromossome

    This class defines the representation of a Chromossome as a binary Tree,
    as used in Genetic Programming.
    """

    def __init__(self, symbol, left=None, right=None):
        self.symbol = symbol
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setSymbol(self, symbol):
        self.symbol = symbol

    def setLeft(self, symbol):
        self.left = symbol

    def setRight(self, symbol):
        self.right = symbol

    def __str__(self):
        return str(self.symbol)
