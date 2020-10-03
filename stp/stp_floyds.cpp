// This program utilises Floyd-Warshall's Algorithm to solve STP

#include <vector>
#include <map>

#include <iostream>

/*
struct Graph {
    int num_of_nodes;
    // edges : i -> (j -> a_ij)
    std::map<int, std::map<int, int> > edges;
};

void print_graph(const Graph& graph) {
    for(int i = 0; i < graph.num_of_nodes; i++) {
        std::cout << "node " << i << std::endl;
        std::map<int, int> edges_from_node = graph.edges.find(i)->second;
        for(auto edge : edges_from_node) {
            // edge-map of this node
            std::cout << edges_from_node.size() << std::endl;
        }
    }
}
*/

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

int main() {
    Graph g;
    
    std::cin >> g.num_of_nodes;

    // init edge matrix to zeros
    g.edges.resize(g.num_of_nodes);
    for(int i = 0; i < g.num_of_nodes; i++) {
        g.edges[i].resize(g.num_of_nodes, 0);
    }

    // read edge inputs
    int num_of_edges;
    std::cin >> num_of_edges;
    while(num_of_edges--) {
        int i, j, a_ij, b_ij;
        std::cin >> i >> j >> a_ij >> b_ij;
        
        g.edges[i][j] = a_ij;
        g.edges[j][i] = -b_ij;
    }


    print_graph(g);
    
    return 0;
}
