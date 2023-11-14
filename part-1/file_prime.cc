// Jemin Song
// jeminsong@csu.fullerton.edu
// @jeminsong
// Partners: @lybrenda

#include <cmath>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

bool IsPrime(const int& number) {
  bool is_prime = true;

  for (int i = 2; i <= sqrt(number); ++i) {
    if (number % i == 0) {
      is_prime = false;
      break;
    }
  }
  return is_prime;
}
int main(int argc, char* argv[]) {
  std::vector<std::string> args{argv, argv + argc};
  if (args.size() < 2) {
    std::cout << "Please provide a path to a file. Exiting.\n";
    return 1;
  }
  std::string input_file_name{args.at(1)};
  std::ifstream input_file_stream{input_file_name};
  if (!input_file_stream.is_open()) {
    std::cout << "Could not open the file " << input_file_name
              << ". Exiting.\n";
    return 1;
  }
  while (input_file_stream) {
    std::string some_string;
    input_file_stream >> some_string;
    if (!input_file_stream) {
      break;
    }
    int original_number = std::stoi(some_string);
    std::string reversed_string{some_string.rbegin(), some_string.rend()};
    int reversed_number = std::stoi(reversed_string);
    if (IsPrime(original_number) && IsPrime(reversed_number)) {
      std::cout << original_number << '\n';
    }
  }
  input_file_stream.close();
  return 0;
}
