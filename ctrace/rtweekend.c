#include <stdlib.h>
#include "hittable.h"
#include "rtweekend.h"

double random_double(){
  // returns a random double in [0, 1)
  return rand()/(RAND_MAX+1.0);
}

double random_double_min_max(double min, double max){
  // Returns a random real in [min,max).
  return min + (max-min)*random_double();
}

double clamp(double x, double min, double max){
  if (x < min) {
    return min;
  }
  if (x > max) {
    return max;
  }
  return x;
}
