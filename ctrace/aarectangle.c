//#include "ray.h"
#include "aarectangle.h"
#include "hittable.h"

bool hit_aarectangle(aarectangle_t *rectangle,
		     ray_t *r,
		     double *t_min,
		     double *t_max,
		     hit_record *rec)
{
  if (rectangle->xy == 1) {
	// rectangle in xy plane
	
  // check if rectangle is hit
  double rectangle_k = rectangle->k;
  double r_origin_z = r->origin.z;
  double r_direction_z = r->direction.z;
  double t = (rectangle_k-r_origin_z)/r_direction_z;
  if (t < *t_min || t > *t_max) {
    return false;
  }
  double r_origin_x = r->origin.x;
  double r_direction_x = r->direction.x;
  double x = r_origin_x + t*r_direction_x;
  double r_origin_y = r->origin.y;
  double r_direction_y = r->direction.y;
  double y = r_origin_y + t*r_direction_y;
  
  if (x < rectangle->x0 || x > rectangle->x1 || y < rectangle->y0 || y > rectangle->y1) {
    return false;
  }
  rec->u = (x-rectangle->x0)/(rectangle->x1-rectangle->x0);
  rec->v = (y-rectangle->y0)/(rectangle->y1-rectangle->y0);
  rec->t = t;
  return true;
  }
  else if (rectangle->xz == 1) {
    // check if rectangle is hit
  double rectangle_k = rectangle->k;
  double r_origin_y = r->origin.y;
  double r_direction_y = r->direction.y;
  double t = (rectangle_k-r_origin_y)/r_direction_y;
  if (t < *t_min || t > *t_max) {
    return false;
  }
  double r_origin_x = r->origin.x;
  double r_direction_x = r->direction.x;
  double x = r_origin_x + t*r_direction_x;
  double r_origin_z = r->origin.z;
  double r_direction_z = r->direction.z;
  double z = r_origin_z + t*r_direction_z;  
  if (x < rectangle->x0 || x > rectangle->x1 || z < rectangle->z0 || z > rectangle->z1) {
    return false;
  }
  rec->u = (x-rectangle->x0)/(rectangle->x1-rectangle->x0);
  rec->v = (z-rectangle->z0)/(rectangle->z1-rectangle->z0);
  rec->t = t;
  }
  
}
