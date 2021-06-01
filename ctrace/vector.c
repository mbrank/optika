//vector.c


#include "vector.h"
#include "math.h"
#include "time.h"
#include <stdbool.h>

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
  rvec.x = (float)rand()/(float)RAND_MAX;
  rvec.y = (float)rand()/(float)RAND_MAX;
  rvec.z = (float)rand()/(float)RAND_MAX;
  return rvec;
}

PV_t random_vector_min_max(double min, double max) /* returns random vector in range between
				min and max */
{
  //srand(time(NULL)); /* mora bit za random??? */
  PV_t rvec;
  
  rvec.x = min + (float)(rand() / (float) RAND_MAX) * ( max - min ); 
  rvec.y = min + (float)(rand() / (float) RAND_MAX) * ( max - min );
  rvec.z = min + (float)(rand() / (float) RAND_MAX) * ( max - min ); 

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
    if (length_squared(&r_vec) >= 1) {
      continue;
    }
    return r_vec;
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

  double dot_product = vec_dot(v, n);

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
