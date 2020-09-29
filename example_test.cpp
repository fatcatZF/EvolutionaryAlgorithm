
#include <f_one_max.hpp>
#include <IOHprofiler_csv_logger.h>


std::vector<int> Initialization(int dimension) {
  std::vector<int> x;
  x.reserve(dimension);
  for (int i = 0; i != dimension; ++i){
      x.push_back(rand()% 2);
  }
  return x;
};

int mutation(std::vector<int> &x, double mutation_rate) {
  int result = 0;
  int n = x.size();
  for (int i = 0; i != n; ++i) {
    if (rand() / double(RAND_MAX) < mutation_rate) {
      x[i] = (x[i] + 1) % 2;
      result = 1;
    }
  }
  return result;
}

/// In this session, the algorithm will be tested on only one problem (OneMax).
/// Therefore we declare a OneMax class, and get the fitness by the statement
/// om.evaluate().
void _run_problem() {

  /// Allocate the problem to be tested.
  OneMax om;
  int dimension = 1000;
  om.IOHprofiler_set_number_of_variables(dimension);
  
  /// If no logger is added, there will be not any output files, but users
  /// can still get fitness values.

  /// # For the assignment:
  /// # Please name your algorithm as student_num1-student_num2.
  /// # You can keep it as the same for the practical assignment.
  IOHprofiler_csv_logger logger("./","test-folder","s123456-s234567","s123456-s234567");
  std::vector<int> time_points{1,2,5};
  logger.set_complete_flag(true);
  logger.set_interval(0);
  logger.set_time_points(time_points,10);
  logger.activate_logger();
  logger.track_problem(om);


  std::vector<int> x;
  std::vector<int> x_star;
  double y;
  double best_value;
  double mutation_rate = 1.0/dimension;

  x = Initialization(dimension);
  x_star = x;
  y = om.evaluate(x);
  logger.do_log(om.loggerInfo());
  best_value = y;

  while(!om.IOHprofiler_hit_optimal()) {
    x = x_star;
    if(mutation(x,mutation_rate)) {
      y = om.evaluate(x);
      logger.do_log(om.loggerInfo());
    }
    if(y > best_value) {
      best_value = y;
      x_star = x;
    }
  }
}

int main(){
  _run_problem();
  return 0;
}

