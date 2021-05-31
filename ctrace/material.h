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
  // lambertian -> 1
  // metal -> 2
} material;


bool calculate_material_reflections(material *mat, ray_t *r_in, PV_t *albedo, hit_record *rec);

#endif

