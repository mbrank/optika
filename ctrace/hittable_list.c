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
  hit_record hitted_sphere = hit_sphere(sphere,
				  r,
				  t_min,
				  t_max,
				  &temp_rec);
  if (hitted_sphere)
    {
      hit_anything = true;
      closest_so_far = temp_rec.t;
      rec = &temp_rec;
    }
  return hit_anything;
}

