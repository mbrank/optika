#include <stdbool.h>
#include "hittable_list.h"
#include "sphere.h"

int check_sphere_hit(sphere_t *sphere,
		     ray_t *r,
		     double *t_min,
		     double *t_max,
		     hit_record *rec,
		     int sphere_id)
{
  // check intersection

  PV_t oc = vec_diff(&(r->origin), &(sphere->center));
  double a = vec_dot(&r->direction, &r->direction);
  double b = vec_dot(&oc, &r->direction);
  double c = vec_dot(&oc, &oc) - sphere->radius*sphere->radius;
  double discriminant = b*b - a*c;
  if (discriminant > 0) {
    double temp = (-b - sqrt(discriminant)) / a;
	if (temp < *t_max && temp > *t_min) {
	  // update record state
	  rec->t = temp;
	  rec->p = at(r, rec->t);
	  rec->normal.x = (rec->p.x - sphere->center.x)/sphere->radius;
	  rec->normal.y = (rec->p.y - sphere->center.y)/sphere->radius;
	  rec->normal.z = (rec->p.z - sphere->center.z)/sphere->radius;
	  // set uv coordinates
	  get_sphere_uv(&rec->normal, &rec->u, &rec->v);
	  rec->object_was_hit = true;
	  return sphere_id;
	}
	temp = (-b + sqrt(discriminant)) / a;
	if (temp < *t_min && temp > *t_max) {
	  // update record state
	  rec->t = temp;
	  rec->p = at(r, rec->t);
	  rec->normal.x = (rec->p.x - sphere->center.x)/sphere->radius;
	  rec->normal.y = (rec->p.y - sphere->center.y)/sphere->radius;
	  rec->normal.z = (rec->p.z - sphere->center.z)/sphere->radius;
	  // set uv coordinates
	  get_sphere_uv(&rec->normal, &rec->u, &rec->v);
	  rec->object_was_hit = true;
	  return sphere_id;
	}

  }
  return -1;
}
int check_aarectangle_hit(aarectangle_t *rectangle,
						  ray_t *r,
						  double *t_min,
						  double *t_max,
						  hit_record *rec,
						  int aarectangle_id)
{

  if (rectangle->xy == 1) {
	// rectangle in xy plane
  // check if rectangle is hit
  double rectangle_k = rectangle->k;
  double r_origin_z = r->origin.z;
  double r_direction_z = r->direction.z;
  double t = (rectangle_k-r_origin_z)/r_direction_z;
  if (t < *t_min || t > *t_max) {
	return -1;
  }
  double r_origin_x = r->origin.x;
  double r_direction_x = r->direction.x;
  double x = r_origin_x + t*r_direction_x;
  double r_origin_y = r->origin.y;
  double r_direction_y = r->direction.y;
  double y = r_origin_y + t*r_direction_y;
    
  if (x < rectangle->x0 || x > rectangle->x1 || y < rectangle->y0 || y > rectangle->y1) {
	return -1;
  }
  rec->u = (x-rectangle->x0)/(rectangle->x1-rectangle->x0);
  rec->v = (y-rectangle->y0)/(rectangle->y1-rectangle->y0);
  rec->t = t;
  PV_t outward_normal = {0, 0, 1};
  set_face_normal(rec, r, &outward_normal);
  rec->p = at(r, rec->t);
  rec->object_was_hit = true;
  return aarectangle_id;
  }

  
  else if (rectangle->xz == 1) {
  // check if rectangle is hit
  double rectangle_k = rectangle->k;
  double r_origin_y = r->origin.y;
  double r_direction_y = r->direction.y;
  double t = (rectangle_k-r_origin_y)/r_direction_y;
  if (t < *t_min || t > *t_max) {
    return -1;
  }
  double r_origin_x = r->origin.x;
  double r_direction_x = r->direction.x;
  double x = r_origin_x + t*r_direction_x;
  double r_origin_z = r->origin.z;
  double r_direction_z = r->direction.z;
  double z = r_origin_z + t*r_direction_z;  
  if (x < rectangle->x0 || x > rectangle->x1 || z < rectangle->z0 || z > rectangle->z1) {
    return -1;
  }
  rec->u = (x-rectangle->x0)/(rectangle->x1-rectangle->x0);
  rec->v = (z-rectangle->z0)/(rectangle->z1-rectangle->z0);
  rec->t = t;
  PV_t outward_normal = {0, 1, 0};
  set_face_normal(rec, r, &outward_normal);
  rec->p = at(r, rec->t);
  rec->object_was_hit = true;
  return aarectangle_id;
  }

  
  else if (rectangle->yz == 1) {
	double rectangle_k = rectangle->k;
  double r_origin_x = r->origin.x;
  double r_direction_x = r->direction.x;
  double t = (rectangle_k-r_origin_x)/r_direction_x;
  if (t < *t_min || t > *t_max) {
    return -1;
  }
  double r_origin_y = r->origin.y;
  double r_direction_y = r->direction.y;
  double y = r_origin_y + t*r_direction_y;
  double r_origin_z = r->origin.z;
  double r_direction_z = r->direction.z;
  double z = r_origin_z + t*r_direction_z;  
  if (y < rectangle->y0 || y > rectangle->y1 || z < rectangle->z0 || z > rectangle->z1) {
    return -1;
  }
  rec->u = (y-rectangle->y0)/(rectangle->y1-rectangle->y0);
  rec->v = (z-rectangle->z0)/(rectangle->z1-rectangle->z0);
  rec->t = t;
  PV_t outward_normal = {1, 0, 0};
  set_face_normal(rec, r, &outward_normal);
  rec->p = at(r, rec->t);
  rec->object_was_hit = true;
  return aarectangle_id;
  }
}




  /*
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
      return -1;  nothing was hit
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

  
  // update record state
  rec->t = root;
  rec->p = at(r, rec->t);
  //rec->normal.x = (rec->p.x - sphere->center.x)/sphere->radius;
  //rec->normal.y = (rec->p.y - sphere->center.y)/sphere->radius;
  //rec->normal.z = (rec->p.z - sphere->center.z)/sphere->radius;
  rec->object_was_hit = true;

  //printf("sphere->rec.p x, %f\n", rec->p.x);
  //printf("sphere->rec.p y, %f\n", rec->p.y);
  //printf("sphere->rec.p z, %f\n", rec->p.z);

  
  PV_t outward_normal;
  outward_normal.x = (rec->p.x - sphere->center.x) / sphere->radius;
  outward_normal.y = (rec->p.y - sphere->center.y) / sphere->radius;
  outward_normal.z = (rec->p.z - sphere->center.z) / sphere->radius;
  set_face_normal(rec, r, &outward_normal);
  rec->object_was_hit = true;
  return sphere_id;
  */

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
