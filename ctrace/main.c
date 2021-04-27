#include <stdlib.h>
#include <stdio.h>
#include <math.h>
//#include "vector.h"
#include "ray.h"
#include <stdbool.h>
#include "hittable_list.h"
#include "constants.h"
#include "sphere.h"
//#include "light.h"

//double hit_sphere(PV_t *center, double radius, ray_t *r)
//{
//  // check if sphere is hit
//  
//  PV_t oc = vec_diff(&(r->origin), center);
//  //double a = vec_dot(&(r->direction), &(r->direction));
//  //double b = vec_dot(&oc, &(r->direction)) * 2.0;
//  //double c = vec_dot(&oc, &oc) - radius*radius;
//  //double discriminant = b*b - 4*a*c;
//  double a = length_squared(&(r->direction));
//  double half_b = vec_dot(&oc, &(r->direction));
//  double c = length_squared(&oc) - radius*radius;
//  double discriminant = half_b*half_b - a*c;
//  if (discriminant < 0)
//    {
//    return -1.0;
//    }
//  else
//    {
//      return (-half_b - sqrt(discriminant))/(2.0*a);
//    }
//}


PV_t ray_color(ray_t *r, hittable_list *world)
{
  //printf("test0");  
  hit_record rec;
  //printf("test1 %lu", sizeof(world));
  PV_t color;
  for (int i = 0; i < (int)(sizeof(&world)/4); i++) {
    //printf("test2 what is i:%d", (int)(sizeof(&world)/4));
    double zero = 0;
    bool sphere_hit_checked = check_sphere_hit(&(world->sphere[i]), r, &zero, &infinity, &rec);
    //printf("test3");
    if (sphere_hit_checked) {
      color.x = 0.5*(rec.normal.x + 1);
      color.y = 0.5*(rec.normal.y + 1);
      color.z = 0.5*(rec.normal.z + 1);
      printf("-------------------\n");
      printf("test4: %f\n", color.x);
      printf("test4: %f\n", color.y);
      printf("test4: %f\n", color.z);
      //return color;
      break;
    }
    //printf("test5");
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
    //return vec_sum(&scaled1, &scaled2);
  }
  return color;
}
  
  //  PV_t sphere_center;
  //  sphere_center.x = 0;
  //  sphere_center.y = 0;
  //  sphere_center.z = -1;
  //  double t = hit_sphere(&sphere_center, 0.5, r);
  //  if (t > 0.0) {
  //
  //    PV_t at_vec = at(r, t);
  //    PV_t at_diff;
  //    at_diff.x = 0;
  //    at_diff.y = 0;
  //    at_diff.z = +1;
  //    
  //    PV_t N_unit = unit_vector(&at_vec);
  //    PV_t N = vec_sum(&N_unit, &at_diff);
  //    PV_t color;
  //    color.x = 0.5*(N.x+1);
  //    color.y = 0.5*(N.y+1);
  //    color.z = 0.5*(N.z+1);
  //    return  color;
  //  }
  //  PV_t unit_direction = unit_vector(&r->direction);
  //  t = 0.5*(unit_direction.y + 1.0);
  //  PV_t color1;
  //  color1.x = 1.0;
  //  color1.y = 1.0;
  //  color1.z = 1.0;
  //  PV_t color2;
  //  color2.x = 0.5;
  //  color2.y = 0.7;
  //  color2.z = 1.0;
  //  PV_t scaled1 = vec_scale(&color1, 1-t);
  //  PV_t scaled2 = vec_scale(&color2, t);
  //  return vec_sum(&scaled1, &scaled2);
  //}

int main(int argc, char *argv[]) {

  // Image
  const auto double aspect_ratio = 16.0/9.0;
  const int image_width = 400;
  const int image_height = (int)(image_width/aspect_ratio); //static_cast<int>(image_width/aspect_ratio);

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
  auto double viewport_height = 2.0;
  auto double viewport_width = (aspect_ratio * viewport_height);
  auto double focal_length = 1.0;

  auto PV_t camera_origin; 
  camera_origin.x = 0;
  camera_origin.y = 0;
  camera_origin.z = 0;

  auto PV_t horizontal; 
  horizontal.x = viewport_width;
  horizontal.y = 0;
  horizontal.z = 0;

  auto PV_t vertical; 
  vertical.x = 0;
  vertical.y = viewport_height;
  vertical.z = 0;

  // Calculate lower left corner of camera
  //printf("viewport_width:%f viewport_height:%f\n255\n", viewport_width, viewport_height);
  PV_t hor_divide = vec_divide(&horizontal, -2);
  PV_t vert_divide = vec_divide(&vertical, -2);
  PV_t scale_orig_hor = vec_sum(&camera_origin, &hor_divide);
  PV_t scale_orig_hor_vert = vec_sum(&scale_orig_hor, &vert_divide);
  PV_t neg_focal_length;
  neg_focal_length.x = 0;
  neg_focal_length.y = 0;
  neg_focal_length.z = -1;
  auto PV_t lower_left_corner = vec_sum(&scale_orig_hor_vert, &neg_focal_length);
  printf("P3\n%i %i\n255\n", image_width, image_height);
  for (int j=image_height-1; j>=0; j--) {
    for (int i=0; i<image_width; i++) {
      auto double u = (double)i / (image_width-1);
      auto double v = (double)j / (image_height-1);

      ray_t r;
      r.origin.x = camera_origin.x;
      r.origin.y = camera_origin.y;
      r.origin.z = camera_origin.z;

      r.direction.x = lower_left_corner.x + u*horizontal.x + v*vertical.x - camera_origin.x;
      r.direction.y = lower_left_corner.y + u*horizontal.y + v*vertical.y - camera_origin.y;
      r.direction.z = lower_left_corner.z + u*horizontal.z + v*vertical.z - camera_origin.z;
      //printf("-------------------------------------------------------\n");
      //printf("lower_left_corner.x=%f\n", lower_left_corner.x);
      //printf("lower_left_corner.y=%f\n", lower_left_corner.y);
      //printf("lower_left_corner.z=%f\n", lower_left_corner.z);
      //printf("r.direction.x=%f\n", r.direction.x);
      //printf("r.direction.y=%f\n", r.direction.y);
      //printf("r.direction.z=%f\n", r.direction.z);
      //printf("u=%f\n", u);
      //printf("image_width=%d\n", image_width);
      //printf("i=%f\n", (double)i);
      //printf("j=%d, i=%d\n", j, i);

      PV_t color = ray_color(&r, &world);
      
      printf("%d %d %d\n",
           (int)(255.99*color.x),
           (int)(255.99*color.y),
           (int)(255.99*color.z));
    }
  }
  return 0;
};
 
