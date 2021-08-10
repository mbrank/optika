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

PV_t ray_color(ray_t *r, PV_t *background, hittable_list *world, int depth, int i, int j)
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
  int current_hit_rectangle = -1;
  double zero = 0;
  // check which sphere is hit first
  for (int k = 0; k < 0; k++)
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
  // check if rectangle is hit before sphere
  for (int l = 0; l < 1; l++)
	{
	  printf("beffbeforetta %f \n", world->aarectangle[0].mat.albedo.color1.y);
	  int aarectangle_hit_checked = check_aarectangle_hit(&(world->aarectangle[l]),
														  r,
														  &zero,
														  &rec.t,
														  &rec, l);
      if (aarectangle_hit_checked > -1) {
		current_hit_rectangle = aarectangle_hit_checked;
		current_hit = -1;
      }
	}
  //printf("current_hit_rectangle %i s\n", current_hit_rectangle);

  // if object is hit, calculate reflections
  if (current_hit > -1)
    {
      bool mat_ref = calculate_material_reflections(&(world->sphere[current_hit].mat),
													r,
													&(world->sphere[current_hit].mat.albedo),
													&rec);
      if (mat_ref) {
		if (world->sphere[current_hit].mat.scattered.direction.x == 0 &&
			world->sphere[current_hit].mat.scattered.direction.y == 0 &&
			world->sphere[current_hit].mat.scattered.direction.z == 0 )
		  {
			// if emitter was hit, return just emitter value
		  PV_t color_to_return = world->sphere[current_hit].mat.attenuation;
		  return color_to_return;
		}
		else{
		  // if emitter was not hit, calculate reflection
		PV_t current_ray_color = ray_color(&(world->sphere[current_hit].mat.scattered),
										   background,
										   world,
										   depth-1, i, j);
		PV_t color_to_return = {world->sphere[current_hit].mat.emitted.x + current_ray_color.x*
								world->sphere[current_hit].mat.attenuation.x,
								world->sphere[current_hit].mat.emitted.y + current_ray_color.y*
								world->sphere[current_hit].mat.attenuation.y,
								world->sphere[current_hit].mat.emitted.z + current_ray_color.z*
								world->sphere[current_hit].mat.attenuation.z};
		return color_to_return;
		}
      }
      PV_t color = {0, 0, 0};
      return color; 
    }
  else if (current_hit_rectangle > -1)     {
      bool mat_ref = calculate_material_reflections(&(world->aarectangle[current_hit_rectangle].mat),
													r,
													&(world->aarectangle[current_hit_rectangle].mat.albedo),
													&rec);
      if (mat_ref) {
		printf("beforetta %f \n", world->aarectangle[current_hit_rectangle].mat.albedo.color1.y);
		if (world->aarectangle[current_hit_rectangle].mat.scattered.direction.x == 0 &&
			world->aarectangle[current_hit_rectangle].mat.scattered.direction.y == 0 &&
			world->aarectangle[current_hit_rectangle].mat.scattered.direction.z == 0 )
		  {
			printf("current_hit_rectangle %i\n", current_hit_rectangle);
			printf("ttatype %i \n", world->aarectangle[current_hit_rectangle].mat.type);
			printf("tta %f \n", world->aarectangle[current_hit_rectangle].mat.albedo.color1.y);
			// if emitter was hit, return just emitter value
		  PV_t color_to_return = world->aarectangle[current_hit_rectangle].mat.attenuation;
		  printf("color to return.x %f\n", color_to_return.x);
		  printf("color to return.y %f\n", color_to_return.y);
		  printf("color to return.z %f\n", color_to_return.z);
		  return color_to_return;
		}
		else{
		  // if emitter was not hit, calculate reflection
		PV_t current_ray_color = ray_color(&(world->aarectangle[current_hit_rectangle].mat.scattered),
										   background,
										   world,
										   depth-1, i, j);
		PV_t color_to_return = {world->aarectangle[current_hit_rectangle].mat.emitted.x + current_ray_color.x*
								world->aarectangle[current_hit_rectangle].mat.attenuation.x,
								world->aarectangle[current_hit_rectangle].mat.emitted.y + current_ray_color.y*
								world->aarectangle[current_hit_rectangle].mat.attenuation.y,
								world->aarectangle[current_hit_rectangle].mat.emitted.z + current_ray_color.z*
								world->aarectangle[current_hit_rectangle].mat.attenuation.z};
		return color_to_return;
		}
      }
      PV_t color = {0, 0, 0};
      return color; 
    }
  else{
	//printf("test background\n");
  	return *background;
  }
  
  //PV_t unit_direction = unit_vector(&r->direction);
  //double t = 0.5*(unit_direction.y + 1.0);
  //PV_t color1;
  //color1.x = 1.0;
  //color1.y = 1.0;
  //color1.z = 1.0;
  //PV_t color2;
  //color2.x = 0.5;
  //color2.y = 0.7;
  //color2.z = 1.0;
  //PV_t scaled1 = vec_scale(&color1, 1-t);
  //PV_t scaled2 = vec_scale(&color2, t);
  //color = vec_sum(&scaled1, &scaled2);
  ////PV_t color = {0, 0, 0};
  //return color;
}
  

