#include "texture.h"

PV_t texture_color(texture_t *texture){
  switch (texture->type) {
  case 1: { // solid color
    return texture->color1;
    break;
  }
  case 2: { // checker board
    double sin_val = sin(10*texture->p.x)*sin(10*texture->p.y)*sin(10*texture->p.z);
	//printf("%f\n", sin_val);
	//printf("texture->p.x %f\n", &texture->p.x);
	if (sin_val < 0) {
	  return texture->color1;
	}
	else {
	  return texture->color2;
	}
    break;
  }
default:
    return texture->color1;
  break;
  }
}
