#!/usr/bin/python3
import argparse
from random import randint

def parse_args():
    parser = argparse.ArgumentParser(
        description='Create randomised TCSP problems'
    )
    
    parser.add_argument(
        '-v', '--variables',
        type=int, default=5,
        help='number of temporal variables (including X_0=0)',
    )

    parser.add_argument(
        '-c', '--constraints',
        type=int, default=5,
        help='number of constraints globally',
    )


    parser.add_argument(
        '-i', '--intervals',
        type=int, default=1,
        help='number of intervals per constraint',
    )

    args = parser.parse_args()
    return args

def generate_problem(variables, constraints, intervals):
    X = [0] + [randint(0, 100) for _ in range(variables-1)]    
    T = []

    visited_edges = set()    

    for c in range(constraints):
        T.append({})

        i = randint(0, variables-1)
        j = randint(0, variables-1)
        while (i, j) in visited_edges or (j, i) in visited_edges:
            i = randint(0, variables-1)
            j = randint(0, variables-1)

        i, j = min(i, j), max(i, j)
        visited_edges.add( (i, j) )

        T[c]['i'] = i
        T[c]['j'] = j
        T[c]['intervals'] = []

        diff = X[j] - X[i]

        for _ in range(intervals):
            T[c]['intervals'].append(
                (randint(-100, diff), randint(diff, 200))
            )
    
    from pprint import pprint
    #pprint(X)
    #pprint(T)

    print(variables, constraints)
    for constraint in range(constraints):
        Tij = T[constraint]
        print(Tij['i'], Tij['j'], len(Tij['intervals']), end=' ')
        for a, b in Tij['intervals']:
            print(a, b, end=' ')
        print()


if __name__ == '__main__':
    args = parse_args()
    generate_problem(args.variables, args.constraints, args.intervals)
