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
  
  //printf("inside sphere: rec normal x: %f\n", rec->normal.x);
  //printf("inside sphere: rec normal y: %f\n", rec->normal.y);
  //printf("inside sphere: rec normal z: %f\n", rec->normal.z);
  //printf("inside sphere: rec t: %f\n", rec->t);

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
	  //printf("temp1: \n");
	  //printf("  x: %f\n", rec->normal.x);
	  //printf("  y: %f\n", rec->normal.y);
	  //printf("  z: %f\n", rec->normal.z);

	  
	  //rec->normal.x = (rec->p.x - sphere->center.x)/sphere->radius;
	  //rec->normal.y = (rec->p.y - sphere->center.y)/sphere->radius;
	  //rec->normal.z = (rec->p.z - sphere->center.z)/sphere->radius;
	  PV_t outward_normal;
	  outward_normal.x = (rec->p.x - sphere->center.x) / sphere->radius;
	  outward_normal.y = (rec->p.y - sphere->center.y) / sphere->radius;
	  outward_normal.z = (rec->p.z - sphere->center.z) / sphere->radius;
	  set_face_normal(rec, r, &outward_normal);

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
	  //printf("temp2:\n");
	  //printf("  x: %f\n", rec->normal.x);
	  //printf("  y: %f\n", rec->normal.y);
	  //printf("  z: %f\n", rec->normal.z);


	  //rec->normal.x = (rec->p.x - sphere->center.x)/sphere->radius;
	  //rec->normal.y = (rec->p.y - sphere->center.y)/sphere->radius;
	  //rec->normal.z = (rec->p.z - sphere->center.z)/sphere->radius;
	  PV_t outward_normal;
	  outward_normal.x = (rec->p.x - sphere->center.x) / sphere->radius;
	  outward_normal.y = (rec->p.y - sphere->center.y) / sphere->radius;
	  outward_normal.z = (rec->p.z - sphere->center.z) / sphere->radius;
	  set_face_normal(rec, r, &outward_normal);


	  // set uv coordinates
	  get_sphere_uv(&rec->normal, &rec->u, &rec->v);
	  rec->object_was_hit = true;
	  return sphere_id;
	}

  }
  //printf("sphere not hit\n");
  return -1;
}
int check_aarectangle_hit(aarectangle_t *rectangle,
						  ray_t *r,
						  double *t_min,
						  double *t_max,
						  hit_record *rec,
						  int aarectangle_id)
{
  //printf("aa rectangle id: %i\n", aarectangle_id);
  if (rectangle->xy == 1) {
	//printf("xy aa rectangle id: %i\n", aarectangle_id);
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
  //printf("aa rectangle id: %i\n", aarectangle_id);
  return aarectangle_id;
  }

  
  else if (rectangle->xz == 1) {
	//printf("xz aa rectangle id: %i\n", aarectangle_id);
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
  //printf("aa rectangle id: %i\n", aarectangle_id);
  return aarectangle_id;
  }

  
  else if (rectangle->yz == 1) {
	//printf("yz aa rectangle id: %i\n", aarectangle_id);
  double rectangle_k = rectangle->k;
  double r_origin_x = r->origin.x;
  double r_direction_x = r->direction.x;
  double t = (rectangle_k-r_origin_x)/r_direction_x;
  if (t < *t_min || t > *t_max) {
	//printf("12 rectangle id: %i\n", aarectangle_id);
    return -1;
  }
  double r_origin_y = r->origin.y;
  double r_direction_y = r->direction.y;
  double y = r_origin_y + t*r_direction_y;
  double r_origin_z = r->origin.z;
  double r_direction_z = r->direction.z;
  double z = r_origin_z + t*r_direction_z;  
  if (y < rectangle->y0 || y > rectangle->y1 || z < rectangle->z0 || z > rectangle->z1) {
	//printf("13 rectangle id: %i\n", aarectangle_id);
    return -1;
  }
  rec->u = (y-rectangle->y0)/(rectangle->y1-rectangle->y0);
  rec->v = (z-rectangle->z0)/(rectangle->z1-rectangle->z0);
  rec->t = t;
  PV_t outward_normal = {1, 0, 0};
  //printf("yz entering setfacenormal\n");
  set_face_normal(rec, r, &outward_normal);
  //rec->normal.x = 1;
  //rec->normal.y = 0;
  //rec->normal.z = 0;
  rec->p = at(r, rec->t);
  rec->object_was_hit = true;
  //printf("14 rectangle id: %i\n", aarectangle_id);
  //printf("aa rectangle id: %i\n", aarectangle_id);
  return aarectangle_id;
  }
}

int check_box_hit(box_t *box,
				  ray_t *r,
				  double *t_min,
				  double *t_max,
				  hit_record *rec,
				  int box_id){

  aarectangle_t rectangles[6];

  // XY
  aarectangle_t xy_rect1;
  xy_rect1.x0 = box->p0.x;
  xy_rect1.x1 = box->p1.x;
  xy_rect1.y0 = box->p0.y;
  xy_rect1.y1 = box->p1.y;
  xy_rect1.z1 = box->p1.z;
  rectangles[0] = xy_rect1;

  aarectangle_t xy_rect2;
  xy_rect2.x0 = box->p0.x;
  xy_rect2.x1 = box->p1.x;
  xy_rect2.y0 = box->p0.y;
  xy_rect2.y1 = box->p1.y;
  xy_rect2.z1 = box->p0.z;
  rectangles[1] = xy_rect2;

  // XZ
  aarectangle_t xz_rect1;
  xz_rect1.x0 = box->p0.x;
  xz_rect1.x1 = box->p1.x;
  xz_rect1.z0 = box->p0.z;
  xz_rect1.z1 = box->p1.z;
  xz_rect1.y0 = box->p0.y;
  rectangles[2] = xz_rect1;

  aarectangle_t xz_rect2;
  xz_rect2.x0 = box->p0.x;
  xz_rect2.x1 = box->p1.x;
  xz_rect2.z0 = box->p0.z;
  xz_rect2.z1 = box->p1.z;
  xz_rect2.y1 = box->p1.y;
  rectangles[3] = xz_rect2;

  // XZ
  aarectangle_t yz_rect1;
  yz_rect1.y0 = box->p0.y;
  yz_rect1.y1 = box->p1.y;
  yz_rect1.z0 = box->p0.z;
  yz_rect1.z1 = box->p1.z;
  yz_rect1.x0 = box->p0.x;
  rectangles[4] = yz_rect1;

  aarectangle_t yz_rect2;
  yz_rect2.y0 = box->p0.y;
  yz_rect2.y1 = box->p1.y;
  yz_rect2.z0 = box->p0.z;
  yz_rect2.z1 = box->p1.z;
  yz_rect2.x1 = box->p1.x;
  rectangles[5] = yz_rect2;

  int rectangle_hit_init = -1;
  int rectangle_hit = -1;
  for (int i = 0; i < 6; ++i) {
    rectangle_hit = check_aarectangle_hit(&rectangles[i],
										  r, t_min,
										  t_max, rec, i);
	if (rectangle_hit > rectangle_hit_init

	 ) {
	  
	}
  }
  if (rectangle_hit > 0){
	return box_id;
  }
    return -1;
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
