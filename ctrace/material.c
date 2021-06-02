#include "material.h"

bool calculate_material_reflections(material *mat, ray_t *r_in, PV_t *albedo, hit_record *rec)
//takes material struct and color
{
  switch (mat->type) {
  case 1: { // lambertian
    //printf("lambertian -> r_in.direction x, %f\n", r_in->direction.x);
    //printf("lambertian -> r_in.direction y, %f\n", r_in->direction.y);
    //printf("lambertian -> r_in.direction z, %f\n", r_in->direction.z);
    //printf("lambertian -> r_in.origin x, %f\n", r_in->origin.x);
    //printf("lambertian -> r_in.origin y, %f\n", r_in->origin.y);
    //printf("lambertian -> r_in.origin z, %f\n", r_in->origin.z);
    //printf("  lambertian rec normal: %f, %f, %f\n",
	//	   rec->normal.x,
	//	   rec->normal.y,
	//	   rec->normal.z);

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
    mat->attenuation = *albedo;
    //printf("lambertian attenuation x, %f\n", mat->attenuation.x);
    //printf("lambertian attenuation y, %f\n", mat->attenuation.y);
    //printf("lambertian attenuation z, %f\n", mat->attenuation.z);
    return true;
    break;
  }
  case 2: { // metal
    //printf("metal -> r_in.direction x, %f\n", r_in->direction.x);
    //printf("metal -> r_in.direction y, %f\n", r_in->direction.y);
    //printf("metal -> r_in.direction z, %f\n", r_in->direction.z);
    //printf("metal -> rec_normal: %f, %f, %f\n",
	//	   rec->normal.x,
	//	   rec->normal.y,
	//	   rec->normal.z);
    //printf("metal -> rec_normal y, %f\n", r_in->origin.y);
    //printf("metal -> rec_normal z, %f\n", r_in->origin.z);
    //printf("material->rec.p x, %f\n", rec->p.x);
    //printf("material->rec.p y, %f\n", rec->p.y);
    //printf("material->rec.p z, %f\n", rec->p.z);

    // calculate reflection
	//PV_t normal =  rec->normal;
    //printf("metal -> _normal: %f, %f, %f\n",
	//	   normal.x,
	//	   normal.y,
	//	   normal.z);

	PV_t unit_vec = unit_vector(&r_in->direction);
    PV_t reflected = reflect(&unit_vec, &rec->normal);

	//PV_t unit_vec = unit_vector(&r_in->direction);
    // update material
	//printf("unit_vec: %f, %f, %f\n",
	//	   unit_vec.x,
	//	   unit_vec.y,
	//	   unit_vec.z);
	//printf("reflected: %f, %f, %f\n",
	//	   reflected.x,
	//	   reflected.y,
	//	   reflected.z);

    ray_t scattered;
    scattered.origin = rec->p;

	PV_t unit_fuzz = random_in_unit_sphere();
    scattered.direction.x = reflected.x+mat->fuzz*unit_fuzz.x;
    scattered.direction.y = reflected.y+mat->fuzz*unit_fuzz.y;
	scattered.direction.z = reflected.z+mat->fuzz*unit_fuzz.z;
	//printf("metal r_in origin: %f, %f, %f\n",
	//	   r_in->origin.x,
	//	   r_in->origin.y,
	//	   r_in->origin.z);
	//printf(" metal r_in direction: %f, %f, %f\n",
	//	   r_in->direction.x,
	//	   r_in->direction.y,
	//	   r_in->direction.z);
    //printf("  metal rec normal: %f, %f, %f\n",
	//	   rec->normal.x,
	//	   rec->normal.y,
	//	   rec->normal.z);
    //printf("   metal rec p: %f, %f, %f\n",
	//	   rec->p.x,
	//	   rec->p.y,
	//	   rec->p.z);
	//printf("    scattered metal origin: %f, %f, %f\n",
	//	   scattered.origin.x,
	//	   scattered.origin.y,
	//	   scattered.origin.z);
    //printf("      scattered metal direction: %f, %f, %f\n",
	//	   scattered.direction.x,
	//	   scattered.direction.y,
	//	   scattered.direction.z);

    mat->scattered = scattered;
    mat->attenuation = *albedo;

    // update reflected ray
    r_in->origin = rec->p;
    r_in->direction = reflected;
    
    // check dot product
    double dot_product = vec_dot(&scattered.direction, &rec->normal);
    if (dot_product > 0) {
      return true;
    }
    return false;
    //return (dot(scattered.direction(), rec.normal) > 0);
    //printf("metal attenuation x, %f\n", mat->attenuation.x);
    //printf("metal attenuation y, %f\n", mat->attenuation.y);
    //printf("metal attenuation z, %f\n", mat->attenuation.z);
    break;
  }
  default:
    printf("DEFAULT\n");
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
