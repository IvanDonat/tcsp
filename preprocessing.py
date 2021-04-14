#!/usr/bin/python3

def intersect(I, J):
    """
    Returns the intersection of intervals given by lists I and J
    Remark: both lists have to be of the form of ordered disjoint intervals.
    """
    
    # TODO fix this merge, experimental
    return cleanup_intervals([
        [max(first[0], second[0]), min(first[1], second[1])] 
          for first in I for second in J  if max(first[0], second[0]) <= min(first[1], second[1])
    ])
    
def compose(I, J):
    """
    Returns the composition of interval lists I and J.
    Remark: both lists have to be of the form of ordered disjoint intervals.
    """

    return cleanup_intervals([
        (i[0] + j[0], i[1] + j[1])
        for i in I for j in J
    ])

def cleanup_intervals(I):
    """
    Returns an ordered disjoint list of intervals given a list of intervals.
    """
    
    ret = []
    
    for begin, end in sorted(I):
        if ret and ret[-1][1] >= begin - 1:
            ret[-1][1] = max(ret[-1][1], end)
        else:
            ret.append( [begin, end] )
    
    return [(a, b) for a, b in ret]

    
def PC_1(T, verbose=False):
    """
    Applies the PC-1 algorithm onto the constraints given by T.
    Returns 
    """
    
    # set up constraints into adj matrix form
    num_variables = max([max(t['i'], t['j']) for t in T]) + 1
    mat = [ [ None for i in range(num_variables) ] for j in range(num_variables) ]
    for constr in T:
        i, j, intervals = constr['i'], constr['j'], constr['intervals']
        
        mat[i][j] = intervals
        mat[j][i] = [(-b, -a) for a, b in reversed(intervals)]
        # ^ for reverse, we take each interval (a,b) and convert it into (-b,-a)
        #   note we want to also reverse the order of all intervals so that it is again increasing
        
    
    # actual PC-1 core algorithm:
    changed = True
    while changed:
        changed = False
        for k in range(num_variables):
            for i in range(num_variables):
                for j in range(num_variables):
                    # T_ij = T_ij + T_ik x T_kj

                    if mat[i][k] == None or mat[k][j] == None:
                        # if we cannot compose
                        continue
                    elif mat[i][j] == None:
                        # if unset it means no constraint, so only compose
                        mat[i][j] = compose(mat[i][k], mat[k][j])
                    else:
                        # intersect&compose
                        op = intersect(mat[i][j], compose(mat[i][k], mat[k][j]))
                        if mat[i][j] != op:
                            mat[i][j] = op
                            changed = True

                    if not mat[i][j]:
                        if verbose: print('Unsatisfiability deduced at the PC-1 level.')
                        return None
    
    # convert back to standard form used elsewhere:
    S = []
    for i in range(num_variables):
        for j in range(i, num_variables):
            if mat[i][j]:
                S += [{'i': i, 'j': j, 'intervals': mat[i][j]}]
    return S