int main(int argc, char *argv[]) {

  // To create new random number and not repeated
  srand(time(NULL)); /* mora bit za random??? */

  // Image
  const auto double aspect_ratio = 1.0; //16.0/9.0;
  const int image_width = 600;
  const int image_height = (int)(image_width/aspect_ratio); //static_cast<int>(image_width/aspect_ratio);
  const int samples_per_pixel = 200;
  const int max_depth = 10;
  const double R = cos(pi/4);
  hittable_list world;

  /*
  // aarectangle green
  aarectangle_t rectangle_green;
  rectangle_green.x0 = 1;
  rectangle_green.y1 = 1;
  rectangle_green.y0 = 0;
  rectangle_green.y1 = 555;
  rectangle_green.z0 = 0;
  rectangle_green.z1 = 555;
  rectangle_green.k = 555;
  rectangle_green.yz = 1;
  rectangle_green.mat.type = 1;
  rectangle_green.mat.albedo.type = 1;
  rectangle_green.mat.albedo.color1.x = 0.12;
  rectangle_green.mat.albedo.color1.y = 0.45;
  rectangle_green.mat.albedo.color1.z = 0.15;
  
  // aarectangle red
  aarectangle_t rectangle_red;
  rectangle_red.y0 = 0;
  rectangle_red.y1 = 555;
  rectangle_red.z0 = 0;
  rectangle_red.z1 = 555;
  rectangle_red.k = 0;
  rectangle_red.yz = 1;
  rectangle_red.mat.type = 1;
  rectangle_red.mat.albedo.type = 1;
  rectangle_red.mat.albedo.color1.x = 0.65;
  rectangle_red.mat.albedo.color1.y = 0.05;
  rectangle_red.mat.albedo.color1.z = 0.05;
  */
  
  // aarectangle light
  aarectangle_t rectangle_light;
  rectangle_light.x0 = 213;
  rectangle_light.x1 = 343;
  rectangle_light.z0 = 227;
  rectangle_light.z1 = 332;
  rectangle_light.k = 554;
  rectangle_light.y0 = rectangle_light.k-1;
  rectangle_light.y1 = rectangle_light.k+1;
  rectangle_light.xz = 1;
  rectangle_light.mat.type = 4;
  rectangle_light.mat.albedo.type = 1;
  rectangle_light.mat.albedo.color1.x = 15;
  rectangle_light.mat.albedo.color1.y = 15;
  rectangle_light.mat.albedo.color1.z = 15;

  /*
  // aarectangle white_top
  aarectangle_t rectangle_white_top;
  rectangle_white_top.x0 = 0;
  rectangle_white_top.x1 = 555;
  rectangle_white_top.z0 = 0;
  rectangle_white_top.z1 = 555;
  rectangle_white_top.k = 0;
  rectangle_white_top.xz = 1;
  rectangle_white_top.mat.type = 4;
  rectangle_white_top.mat.albedo.type = 1;
  rectangle_white_top.mat.albedo.color1.x = 0.73;
  rectangle_white_top.mat.albedo.color1.y = 0.73;
  rectangle_white_top.mat.albedo.color1.z = 0.73;

  // aarectangle white_bottom
  aarectangle_t rectangle_white_bottom;
  rectangle_white_bottom.x0 = 0;
  rectangle_white_bottom.x1 = 555;
  rectangle_white_bottom.z0 = 0;
  rectangle_white_bottom.z1 = 555;
  rectangle_white_bottom.k = 555;
  rectangle_white_bottom.xz = 1;
  rectangle_white_bottom.mat.type = 4;
  rectangle_white_bottom.mat.albedo.type = 1;
  rectangle_white_bottom.mat.albedo.color1.x = 0.73;
  rectangle_white_bottom.mat.albedo.color1.y = 0.73;
  rectangle_white_bottom.mat.albedo.color1.z = 0.73;

  // aarectangle white_back
  aarectangle_t rectangle_white_back;
  rectangle_white_back.x0 = 0;
  rectangle_white_back.x1 = 555;
  rectangle_white_back.y0 = 0;
  rectangle_white_back.y1 = 555;
  rectangle_white_back.k = 555;
  rectangle_white_back.xy = 1;
  rectangle_white_back.mat.type = 4;
  rectangle_white_back.mat.albedo.type = 1;
  rectangle_white_back.mat.albedo.color1.x = 0.73;
  rectangle_white_back.mat.albedo.color1.y = 0.73;
  rectangle_white_back.mat.albedo.color1.z = 0.73;
  */
  
  //world.sphere[0] = sphere_ground;
  //world.sphere[1] = sphere_center;
  //world.sphere[2] = sphere_light;
  //world.aarectangle[0] = rectangle_green;
  //world.aarectangle[1] = rectangle_red;
  world.aarectangle[0] = rectangle_light;
  //world.aarectangle[3] = rectangle_white_top;
  //world.aarectangle[4] = rectangle_white_bottom;
  //world.aarectangle[5] = rectangle_white_back;
  
  PV_t background = {0,0,0};

  // Camera
  camera cam;
  PV_t lookfrom = {278, 278, -800};
  PV_t lookat = {278, 278, 0};
  PV_t vup = {0, 1, 0};
  PV_t dist_to_focus_diff = vec_diff(&lookfrom, &lookat);
  double dist_to_focus = 10;//vec_len(&dist_to_focus_diff);
  double aperture = 0.0;
  double vfov = 40;

  
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
	PV_t color = ray_color(&r, &background, &world, max_depth, i, j);
	pixel_color.x += color.x;
	pixel_color.y += color.y;
	pixel_color.z += color.z;
      }
      write_color(&pixel_color, samples_per_pixel);
    }
  }
  return 0;
};
 
