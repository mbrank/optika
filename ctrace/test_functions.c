#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <stdbool.h>
#include "vector.h"
#include <time.h>
int main(){
  PV_t rnd = random_in_unit_sphere();
  printf("rnd.x: %f\n", rnd.x);
  printf("rnd.y: %f\n", rnd.z);
  printf("rnd.z: %f\n", rnd.y);

  printf("----------------------\n");
  srand(time(0));
  for(int i = 0; i<5; i++)
        printf(" %d ", rand());
   
    return 0;
}
