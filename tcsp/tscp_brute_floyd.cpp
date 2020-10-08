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
    int i, j; // redundant but needed
    int l, r;
};

struct Edge {
    int i, j;
    std::vector<Interval> intervals;
};

struct CSP {
    int num_of_nodes, num_of_edges;
    std::vector<Edge> edges;
    Graph graph;
};


CSP load_tcsp_from_stdin() {
    CSP csp;

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

// mod:
// CSP contains Graph graph
// this graph will be constructed/deconstructed as intervals are selected
// and passed onto solver
void back(CSP &csp, std::vector<Interval> &intervals, std::vector<std::vector<Interval>> &C); // declare

void forward(CSP &csp, std::vector<Interval> &intervals, std::vector<std::vector<Interval>> &C) {
    std::cout << "forward: ";
    for(Interval i : intervals)
        std::cout << "[" << i.l << "," << i.r << "] ";
    std::cout << std::endl;

    if(intervals.size() == csp.edges.size()) {
        // TODO union solve with M
        Graph d_graph = generate_d_graph(csp.graph);
        if(!has_d_graph_negative_cycle(d_graph)) {
            std::cout << "POG" << std::endl;
            // this is where we union M
        }

        back(csp, intervals, C);
        return;
    }

    int i = intervals.size();
    
    if(i < C.size()) {    
        C[i] = {};
        for(Interval iv : csp.edges[i].intervals) {
            C[i].push_back(iv);

            /* for now we dont prune
            if(* TODO if not consistent / false) {
                C.pop_back();
            } */
        }
    }
  
    if(i < C.size() && !C[i].empty()) {
        Interval new_I = C[i][0];
        C[i].erase(C[i].begin());

        intervals.push_back(new_I);
        csp.graph.edges[new_I.i][new_I.j] = new_I.r;
        csp.graph.edges[new_I.j][new_I.i] = -new_I.l;

        forward(csp, intervals, C);
    }
    else
        back(csp, intervals, C); 
}

void back(CSP &csp, std::vector<Interval> &intervals, std::vector<std::vector<Interval>> &C) {
    std::cout << "back: ";
    for(Interval i : intervals)
        std::cout << "[" << i.l << "," << i.r << "] ";
    std::cout << std::endl;

    int i = intervals.size() - 1;
    if(i == 0) return;
    if(i < C.size() && C[i].size()) {
        Interval new_I = C[i][0];
        C[i].erase(C[i].begin());

        intervals[i] = new_I;

        csp.graph.edges[new_I.i][new_I.j] = new_I.r;
        csp.graph.edges[new_I.j][new_I.i] = -new_I.l;

        forward(csp, intervals, C);
    }
    else {
        Interval iv = intervals.back();
        intervals.pop_back();
        csp.graph.edges[iv.i][iv.j] = INF;
        csp.graph.edges[iv.j][iv.i] = INF;
        back(csp, intervals, C);
    }
}

int main() {
    CSP meta = load_tcsp_from_stdin();

    std::vector< std::vector<Interval> > C;
    C.resize(meta.num_of_edges);
    
    std::vector<Interval> ivs;
    forward(meta, ivs, C);
    

    std::cout << "cool" << std::endl;

    return 0;
}
