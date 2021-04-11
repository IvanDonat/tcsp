from random import randint, uniform

from problem_generator import generate_problem
from verifier import verify_witness


def random_gene(T, r):
    """ Returns a random assignment within the range [-r, r], and X_0 = 0. """
    num_variables = max([max(t['i'], t['j']) for t in T])
    return [0] + [randint(-r, r) for _ in range(num_variables)]

def sweep_line(intervals):
    """
    Given a list of intervals, returns a pair consisting of:
      1) the number of unsatisfied intervals
      2) the midpoint of a maximal number of unsatisfied overlapping intervals
    """
    
    L = []
    for l, r in intervals:
        L.append( (l, 1) )
        L.append( (r, -1) )
        
    L.sort(key=lambda a: 10*a[0] - a[1])
    
    c = 0
    top = -1
    top_index = 0
    
    for index, (point, increment) in enumerate(L):
        c += increment
        if c > top:
            top = c
            top_index = index
    
    sol = int( (L[top_index][0] + L[top_index+1][0])/2 )
    
    # returns the number of intervals unsatisfied and time point
    return len(intervals) - top, sol

def walk_gene(gene, T, pick_best_gene=True):
    """
    Walk a gene toward a more locally optimal assignment.
    
    Arguments:
    gene -- gene
    T -- constraint problem
    pick_best_gene -- whether to pick a random gene and assign it an optimal value, 
                      or attempt all genes and find the best improvement
    """
    
    num_variables = max([max(t['i'], t['j']) for t in T])
    
    constraints_per_variable = [list() for i in range(num_variables + 1)]
    failed_per_variable = [0 for i in range(num_variables + 1)]
    # at index i should contain availability intervals (given other variables are fixed.)
    # remark: existence of an interval is local with respect to one constraint
    # remark: so if intersection is empty, then there is no "safe" place to put this variable
    
    for c in T:
        i, j = c['i'], c['j']
        intervals = c['intervals']
        for l, r in intervals:
            # X_j - X_i in (l, r)
            # fix X_j to genes[j]
            # so genes[j] - X_i in (l, r)
            # then X_i in [X_j - r, X_j - l]
            constraints_per_variable[i].append( (gene[j] - r, gene[j] - l) )
            constraints_per_variable[j].append( (gene[i] + l, gene[i] + r) )
            
            if gene[j] - gene[i] < l or gene[j] - gene[i] > r:
                failed_per_variable[i] += 1
                failed_per_variable[j] += 1
            
    
    # for each constraint, sweep line, find best option
    # (later? we want to pick whatever REDUCES the unsatisfieds the most)
    # for now: pick a random variable and modify it according to sweep_line
    # if no later, then we can make the loop upstairs simpler (to only do stuff if "i" is mentioned)

    if pick_best_gene:
        reduction = -1
        best_gene = -1
        new_gene_base = 0
        for i in range(1, num_variables+1):
            faileds = failed_per_variable[i]
            new_faileds, new_gene_base = sweep_line(constraints_per_variable[i])
            
            if faileds - new_faileds >= reduction: #important to have \geq so it doesnt get stuck on 1 if 1 is best
                reduction = faileds - new_faileds
                best_gene = i
                best_gene_base = new_gene_base
        gene[best_gene] = best_gene_base
    else:
        i = randint(1, num_variables)
        gene[i] = sweep_line(constraints_per_variable[i])[1]
        
    return gene


"""
----------------------------------------------
Genetic Particularities
----------------------------------------------
"""

def fitness(gene, T):
    return -len(verify_witness(gene, T))

def select(genes, retainment_ratio, T):
    genes.sort(key=lambda g: -fitness(g, T))
    return genes[: int(len(genes)*retainment_ratio+1)]

def crossover(genes, gene_pool_size):
    while len(genes) < gene_pool_size:
        i = randint(0, len(genes)-1)
        j = randint(0, len(genes)-1)
        cross_index = randint(1, len(genes[0])-1)
        genes += [ genes[i][:cross_index] + genes[j][cross_index:] ]
        
    return genes

def mutate(T, genes, mutation_chance, r):
    for g in genes:
        if uniform(0, 1) < mutation_chance:
    # TODO:
    #        g[randint(0, len(g)-1)] = randint(-r, r)
    # or
            walk_gene(g, T)
            
    return genes
    

"""
----------------------------------------------
          Main Algorithms Start Here.
----------------------------------------------
"""
    

def direct_random(T, r, iterations):
    """
    Direct random algorithm.
    
    Arguments:
    T -- the constraint problem
    r -- range [-r, r] of assignments to consider
    iterations -- number of maximum random iterations
    """
    
    best_gene = None
    best_gene_failed = None
    
    for i in range(iterations):
        gene = random_gene(T, r)
        gene_failed = verify_witness(gene, T)
        if not best_gene or len(gene_failed) < len(best_gene_failed):
            best_gene = gene
            best_gene_failed = gene_failed
        
        if len(gene_failed) == 0:
            break
            
    print(f'num iterations: {i+1}')
    print('best gene:', best_gene)
    print('constraints failed:', len(best_gene_failed), 'out of:', len(T)) 
    print('failed constraints:', best_gene_failed)
    
    
def direct_walk(T, r, max_iterations, max_flips, pick_best_gene):
    """
    Direct walk-based algorithm.
    
    Arguments:
    T -- the constraint problem
    r -- range [-r, r] of assignments to consider
    max_iterations -- number of maximum random iterations
    max_flips -- maximum number of walks per iteration
    pick_best_gene -- whether to do extra work to find best gene to walk
    """
    
    best_gene = None
    best_gene_failed = None
    
    for i in range(max_iterations):
        gene = random_gene(T, r)
        
        for j in range(max_flips):
            gene_failed = verify_witness(gene, T)
            
            if not best_gene or len(gene_failed) < len(best_gene_failed):
                best_gene = gene
                best_gene_failed = gene_failed
            
            if len(gene_failed) == 0:
                break
                
            gene = walk_gene(gene, T, pick_best_gene)
                
        # necessary for double break after flips loop
        if len(gene_failed) == 0: break
    
    print(f'num iterations: {i+1}')
    print('best gene:', best_gene)
    print('constraints failed:', len(best_gene_failed), 'out of:', len(T)) 
    print('failed constraints:', best_gene_failed)
    
        
def direct_genetic(T, r,
            gene_pool_size,
            retainment_ratio,
            mutation_chance,
            max_iterations):
    
    """
    Direct genetic algorithm.
    
    Arguments:
    T -- the constraint problem
    r -- range [-r, r] of assignments to consider
    gene_pool_size -- number of genes kept in the pool
    retainment_ratio -- probability of keeping a gene from one iteration to the other
    mutation_chance -- how likely a gene is to be walked
    max_iterations -- maximum number of iterations before failure
    """
    
    genes = [random_gene(T, r) for i in range(gene_pool_size)]
    
    for it in range(max_iterations):
        genes = select(genes, retainment_ratio, T)
        genes = crossover(genes, gene_pool_size)
        genes = mutate(T, genes, mutation_chance, r)
    
    best_gene = select(genes, 1, T)[0] # to sort genes such that first is best
    best_gene_failed = verify_witness(best_gene, T)
    print('best gene:', best_gene)
    print('constraints failed:', len(best_gene_failed), 'out of:', len(T)) 
    print('failed constraints:', best_gene_failed)