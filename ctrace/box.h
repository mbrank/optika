#ifndef BOX_H
#define BOX_H

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <stdbool.h>
#include "ray.h"
#include "hittable.h"
#include "material.h"
#include "aarectangle.h"

typedef struct box_type{
  PV_t p0;
  PV_t p1;
  material mat;
} box_t;

// prototypes for aarectangle functions

//bool hit_aarectangle(aarectangle_t *sphere,
//		     ray_t *r,
//		     double *t_min,
//		     double *t_max,
//		     hit_record *rec);
//
#endif
