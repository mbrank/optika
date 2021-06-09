#include "camera.h"

ray_t camera_get_ray(camera *cam, double s, double t){

  PV_t rnd_unit_disc = random_in_unit_disc();
  PV_t rd;
  rd.x = cam->lens_radius*rnd_unit_disc.x;
  rd.y = cam->lens_radius*rnd_unit_disc.y;
  rd.z = cam->lens_radius*rnd_unit_disc.z;

  PV_t offset;
  offset.x = cam->u.x * rd.x + cam->v.x * rd.y;
  offset.y = cam->u.y * rd.x + cam->v.y * rd.y;
  offset.z = cam->u.z * rd.x + cam->v.z * rd.y;

  PV_t origin = cam->camera_origin;
  ray_t ray;
  ray.origin.x = origin.x + offset.x;  
  ray.origin.y = origin.y + offset.y;
  ray.origin.z = origin.z + offset.z;

  ray.direction.x = cam->lower_left_corner.x + s*cam->horizontal.x + t*cam->vertical.x - origin.x - offset.x;
  ray.direction.y = cam->lower_left_corner.y + s*cam->horizontal.y + t*cam->vertical.y - origin.y - offset.y;	
  ray.direction.z = cam->lower_left_corner.z + s*cam->horizontal.z + t*cam->vertical.z - origin.z - offset.z;	

  return ray;
  
};

void initialize_camera(camera *cam, PV_t lookfrom, PV_t lookat, PV_t vup,
					   double vfov, double aspect_ratio,
					   double aperture, double focus_dist)
{
  cam->vfov = vfov;
  cam->theta = degrees_to_radians(vfov);
  cam->aspect_ratio = aspect_ratio;
  cam->h = tan(cam->theta/2);
  cam->viewport_height = 2.0*cam->h;
  cam->viewport_width = (aspect_ratio * cam->viewport_height);

  PV_t look_from_at_substraction;
  look_from_at_substraction.x = lookfrom.x - lookat.x;
  look_from_at_substraction.y = lookfrom.y - lookat.y;
  look_from_at_substraction.z = lookfrom.z - lookat.z;
  
  cam->w = unit_vector(&look_from_at_substraction);

  PV_t cross_vup_w = vec_cross(&vup, &cam->w);
  cam->u = unit_vector(&cross_vup_w);

  cam->v = vec_cross(&cam->w, &cam->u);

  cam->camera_origin.x = lookfrom.x;
  cam->camera_origin.y = lookfrom.y;
  cam->camera_origin.z = lookfrom.z;
  
  cam->horizontal.x = focus_dist*cam->viewport_width*cam->u.x;//vec_scale(&u, cam->viewport_width);
  cam->horizontal.y = focus_dist*cam->viewport_width*cam->u.y;
  cam->horizontal.z = focus_dist*cam->viewport_width*cam->u.z;
  

  cam->vertical.x = focus_dist*cam->viewport_height*cam->v.x;//vec_scale(&u, cam->viewport_width);
  cam->vertical.y = focus_dist*cam->viewport_height*cam->v.y;
  cam->vertical.z = focus_dist*cam->viewport_height*cam->v.z;

  //cam->vertical = vec_scale(&cam->v, cam->viewport_height);
  
  // Calculate lower left corner of camera
  PV_t hor_divide = vec_divide(&cam->horizontal, -2);
  PV_t vert_divide = vec_divide(&cam->vertical, -2);
  PV_t scale_orig_hor = vec_sum(&cam->camera_origin, &hor_divide);
  PV_t scale_orig_hor_vert = vec_sum(&scale_orig_hor, &vert_divide);
  PV_t neg_w = vec_scale(&cam->w, -1*focus_dist); // multiply w with -1
  cam->lower_left_corner = vec_sum(&scale_orig_hor_vert, &neg_w);

  cam->lens_radius = aperture/2;
}

//camera *camera_init(){
//  camera *cam = malloc(sizeof(*cam));
//
//  if (!cam) {
//        perror("malloc failed");
//        exit(1);
//    }
//  cam->aspect_ratio = 16.0/9.0;
//  cam->viewport_height = 2.0;
//  cam->viewport_width = (cam->aspect_ratio * cam->viewport_height);
//  cam->focal_length = 1.0;
//
//  cam->camera_origin.x = 0;
//  cam->camera_origin.y = 0;
//  cam->camera_origin.z = 0;
//
//  cam->horizontal.x = cam->viewport_width;
//  cam->horizontal.y = 0;
//  cam->horizontal.z = 0;
//
//  cam->vertical.x = 0;
//  cam->vertical.y = cam->viewport_height;
//  cam->vertical.z = 0;
//
//  // Calculate lower left corner of camera
//  PV_t hor_divide = vec_divide(&(cam->horizontal), -2);
//  PV_t vert_divide = vec_divide(&(cam->vertical), -2);
//  PV_t scale_orig_hor = vec_sum(&(cam->camera_origin), &hor_divide);
//  PV_t scale_orig_hor_vert = vec_sum(&scale_orig_hor, &vert_divide);
//  PV_t neg_focal_length;
//  neg_focal_length.x = 0;
//  neg_focal_length.y = 0;
//  neg_focal_length.z = -1;
//  cam->lower_left_corner = vec_sum(&scale_orig_hor_vert, &neg_focal_length);
//  return cam;
//}
