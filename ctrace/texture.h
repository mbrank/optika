#ifndef TEXTURE_H
#define TEXTURE_H

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <stdbool.h>
#include "ray.h"
#include "hittable.h"

typedef struct texture_type{
  int type;
  double u;
  double v;
  PV_t p;
  PV_t color1;
  PV_t color2;
} texture_t;

PV_t texture_color(texture_t *texture);

#endif
