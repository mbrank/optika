#ifndef SPHERE_H
#define SPHERE_H

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <stdbool.h>
#include "ray.h"
#include "hittable.h"
#include "material.h"

typedef struct sphere_type{
  PV_t center;
  double radius;
  material mat;
} sphere_t;

// prototypes for sphere functions
void get_sphere_uv(PV_t *p, double *u, double *v);
//bool hit_sphere(sphere_t *sphere,
//		ray_t *r,
//		double *t_min,
//		double *t_max,
//		hit_record *rec);

#endif
