from IOHexperimenter import IOH_function, IOH_logger, IOHexperimenter
import numpy as np
import sys

dimension = 100
independent_runs = 20
budget = 50000

## !! This is where your algorithm locates, please replace the function name by your names and remain arguments the same.
def studentname1_studentname2_GA(problem):
    mutate_rate = 0.5



    n = problem.number_of_variables
    
    fopt = -sys.maxsize-1 #?

    ## !! IOHprofiler_hit_optimal() returns True if the optimum has been found.
    ## !! IOHprofiler_get_evaluations() returns the number of function evaluations has been done on the problem. 
    while not problem.final_target_hit and problem.evaluations < budget:
       
        x = np.random.rand(n) < 0.5
        
        ## !! evaluate(x) returns the fitness of x on the problem, and the number of function evaluations plus one.
        ## !! do_log(problem.loggerInfo()) will output the evaluation info. Please make sure you call this function after every evaluate(x). 
        f = problem(x)

        if f >= fopt:
            x_prime = x
            fopt = f

    return x_prime, fopt

if __name__ == '__main__':

    ## Declariation of OneMax and LeadingOnes as Problem(1,dimension). 1 is the instance_id, which means no transformation on the problems.
    om = IOH_function("OneMax", 16, 1)
    om.f.IOHprofiler_set_problem_id(1)
    lo = IOH_function("LeadingOnes", 16, 1)
    lo.f.IOHprofiler_set_problem_id(2)
    
    ## Declariation of IOHprofiler_csv_logger.
    ## 'result' is the name of output folder.
    ## 'studentname1_studentname2' represents algorithm name and algorithm info, which will be caption of the algorithm in IOHanalyzer.
    logger = IOH_logger("./", "result", "studentname1_studentname2", "studentname1_studentname2")
    
    om.add_logger(logger)

    ## Testing the algorithm on OneMax with 20 independent runs.
    # print('F1 OneMax ...')
    for i in range(independent_runs):
        om.reset()
        # print(' ' + 'run {}/{}'.format(i + 1, independent_runs) + '...', end=' ')
        xopt, fopt = studentname1_studentname2_GA(om)
        # print('xopt: {}, fopt: {:.2f}'.format(1 * xopt, fopt))

    lo.add_logger(logger)

    ## Testing the algorithm on OneMax with 20 independent runs.
    # print('F2 LeadingOnes ...')
    for i in range(independent_runs):
        lo.reset()
        # print(' ' + 'run {}/{}'.format(i + 1, independent_runs) + '...', end=' ')
        xopt, fopt = studentname1_studentname2_GA(lo)
        # print('xopt: {}, fopt: {:.2f}'.format(1 * xopt, fopt))
