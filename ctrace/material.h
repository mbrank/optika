#ifndef MATERIAL_H
#define MATERIAL_H

#include "ray.h"
#include "hittable.h"
#include "texture.h"

typedef struct material_t{
  // define only albedo and type
  //ray_t r_in;
  hit_record rec;
  texture_t albedo; // color
  PV_t attenuation;
  ray_t scattered;
  double fuzz; // factor to fuzz reflections, 0 is no perturbation (only metal)
  double ir; // index of refraction (only dielectric)
  //char type[10];
  int type; // type of material
  // lambertian -> 1
  // metal -> 2
  // dielectric -> 3
  // diffuse light -> 4

  PV_t emitted;
} material;

double reflectance(double cosine,
				   double ref_idx);
bool calculate_material_reflections(material *mat,
									ray_t *r_in,
									texture_t *albedo,
									hit_record *rec);
//PV_t emitted(material *mat, double *u, double *v, PV_t *p);
#endif

