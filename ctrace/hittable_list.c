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

      //pass data from temporary recorder
      //rec = &temp_rec; how to pass fill temp_rec to rec struct
      rec->normal.x = temp_rec.normal.x;
      rec->normal.y = temp_rec.normal.y;
      rec->normal.z = temp_rec.normal.z;
      rec->p.x = temp_rec.p.x;
      rec->p.y = temp_rec.p.y;
      rec->p.z = temp_rec.p.z;
      rec->t = temp_rec.t;
      rec->front_face = temp_rec.front_face;
      rec->object_was_hit = temp_rec.object_was_hit;
      
      //printf("temp_rec.normal.x: %f\n", temp_rec.normal.x);
      //printf("rec->normal.x: %f\n", rec->normal.x);
    }
  return hit_anything;
}

