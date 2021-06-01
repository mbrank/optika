#include "material.h"

bool calculate_material_reflections(material *mat, ray_t *r_in, PV_t *albedo, hit_record *rec)
//takes material struct and color
{
  switch (mat->type) {
  case 1: { // lambertian
    PV_t scatter_direction;
	PV_t random_unit_vec = random_unit_vector();
	scatter_direction.x = rec->normal.x + random_unit_vec.x;
	scatter_direction.y = rec->normal.y + random_unit_vec.y;
	scatter_direction.z = rec->normal.z + random_unit_vec.z;

	if (near_zero(&scatter_direction)) {
	  scatter_direction = rec->normal;
	}
	//ray_t scattered;
	mat->scattered.origin = rec->p;  //ray(rec.p, scatter_direction);
	mat->scattered.direction = scatter_direction;
    mat->attenuation = mat->albedo;
	//printf("lambertian attenuation x, %f\n", mat->attenuation.x);
	//printf("lambertian attenuation y, %f\n", mat->attenuation.y);
	//printf("lambertian attenuation z, %f\n", mat->attenuation.z);
    break;
  }
  case 2: { // metal
    PV_t reflected = reflect(unit_vector(&r_in->direction), rec->normal);
	ray_t scattered;
	scattered.origin = rec->p,
	scattered.direction = reflected;
	mat->scattered = scattered;
	mat->attenuation = mat->albedo;
	//printf("metal attenuation x, %f\n", mat->attenuation.x);
	//printf("metal attenuation y, %f\n", mat->attenuation.y);
	//printf("metal attenuation z, %f\n", mat->attenuation.z);
    break;
  }
  default:
    break;
  }
  //PV_t rc_norm = mat->rec.normal;
  //PV_t unit_vec = random_unit_vector();
  //PV_t scatter_direction;
  //scatter_direction.x = rc_norm.x + unit_vec.x;
  //scatter_direction.y = rc_norm.y + unit_vec.y;
  //scatter_direction.z = rc_norm.z + unit_vec.z;
  ////ray_t scattered;
  //mat->scattered.origin = mat->rec.p;
  //mat->scattered.direction = scatter_direction;
  //mat->attenuation = *albedo; //albedo
  return true;
}
