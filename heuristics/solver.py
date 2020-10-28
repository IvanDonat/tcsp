#!/usr/bin/python3

from pprint import pprint

INF = 1e9

consistent_stps = 0
dead_ends = 0

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

def backtrack(all_constraints, unused_constraints_indices, graph):
    global consistent_stps, dead_ends

    if not unused_constraints_indices:
        d_graph = generate_d_graph(graph)
        if consistent(d_graph):
            print_min_sol(d_graph)
            consistent_stps += 1
        else:
            dead_ends += 1
        return

    constr_id = pick_constraint(all_constraints, unused_constraints_indices)
    unused_constraints_indices.remove(constr_id)
    constr = all_constraints[constr_id]
    
    i, j = constr['i'], constr['j']
    for interval in constr['intervals']:
        graph[i][j] = interval[1]
        graph[j][i] = -interval[0]

        d_graph = generate_d_graph(graph)
        if consistent(d_graph):
            backtrack(all_constraints, unused_constraints_indices, graph)
        else:
            dead_ends += 1
    
        graph[i][j] = INF
        graph[j][i] = INF

    unused_constraints_indices.append(constr_id)


if __name__ == '__main__':
    num_nodes, num_constraints = map(int, input().split())
    constraints = []
    for c in range(num_constraints):
        i, j, n, *intervals = map(int, input().split())
        constraints.append({
                'i': i, 'j': j,
                'intervals': list(zip(intervals[::2], intervals[1::2])),
        })

    pprint(constraints)
    graph = discrete_graph(num_nodes)
    backtrack(constraints, [i for i in range(len(constraints))], graph)
    print(
        'dead ends:', dead_ends,
        '\nconsistent stps:', consistent_stps,
    )
