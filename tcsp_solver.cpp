#include <vector>
#include <iostream>
#include <algorithm>

#include "graph.h"
#include "graphutil.h"
#include "tcsp.h"

TCSP load_tcsp_from_stdin() {
    TCSP csp;

    std::cin >> csp.num_of_nodes;
    std::cin >> csp.num_of_edges;
    csp.edges.resize(csp.num_of_edges);   
    csp.graph.num_of_nodes = csp.num_of_nodes;

    csp.graph.edges = discrete_graph(csp.num_of_nodes);

    for(int edge_id = 0; edge_id < csp.num_of_edges; edge_id++) {
        // read i, j, N, [a_i, b_i] for i 0 to N
        int i, j, N, a_i, b_i;
        std::cin >> i >> j >> N;

        csp.edges[edge_id] = {i, j, {}};

        while(N--) {
            std::cin >> a_i >> b_i;
            csp.edges[edge_id].intervals.push_back( {i, j, a_i, b_i} );
        }
    }

    return csp;
}

void bettertrack(
    TCSP &tcsp,
    std::vector<Interval> &intervals)
{
    
    for(Interval iv : intervals)
        std::cout << "[" << iv.l << ", " << iv.r << "] ";    
    std::cout << std::endl;

    if(intervals.size() == tcsp.edges.size()) {
        Graph d_graph = generate_d_graph(tcsp.graph);
        //M = d_graph_union(M, d_graph);
        if(!has_d_graph_negative_cycle(d_graph)) {
            std::cout << "POG" << std::endl;
            print_earliest_possible_time(d_graph);
        }
        return;
    }

    int i = intervals.size();
    for(Interval iv : tcsp.edges[i].intervals) {
        intervals.push_back(iv);
        tcsp.graph.edges[iv.i][iv.j] = iv.r;
        tcsp.graph.edges[iv.j][iv.i] = -iv.l;
        
        Graph d_graph = generate_d_graph(tcsp.graph);
        if(!has_d_graph_negative_cycle(d_graph))
            bettertrack(tcsp, intervals);

        intervals.pop_back();
        tcsp.graph.edges[iv.i][iv.j] = INF;
        tcsp.graph.edges[iv.j][iv.i] = INF;
    }
}

int main() {
    TCSP meta = load_tcsp_from_stdin();
    std::vector<Interval> ivs;
    bettertrack(meta, ivs);
    std::cout << "finished" << std::endl;
    return 0;
}
