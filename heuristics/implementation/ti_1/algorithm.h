

#ifndef ALGORITHM_H
#define ALGORITHM_H

#include <set>
#include <cmath>
#include <bitset>
#include <vector>
#include <utility>
#include "graph.h"

typedef std::pair<double, double> pdd;

double heuristics_ConstructiveTSP(std::vector<pdd> &cities, bool att);
double euc_2d(pdd city1, pdd city2);
double att_dist(pdd city1, pdd city2);

#endif