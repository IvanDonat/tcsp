from random import choice, randint, uniform

from problem_generator import generate_problem
from verifier import verify_witness

from exact_solver import consistent
from exact_solver import discrete_graph
from exact_solver import generate_d_graph
from exact_solver import get_min_sol
from exact_solver import solve_stp

def random_gene(T):
    """
    Returns a random gene, ie. selection of intervals for the constraints.
    The gene is of the form [interval selection, distance graph, failed constraints]
    """
    
    num_variables = max([max(t['i'], t['j']) for t in T])
    interval_selection = [randint(0, len(constr['intervals'])-1) for constr in T]
    gene = [interval_selection, discrete_graph(num_variables+1), None]
    update_graph(gene, T)
    d_graph = generate_d_graph(gene[1]) # costly op.
    failed = verify_witness(get_min_sol(d_graph), T)
    gene[2] = failed
    
    return gene

def gene_to_witness(gene, T):
    """
    Given a gene, returns a particular solution.
    """
    
    update_graph(gene, T)
    d_graph = generate_d_graph(gene[1])
    return get_min_sol(d_graph)

def update_graph(gene, T):
    """
    Updates a gene's distance graph to apply all the gene interval selections.
    (Remark: this is used so that later it is possible to change interval selection in O(1) using update_graph_at_constraint)
    """
    
    interval_selection = gene[0]
    graph = gene[1]
    gene[2] = None # unset
    
    for i, constr in enumerate(T):
        interval_index = interval_selection[i]
        
        i, j = constr['i'], constr['j']
        interval = constr['intervals'][interval_index]
        
        graph[i][j] = interval[1]
        graph[j][i] = -interval[0]

def update_graph_at_constraint(gene, constraint_index, T):
    """
    Update a gene's distance graph to apply the interval selection at gene[constraint_index]
    """
    
    interval_selection = gene[0]
    graph = gene[1]
    gene[2] = None # unset
    
    interval_index = interval_selection[constraint_index]
    constr = T[constraint_index]
    
    i, j = constr['i'], constr['j']
    interval = constr['intervals'][interval_index]

    graph[i][j] = interval[1]
    graph[j][i] = -interval[0]
    
def walk_gene(gene, T):
    """
    Randomly updates an interval selection on a gene.
    Note: this does not reload the failed constraints.
    """
    
    # ignore all that have no choice
    # create list of plausible indices and filter it.
    candidate_indices = [j for j in range(len(T))]
    candidate_indices = list(filter(
        lambda x: len(T[x]['intervals']) > 1,
        candidate_indices
    ))
    
    idx = choice(candidate_indices)
    gene[0][idx] = randint(0, len(T[idx]['intervals'])-1)
    update_graph_at_constraint(gene, idx, T)
    
    
    
    
"""
----------------------------------------------
          Genetic particularities.
----------------------------------------------
"""
    
def evaluate(genes, T):
    """
    For each gene, compute the failed constraints.
    """
    
    for g in genes:
        d_graph = generate_d_graph(g[1]) # costly op.
        g[2] = verify_witness(get_min_sol(d_graph), T)
    return genes

def fitness(gene, T):
    """
    Returns the fitness of a gene.
    Remark: make sure it has been evaluated since last change.
    """
    
    return -len(gene[2])

def select(genes, retainment_ratio, T):
    """
    Keep the top retainment_ratio ratio most fit genes.
    """
    
    genes.sort(key=lambda g: -fitness(g, T))
    return genes[: int(len(genes)*retainment_ratio+1) ]

def crossover(genes, gene_pool_size, T):
    """
    Cross over the genes individually, creating new genes, until gene_pool_size is full.
    """
    
    num_variables = max([max(t['i'], t['j']) for t in T])
    while len(genes) < gene_pool_size:
        i = randint(0, len(genes)-1)
        j = randint(0, len(genes)-1)
        cross_index = randint(1, len(genes[0])-1)
        
        g = [
            genes[i][0][:cross_index] + genes[j][0][cross_index:],
            discrete_graph(num_variables+1),
            None
        ]
        
        genes.append(g)
        
    return genes

def mutate(T, genes, mutation_chance):
    """
    Randomly walk genes.
    """
    
    for g in genes:
        if uniform(0, 1) < mutation_chance:
            walk_gene(g, T)
            
    return genes

"""
----------------------------------------------
          Main Algorithms Start Here.
----------------------------------------------
"""
    
    
def meta_random(T, iterations=50):
    """
    Meta random algorithm.
    
    Arguments:
    T -- the constraints
    iterations -- max number of iterations
    """
    
    best_gene = None
    best_gene_failed = None
    
    for i in range(iterations):
        gene = random_gene(T)
        gene_failed = gene[2]
        
        if not best_gene or len(gene_failed) < len(best_gene_failed):
            best_gene = gene
            best_gene_failed = gene_failed
        
        if len(gene_failed) == 0:
            break
        
    print(f'num iterations: {i+1}')
    print('best gene:', best_gene)
    print('constraints failed:', len(best_gene_failed), 'out of:', len(T)) 
    print('failed constraints:', best_gene_failed)
    
    return best_gene
    
    
def meta_walk(T, max_iterations, max_flips):
    """
    Meta walk algorithm.
    
    Arguments:
    T -- the constraints
    max_iterations -- max number of iterations
    max_flips -- max number of flips
    """
        
    num_variables = max([max(t['i'], t['j']) for t in T])
    graph = discrete_graph(num_variables+1)
    
    best_gene = None
    best_gene_failed = None
    
    for i in range(max_iterations):
        gene = random_gene(T)
        update_graph(gene, T)
        
        for j in range(max_flips):
            # at each iteration we modify

            is_consistent, witness = solve_stp(gene[1])
            gene_failed = verify_witness(witness, T)
            gene[2] = gene_failed
            
            if not best_gene or len(gene_failed) < len(best_gene_failed):
                best_gene = gene
                best_gene_failed = gene_failed

            if is_consistent:
                break
                
            walk_gene(gene, T)
        
    print(f'num flips: {i+1}, num iterations: {j+1}')
    print('best gene:', best_gene)
    print('constraints failed:', len(best_gene_failed), 'out of:', len(T)) 
    print('failed constraints:', best_gene_failed)
    
    return best_gene

def meta_genetic(T,
            gene_pool_size,
            retainment_ratio,
            mutation_chance,
            max_iterations):
    
    """
    Meta genetic algorithm.
    
    Arguments:
    T -- the constraints
    gene_pool_size -- number of genes to keep at once
    retainment_ratio -- ratio of genes to keep from one iteration into the next
    mutation_chance -- chance of walking a gene at iteration step
    max_iterations -- max number of iterations to run
    """
    
    genes = [random_gene(T) for i in range(gene_pool_size)]
    
    for it in range(max_iterations):
        genes = evaluate(genes, T)
        genes = select(genes, retainment_ratio, T)
        genes = crossover(genes, gene_pool_size, T)
        genes = mutate(T, genes, mutation_chance)
    
    genes = evaluate(genes, T)
    best_gene = select(genes, 1, T)[0] # to sort genes such that first is best
    best_gene_failed = best_gene[2]
    print('best gene:', best_gene[0])
    print('constraints failed:', len(best_gene_failed), 'out of:', len(T)) 
    print('failed constraints:', best_gene_failed)
    
    return best_gene