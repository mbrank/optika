#ifndef AARECTANGLE_H
#define AARECTANGLE_H

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <stdbool.h>
#include "ray.h"
#include "hittable.h"
#include "material.h"

typedef struct aarectangle_type{
  double x0;
  double x1;
  double y0;
  double y1;
  double z0;
  double z1;
  int xy;
  int xz;
  int yz;
  double k;
  material mat;
} aarectangle_t;

// prototypes for aarectangle functions

//bool hit_aarectangle(aarectangle_t *sphere,
//		     ray_t *r,
//		     double *t_min,
//		     double *t_max,
//		     hit_record *rec);
//
#endif
