#!/usr/bin/python3

from pprint import pprint

INF = 1e9

def print_min_sol(d_graph):
    for i in range(len(d_graph)):
        print(-d_graph[i][0], end=' ')
    print()

def discrete_graph(N):
    mat = [[INF for _ in range(N)] for _ in range(N)]
    for i in range(N):
        mat[i][i] = 0
    return mat

def generate_d_graph(graph):
    N = len(graph)
    E = discrete_graph(N)
    
    for i in range(N):
        E[i][i] = 0 # redundant

    for i in range(N):
        for j in range(N):
            E[i][j] = graph[i][j]

    for k in range(N):
        for i in range(N):
            for j in range(N):
                E[i][j] = min(
                    E[i][j],
                    E[i][k] + E[k][j],
                )

    return E

def consistent(d_graph):
    for i in range(len(d_graph)):
        if d_graph[i][i] < 0: return False
    return True

def pick_constraint(all_constraints, unused_constraints_indices):
    least_intervals = unused_constraints_indices[0]
    num = len(all_constraints[least_intervals]['intervals'])
    for idx in unused_constraints_indices:
        if len(all_constraints[idx]['intervals']) < num:
            num = len(all_constraints[idx]['intervals'])
            least_intervals = idx
    
    # return first unused:
    #return list(unused_constraints_indices)[0]

    # return constraint with least intervals on it
    return least_intervals

def backtrack(all_constraints, available_constraints, graph, pick_constraint, stats=None):
    if stats == None:
        stats = {'consistent': 0, 'dead': 0, 'total': 0}
        
    if not available_constraints:
        stats['total'] += 1
        d_graph = generate_d_graph(graph)
        if consistent(d_graph):
            stats['consistent'] += 1
        else:
            stats['dead'] += 1
        return stats

    constr = pick_constraint(available_constraints)
    available_constraints.remove(constr)
    
    i, j = constr['i'], constr['j']
    for interval in constr['intervals']:
        stats['total'] += 1
        graph[i][j] = interval[1]
        graph[j][i] = -interval[0]

        d_graph = generate_d_graph(graph)
        if consistent(d_graph):
            backtrack(all_constraints, available_constraints, graph, pick_constraint, stats)
        else:
            stats['dead'] += 1
    
        graph[i][j] = INF
        graph[j][i] = INF

    available_constraints.append(constr)
    return stats


def solve(num_variables, constraints, pick_constraint=lambda x: x[0]):
    return backtrack(constraints, constraints, discrete_graph(num_variables), pick_constraint)
     
