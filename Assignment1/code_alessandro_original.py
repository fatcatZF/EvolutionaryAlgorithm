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




def studentname1_studentname2_GA(problem):
    n = problem.number_of_variables #The number of element in each vector
    fopt = -sys.maxsize-1 #The initial optimum.

    #Initialize the parent population.
    x = np.array([np.random.rand(n) < 0.5 for i in range(500)])
    

    #Evaluate parent population
    fit = np.array([problem(individual) for individual in x])
    fit_scaled = fit - np.min(fit)

    #Set up the ending criterion.
    while not problem.final_target_hit and problem.evaluations < budget:

        #Select the individuals to mate depending on their fitness
        selection_probability = fit_scaled/np.sum(fit_scaled)
        x_prime_index = np.random.choice(range(len(x)), len(x), replace = True, p = selection_probability)
        x_prime = x[x_prime_index]

        #Generate a population from the crossing over between selected individuals.
        couples = [[x_prime_index[i-1],x_prime_index[i]] for i in range(1, len(x_prime_index),2)]
    
        x_prime_prime = []
        for couple in couples:
            if np.random.random() < 0.6:
                cross_points = np.sort(np.random.randint(0,99, size=2))
                child1, child2 = crossover(x_prime[couple[0]], x_prime[couple[1]], cross_points)
                x_prime_prime.append(child1) 
                x_prime_prime.append(child2)
                
            
            else:
                x_prime_prime.append(x_prime[couple[0]]) 
                x_prime_prime.append(x_prime[couple[1]])
                
        

        #Produce a mutation on this population
        for k in range(len(x_prime_prime)):
            for j in range(n):
                if np.random.random() < 0.01:
                    x_prime_prime[k][j] = -1*x_prime_prime[k][j] + 1

        x_prime_prime_prime = x_prime_prime
        #Evaluate the population
        fit = [problem(individual) for individual in x_prime_prime_prime]


        #Check if you reached the optimum
        fopt = np.max(fit)
        
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

