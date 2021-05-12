#include "camera.h"

ray_t camera_get_ray(camera *cam, double u, double v){
  PV_t origin = cam->camera_origin;

  PV_t dir;
  dir.x = cam->lower_left_corner.x+u*cam->horizontal.x+v*cam->vertical.x-cam->camera_origin.x;
  dir.y = cam->lower_left_corner.y+u*cam->horizontal.y+v*cam->vertical.y-cam->camera_origin.y;
  dir.z = cam->lower_left_corner.z+u*cam->horizontal.z+v*cam->vertical.z-cam->camera_origin.z;

  ray_t ray;
  ray.origin = origin;
  ray.direction = dir;
  return ray;
  
};

void camera_init(camera cam){
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
  PV_t neg_focal_length;
  neg_focal_length.x = 0;
  neg_focal_length.y = 0;
  neg_focal_length.z = -1;
  cam.lower_left_corner = vec_sum(&scale_orig_hor_vert, &neg_focal_length);

}
