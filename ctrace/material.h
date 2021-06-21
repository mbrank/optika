#ifndef MATERIAL_H
#define MATERIAL_H

#include "ray.h"
#include "hittable.h"

typedef struct material_t{
  // define only albedo and type
  //ray_t r_in;
  hit_record rec;
  PV_t albedo; // color
  PV_t attenuation;
  ray_t scattered;
  //char type[10];
  int type; // type of material
  double fuzz; // factor to fuzz reflections, 0 is no perturbation (only metal)
  double ir; // index of refraction (only dielectric)
  // lambertian -> 1
  // metal -> 2
  // dielectric -> 3
  // diffuse_light -> 4
  double u; // texture coordinate (in case of texture and perlin materials)
  double v; // texture coordinate (in case of texture and perlin materials)
  PV_t emitter; // color of emission
} material;

double reflectance(double cosine,
				   double ref_idx);
bool calculate_material_reflections(material *mat,
									ray_t *r_in,
									PV_t *albedo,
									hit_record *rec);

#endif

