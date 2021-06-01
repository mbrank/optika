//#include "ray.h"
#include "sphere.h"
#include "hittable.h"

bool hit_sphere(sphere_t *sphere,
		ray_t *r,
		double *t_min,
		double *t_max,
		hit_record *rec)
{

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
  if (discriminant < 0)
    {
      rec->object_was_hit = false;
      return false;
    }

  double sqrtd = sqrt(discriminant);

  // Find the nearest root that lies in the acceptable range.
  auto double root = (-half_b - sqrtd) / a;
  if (root < *t_min || *t_max < root) {
    root = (-half_b + sqrtd) / a;
    if (root < *t_min || *t_max < root){
      rec->object_was_hit = false;
      return false;
    }
  }

  // update record state
  rec->t = root;
  rec->p = at(r, rec->t);
  rec->normal.x = (rec->p.x - sphere->center.x)/sphere->radius;
  rec->normal.y = (rec->p.y - sphere->center.y)/sphere->radius;
  rec->normal.z = (rec->p.z - sphere->center.z)/sphere->radius;
  rec->object_was_hit = true;

  // calculate face normal
  PV_t outward_normal;
  outward_normal.x = (rec->p.x - sphere->center.x) / sphere->radius;
  outward_normal.y = (rec->p.y - sphere->center.y) / sphere->radius;
  outward_normal.z = (rec->p.z - sphere->center.z) / sphere->radius;
  set_face_normal(rec, r, &outward_normal);
  
  return true;
}
