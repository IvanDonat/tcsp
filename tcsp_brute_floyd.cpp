// This program solves TSCP

#include <vector>
#include <iostream>
#include <algorithm>

#define INF 1e9

struct Graph {
    int num_of_nodes;
    std::vector< std::vector<int>> edges;
};

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

std::vector< std::vector<int> > inf_but_diagonal(int n) {
    std::vector< std::vector<int> > ret;
    ret.resize(n);
    for(int i = 0; i < n; i++)
        ret[i].resize(n, INF);
    for(int i = 0; i < n; i++)
        ret[i][i] = 0;
    return ret;
}

Graph create_graph_from_stdin() {
    Graph g;
    std::cin >> g.num_of_nodes;

    g.edges = inf_but_diagonal(g.num_of_nodes);
    
    // read edge inputs
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

Graph generate_d_graph(const Graph& graph) {
    int N = graph.num_of_nodes;
    std::vector< std::vector<int> > E = inf_but_diagonal(N);

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

bool has_d_graph_negative_cycle(const Graph& d_graph) {
    for(int i = 0; i < d_graph.num_of_nodes; i++) {
        if(d_graph.edges[i][i] < 0)
            return true;    
    }
    return false;
}

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


TCSP load_tcsp_from_stdin() {
    TCSP csp;

    std::cin >> csp.num_of_nodes;
    std::cin >> csp.num_of_edges;
    csp.edges.resize(csp.num_of_edges);   
    csp.graph.num_of_nodes = csp.num_of_nodes;

    csp.graph.edges = inf_but_diagonal(csp.num_of_nodes);

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
        else
            std::cout << "hehe caughtincosn"  << std::endl;

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