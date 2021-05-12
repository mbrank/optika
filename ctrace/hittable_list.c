//#include "hittable.h"
//#include "sphere.h"
#include <stdbool.h>
//#include "ray.h"
#include "hittable_list.h"
//#include "sphere.h"

bool check_sphere_hit(sphere_t *sphere,
		      ray_t *r,
		      double *t_min,
		      double *t_max,
		      hit_record *rec)
{
  hit_record temp_rec;
  bool hit_anything = false;
  double closest_so_far = temp_rec.t;
  //printf("check sphere hit tmin:%f\n", *t_max);
  bool hitted_sphere = hit_sphere(sphere,
				  r,
				  t_min,
				  t_max,
				  &temp_rec);
  if (hitted_sphere)
    {
      hit_anything = true;
      closest_so_far = temp_rec.t;

      //rec = &temp_rec; how to pass fill temp_rec to rec struct
      rec->normal.x = temp_rec.normal.x;
      rec->normal.y = temp_rec.normal.y;
      rec->normal.z = temp_rec.normal.z;
      //printf("check_sphere_hit: %f", rec->normal.x);
      //printf("check_sphere_hit: %f", rec->normal.x);
    }
  return hit_anything;
}

