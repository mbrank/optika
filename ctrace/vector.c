//vector.c
#include "vector.h"
#include "math.h"
#include "time.h"
#include <stdbool.h>
#include "rtweekend.h"

//vector sum function 
PV_t vec_sum(const PV_t *v1, const PV_t *v2)   
{
PV_t v3 = {v1->x + v2->x, v1->y + v2->y, v1->z + v2->z};
  return v3;
}

//difference between 2 vectors
PV_t vec_diff(PV_t *v1, PV_t *v2)
{
    PV_t v3 = {v1->x - v2->x, v1->y - v2->y, v1->z - v2->z };
   return v3;   
}

//dot product of 2 vectors
double vec_dot(PV_t *v1, PV_t *v2) 
{
  return v1->x * v2->x + v1->y * v2->y + v1->z * v2->z;
}

//cross product of 2 vectors
PV_t vec_cross(PV_t *v1, PV_t *v2) 
{
  PV_t cross;
  cross.x = v1->y*v2->z - v1->z*v2->y; 
  cross.y = v1->z*v2->x - v1->x*v2->z;
  cross.z = v1->x*v2->y - v1->y*v2->x;
  return cross;
}

//scale a vector by a factor
PV_t vec_scale(PV_t *v1, double fact)
{	
	PV_t scale = {(v1->x)*fact, (v1->y)*fact, (v1->z)*fact};
	return scale;
}

double vec_len(PV_t *v1)  /* Vector whose length is desired */
{
	double v = sqrt((v1->x * v1->x) + (v1->y * v1->y) + (v1->z * v1->z));
	return(v);
}

PV_t vec_divide(PV_t *v1, double fact)
{	
	PV_t scale = {(v1->x)/fact, (v1->y)/fact, (v1->z)/fact};
	return scale;
}

double length_squared(PV_t *v1)
{
  return pow((v1->x), 2) + pow((v1->y), 2) + pow((v1->z), 2);
}

PV_t random_vector() /* returns random vector */
{
  //srand(time(NULL)); /* mora bit za random??? */
  PV_t rvec;
  rvec.x = (double)rand()/(double)RAND_MAX;
  rvec.y = (double)rand()/(double)RAND_MAX;
  rvec.z = (double)rand()/(double)RAND_MAX;
  return rvec;
}

PV_t random_vector_min_max(double min, double max) /* returns random vector in range between
				min and max */
{
  //srand(time(NULL)); /* mora bit za random??? */
  PV_t rvec;
  
  rvec.x = min + (double)(rand() / (double) RAND_MAX) * ( max - min ); 
  rvec.y = min + (double)(rand() / (double) RAND_MAX) * ( max - min );
  rvec.z = min + (double)(rand() / (double) RAND_MAX) * ( max - min ); 

  return rvec;
}

PV_t unit_vector(PV_t *vec)
{
  return vec_divide(vec, vec_len(vec));
}

PV_t random_in_unit_sphere()
{
  while (true) {
    PV_t r_vec = random_vector_min_max(-1, 1);
	PV_t p;
	do
	  {
		PV_t r_vec = {2*random_double()-1, 2*random_double()-1, 2*random_double()-1};		
	  } while (length_squared(&p) >= 1.0);
    if (length_squared(&r_vec) >= 1) {
      continue;
    }
    return r_vec;
  }
}


PV_t random_in_unit_disc()
{
  while (true) {
	PV_t p = {random_double_min_max(-1,1),
			  random_double_min_max(-1,1),
			  0};
	if (length_squared(&p) >= 1) {
	  continue;
	}
	return p;
  }
}

PV_t random_unit_vector()
{
  PV_t rnd = random_in_unit_sphere();
  return unit_vector(&rnd);
}



PV_t reflect( PV_t *v,  PV_t *n)
{
  
  PV_t reflected;
  //printf("vec_dot v: %f, %f, %f\n", v->x, v->y, v->z);
  //printf("vec_dot n: %f, %f, %f\n", n->x, n->y, n->z);  
  double dot_product = vec_dot(v, n);
  //printf("dot product: %f\n", dot_product);
  // calculate and return reflected vector
  reflected.x = v->x - 2*dot_product*n->x;
  reflected.y = v->y - 2*dot_product*n->y;
  reflected.z = v->z - 2*dot_product*n->z;
  return reflected;
}

bool near_zero(PV_t *v)
{
  const auto double s = 1e-8;
  return (fabs(v->x) < s) && (fabs(v->y) < s) && (fabs(v->z) < s);
}


bool refract(PV_t *v, PV_t *n, double ni_over_nt, PV_t *refracted)
{
    PV_t uv = unit_vector(v);
    double dt = vec_dot(&uv, n);
    double discriminant = 1.0 - ni_over_nt*ni_over_nt*(1-dt*dt);
    if (discriminant > 0) {
	  refracted->x = ni_over_nt*(uv.x - n->x*dt) - n->x*sqrt(discriminant);
	  refracted->y = ni_over_nt*(uv.y - n->y*dt) - n->y*sqrt(discriminant);
	  refracted->z = ni_over_nt*(uv.z - n->z*dt) - n->z*sqrt(discriminant);
	  return true;
    }
    else
        return false;

}
//PV_t refract(PV_t *uv, PV_t *n, double etai_over_etat)
//{
//
//  PV_t scale = vec_scale(uv, -1);
//  double cos_theta = fmin(vec_dot(&scale, n), 1.0);
//  PV_t r_out_perp = {etai_over_etat * (uv->x + cos_theta*n->x),
//					 etai_over_etat * (uv->y + cos_theta*n->y),
//					 etai_over_etat * (uv->z + cos_theta*n->z)};
//  PV_t r_out_parallel = {-sqrt(fabs(1.0 - length_squared(&r_out_perp))) * n->x,
//						 -sqrt(fabs(1.0 - length_squared(&r_out_perp))) * n->y,
//						 -sqrt(fabs(1.0 - length_squared(&r_out_perp))) * n->z};
//  PV_t r_out_perp_parallel = {r_out_perp.x+r_out_parallel.x,
//							  r_out_perp.y+r_out_parallel.y,
//							  r_out_perp.z+r_out_parallel.z};
//  return r_out_perp_parallel;
//}
