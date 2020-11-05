#!/usr/bin/python3
import argparse
from random import uniform, randint

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
        '-p', '--constraint-probability',
        type=float, default=0.2,
        help='probability to generate a constraint between a pair of distinct variables',
    )


    parser.add_argument(
        '-i', '--intervals',
        type=int, default=1,
        help='max number of intervals per constraint',
    )

    args = parser.parse_args()
    return args

def generate_problem(variables, constraint_probability, max_intervals):
    X = [0] + [randint(0, 100) for _ in range(variables-1)]    
    T_all = []

    visited_edges = set()    

    for j in range(1, variables):
        T_all.append({
            'i': 0,
            'j': j,
            'intervals': [(-100, 100)]
        })
    
    for i in range(1, variables):
        for j in range(i+1, variables):
            if uniform(0, 1) < constraint_probability:
                T = {}
                diff = X[j] - X[i]
                T['i'] = i
                T['j'] = j
                T['intervals'] = []
                for _ in range(randint(1, max_intervals)):
                    m = randint(-100, 90)
                    T['intervals'].append( (m, m+10) )
                T_all.append(T)

    for i in range(variables):
        for j in range(i+1, variables):
            # i like to link all of them to 0 at least because it makes things easier for no cost
            if i == 0 or uniform(0, 1) < constraint_probability:
                T = {}
                diff = X[j] - X[i]
                T['i'] = i
                T['j'] = j
                T['intervals'] = []
                for _ in range(randint(1, max_intervals)):
                    m = randint(-100, 90)
                    T['intervals'].append( (m, m+10) )
                T_all.append(T)

    print(variables, len(T_all))
    for constraint in range(len(T_all)):
        Tij = T_all[constraint]
        print(Tij['i'], Tij['j'], len(Tij['intervals']), end=' ')
        for a, b in Tij['intervals']:
            print(a, b, end=' ')
        print()


if __name__ == '__main__':
    args = parse_args()
    generate_problem(args.variables, args.constraint_probability, args.intervals)
