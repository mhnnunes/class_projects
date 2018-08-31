

#ifndef IO_H
#define IO_H

#include <vector>

typedef std::pair<int, int> pii;
typedef std::pair<double, double> pdd;
typedef std::pair<double, pdd> ppdd;
typedef std::pair<int, pii> ppii;

void readInput(std::vector<pdd> &cities, bool &att);

#endif