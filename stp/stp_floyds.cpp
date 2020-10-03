// This program utilises Floyd-Warshall's Algorithm to solve STP

#include <vector>
#include <iostream>
#include <algorithm>

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

void print_minimal_network(const Graph& d_graph) {
    for(int i = 0; i < d_graph.num_of_nodes; i++) {
        for(int j = 0; j < d_graph.num_of_nodes; j++) {
            std::cout << "[ " << -d_graph.edges[j][i] << " , " << d_graph.edges[i][j] << " ]   ";
        }
        std::cout << std::endl;
    }
}

std::vector< std::vector<int> > inf_but_diagonal(int n) {
    std::vector< std::vector<int> > ret;
    ret.resize(n);
    for(int i = 0; i < n; i++)
        ret[i].resize(n, 1e9);
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

int main() {
    Graph g = create_graph_from_stdin();

    std::cout << std::endl << "Adjacency Matrix" << std::endl;
    print_graph(g);
    
    std::cout << std::endl << "Distance Graph" << std::endl;
    Graph d_graph = generate_d_graph(g);
    print_graph(d_graph);

    if(has_d_graph_negative_cycle(d_graph)) {
        std::cout << "Problem is unsatisfiable" << std::endl;
        return 1;
    }

    std::cout << std::endl << "Minimal Network Representation" << std::endl;
    print_minimal_network(d_graph);
    return 0;
}
