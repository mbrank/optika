#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "ray.h"
#include <stdbool.h>
#include "hittable_list.h"
#include "constants.h"
#include "sphere.h"
#include "camera.h"
#include "color.h"
#include "rtweekend.h"
#include "material.h"
#include <time.h>


//PV_t attenuation_ray_color(){
//}

PV_t ray_color(ray_t *r, hittable_list *world, int depth)
{
  hit_record rec;
  PV_t color;
  //printf("sizeof world: %d\n", sizeof(&world));
  //for (int i = 0; i < (int)(sizeof(&world)/4); i++) {
  for (int i = 0; i < 4; i++) {
    double zero = 0;
    bool sphere_hit_checked = check_sphere_hit(&(world->sphere[i]),
					       r,
					       &zero,
						   &infinity,
					       &rec);
    if (depth <= 0) {
      PV_t depth_exceeded;
      depth_exceeded.x = 0;
      depth_exceeded.y = 0;
      depth_exceeded.z = 0;
      return depth_exceeded;
    }

    if (sphere_hit_checked) {

	  //ray_t scattered;
	  //PV_t attenuation;

	  bool mat_ref = calculate_material_reflections(&(world->sphere[i].mat),
													r,
													&(world->sphere[i].mat.albedo),
													&rec);
	  if (mat_ref) {

		  return ray_color(&(world->sphere[i].mat.scattered), world, depth-1);
	  }
	  
	  /*
      PV_t target;
	  PV_t random_unit_vec = random_unit_vector();
      target.x = rec.p.x+rec.normal.x+random_unit_vec.x;
      target.y = rec.p.y+rec.normal.y+random_unit_vec.y;
      target.z = rec.p.z+rec.normal.z+random_unit_vec.z;
      PV_t target_min_rec_p;
      target_min_rec_p.x = target.x - rec.p.x;
      target_min_rec_p.y = target.y - rec.p.y;
      target_min_rec_p.z = target.z - rec.p.z;
      ray_t reflected_ray;
      reflected_ray.origin = rec.p;
      reflected_ray.direction = target_min_rec_p;
	  */
	  
      //return ray_color(&reflected_ray, world, depth-1);

	  PV_t color = {0, 0, 0};
	  return color; 
    }
    PV_t unit_direction = unit_vector(&r->direction);
    double t = 0.5*(unit_direction.y + 1.0);
    PV_t color1;
    color1.x = 1.0;
    color1.y = 1.0;
    color1.z = 1.0;
    PV_t color2;
    color2.x = 0.5;
    color2.y = 0.7;
    color2.z = 1.0;
    PV_t scaled1 = vec_scale(&color1, 1-t);
    PV_t scaled2 = vec_scale(&color2, t);
    color = vec_sum(&scaled1, &scaled2);
  }
  return color;
}
  

int main(int argc, char *argv[]) {

  // To create new random number and not repeated
  srand(time(NULL)); /* mora bit za random??? */
    
  // Image
  const auto double aspect_ratio = 16.0/9.0;
  const int image_width = 400;
  const int image_height = (int)(image_width/aspect_ratio); //static_cast<int>(image_width/aspect_ratio);
  const int samples_per_pixel = 300;
  const int max_depth = 20;
  
  hittable_list world;

  // sphere center
  sphere_t sphere0;
  sphere0.center.x = 0; 
  sphere0.center.y = 0;
  sphere0.center.z = -1;
  sphere0.radius = 0.5;
  sphere0.mat.type = 1;
  sphere0.mat.albedo.x = 0.7;
  sphere0.mat.albedo.y = 0.3;
  sphere0.mat.albedo.z = 0.3;
  // sphere ground
  sphere_t sphere1;
  sphere1.center.x = 0; 
  sphere1.center.y = -100.5;
  sphere1.center.z = -1;
  sphere1.radius = 100;
  sphere1.mat.type = 1;
  sphere1.mat.albedo.x = 0.8;
  sphere1.mat.albedo.y = 0.8;
  sphere1.mat.albedo.z = 0.0;
  // sphere right
  sphere_t sphere2;
  sphere2.center.x = -1; 
  sphere2.center.y = 0;
  sphere2.center.z = -1;
  sphere2.radius = 0.5;
  sphere2.mat.type = 2;
  sphere2.mat.albedo.x = 0.8;
  sphere2.mat.albedo.y = 0.8;
  sphere2.mat.albedo.z = 0.8;
  // sphere left
  sphere_t sphere3;
  sphere3.center.x = 1; 
  sphere3.center.y = 0;
  sphere3.center.z = -1;
  sphere3.radius = 0.5;
  sphere3.mat.type = 2;
  sphere3.mat.albedo.x = 0.8;
  sphere3.mat.albedo.y = 0.6;
  sphere3.mat.albedo.z = 0.2;

  world.sphere[0] = sphere1;
  world.sphere[1] = sphere0;
  world.sphere[2] = sphere2;
  world.sphere[3] = sphere3;

  // Camera

  camera cam;

  // how to initialize camera through function
  // initialize camera
  cam.aspect_ratio = 16.0/9.0;
  cam.viewport_height = 2.0;
  cam.viewport_width = (cam.aspect_ratio * cam.viewport_height);
  cam.focal_length = 1.0;

  cam.camera_origin.x = 0;
  cam.camera_origin.y = 0;
  cam.camera_origin.z = 0;

  cam.horizontal.x = cam.viewport_width;
  cam.horizontal.y = 0;
  cam.horizontal.z = 0;

  cam.vertical.x = 0;
  cam.vertical.y = cam.viewport_height;
  cam.vertical.z = 0;

  // Calculate lower left corner of camera
  PV_t hor_divide = vec_divide(&(cam.horizontal), -2);
  PV_t vert_divide = vec_divide(&(cam.vertical), -2);
  PV_t scale_orig_hor = vec_sum(&(cam.camera_origin), &hor_divide);
  PV_t scale_orig_hor_vert = vec_sum(&scale_orig_hor, &vert_divide);
  PV_t neg_focal_length = {0, 0, -1};
  cam.lower_left_corner = vec_sum(&scale_orig_hor_vert, &neg_focal_length);

  printf("P3\n%i %i\n255\n", image_width, image_height);
  for (int j=image_height-1; j>=0; j--) {
    for (int i=0; i<image_width; i++) {
      PV_t pixel_color;
      pixel_color.x = 0;
      pixel_color.y = 0;
      pixel_color.z = 0;
	  //printf("j: %d, i: %d\n", j, i);
      for (int s = 0; s < samples_per_pixel; ++s) {
		auto double u = ((double)i+random_double()) / (image_width-1);
		auto double v = ((double)j+random_double()) / (image_height-1);
		ray_t r = camera_get_ray(&cam, u, v);
		PV_t color = ray_color(&r, &world, max_depth);
		pixel_color.x += color.x;
		pixel_color.y += color.y;
		pixel_color.z += color.z;
      }
      write_color(&pixel_color, samples_per_pixel);
    }
  }
  return 0;
};
 
