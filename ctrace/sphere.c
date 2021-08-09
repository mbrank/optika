//#include "ray.h"
#include "sphere.h"
#include "hittable.h"
#include "constants.h"

void get_sphere_uv(PV_t *p, double *u, double *v)
{
  double theta = acos(-p->y);
  double phi = atan2(-p->z, p->x)+pi;
  *u = phi / (2*pi);
  *v = theta / pi;
}
