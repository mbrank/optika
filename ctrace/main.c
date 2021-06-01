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

PV_t ray_color(ray_t *r, hittable_list *world, int depth, int i, int j)
{
  //printf("i: %d, j: %d\n", i, j);
  // check if depth exceeded
  if (depth <= 0) {
	//printf("depth exceeded\n");
      PV_t depth_exceeded;
      depth_exceeded.x = 0;
      depth_exceeded.y = 0;
      depth_exceeded.z = 0;
      return depth_exceeded;
    }
  //printf("depth exceeded1ss\n");
  // if depth not exceeded check intersection
  hit_record rec;
  rec.t = infinity;
  PV_t color;
  //printf("sizeof world: %d\n", sizeof(&world));
  //for (int i = 0; i < (int)(sizeof(&world)/4); i++) {
  //bool sphere_hit_checked;
  //double shortest_dist = 1e8;
  //double shortest_previous = 1e8;
  //double shortest_so_far = 1e7;
  int sphere_hit_checked = -1;
  int current_hit = -1;
  //printf("depth exceeded1\n");
  // iterate over objects to find shortest hit
  for (int k = 0; k < 4; k++) {
    double zero = 0;
  	//printf("k: %d r_origin: x=%f, y=%f, z=%f\n", k, r->origin.x, r->origin.y, r->origin.z);
    sphere_hit_checked = check_sphere_hit(&(world->sphere[k]),
										  r,
										  &zero,
										  &rec.t,
										  &rec, k);
	if (sphere_hit_checked > -1) {
	  current_hit = sphere_hit_checked;
	}
	//printf("k=%d, rec->p: x=%f, y=%f, z=%f\n", k, rec.p.x, rec.p.y, rec.p.z);
	//printf("shortest_dist: %f\n", shortest_dist);
	  //if (shortest_dist > 0)
	  //{
	  //  printf("shortest_dist: %f, i=%d\n, j=%d, k=%d, depth=%d\n",
	  //		 shortest_dist, i, j, k, depth);
	  //}
	  //printf("hitted_obj_id: %d\n", hitted_obj_id);
  }
  //printf("depth exceeded2\n");

    if (current_hit > -1) {
	  //printf("hitted_obj_id: %d, i: %d, j: %d, depth: %d, attenuation - x: %f, y: %f, z: %f, radius: %f\n",
	  //	 hitted_obj_id, i, j, depth,
	  //	 world->sphere[hitted_obj_id].mat.albedo.x,
	  //	 world->sphere[hitted_obj_id].mat.albedo.y,
	  //	 world->sphere[hitted_obj_id].mat.albedo.z,
	  //	 world->sphere[hitted_obj_id].radius);
	  //printf("hitted_obj_id: %d\n", hitted_obj_id);
	  bool mat_ref = calculate_material_reflections(&(world->sphere[current_hit].mat),
													r,
													&(world->sphere[current_hit].mat.albedo),
													&rec);
	  if (mat_ref) {
		//printf("depth exceeded3\n");

		//return world->sphere[current_hit].mat.albedo;
		PV_t current_ray_color = ray_color(&(world->sphere[current_hit].mat.scattered), world, depth-1, i, j);
		PV_t color_to_return = {current_ray_color.x*world->sphere[current_hit].mat.attenuation.x,
								current_ray_color.y*world->sphere[current_hit].mat.attenuation.y,
								current_ray_color.z*world->sphere[current_hit].mat.attenuation.z};
		//return ray_color(&(world->sphere[current_hit].mat.scattered), world, depth-1, i, j);
		return color_to_return;
	  }
	  PV_t color = {0, 0, 0};
	  return color; 
    }
	//printf("depth exceeded4\n");
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
  return color;
}
  

int main(int argc, char *argv[]) {

  // To create new random number and not repeated
  srand(time(NULL)); /* mora bit za random??? */

  // Image
  const auto double aspect_ratio = 16.0/9.0;
  const int image_width = 400;
  const int image_height = (int)(image_width/aspect_ratio); //static_cast<int>(image_width/aspect_ratio);
  const int samples_per_pixel = 100;
  const int max_depth = 5;
  
  hittable_list world;

  // sphere ground
  sphere_t sphere0;
  sphere0.center.x = 0; 
  sphere0.center.y = -100.5;
  sphere0.center.z = -1;
  sphere0.radius = 100;
  sphere0.mat.type = 1;
  sphere0.mat.albedo.x = 0.8;
  sphere0.mat.albedo.y = 0.8;
  sphere0.mat.albedo.z = 0.0;
  // sphere center
  sphere_t sphere1;
  sphere1.center.x = 0; 
  sphere1.center.y = 0;
  sphere1.center.z = -1;
  sphere1.radius = 0.5;
  sphere1.mat.type = 1;
  sphere1.mat.albedo.x = 0.7;
  sphere1.mat.albedo.y = 0.3;
  sphere1.mat.albedo.z = 0.3;
  // sphere left
  sphere_t sphere2;
  sphere2.center.x = -1; 
  sphere2.center.y = 0;
  sphere2.center.z = -1;
  sphere2.radius = 0.5;
  sphere2.mat.type = 2;
  sphere2.mat.albedo.x = 0.8;
  sphere2.mat.albedo.y = 0.8;
  sphere2.mat.albedo.z = 0.8;
  // sphere right
  sphere_t sphere3;
  sphere3.center.x = 1; 
  sphere3.center.y = 0;
  sphere3.center.z = -1;
  sphere3.radius = 0.5;
  sphere3.mat.type = 2;
  sphere3.mat.albedo.x = 0.8;
  sphere3.mat.albedo.y = 0.6;
  sphere3.mat.albedo.z = 0.2;

  world.sphere[0] = sphere0;
  world.sphere[1] = sphere2;
  world.sphere[2] = sphere1;
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
 
