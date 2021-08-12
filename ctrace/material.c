#include "material.h"
#include "rtweekend.h"

double reflectance(double cosine, double ref_idx)
{
  // Use Schlick's approximation for reflectance.
  double r0 = (1.0-ref_idx) / (1.0+ref_idx);
  r0 = r0*r0;
  return r0 + (1.0-r0)*pow((1.0 - cosine), 5);
}



bool calculate_material_reflections(material *mat, ray_t *r_in, texture_t *albedo, hit_record *rec)
//takes material struct and color
{
  //printf("material type: %i\n", mat->type);
  //printf("material albedo: %f\n", mat->albedo.color1.x);
  switch (mat->type) {
  case 1: { // lambertian
    PV_t scatter_direction;
    PV_t random_unit_vec = random_unit_vector();
	PV_t emitted = {0,0,0};
	mat->emitted = emitted;
    scatter_direction.x = rec->normal.x + random_unit_vec.x;
    scatter_direction.y = rec->normal.y + random_unit_vec.y;
    scatter_direction.z = rec->normal.z + random_unit_vec.z;
    
    if (near_zero(&scatter_direction)) {
      scatter_direction = rec->normal;
    }
    mat->scattered.origin = rec->p;  //ray(rec.p, scatter_direction);
    mat->scattered.direction = scatter_direction;

	// offset to avoid self-intersection
	double offset = 0.001;
	mat->scattered.origin.x = mat->scattered.origin.x+mat->scattered.direction.x*offset;
	mat->scattered.origin.y = mat->scattered.origin.y+mat->scattered.direction.y*offset;
	mat->scattered.origin.z = mat->scattered.origin.z+mat->scattered.direction.z*offset;
	
	albedo->p = rec->p;
    mat->attenuation = texture_color(albedo);
	//if (mat->type == 1)
	//  {
	//  printf("Is reflected 1\n");
	//  printf("rec->p.x: %f\n", rec->p.x);
	//  printf("rec->p.y: %f\n", rec->p.y);
	//  printf("rec->p.z: %f\n", rec->p.z);
	//  printf("rec->normal.x: %f\n", rec->normal.x);
	//  printf("rec->normal.y: %f\n", rec->normal.y);
	//  printf("rec->normal.z: %f\n", rec->normal.z);
	//  printf("mat->scattered.origin.x: %f\n", mat->scattered.origin.x);
	//  printf("mat->scattered.origin.y: %f\n", mat->scattered.origin.y);
	//  printf("mat->scattered.origin.z: %f\n", mat->scattered.origin.z);
	//  printf("mat->scattered.direction.x: %f\n", mat->scattered.direction.x);
	//  printf("mat->scattered.direction.y: %f\n", mat->scattered.direction.y);
	//  printf("mat->scattered.direction.z: %f\n", mat->scattered.direction.z);
	//  printf("mat->attenuation.x: %f\n", mat->attenuation.x);
	//  printf("mat->attenuation.y: %f\n", mat->attenuation.y);
	//  printf("mat->attenuation.z: %f\n", mat->attenuation.z);
	//
	//	  }
    return true;
    break;
  }
  case 2: { // metal
    PV_t unit_vec = unit_vector(&r_in->direction);
    PV_t reflected = reflect(&unit_vec, &rec->normal);
    ray_t scattered;
	PV_t emitted = {0,0,0};
	mat->emitted = emitted;

    scattered.origin = rec->p;
	albedo->p = rec->p;

    PV_t unit_fuzz = random_in_unit_sphere();
    scattered.direction.x = reflected.x+mat->fuzz*unit_fuzz.x;
    scattered.direction.y = reflected.y+mat->fuzz*unit_fuzz.y;
    scattered.direction.z = reflected.z+mat->fuzz*unit_fuzz.z;
    mat->scattered = scattered;
    mat->attenuation = texture_color(albedo);

    // update reflected ray
    r_in->origin = rec->p;
    r_in->direction = reflected;
    
    // check dot product
    double dot_product = vec_dot(&scattered.direction, &rec->normal);
    if (dot_product > 0) {
      return true;
    }
    return false;
    break;
  }
  case 3: { // dielectric
	PV_t emitted = {0,0,0};
	mat->emitted = emitted;

	PV_t outward_normal;
	PV_t reflected = reflect(&r_in->direction, &rec->normal);
	double ni_over_nt;
	mat->attenuation.x = 1.0;
	mat->attenuation.y = 1.0;
	mat->attenuation.z = 1.0;
	PV_t refracted;
	double reflect_prob;
	double cosine;
	if (vec_dot(&r_in->direction, &rec->normal) > 0) {
	  outward_normal = vec_scale(&rec->normal, -1.0);
	  ni_over_nt = mat->ir;
	  cosine = vec_dot(&r_in->direction, &rec->normal) / vec_len(&r_in->direction);
	  cosine = sqrt(1 - mat->ir*mat->ir*(1-cosine*cosine));	  
	}
	else {
	  outward_normal = rec->normal;
	  ni_over_nt = 1.0 / mat->ir;
	  cosine = -1.0*vec_dot(&r_in->direction, &rec->normal) / vec_len(&r_in->direction);
	}

	if (refract(&r_in->direction, &outward_normal, ni_over_nt, &refracted)) {
	  reflect_prob = reflectance(cosine, mat->ir);
	}
	else{
	  reflect_prob = 1.0;
	}
	if (random_double() < reflect_prob)
	  {
		mat->scattered.origin = rec->p;
		mat->scattered.direction = reflected;
	  }
	else
	  {
		mat->scattered.origin = rec->p;
		mat->scattered.direction = refracted;
	  }
	return true;
  }
  case 4: {
	//printf("Mterial 4\n");
    mat->attenuation = albedo->color1;
	//printf("albedo->color1.x %f\n", albedo->color1.x);
	//printf("albedo->color1.y %f\n", albedo->color1.y);
	//printf("albedo->color1.z %f\n", albedo->color1.z);
	//printf("mat->attenuation.x %f\n", mat->attenuation.x);
	//printf("mat->attenuation.y %f\n", mat->attenuation.y);
	//printf("mat->attenuation.z %f\n", mat->attenuation.z);
	mat->scattered.origin = rec->p;
	mat->scattered.direction.x = 0;
	mat->scattered.direction.y = 0;
	mat->scattered.direction.z = 0;
	//if (mat->type == 4)
	//  {
	//  printf("Is reflected 4\n");
	//  printf("rec->p.x: %f\n", rec->p.x);
	//  printf("rec->p.y: %f\n", rec->p.y);
	//  printf("rec->p.z: %f\n", rec->p.z);
	//  printf("rec->normal.x: %f\n", rec->normal.x);
	//  printf("rec->normal.y: %f\n", rec->normal.y);
	//  printf("rec->normal.z: %f\n", rec->normal.z);
	//  printf("mat->scattered.origin.x: %f\n", mat->scattered.origin.x);
	//  printf("mat->scattered.origin.y: %f\n", mat->scattered.origin.y);
	//  printf("mat->scattered.origin.z: %f\n", mat->scattered.origin.z);
	//  printf("mat->scattered.direction.x: %f\n", mat->scattered.direction.x);
	//  printf("mat->scattered.direction.y: %f\n", mat->scattered.direction.y);
	//  printf("mat->scattered.direction.z: %f\n", mat->scattered.direction.z);
	//  printf("mat->attenuation.x: %f\n", mat->attenuation.x);
	//  printf("mat->attenuation.y: %f\n", mat->attenuation.y);
	//  printf("mat->attenuation.z: %f\n", mat->attenuation.z);
	//  }

	return true;
    break;
  }
  default:
	{
	  printf("DEFAULT\n");
    break;
	}
  }
  return true;
}
