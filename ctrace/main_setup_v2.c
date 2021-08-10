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
#include "texture.h"

PV_t ray_color(ray_t *r, hittable_list *world, int depth, int i, int j)
{
  if (depth <= 0) {
      PV_t depth_exceeded;
      depth_exceeded.x = 0;
      depth_exceeded.y = 0;
      depth_exceeded.z = 0;
      return depth_exceeded;
    }
  hit_record rec;
  PV_t color = {0, 0, 0}; // background color
  rec.t = infinity;
  //PV_t color;
  int sphere_hit_checked = -1;
  int current_hit = -1;
  double zero = 0;
  for (int k = 0; k < 2; k++)
    {
      sphere_hit_checked = check_sphere_hit(&(world->sphere[k]),
					    r,
					    &zero,
					    &rec.t,
					    &rec, k);
      if (sphere_hit_checked > -1) {
	current_hit = sphere_hit_checked;
      }
    }
  if (current_hit > -1)
    {
      bool mat_ref = calculate_material_reflections(&(world->sphere[current_hit].mat),
						    r,
						    &(world->sphere[current_hit].mat.albedo),
						    &rec);
      if (mat_ref) {
	PV_t current_ray_color = ray_color(&(world->sphere[current_hit].mat.scattered),
					   world,
					   depth-1, i, j);
	PV_t color_to_return = {current_ray_color.x*
				world->sphere[current_hit].mat.attenuation.x,
				current_ray_color.y*
				world->sphere[current_hit].mat.attenuation.y,
				current_ray_color.z*
				world->sphere[current_hit].mat.attenuation.z};
	return color_to_return;
      }
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
  //PV_t color = {0, 0, 0};
  return color;
}
  

int main(int argc, char *argv[]) {

  // To create new random number and not repeated
  srand(time(NULL)); /* mora bit za random??? */

  // Image
  const auto double aspect_ratio = 16.0/9.0;
  const int image_width = 400;
  const int image_height = (int)(image_width/aspect_ratio); //static_cast<int>(image_width/aspect_ratio);
  const int samples_per_pixel = 200;
  const int max_depth = 10;
  const double R = cos(pi/4);
  hittable_list world;

  // sphere ground
  sphere_t sphere_ground;
  sphere_ground.center.x = 0; 
  sphere_ground.center.y = -10;
  sphere_ground.center.z = 0;
  sphere_ground.radius = 10;
  sphere_ground.mat.type = 1;
  sphere_ground.mat.albedo.type = 2;
  sphere_ground.mat.albedo.color1.x = 0.2;
  sphere_ground.mat.albedo.color1.y = 0.3;
  sphere_ground.mat.albedo.color1.z = 0.1;
  sphere_ground.mat.albedo.color2.x = 0.9;
  sphere_ground.mat.albedo.color2.y = 0.9;
  sphere_ground.mat.albedo.color2.z = 0.9;
  
  // sphere center
  sphere_t sphere_center;
  sphere_center.center.x = 0; 
  sphere_center.center.y = 10;
  sphere_center.center.z = 0;
  sphere_center.radius = 10;
  sphere_center.mat.type = 1;
  sphere_center.mat.albedo.type = 2;
  sphere_center.mat.albedo.color1.x = 0.2;
  sphere_center.mat.albedo.color1.y = 0.3;
  sphere_center.mat.albedo.color1.z = 0.1;
  sphere_center.mat.albedo.color2.x = 0.9;
  sphere_center.mat.albedo.color2.y = 0.9;
  sphere_center.mat.albedo.color2.z = 0.9;

  //sphere_center.mat.ir = 1.5;
  
  world.sphere[0] = sphere_ground;
  world.sphere[1] = sphere_center;
  // Camera

  camera cam;
  PV_t lookfrom = {13, 2, 4};
  PV_t lookat = {0, 0, 0};
  PV_t vup = {0, 1, 0};
  PV_t dist_to_focus_diff = vec_diff(&lookfrom, &lookat);
  double dist_to_focus = 10;//vec_len(&dist_to_focus_diff);
  double aperture = 0.0;
  double vfov = 20;
  initialize_camera(&cam, lookfrom, lookat, vup, vfov, aspect_ratio,
		    aperture, dist_to_focus);

  printf("P3\n%i %i\n255\n", image_width, image_height);
  for (int j=image_height-1; j>=0; j--) {
    for (int i=0; i<image_width; i++) {
      PV_t pixel_color;
      pixel_color.x = 0;
      pixel_color.y = 0;
      pixel_color.z = 0;
      for (int s = 0; s < samples_per_pixel; ++s) {
	auto double u = ((double)i+random_double()) / (image_width-1);
	auto double v = ((double)j+random_double()) / (image_height-1);
	ray_t r = camera_get_ray(&cam, u, v);
	PV_t color = ray_color(&r, &world, max_depth, i, j);
	pixel_color.x += color.x;
	pixel_color.y += color.y;
	pixel_color.z += color.z;
      }
      write_color(&pixel_color, samples_per_pixel);
    }
  }
  return 0;
};
 
