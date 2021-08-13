#ifndef HITTABLE_LIST_H
#define HITTABLE_LIST_H
//#include "hittable.h"
#include "sphere.h"
#include "aarectangle.h"
#include "box.h"
//#include <stdbool.h>
//#include "ray.h"

typedef struct hittable_list{
  // struct of objects in the scene
  sphere_t sphere[5];
  aarectangle_t aarectangle[18];
  box_t box[2];
} hittable_list;

int check_sphere_hit(sphere_t *sphere,
		     ray_t *r,
		     double *t_min,
		     double *t_max,
		     hit_record *rec, int sphere_id);

int check_aarectangle_hit(aarectangle_t *rectangle,
						  ray_t *r,
						  double *t_min,
						  double *t_max,
						  hit_record *rec,
						  int aarectangle_id);

int check_box_hit(box_t *box,
				  ray_t *r,
				  double *t_min,
				  double *t_max,
				  hit_record *rec,
				  int box_id);


#endif
