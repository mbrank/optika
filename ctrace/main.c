#include <stdlib.h>
#include <stdio.h>
#include <math.h>
//#include "vector.h"
#include "ray.h"
#include <stdbool.h>
#include "hittable_list.h"
#include "constants.h"
#include "sphere.h"
#include "camera.h"
#include "color.h"
#include "rtweekend.h"
PV_t ray_color(ray_t *r, hittable_list *world)
{
  hit_record rec;
  PV_t color;
  for (int i = 0; i < (int)(sizeof(&world)/4); i++) {
    double zero = 0;
    bool sphere_hit_checked = check_sphere_hit(&(world->sphere[i]),
					       r,
					       &zero,
					       &infinity,
					       &rec);
    if (sphere_hit_checked) {
      color.x = 0.5*(rec.normal.x + 1);
      color.y = 0.5*(rec.normal.y + 1);
      color.z = 0.5*(rec.normal.z + 1);
      break;
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

  // Image
  const auto double aspect_ratio = 16.0/9.0;
  const int image_width = 400;
  const int image_height = (int)(image_width/aspect_ratio); //static_cast<int>(image_width/aspect_ratio);
  const int samples_per_pixel = 100;

  hittable_list world;
  sphere_t sphere0;
  sphere0.center.x = 0; 
  sphere0.center.y = 0;
  sphere0.center.z = -1;
  sphere0.radius = 0.5;
  sphere_t sphere1;
  sphere1.center.x = 0; 
  sphere1.center.y = -100.5;
  sphere1.center.z = -1;
  sphere1.radius = 100;
  world.sphere[0] = sphere0;
  world.sphere[1] = sphere1;
  // Camera

  camera cam;
  camera_init(cam);
  //auto double viewport_height = 2.0;
  //auto double viewport_width = (aspect_ratio * viewport_height);
  //auto double focal_length = 1.0;
  //auto PV_t camera_origin; 
  //camera_origin.x = 0;
  //camera_origin.y = 0;
  //camera_origin.z = 0;
  //auto PV_t horizontal; 
  //horizontal.x = viewport_width;
  //horizontal.y = 0;
  //horizontal.z = 0;
  //auto PV_t vertical; 
  //vertical.x = 0;
  //vertical.y = viewport_height;
  //vertical.z = 0;
  //// Calculate lower left corner of camera
  //PV_t hor_divide = vec_divide(&horizontal, -2);
  //PV_t vert_divide = vec_divide(&vertical, -2);
  //PV_t scale_orig_hor = vec_sum(&camera_origin, &hor_divide);
  //PV_t scale_orig_hor_vert = vec_sum(&scale_orig_hor, &vert_divide);
  //PV_t neg_focal_length;
  //neg_focal_length.x = 0;
  //neg_focal_length.y = 0;
  //neg_focal_length.z = -1;
  //auto PV_t lower_left_corner = vec_sum(&scale_orig_hor_vert, &neg_focal_length);
  printf("P3\n%i %i\n255\n", image_width, image_height);
  for (int j=image_height-1; j>=0; j--) {
    for (int i=0; i<image_width; i++) {
      PV_t pixel_color;
      pixel_color.x = 0;
      pixel_color.y = 0;
      pixel_color.z = 0;
      for (int s = 0; s < samples_per_pixel; ++s) {
	auto double u = (double)i / (image_width-1);
	auto double v = (double)j / (image_height-1);
	ray_t r = camera_get_ray(&cam, u, v);
	PV_t color = ray_color(&r, &world);
	pixel_color.x += color.x;
	pixel_color.y += color.y;
	pixel_color.z += color.z;
      }
      write_color(&pixel_color, samples_per_pixel);

      //auto double u = (double)i / (image_width-1);
      //auto double v = (double)j / (image_height-1);
      //ray_t r;
      //r.origin.x = camera_origin.x;
      //r.origin.y = camera_origin.y;
      //r.origin.z = camera_origin.z;
      //r.direction.x = lower_left_corner.x + u*horizontal.x + v*vertical.x - camera_origin.x;
      //r.direction.y = lower_left_corner.y + u*horizontal.y + v*vertical.y - camera_origin.y;
      //r.direction.z = lower_left_corner.z + u*horizontal.z + v*vertical.z - camera_origin.z;
      //PV_t color = ray_color(&r, &world);
      //printf("%d %d %d\n",
      //     (int)(255.99*color.x),
      //     (int)(255.99*color.y),
      //     (int)(255.99*color.z));
    }
  }
  return 0;
};
 