#include "ray.h"
#include "hittable.h"

typedef struct material_t{
  ray_t ray;
  hit_record rec;
  PV_t attenuation;
  ray_t scattered;
} material;


bool lambertian_material(material *mat, PV_t *a)
//takes material struct and color
{
  PV_t rc_norm = mat->rec.normal;
  PV_t unit_vec = random_unit_vector();
  PV_t scatter_direction;
  scatter_direction.x = rc_norm.x + unit_vec.x;
  scatter_direction.y = rc_norm.y + unit_vec.y;
  scatter_direction.z = rc_norm.z + unit_vec.z;
  //ray_t scattered;
  mat->scattered.origin = mat->rec.p;
  mat->scattered.direction = scatter_direction;
  mat->attenuation = *a; //albedo
  return true;
}
