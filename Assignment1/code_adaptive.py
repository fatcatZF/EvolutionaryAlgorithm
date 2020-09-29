from IOHexperimenter import IOH_function, IOH_logger, IOHexperimenter
import numpy as np
import sys

dimension = 100
independent_runs = 20
budget = 50000





#n-point crossover
#def crossover(parent1, parent2, cross_points):
#    split_parent1 = np.split(parent1, cross_points)
#    split_parent2 = np.split(parent2, cross_points)
#    child1, child2 = np.array([]), np.array([])
#    for i in range(len(split_parent1)):
#        if i % 2 == 0:
#            child1 = np.concatenate([child1 , split_parent1[i]])
#            child2 = np.concatenate([child2 , split_parent2[i]])
#        else:
#            child1 = np.concatenate([child1 , split_parent2[i]])
#            child2 = np.concatenate([child2 , split_parent1[i]]) 
#    return child1, child2





def crossover(parent1, parent2, cross_points):
    child1, child2 = np.array([]), np.array([])
    for i in range(len(parent1)):
        if np.random.random() <= 0.5:
            child1 = np.append(child1 , parent1[i])
            child2 = np.append(child2 , parent2[i])
        else:
            child1 = np.append(child1 , parent2[i])
            child2 = np.append(child2 , parent1[i]) 
    return child1, child2




def studentname1_studentname2_GA(problem, pc_init=0.9, pc_min=0.6, pm_init=1/dimension, pm_max=0.1):
    n = problem.number_of_variables #The number of element in each vector
    fopt = -sys.maxsize-1 #The initial optimum. #?

    #Initialize the parent population. 250 parents
    x = np.array([np.random.rand(n) < 0.5 for i in range(500)]) #population size
    #True/False?

    #Evaluate parent population
    fit = np.array([problem(individual) for individual in x])
    fit_scaled = fit - np.min(fit)

    step_pc = 2*(pc_init-pc_min)/budget
    step_pm = (pm_max-pm_init)/budget

    run_time = 0
    #Set up the ending criterion.
    crossover_times=0
    mutation_times = 0
    while not problem.final_target_hit and problem.evaluations < budget:
        pc = max(pc_min, pc_init-run_time*step_pc)
        pm = min(pm_max, pm_init+run_time*step_pm)
        #Select the individuals to mate depending on their fitness
        selection_probability = fit_scaled/np.sum(fit_scaled)
        x_prime_index = np.random.choice(range(len(x)), len(x), replace = True, p = selection_probability)
        #The same parent can be choiced 
        x_prime = x[x_prime_index]
        x_prime = np.random.permutation(x_prime)
        #Generate a population from the crossing over between selected individuals.
        couples = [[x_prime_index[i-1],x_prime_index[i]] for i in range(1, len(x_prime_index),2)]
    
        x_prime_prime = []
        for couple in couples:
            if np.random.random() < pc: #Probability of crossover
                cross_points = np.sort(np.random.randint(99, size=2))
                child1, child2 = crossover(x_prime[couple[0]], x_prime[couple[1]], cross_points)
                x_prime_prime.append(child1) 
                x_prime_prime.append(child2)
                crossover_times+=1
            
            else:
                x_prime_prime.append(x_prime[couple[0]]) 
                x_prime_prime.append(x_prime[couple[1]])
                
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

    logger = IOH_logger("./", "result", "studentname1_studentname2", "studentname1_studentname2")
    
    om.add_logger(logger)

    ## Testing the algorithm on OneMax with 20 independent runs.
    # print('F1 ' + om.IOHprofiler_get_problem_name() + '...')
    for i in range(independent_runs):
        om.reset()
        #print(' ' + 'run {}/{}'.format(i + 1, independent_runs) + '...', end=' ')
        fopt = studentname1_studentname2_GA(om)
        print(fopt)

    om.add_logger(logger)
    
