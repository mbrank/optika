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
  rec.t = infinity;
  int sphere_hit_checked = -1;
  int current_hit = -1;
  int current_hit_rectangle = -1;
  int current_hit_box = -1;
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
  for (int l = 0; l < 18; l++)
	{
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
  // check if box is hit before sphere
  for (int b = 0; b<0; b++) {
    int box_hit_checked = check_box_hit(&(world->box[b]),
										r,
										&zero,
										&rec.t,
										&rec, b);
	if (box_hit_checked > -1) {
	  current_hit_box = box_hit_checked;
	  current_hit_rectangle = -1;
	  current_hit = -1;
	}
  }

  
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
		if (world->aarectangle[current_hit_rectangle].mat.scattered.direction.x == 0 &&
			world->aarectangle[current_hit_rectangle].mat.scattered.direction.y == 0 &&
			world->aarectangle[current_hit_rectangle].mat.scattered.direction.z == 0 )
		  {


			PV_t color_to_return = world->aarectangle[current_hit_rectangle].mat.attenuation;
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
  else if (current_hit_box > -1) {
    bool mat_ref = calculate_material_reflections(&(world->box[current_hit_box].mat),
													r,
													&(world->box[current_hit_box].mat.albedo),
													&rec);
	if (mat_ref) {
		if (world->box[current_hit_box].mat.scattered.direction.x == 0 &&
			world->box[current_hit_box].mat.scattered.direction.y == 0 &&
			world->box[current_hit_box].mat.scattered.direction.z == 0 )
		  {
			PV_t color_to_return = world->box[current_hit_box].mat.attenuation;
		  return color_to_return;
		}
		else{
		  PV_t current_ray_color = ray_color(&(world->box[current_hit_box].mat.scattered),
										   background,
										   world,
										   depth-1, i, j);
		
		PV_t color_to_return = {world->box[current_hit_box].mat.emitted.x + current_ray_color.x*
								world->box[current_hit_box].mat.attenuation.x,
								world->box[current_hit_box].mat.emitted.y + current_ray_color.y*
								world->box[current_hit_box].mat.attenuation.y,
								world->box[current_hit_box].mat.emitted.z + current_ray_color.z*
								world->box[current_hit_box].mat.attenuation.z};
		return color_to_return;
		  }
		}
      
      PV_t color = {0, 0, 0};
      return color;     
  }
 else{
	return *background;
	}
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

  sphere_t sphere_center;
  sphere_center.center.x = 300; 
  sphere_center.center.y = 300;
  sphere_center.center.z = 300;
  sphere_center.radius = 100;
  sphere_center.mat.type = 1;
  sphere_center.mat.albedo.type = 1;
  sphere_center.mat.albedo.color1.x = 0.115;
  sphere_center.mat.albedo.color1.y = 0.35;
  sphere_center.mat.albedo.color1.z = 0.45;

  // aarectangle green
  aarectangle_t rectangle_green;
  rectangle_green.y0 = 0;
  rectangle_green.y1 = 555;
  rectangle_green.z0 = 0;
  rectangle_green.z1 = 555;
  rectangle_green.k = 555;
  rectangle_green.x0 = rectangle_green.k-10;
  rectangle_green.x1 = rectangle_green.k+10;
  rectangle_green.yz = 1;
  rectangle_green.mat.type = 1;
  rectangle_green.mat.albedo.type = 1;
  rectangle_green.mat.albedo.color1.x = 0.12;
  rectangle_green.mat.albedo.color1.y = 0.45;
  rectangle_green.mat.albedo.color1.z = 0.15;
  
  // aarectangle red
  aarectangle_t rectangle_red;
  rectangle_red.y0 = 0;
  rectangle_red.y1 = 5550;
  rectangle_red.z0 = 0;
  rectangle_red.z1 = 5550;
  rectangle_red.k = 0;
  rectangle_red.yz = 1;
  rectangle_red.x0 = rectangle_red.k-10;
  rectangle_red.x1 = rectangle_red.k+10;
  rectangle_red.mat.type = 1;
  rectangle_red.mat.albedo.type = 1;
  rectangle_red.mat.albedo.color1.x = 0.65;
  rectangle_red.mat.albedo.color1.y = 0.05;
  rectangle_red.mat.albedo.color1.z = 0.05;
  
  
  // aarectangle light
  aarectangle_t rectangle_light;
  rectangle_light.x0 = 213;
  rectangle_light.x1 = 343;
  rectangle_light.z0 = 227;
  rectangle_light.z1 = 332;
  rectangle_light.k = 554;
  rectangle_light.y0 = rectangle_light.k-10;
  rectangle_light.y1 = rectangle_light.k+10;
  rectangle_light.xz = 1;
  rectangle_light.mat.type = 4;
  rectangle_light.mat.albedo.type = 1;
  rectangle_light.mat.albedo.color1.x = 15;
  rectangle_light.mat.albedo.color1.y = 15;
  rectangle_light.mat.albedo.color1.z = 15;

  
  // aarectangle white_bottom
  aarectangle_t rectangle_white_bottom;
  rectangle_white_bottom.x0 = 0;
  rectangle_white_bottom.x1 = 555;
  rectangle_white_bottom.z0 = 0;
  rectangle_white_bottom.z1 = 555;
  rectangle_white_bottom.k = 0;
  rectangle_white_bottom.xz = 1;
  //rectangle_white_bottom.y0 = rectangle_white_bottom.k-10;
  //rectangle_white_bottom.y1 = rectangle_white_bottom.k+10;
  rectangle_white_bottom.mat.type = 1;
  rectangle_white_bottom.mat.albedo.type = 1;
  rectangle_white_bottom.mat.albedo.color1.x = 0.73;
  rectangle_white_bottom.mat.albedo.color1.y = 0.73;
  rectangle_white_bottom.mat.albedo.color1.z = 0.73;
  
  // aarectangle white_top
  aarectangle_t rectangle_white_top;
  rectangle_white_top.x0 = 0;
  rectangle_white_top.x1 = 555;
  rectangle_white_top.z0 = 0;
  rectangle_white_top.z1 = 555;
  rectangle_white_top.k = 555;
  rectangle_white_top.xz = 1;
  rectangle_white_top.y0 = rectangle_white_top.k-10;
  rectangle_white_top.y1 = rectangle_white_top.k+10;
  rectangle_white_top.mat.type = 1;
  rectangle_white_top.mat.albedo.type = 1;
  rectangle_white_top.mat.albedo.color1.x = 0.73;
  rectangle_white_top.mat.albedo.color1.y = 0.73;
  rectangle_white_top.mat.albedo.color1.z = 0.73;

  
  // aarectangle white_back
  aarectangle_t rectangle_white_back;
  rectangle_white_back.x0 = 0;
  rectangle_white_back.x1 = 555;
  rectangle_white_back.y0 = 0;
  rectangle_white_back.y1 = 555;
  rectangle_white_back.k = 555;
  rectangle_white_back.xy = 1;
  rectangle_white_back.z0 = rectangle_white_back.k-10;
  rectangle_white_back.z1 = rectangle_white_back.k+10;
  rectangle_white_back.mat.type = 1;
  rectangle_white_back.mat.albedo.type = 1;
  rectangle_white_back.mat.albedo.color1.x = 0.73;
  rectangle_white_back.mat.albedo.color1.y = 0.73;
  rectangle_white_back.mat.albedo.color1.z = 0.73;

  box_t box1;
  box1.p0.x = 130;
  box1.p0.y = 0;
  box1.p0.z = 65;
  box1.p1.x = 295;
  box1.p1.y = 165;
  box1.p1.z = 230;
  box1.mat.type = 1;
  box1.mat.albedo.type = 1;
  box1.mat.albedo.color1.x = 0.73;
  box1.mat.albedo.color1.y = 0.73;
  box1.mat.albedo.color1.z = 0.73;

  box_t box2;
  box2.p0.x = 265;
  box2.p0.y = 0;
  box2.p0.z = 295;
  box2.p1.x = 430;
  box2.p1.y = 330;
  box2.p1.z = 460;
  box2.mat.type = 1;
  box2.mat.albedo.type = 1;
  box2.mat.albedo.color1.x = 0.73;
  box2.mat.albedo.color1.y = 0.73;
  box2.mat.albedo.color1.z = 0.73;
  
  //world.sphere[0] = sphere_center;
  world.sphere[0] = sphere_center;
  //world.sphere[2] = sphere_light;
  //world.aarectangle[0] = rectangle_green;
  //world.aarectangle[1] = rectangle_red;
  world.aarectangle[0] = rectangle_light;
  world.aarectangle[1] = rectangle_green;
  world.aarectangle[2] = rectangle_white_top;
  world.aarectangle[3] = rectangle_white_back;
  world.aarectangle[4] = rectangle_red;
  world.aarectangle[5] = rectangle_white_bottom;

  // Boxes test
  aarectangle_t xy_rect1;
  xy_rect1.xy = 1;
  xy_rect1.x0 = 265;
  xy_rect1.x1 = 430;
  xy_rect1.y0 = 0;
  xy_rect1.y1 = 330;
  xy_rect1.k = 460;
  xy_rect1.mat.type = 1;
  xy_rect1.mat.albedo.type = 1;
  xy_rect1.mat.albedo.color1.x = 0.73;
  xy_rect1.mat.albedo.color1.y = 0.73;
  xy_rect1.mat.albedo.color1.z = 0.73;
  world.aarectangle[6] = xy_rect1;

  aarectangle_t xy_rect2;
  xy_rect2.xy = 1;
  xy_rect2.x0 = 265;
  xy_rect2.x1 = 430;
  xy_rect2.y0 = 0;
  xy_rect2.y1 = 330;
  xy_rect2.k = 295;
  xy_rect2.mat.type = 1;
  xy_rect2.mat.albedo.type = 1;
  xy_rect2.mat.albedo.color1.x = 0.73;
  xy_rect2.mat.albedo.color1.y = 0.73;
  xy_rect2.mat.albedo.color1.z = 0.73;
  world.aarectangle[7] = xy_rect2;

  // XZ
  aarectangle_t xz_rect3;
  xz_rect3.xz = 1;
  xz_rect3.x0 = 265;
  xz_rect3.x1 = 430;
  xz_rect3.z0 = 295;
  xz_rect3.z1 = 460;
  xz_rect3.k = 330;
  xz_rect3.mat.type = 1;
  xz_rect3.mat.albedo.type = 1;
  xz_rect3.mat.albedo.color1.x = 0.73;
  xz_rect3.mat.albedo.color1.y = 0.73;
  xz_rect3.mat.albedo.color1.z = 0.73;
  world.aarectangle[8] = xz_rect3;

  aarectangle_t xz_rect4;
  xz_rect4.xz = 1;
  xz_rect4.x0 = 265;
  xz_rect4.x1 = 430;
  xz_rect4.z0 = 295;
  xz_rect4.z1 = 460;
  xz_rect4.k = 0;
  xz_rect4.mat.type = 1;
  xz_rect4.mat.albedo.type = 1;
  xz_rect4.mat.albedo.color1.x = 0.73;
  xz_rect4.mat.albedo.color1.y = 0.73;
  xz_rect4.mat.albedo.color1.z = 0.73;
  world.aarectangle[9] = xz_rect4;

  // XZ
  aarectangle_t yz_rect5;
  yz_rect5.yz = 1;
  yz_rect5.y0 = 0;
  yz_rect5.y1 = 330;
  yz_rect5.z0 = 295;
  yz_rect5.z1 = 460;
  yz_rect5.k = 430;
  yz_rect5.mat.type = 1;
  yz_rect5.mat.albedo.type = 1;
  yz_rect5.mat.albedo.color1.x = 0.73;
  yz_rect5.mat.albedo.color1.y = 0.73;
  yz_rect5.mat.albedo.color1.z = 0.73;
  world.aarectangle[10] = yz_rect5;

  aarectangle_t yz_rect6;
  yz_rect6.yz = 1;
  yz_rect6.y0 = 0;
  yz_rect6.y1 = 330;
  yz_rect6.z0 = 295;
  yz_rect6.z1 = 460;
  yz_rect6.k = 265;
  yz_rect6.mat.type = 1;
  yz_rect6.mat.albedo.type = 1;
  yz_rect6.mat.albedo.color1.x = 0.73;
  yz_rect6.mat.albedo.color1.y = 0.73;
  yz_rect6.mat.albedo.color1.z = 0.73;
  world.aarectangle[11] = yz_rect6;


  // Boxes test - small
  aarectangle_t xy_smallrect1;
  xy_smallrect1.xy = 1;
  xy_smallrect1.x0 = 130;
  xy_smallrect1.x1 = 295;
  xy_smallrect1.y0 = 0;
  xy_smallrect1.y1 = 165;
  xy_smallrect1.k = 230;
  xy_smallrect1.mat.type = 1;
  xy_smallrect1.mat.albedo.type = 1;
  xy_smallrect1.mat.albedo.color1.x = 0.73;
  xy_smallrect1.mat.albedo.color1.y = 0.73;
  xy_smallrect1.mat.albedo.color1.z = 0.73;
  world.aarectangle[12] = xy_smallrect1;

  aarectangle_t xy_smallrect2;
  xy_smallrect2.xy = 1;
  xy_smallrect2.x0 = 130;
  xy_smallrect2.x1 = 295;
  xy_smallrect2.y0 = 0;
  xy_smallrect2.y1 = 165;
  xy_smallrect2.k = 65;
  xy_smallrect2.mat.type = 1;
  xy_smallrect2.mat.albedo.type = 1;
  xy_smallrect2.mat.albedo.color1.x = 0.73;
  xy_smallrect2.mat.albedo.color1.y = 0.73;
  xy_smallrect2.mat.albedo.color1.z = 0.73;
  world.aarectangle[13] = xy_smallrect2;

  // XZ
  aarectangle_t xz_smallrect3;
  xz_smallrect3.xz = 1;
  xz_smallrect3.x0 = 130;
  xz_smallrect3.x1 = 295;
  xz_smallrect3.z0 = 65;
  xz_smallrect3.z1 = 230;
  xz_smallrect3.k = 165;
  xz_smallrect3.mat.type = 1;
  xz_smallrect3.mat.albedo.type = 1;
  xz_smallrect3.mat.albedo.color1.x = 0.73;
  xz_smallrect3.mat.albedo.color1.y = 0.73;
  xz_smallrect3.mat.albedo.color1.z = 0.73;
  world.aarectangle[14] = xz_smallrect3;

  aarectangle_t xz_smallrect4;
  xz_smallrect4.xz = 1;
  xz_smallrect4.x0 = 130;
  xz_smallrect4.x1 = 295;
  xz_smallrect4.z0 = 65;
  xz_smallrect4.z1 = 230;
  xz_smallrect4.k = 0;
  xz_smallrect4.mat.type = 1;
  xz_smallrect4.mat.albedo.type = 1;
  xz_smallrect4.mat.albedo.color1.x = 0.73;
  xz_smallrect4.mat.albedo.color1.y = 0.73;
  xz_smallrect4.mat.albedo.color1.z = 0.73;
  world.aarectangle[15] = xz_smallrect4;

  // XZ
  aarectangle_t yz_smallrect5;
  yz_smallrect5.yz = 1;
  yz_smallrect5.y0 = 0;
  yz_smallrect5.y1 = 165;
  yz_smallrect5.z0 = 295;
  yz_smallrect5.z1 = 230;
  yz_smallrect5.k = 295;
  yz_smallrect5.mat.type = 1;
  yz_smallrect5.mat.albedo.type = 1;
  yz_smallrect5.mat.albedo.color1.x = 0.73;
  yz_smallrect5.mat.albedo.color1.y = 0.73;
  yz_smallrect5.mat.albedo.color1.z = 0.73;
  world.aarectangle[16] = yz_smallrect5;

  aarectangle_t yz_smallrect6;
  yz_smallrect6.yz = 1;
  yz_smallrect6.y0 = 0;
  yz_smallrect6.y1 = 165;
  yz_smallrect6.z0 = 295;
  yz_smallrect6.z1 = 230;
  yz_smallrect6.k = 130;
  yz_smallrect6.mat.type = 1;
  yz_smallrect6.mat.albedo.type = 1;
  yz_smallrect6.mat.albedo.color1.x = 0.73;
  yz_smallrect6.mat.albedo.color1.y = 0.73;
  yz_smallrect6.mat.albedo.color1.z = 0.73;
  world.aarectangle[17] = yz_smallrect6;
  
  //world.box[0] = box1;
  //world.box[1] = box2;
  
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
 
