#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <stdbool.h>
#include "hittable.h"

//inline hit_record set_face_normal(hit_record *h_r, ray_t *r, PV_t *outward_normal)
//{
//  h_r->front_face = vec_dot(&(r->direction), outward_normal) < 0;
//  h_r->normal = h_r->front_face ? *outward_normal : vec_scale(outward_normal, -1);
//  return *h_r;
//};

inline void set_face_normal(hit_record *rec, ray_t *r, PV_t *outward_normal)
{
  rec->front_face = vec_dot(&(r->direction), outward_normal) < 0;
  //printf("set face normal before->normal:\n %f,\n %f,\n %f\n",
  //	 rec->normal.x,
  //	 rec->normal.y,
  //	 rec->normal.z);
  rec->normal = rec->front_face ? *outward_normal : vec_scale(outward_normal, -1);
  //printf("set face normal after->normal\n: %f,\n %f,\n %f\n",
  //	 rec->normal.x,
  //	 rec->normal.y,
  //	 rec->normal.z);
  //return *rec;
};
