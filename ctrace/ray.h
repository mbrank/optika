#ifndef RAY_H
#define RAY_H

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "vector.h"
//vector structure
typedef struct ray_type{
  PV_t origin, direction;
} ray_t;


// prototypes for ray functions

PV_t at(ray_t *, double t);

#endif
