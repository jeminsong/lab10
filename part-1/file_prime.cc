// TODO: add the required header

#include <cmath>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

// Test if a given paramater is a prime or not
// Return true if it is a prime, false otherwise
bool IsPrime(const int& number) {
  // TODO
  // Initialize a Boolean variable with true

  // TODO
  // Loop through the values from 2 to sqrt(number) and check
  // if one finds a divisor of "number"

  // TODO
  // Return the Boolean variable

  // remove the return statement below
  return false;
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
    // Break out of the loop if EOF by checking if the stream is empty
    if (!input_file_stream) {
      break;
    }
    // TODO
    // Convert the number to an integer and store that integer into a variable

    // TODO
    // Reverse the string variable (not the integer variable)
    // std::string variable{variable.rbegin(), variable.rend()};

    // TODO
    // Convert the string to an integer and store that integer into a variable

    // TODO
    // Check if both the integer corresponding to the string
    // and the integer corresponding to the reverse string are primes
    // then display then integer only (not its reverse)
  }
  input_file_stream.close();
  return 0;
}
