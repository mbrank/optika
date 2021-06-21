#ifndef HITTABLE_H
#define HITTABLE_H

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "ray.h"
#include <stdbool.h>  

typedef struct hit_record_type{
  PV_t p; //point
  PV_t normal;
  double t;
  double u; // texture coordinate to get correct color
  double v; // texture coordinate to get correct color
  bool front_face;
  bool object_was_hit;
} hit_record;


//inline hit_record set_face_normal(hit_record *h_r,
//ray_t *r, PV_t *outward_normal);

void set_face_normal(hit_record *rec, ray_t *r, PV_t *outward_normal);

#endif
