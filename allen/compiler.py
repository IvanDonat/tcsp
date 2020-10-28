#!/usr/bin/python3

from enum import Enum

INF = 1e9

relations = dict(
    'BEFORE': [],
    'MEETS': [],
    'OVERLAPS': [],
    'STARTS': [],
    'DURING': [],
    'ENDS': '',
    'EQUALS': [('-INF', '0'), ('0', 'INF')],
)

intervals = {}
constraints = {}

def parse_stdin():
    n = int(input())
    point_id = 0
    for _ in range(n):
        A, rel, B = input().split()
        
        if B > A:
            print('plz enter smaller lexicographic interval first, ')
        
        if rel not in relations:
            print(f'dont know relation: {rel}')

        if A not in intervals:
            intervals[A] = (point_id, point_id+1)
            point_id += 2
        if B not in intervals:
            intervals[A] = (point_id, point_id+1)
            point_id += 2
    
        reverse = B > A
        A, B = min(A, B), max(A, B)

        if A not in constraints:
            constraints[A] = {B: []}

        for c in relations[rel]:
            constraints[A][B].append(c if not reverse else c[::-1])
        

def print_result():
    print(intervals)
    print(constraints)
    # use len(relations.split)/2 to determine how many intervals

def main():
    parse_stdin()
    print_result()

if __name__ == '__main__':
    main()
