//camera.h
#ifndef CAMERA_H
#define CAMERA_H
#include "ray.h"
#include "rtweekend.h"

typedef struct camera_type{
  PV_t lookfrom;
  PV_t lookat;
  PV_t vup;
  double vfov;
  double aspect_ratio;
  double theta;
  double h;
  double viewport_height;
  double viewport_width;
  //double focal_length;
  PV_t camera_origin;
  PV_t horizontal; 
  PV_t vertical; 
  PV_t lower_left_corner;
  double lens_radius;
  PV_t w;
  PV_t u;
  PV_t v;
} camera;


ray_t camera_get_ray(camera *cam, double u, double v);
void initialize_camera(camera *cam, PV_t lookfrom, PV_t lookat, PV_t vup,
					   double vfov, double aspect_ratio, double aperture,
					   double dist_to_focus);

//camera *camera_init();

#endif
