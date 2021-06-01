#ifndef HITTABLE_LIST_H
#define HITTABLE_LIST_H
//#include "hittable.h"
#include "sphere.h"
//#include <stdbool.h>
//#include "ray.h"

typedef struct hittable_list{
  // struct of objects in the scene
  sphere_t sphere[4];
} hittable_list;

int check_sphere_hit(sphere_t *sphere,
		      ray_t *r,
		      double *t_min,
		      double *t_max,
			  hit_record *rec, int sphere_id);

#endif
