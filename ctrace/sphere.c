//#include "ray.h"
#include "sphere.h"

void get_sphere_uv(PV_t *p, double *u, double *v)
{
  // calculate texture coordinates of the sphere
  double theta = acos(-p->y);
  double phi = atan2(-p->z, p->x)+pi;
  *u = phi / (2*pi);
  *v = theta / pi;
}
