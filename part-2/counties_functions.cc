// Brenda Ly
// ly.brenda2013@csu.fullerton.edu
// @lybrenda
// Partners: @jeminsong

#include "counties_functions.h"

std::string AllCountiesString(
    const std::vector<std::vector<std::string>>& ca_counties) {
  std::string all_counties_string;
  for (const auto& count_vec : ca_counties.at(0)) {
    all_counties_string += (count_vec + ' ');
  }
  return all_counties_string;
}
int CountyIndex(const std::vector<std::vector<std::string>>& ca_counties,
                const std::string& match_county) {
  int index{-1};
  int count = 0;
  for (const auto& count_vec : ca_counties.at(0)) {
    if (count_vec == match_county) {
      index = count;
      break;
    }
    count++;
  }
  return index;
}
