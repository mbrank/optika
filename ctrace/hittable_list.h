#ifndef HITTABLE_LIST_H
#define HITTABLE_LIST_H
//#include "hittable.h"
#include "sphere.h"
#include "aarectangle.h"
//#include <stdbool.h>
//#include "ray.h"

typedef struct hittable_list{
  // struct of objects in the scene
  sphere_t sphere[1000];
  aarectangle_t aarectangle[1000];
} hittable_list;

int check_sphere_hit(sphere_t *sphere,
		     ray_t *r,
		     double *t_min,
		     double *t_max,
		     hit_record *rec, int sphere_id);

int check_aarectangle_hit(aarectangle_t *aarectangle,
					 ray_t *r,
					 double *t_min,
					 double *t_max,
					 hit_record *rec, int aa_rectangle_id);


#endif
