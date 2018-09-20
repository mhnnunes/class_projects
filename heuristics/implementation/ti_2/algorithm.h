
// Copyright 2018 Matheus Nunes <mhnnunes@dcc.ufmg.br>
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

#ifndef ALGORITHM_H
#define ALGORITHM_H

#include <cmath>
#include <vector>
#include <utility>

typedef long double lld;
typedef std::pair<double, int> pdi; 
typedef std::pair<double, double> pdd;

double euc_2d(pdd city1, pdd city2);

double att_dist(pdd city1, pdd city2);

double calculateDist(pdd city1, pdd city2, bool att);

lld calculate_tour_cost(std::vector<int> &tour, std::vector<pdd> &cities,
                        bool att);

lld heuristics_ConstructiveTSP(std::vector<pdd> &cities,
						       std::vector<int> &tour,
						       int ncities, bool att);

lld heuristics_VND_TSP(std::vector<pdd> &cities,
					   std::vector<int> &tour,
					   int ncities, bool att);

void swap_2Opt(std::vector<int> &tour,
               int i, int k,
               bool att);

lld search_2Opt_TSP(std::vector<pdd> &cities,
					std::vector<int> &tour,
                    lld initialcost,
					int ncities, bool att);

lld search_3Opt_TSP(std::vector<pdd> &cities,
					std::vector<int> &tour,
					int ncities, bool att);

void swap_3Opt(std::vector<int> &tour, int i, int k, int ncities);

void print_tour(std::vector<int> tour, std::vector<pdd> &cities);

#endif