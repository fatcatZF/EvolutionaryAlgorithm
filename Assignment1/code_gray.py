from IOHexperimenter import IOH_function, IOH_logger, IOHexperimenter
import numpy as np
import sys

dimension = 100
independent_runs = 20
budget = 50000


def bi2gray(a):
    return np.concatenate([np.array([a[0]]),np.bitwise_xor(a[0:-1],a[1:])])


def gray2bi(g):
    a = [int(g[0])]
 
    for i in range(1,len(g)):
       # print("ai-1: ", a[i-1])
       # print("type: ", type(a[i-1]))
       # print("gi: ",g[i])
       # print("type: ",type(g[i]))
        a.append(np.bitwise_xor(a[i-1],int(g[i])))
    return np.array(a)


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
def crossover_uniform(parent1, parent2, cross_points=0.5):
    """
    uniform crossover
    args:
        cross_points:probability of exchange of one bit
    """
    child1, child2 = np.array([]), np.array([])
    for i in range(len(parent1)):
        if np.random.random() <= cross_points:
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
    return np.array(couples)


def selection_t(problem, x, population , n=10):
    """
    tournament selection
    n: size of tournament
    """
    fit = np.array([problem(individual) for individual in x])
    
    x_prime = []
    for i in range(population):
        tournament = np.random.choice(np.arange(len(x)),n, replace=True)
         
        
        
        selected_index = np.argmax(fit[tournament])
        selected = x[tournament][selected_index]
      
        x_prime.append(selected)
    couples = [[x_prime[i-1],x_prime[i]] for i in range(1, len(x_prime),2)]
   
    return np.array(couples)
    


def studentname1_studentname2_GA(problem, pc_init=0.9, pc_end=0.6, pm_init=1/dimension, 
                                pm_end=0.1, selection=selection_t,
                                crossover = crossover_uniform, crossover_size = 5, 
                                adaptive_c=False,adaptive_m=True, population=100):
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

    x = np.array([np.random.rand(n) < 0.5 for i in range(population)]) 
    
    
    
    step_pc = (pc_end-pc_init)/budget if adaptive_c else 0
    step_pm = (pm_end-pm_init)/budget if adaptive_m else 0

    run_time = 0
    #Set up the ending criterion.
    crossover_times=0
    mutation_times = 0
    pc = pc_init
    pm = pm_init
    while not problem.final_target_hit and problem.evaluations < budget:
        
        pc = max(pc_end, pc_init+run_time*step_pc) if adaptive_c else pc_init
        pm = min(pm_end, pm_init+run_time*step_pm) if adaptive_m else pm_init 
       
        couples = selection(problem,x,population)
        couples = list(map(bi2gray, couples)) #convert to gray code
        
        x_prime_prime = []
        for couple in couples:
            if np.random.random() < pc: #Probability of crossover
                cross_points = np.sort(np.random.randint(99, size=crossover_size)) if crossover==crossover_n else 0.4
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
                    x_prime_prime[k][j] = -1*x_prime_prime[k][j] + 1 #Flip x_p_p[j]

        x_prime_prime_prime = x_prime_prime
       # print(type(x_prime_prime_prime))
       # print(x_prime_prime_prime)
       # print(x_prime_prime_prime.shape)
       # x_prime_prime_prime = list(map(gray2bi, x_prime_prime_prime))#convert to binary code
        #Evaluate the population
        x_prime_prime_prime = [gray2bi(individual) for individual in x_prime_prime_prime]
        fit = [problem(individual) for individual in x_prime_prime_prime]


        #Check if you reached the optimum
        fopt = np.max(fit)
        run_time+=1
        x = np.array(x_prime_prime_prime)        
    #Return the best fitting and the optimum
    return fopt




        
if __name__ == '__main__':
    om = IOH_function("OneMax", 100, 1)
    lo = IOH_function("LeadingOnes", 100, 1)
    args = dict()
    problem = om if input("please enter the object function(onemax or leadones): ").lower()=="onemax" else lo
    problem_name = "maxone" if problem==om else "leadingones"
    adaptive_c = True if input("use adaptive crossover: (True/False) ").lower()=="true" else False
    adaptive_m = True if input("use adaptive mutation: (True/False) ").lower()=="true" else False
   
    pc_init = float(input("Please input initial probability of crossover: "))
    pm_init = float(input("Please input initial probability of mutation: "))
    if adaptive_c:
      pc_end = float(input("Please input end probability of crossover: "))
      args['pc_end']=pc_end
    if adaptive_m:
      pm_end = float(input("Please input end probability of mutation: "))
      args['pm_end']=pm_end
      #args['pc_end']=pc_end
    population = int(input("Please input population: "))
    crossover = crossover_uniform if input("Please input crossover function(uniform/npoints): ").lower()=="uniform" else crossover_n
    if crossover==crossover_n:
       crossover_size = int(input("please input crossover size: "))
       args['crossover_size']=crossover_size
    
    #the args of GA function
    args.update({'adaptive_c':adaptive_c,'adaptive_m':adaptive_m, 'pc_init':pc_init, 'pm_init':pm_init, 'crossover':crossover, 'population':population})
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
    
