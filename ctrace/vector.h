//vector.h
#ifndef VECTOR_H
#define VECTOR_H


#include <stdlib.h>
#include <stdio.h>
#include <math.h>

//vector structure
typedef struct vector_type{
   double x, y, z;
} PV_t;


//  prototypes for the vector functions  

PV_t vec_sum(PV_t *, PV_t *);
PV_t vec_diff(PV_t *, PV_t *);
double vec_dot(PV_t *, PV_t *);
PV_t vec_scale(PV_t *, double fact);
double vec_len(PV_t *);
PV_t vec_divide(PV_t *v1, double fact);
double length_squared(PV_t *v1);
PV_t random_vector();
PV_t random_vector_min_max(double min, double max);
PV_t unit_vector(PV_t *vec);


#endif
