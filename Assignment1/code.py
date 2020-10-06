from IOHexperimenter import IOH_function, IOH_logger, IOHexperimenter
import numpy as np
import sys

dimension = 100
independent_runs = 20
budget = 50000



#n-point crossover(1-point crossover)
def crossover_n(parent1, parent2, cross_points):
    split_parent1 = np.split(parent1, cross_points)
    split_parent2 = np.split(parent2, cross_points)
    child1, child2 = np.array([]), np.array([])
    for i in range(len(split_parent1)):
        if i % 2 == 0:
            child1 = np.concatenate([child1 , split_parent1[i]])
            child2 = np.concatenate([child2 , split_parent2[i]])
        else:
            child1 = np.concatenate([child1 , split_parent2[i]])
            child2 = np.concatenate([child2 , split_parent1[i]]) 
    return child1, child2




#uniform crossover
def crossover_uniform(parent1, parent2, cross_points):
    child1, child2 = np.array([]), np.array([])
    for i in range(len(parent1)):
        if np.random.random() <= 0.5:
            child1 = np.append(child1 , parent1[i])
            child2 = np.append(child2 , parent2[i])
        else:
            child1 = np.append(child1 , parent2[i])
            child2 = np.append(child2 , parent1[i]) 
    return child1, child2



def selection_p(problem, x, population):
    """
    proportional mating selection
    """
    fit = np.array([problem(individual) for individual in x])
    fit_scaled = fit -np.min(fit)
    selection_probability = fit_scaled/np.sum(fit_scaled)
    x_prime_index = np.random.choice(range(len(x)),population, replace=True, p=selection_probability)
    x_prime = x[x_prime_index]
    couples = [[x_prime[i-1],x_prime[i]] for i in range(1, len(x_prime),2)]
    return couples


def selection_t(problem, x, population , n=10):
    """
    tournament selection
    n: size of tournament
    """
    x_prime = []
    for i in range(population):
        tournament = np.random.choice(np.arange(len(x)),n, replace=True)
        selected = max(x[tournament],key=problem)
        
        x_prime.append(selected)
    couples = [[x_prime[i-1],x_prime[i]] for i in range(1, len(x_prime),2)]
   
    return couples
    


def studentname1_studentname2_GA(problem, pc_init=0.9, pc_min=0.6, pm_init=1/dimension, 
                                pm_max=0.1, selection=selection_t,
                                crossover = crossover_uniform, crossover_size = 5, 
                                is_adaptive=True, population=100):
    """
    Implementation of Genetic Algorithm
     args:
        problem: object function
        is_adaptive: whether use adaptive method for pm and pc
        pc_init: initialized probability of crossover
        pm_init: initialized probability of mutation
        pc_min: if adaptive, the minimal pc
        pm_max: if adaptive, the maximal pm
        population: size of population
        crossover: the crossover function: n-points crossover or uniform crossover
        crossover_size: if use n-points crossover, the size of cross points

     return: the optimal fitness value
    """
    n = problem.number_of_variables #The number of element in each vector
    fopt = -sys.maxsize-1 #The initial optimum. #?

    #Initialize the parent population. 250 parents
    x = np.array([np.random.rand(n) < 0.5 for i in range(population)]) 
    
    
    if is_adaptive:
        step_pc = (pc_init-pc_min)/budget
        step_pm = (pm_max-pm_init)/budget

    run_time = 0
    #Set up the ending criterion.
    crossover_times=0
    mutation_times = 0
    pc = pc_init
    pm = pm_init
    while not problem.final_target_hit and problem.evaluations < budget:
        if is_adaptive:
            pc = max(pc_min, pc_init-run_time*step_pc)
            pm = min(pm_max, pm_init+run_time*step_pm)
       # fit = np.array([problem(individual) for individual in x])
       # fit_scaled = fit - np.min(fit)
        #Select the individuals to mate depending on their fitness
        #selection_probability = fit_scaled/np.sum(fit_scaled)
       # x_prime_index = np.random.choice(range(len(x)), len(x), replace = True, p = selection_probability)
        #The same parent can be choiced 
       # x_prime = x[x_prime_index]
        #Generate a population from the crossing over between selected individuals.
       # couples = [[x_prime_index[i-1],x_prime_index[i]] for i in range(1, len(x_prime_index),2)]
        couples = selection(problem,x,population)
        x_prime_prime = []
        for couple in couples:
            if np.random.random() < pc: #Probability of crossover
                cross_points = np.sort(np.random.randint(99, size=crossover_size))
                child1, child2 = crossover(couple[0], couple[1], cross_points)
                x_prime_prime.append(child1) 
                x_prime_prime.append(child2)
                crossover_times+=1
            
            else:
                x_prime_prime.append(couple[0]) 
                x_prime_prime.append(couple[1])
                
        x_prime_prime = np.array(x_prime_prime)
               
        
        
        #Produce a mutation on this population
        for k in range(len(x_prime_prime)):
            for j in range(n):
                if np.random.random() < pm:
                    mutation_times+=1
                    x_prime_prime[k][j] = -1*x_prime_prime[k][j] + 1 #Flip x_p_p[j]

        x_prime_prime_prime = x_prime_prime
        #Evaluate the population
        fit = [problem(individual) for individual in x_prime_prime_prime]


        #Check if you reached the optimum
        fopt = np.max(fit)
        run_time+=1
        x = x_prime_prime_prime        
    #Return the best fitting and the optimum
    return fopt




        
if __name__ == '__main__':
    om = IOH_function("OneMax", 100, 1)
    lo = IOH_function("LeadingOnes", 100, 1)
    args = dict()
    problem = om if input("please enter the object function(onemax or leadones): ").lower()=="onemax" else lo
    problem_name = "maxone" if problem==om else "leadingones"
    is_adaptive = True if input("use adaptive method: (True/False)").lower()=="true" else False
   
    pc_init = float(input("Please input initial probability of crossover: "))
    pm_init = float(input("Please input initial probability of mutation: "))
    if is_adaptive:
      pm_max = float(input("Please input maximal probability of mutation: "))
      pc_min = float(input("Please input minimal probability of crossover: "))
      args['pm_max']=pm_max
      args['pc_min']=pc_min
    population = int(input("Please input population: "))
    crossover = crossover_uniform if input("Please input crossover function(uniform/npoints): ").lower()=="uniform" else crossover_n
    if crossover==crossover_n:
       crossover_size = int(input("please input crossover size: "))
       args['crossover_size']=crossover_size
    
    #the args of GA function
    args.update({'is_adaptive':is_adaptive, 'pc_init':pc_init, 'pm_init':pm_init, 'crossover':crossover, 'population':population})
    print(args)
    logger = IOH_logger("./", "result", "studentname1_studentname2", "studentname1_studentname2")
    
    #om.add_logger(logger)
    problem.add_logger(logger)

    ## Testing the algorithm on OneMax with 20 independent runs.
    # print('F1 ' + om.IOHprofiler_get_problem_name() + '...')
    for i in range(independent_runs):
        #om.reset()
        problem.reset()
        #print(' ' + 'run {}/{}'.format(i + 1, independent_runs) + '...', end=' ')
        fopt = studentname1_studentname2_GA(problem, **args)
        num_evaluations = problem.evaluations
        print("score: ",fopt," number of evaluations: ",num_evaluations)

    problem.add_logger(logger)
    
