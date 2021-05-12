//#include "ray.h"
#include "sphere.h"
#include "hittable.h"

bool hit_sphere(sphere_t *sphere,
		ray_t *r,
		double *t_min,
		double *t_max,
		hit_record *rec)
{
  //printf("test11, %f", *t_min);
  // check if sphere is hit
  PV_t oc = vec_diff(&(r->origin), &(sphere->center));
  oc.x = r->origin.x - sphere->center.x;
  oc.y = r->origin.y - sphere->center.y;
  oc.z = r->origin.z - sphere->center.z;
  double a = length_squared(&(r->direction));
  double half_b = vec_dot(&oc, &(r->direction));
  double c = length_squared(&oc) - sphere->radius*sphere->radius;
  double discriminant = half_b*half_b - a*c;
  //setbuf(stdout, NULL);
  //printf("test12");
  if (discriminant < 0)
    {
      //printf("\ntest12.112123\n");
      rec->object_was_hit = false;
      return false;
      //return *rec;
    
    }
  //printf("test12.4");
  double sqrtd = sqrt(discriminant);
  //printf("test12.7");
  // Find the nearest root that lies in the acceptable range.
  auto double root = (-half_b - sqrtd) / a;
  //printf("test13.1");
  //printf("pointer t first:");
  //printf("pointer t second:");
  //printf("pointer t: %f\n", *t_min);
  if (root < *t_min || *t_max < root) {
    root = (-half_b + sqrtd) / a;
    if (root < *t_min || *t_max < root){
      rec->object_was_hit = false;
      return false;
    }
  }
  //else
  //  {
  //    return (-half_b - sqrt(discriminant))/(2.0*a);
  //  }
  rec->t = root;
  rec->p = at(r, rec->t);
  //printf("test14");
  //rec->normal.x = (rec->p.x - sphere->center.x)/sphere->radius;
  //rec->normal.y = (rec->p.y - sphere->center.y)/sphere->radius;
  //rec->normal.z = (rec->p.z - sphere->center.z)/sphere->radius;
  PV_t outward_normal;
  outward_normal.x = (rec->p.x - sphere->center.x) / sphere->radius;
  outward_normal.y = (rec->p.y - sphere->center.y) / sphere->radius;
  outward_normal.z = (rec->p.z - sphere->center.z) / sphere->radius;
  set_face_normal(rec, r, &outward_normal);
  //printf("rec->normal.x: %f\n", rec->normal.x);
  rec->object_was_hit = true;
  return true;
}
