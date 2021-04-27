//ray.c

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "ray.h"

PV_t at(ray_t *r, double t){
  PV_t scaled = vec_scale(&r->direction, t);
  return vec_sum(&r->origin, &scaled);
}
