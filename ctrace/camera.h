//camera.h
#ifndef CAMERA_H
#define CAMERA_H
#include "ray.h"

typedef struct camera_type{
  double aspect_ratio;
  double viewport_height;
  double viewport_width;
  double focal_length;

  PV_t camera_origin;

  PV_t horizontal; 

  PV_t vertical; 

  PV_t lower_left_corner;

} camera;


ray_t camera_get_ray(camera *cam, double u, double v);

void camera_init();

#endif
