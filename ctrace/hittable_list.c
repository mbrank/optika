#include <stdbool.h>
#include "hittable_list.h"

int check_sphere_hit(sphere_t *sphere,
					 ray_t *r,
					 double *t_min,
					 double *t_max,
					 hit_record *rec,
					 int sphere_id)
{
  //hit_record temp_rec;
  //bool hit_anything = false;
  int hit_anything = -1;

  //double closest_so_far = temp_rec.t;
  double closest_so_far = *t_max;

  // check intersection
  PV_t oc = vec_diff(&(r->origin), &(sphere->center));
  oc.x = r->origin.x - sphere->center.x;
  oc.y = r->origin.y - sphere->center.y;
  oc.z = r->origin.z - sphere->center.z;
  double a = length_squared(&(r->direction));
  double half_b = vec_dot(&oc, &(r->direction));
  double c = length_squared(&oc) - sphere->radius*sphere->radius;
  double discriminant = half_b*half_b - a*c;
    if (discriminant < 0)
    {
      rec->object_was_hit = false;
      return -1; // nothing was hit
    }
  double sqrtd = sqrt(discriminant);
  auto double root = (-half_b - sqrtd) / a;
  if (root < *t_min || *t_max < root) {
    root = (-half_b + sqrtd) / a;
    if (root < *t_min || *t_max < root){
      rec->object_was_hit = false;
      return -1;
    }
  }
  
  rec->t = root;
  rec->p = at(r, rec->t);
  PV_t outward_normal;
  outward_normal.x = (rec->p.x - sphere->center.x) / sphere->radius;
  outward_normal.y = (rec->p.y - sphere->center.y) / sphere->radius;
  outward_normal.z = (rec->p.z - sphere->center.z) / sphere->radius;
  set_face_normal(rec, r, &outward_normal);
  rec->object_was_hit = true;
  return sphere_id;
}
//  bool hitted_sphere = hit_sphere(sphere,
//				  r,
//				  t_min,
//				  t_max,
//				  &temp_rec);
//  if (hitted_sphere)
//    {
//      //hit_anything = true;
//	  hit_anything = sphere_id;
//      closest_so_far = temp_rec.t;
//
//      rec->normal.x = temp_rec.normal.x;
//      rec->normal.y = temp_rec.normal.y;
//      rec->normal.z = temp_rec.normal.z;
//      rec->p.x = temp_rec.p.x;
//      rec->p.y = temp_rec.p.y;
//      rec->p.z = temp_rec.p.z;
//      rec->t = temp_rec.t;
//      rec->front_face = temp_rec.front_face;
//      rec->object_was_hit = temp_rec.object_was_hit;
//
//    }
//  return hit_anything;
//}
