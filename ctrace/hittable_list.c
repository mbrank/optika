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
  //int hit_anything = -1;

  //double closest_so_far = temp_rec.t;
  //double closest_so_far = *t_max;

  // check intersection

  PV_t oc = vec_diff(&(r->origin), &(sphere->center));
  //oc.x = r->origin.x - sphere->center.x;
  //oc.y = r->origin.y - sphere->center.y;
  //oc.z = r->origin.z - sphere->center.z;
  double a = vec_dot(&r->direction, &r->direction);
  double b = vec_dot(&oc, &r->direction);
  double c = vec_dot(&oc, &oc) - sphere->radius*sphere->radius;
  double discriminant = b*b - a*c;
  //setbuf(stdout, NULL);
  if (discriminant > 0) {
    double temp = (-b - sqrt(discriminant)) / a;
	if (temp < *t_max && temp > *t_min) {
	  // update record state
	  rec->t = temp;
	  rec->p = at(r, rec->t);
	  rec->normal.x = (rec->p.x - sphere->center.x)/sphere->radius;
	  rec->normal.y = (rec->p.y - sphere->center.y)/sphere->radius;
	  rec->normal.z = (rec->p.z - sphere->center.z)/sphere->radius;
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
	  rec->object_was_hit = true;
	  return sphere_id;
	}

  }
  return -1;



}

  int check_aarectangle_hit(aarectangle_t *aarectangle,
							ray_t *r,
							double *t_min,
							double *t_max,
							hit_record *rec,
							int aarectangle_id)
  {
	//printf("checking rectangle\n");
	double t = (aarectangle->k-r->origin.z) / r->direction.z;
	//printf("aarectangle->k: %f, r origin z:%f\n" ,aarectangle->k, r->origin.z);
	//printf("rect->t: %f\n" , t);
	//printf("NO PASS: *t_min, *t_max, %f, %f\n", *t_min, *t_max);
    if (t < *t_min || t > *t_max)
	  {
	  //return false;
	  //printf("*t_min, *t_max, %f, %f\n", *t_min, *t_max);
	  return -1;
	  }

	//printf("Pass\n");
	double x = r->origin.x + t*r->direction.x;
    double y = r->origin.y + t*r->direction.y;

	//printf("C: x->%f\n", x);
	//printf("C: y->%f\n", y);
	//printf("Pass\n");
	//printf("C: aarectangle->x0->%f\n", aarectangle->x0);
	//printf("C: aarectangle->x1->%f\n", aarectangle->x1);
	
    if (x < aarectangle->x0 || x > aarectangle->x1 || y < aarectangle->y0 || y > aarectangle->y1)
	  {
	  // return false;
	  return -1;
	  }

	//printf("Hit\n");
	rec->u = (x-aarectangle->x0)/(aarectangle->x1-aarectangle->x0);
    rec->v = (y-aarectangle->y0)/(aarectangle->y1-aarectangle->y0);
    rec->t = t;
	PV_t outward_normal = {0,0,1};
    set_face_normal(rec, r, &outward_normal);
    rec->p = at(r, t);
	return aarectangle_id;
  }
