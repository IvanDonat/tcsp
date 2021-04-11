#!/usr/bin/python3

from pprint import pprint
from verifier import verify_witness
from problem_generator import generate_problem

INF = 1e9

def discrete_graph(N):
    """
    Returns an N*N matrix with INF entries everywhere except 0 on the leading diagonal.
    """
    
    mat = [[INF for _ in range(N)] for _ in range(N)]
    for i in range(N):
        mat[i][i] = 0
    return mat

def generate_d_graph(graph):
    """
    Given a distance graph, generates the corresponding d-graph
    (see R. Dechter - Temporal Constraint Networks)
    """
    
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
    """
    Returns whether a d-graph has a consistent solution.
    (iff no entry on leading diagonal is negative)
    """
    
    for i in range(len(d_graph)):
        if d_graph[i][i] < 0: return False
    return True

def get_min_sol(d_graph):
    """
    Given a consistent d_graph, returns a particular valid assignment.
    Namely, the solution with minimal values.
    """
    
    return [-d_graph[i][0] for i in range(len(d_graph))]

def backtrack(constraints):
    """
    Perform a backtracking search in order to find a solution to a TCSP given by 'constraints'.
    Returns None or a particular valid assignment list.
    """
    
    i = 0
    selection = [None for _ in range(len(constraints))]
    latest = [-1 for _ in range(len(constraints))]
    
    while 0 <= i < len(constraints):
        select_value_gbj(constraints, i, selection, latest)
        print(i)
        if selection[i] is None:
            print('jumping', i, latest[i])
            i = latest[i]
        else:
            i = i + 1
            if i < len(constraints):
                selection[i] = None
                latest[i] = -1
    
    if i == -1:
        print('UNSAT')
        return None
    else:
        # turn selection into minimal working example, and return it
        graph = discrete_graph(max([max(t['i'], t['j']) for t in constraints]) + 1)
        for k, constr in enumerate(constraints):
            graph[constr['i']][constr['j']] = constr['intervals'][selection[k]][1]
            graph[constr['j']][constr['i']] = -constr['intervals'][selection[k]][0]
        d_graph = generate_d_graph(graph)
        return get_min_sol(d_graph)

def max_k_consistent(constraints, i, selection, latest):
    """
    Compute whether the assignment selection assigned only at a_j where j <= latest or i == j is consistent.
    """
    
    graph = discrete_graph(max([max(t['i'], t['j']) for t in constraints]) + 1)
    
    # x_i = a
    constr = constraints[i]
    graph[constr['i']][constr['j']] = constr['intervals'][selection[i]][1]
    graph[constr['j']][constr['i']] = -constr['intervals'][selection[i]][0]
    
    k = 0
    while k < i:
        latest[i] = max(latest[i], k)
        
        # a_k-tuple graph
        constr = constraints[k]
        graph[constr['i']][constr['j']] = constr['intervals'][selection[k]][1]
        graph[constr['j']][constr['i']] = -constr['intervals'][selection[k]][0]
        
        d_graph = generate_d_graph(graph)
        if not consistent(d_graph):
            return False
        else:
            k += 1
    
    return True
            

def select_value_gbj(constraints, i, selection, latest):
    """
    Make an interval selection at index i.
    Also updates the list latest to be used for backjumping.
    """
    
    intervals = constraints[i]['intervals']
    
    if selection[i] is None:
        selection[i] = -1
    
    while selection[i] + 1 < len(intervals):
        selection[i] += 1
        if max_k_consistent(constraints, i, selection, latest):
            return
    
    selection[i] = None
    
def solve_stp(graph):
    """
    Given adjacency matrix solve simple temporal problem.
    Returns (is consistent, particular solution).
    """
    
    d_graph = generate_d_graph(graph)
    return consistent(d_graph), get_min_sol(d_graph)

def solve(constraints):
    """
    Solve the general TCSP given by 'constraints'.
    Returns a valid assignment X or None.
    """
    
    from copy import deepcopy
    c2 = deepcopy(constraints)
    c2.sort(key=lambda l: len(l['intervals']))
    return backtrack(c2)
