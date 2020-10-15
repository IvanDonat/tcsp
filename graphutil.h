#ifndef GRAPHUTIL_H
#define GRAPHUTIL_H

#include <iostream>

#include "graph.h"

#define INF 1e9


std::vector< std::vector<int> > discrete_graph(int n) {
    /*
        Return an NxN matrix containing all INF except the leading
        diagonal, which consists of zeros.
    */

    std::vector< std::vector<int> > ret;
    ret.resize(n);
    for(int i = 0; i < n; i++)
        ret[i].resize(n, INF);
    for(int i = 0; i < n; i++)
        ret[i][i] = 0;
    return ret;
}

Graph generate_d_graph(const Graph& graph) {
    /*
        Returns a d_graph given an STP constraint distance graph.
    */
    int N = graph.num_of_nodes;
    std::vector< std::vector<int> > E = discrete_graph(N);

    for(int i = 0; i < N; i++)
        E[i][i] = 0;
    
    for(int i = 0; i < N; i++)
        for(int j = 0; j < N; j++)
            E[i][j] = graph.edges[i][j];

    // tighten
    for(int k = 0; k < N; k++) {
    for(int i = 0; i < N; i++) {
    for(int j = 0; j < N; j++) {
        E[i][j] = std::min(
            E[i][j],
            E[i][k] + E[k][j]
        );
    }}}
     
    return {N, E};
}

void print_graph(const Graph& graph) {
    for(int i = 0; i < graph.num_of_nodes; i++) {
        for(int j = 0; j < graph.num_of_nodes; j++) {
            std::cout << graph.edges[i][j] << " ";
        }
        std::cout << std::endl;
    } 
}

void print_earliest_possible_time(const Graph &d_graph) {
    for(int i = 0; i < d_graph.num_of_nodes; i++) {
        std::cout << i << " " << -d_graph.edges[i][0] << std::endl;
    }
}

Graph create_graph_from_stdin() {
    Graph g;
    std::cin >> g.num_of_nodes;

    g.edges = discrete_graph(g.num_of_nodes);
    
    int num_of_edges;
    std::cin >> num_of_edges;
    while(num_of_edges--) {
        int i, j, a_ij, b_ij;
        std::cin >> i >> j >> a_ij >> b_ij;
        
        g.edges[i][j] = b_ij;
        g.edges[j][i] = -a_ij;
    }

    return g;
}

bool has_d_graph_negative_cycle(const Graph& d_graph) {
    /*
        Returns true <=> graph contains negative entries on the
        leading diagoonal.
    */
    for(int i = 0; i < d_graph.num_of_nodes; i++) {
        if(d_graph.edges[i][i] < 0)
            return true;    
    }
    return false;
}

#endif
