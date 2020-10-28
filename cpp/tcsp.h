#ifndef TCSP_H
#define TCSP_H

#include <vector>

#include "graph.h"

struct Interval {
    int i, j; // i, j are the edges this interval is on
    int l, r; // l, r are the interval bounds
};

struct Edge {
    int i, j; // an edge consists of a set of intervals
    std::vector<Interval> intervals;
};

struct TCSP {
    int num_of_nodes, num_of_edges;
    std::vector<Edge> edges;
    Graph graph;
};

#endif
