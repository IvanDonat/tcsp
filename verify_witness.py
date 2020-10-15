#!/usr/bin/python3

def verify_witness(X, C):
    failed_constraints = []
    for constraint in C:
        i = constraint['i']
        j = constraint['j']

        diff = X[j] - X[i]

        passed = False
        for interval in constraint['intervals']:
            if interval[0] <= diff <= interval[1]:
                passed = True
                break
        
        if not passed:
            failed_constraints += [f"X_i={X[i]}, X_j={X[j]} on {constraint}"]

    return failed_constraints

if __name__ == '__main__':
    num_nodes, num_constraints = map(int, input().split())
    
    constraints = [] 
    for c in range(num_constraints):
        i, j, n, *intervals = map(int, input().split())
        constraints.append(
            {'i': i, 'j': j, 
             'intervals': list(zip(intervals[::2], intervals[1::2]))}
        )
    
    X = list(map(int, input().split()))

    failed_constraints = verify_witness(X, constraints)
    if not failed_constraints:
        print('PASS')
        exit(0)
    else:
        print('FAIL')
        for f in failed_constraints:
            print(f)
        exit(1)
