#!/usr/bin/python3

def verify_witness(X, T):
    """
    Verify an assignment T to problem instance X.
    Returns list of failed constraints.

    Arguments:
    X -- (list) assignment X, where X[i] is the value of X_i
    T -- the constraint problem
    """
    
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