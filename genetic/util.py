#!/usr/bin/python3
import argparse
from random import uniform, randint

def generate_problem(
    variables=10, 
    constraint_probability=0.25, 
    R=100,
    min_intervals=1, 
    max_intervals=5,
    scaling_factor=1,
    ):
    
    T_all = []
    
    for j in range(variables):
        T_all.append({
            'i': 0,
            'j': j,
            'intervals': [(-R, R)],
        })
        
    for i in range(1, variables):
        for j in range(i+1, variables):
            if uniform(0, 1) < constraint_probability:
                num_intervals = randint(min_intervals, max_intervals)
                points = [randint(-R, R) for _ in range(2 * num_intervals)]
                points.sort()
                
                intervals_temp = list(zip(points[::2], points[1::2]))
                
                # apply scaling factor:
                intervals = []
                for a, b in intervals_temp:
                    midpoint = int((a+b)/2)
                    l = int( midpoint - (midpoint-a)*scaling_factor )
                    r = int( midpoint + (b-midpoint)*scaling_factor )
                    intervals.append( (l, r) )
                    
                T_all.append({
                    'i': i,
                    'j': j,
                    'intervals': intervals,
                })

    return T_all

def verify_witness(X, T):
    failed_constraints = []
    for constraint in T:
        i = constraint['i']
        j = constraint['j']

        diff = X[j] - X[i]

        passed = False
        for interval in constraint['intervals']:
            if interval[0] <= diff <= interval[1]:
                passed = True
                break
        
        if not passed:
            failed_constraints += [constraint]

    return failed_constraints