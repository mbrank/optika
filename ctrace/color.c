#include "color.h"
#include <math.h>

inline void write_color(PV_t *pixel_color, int samples_per_pixel){
    auto double r = pixel_color->x;
    auto double g = pixel_color->y;
    auto double b = pixel_color->z;

    // Divide the color by the number of samples.
    auto double scale = 1.0 / samples_per_pixel;
    //r *= scale;
    //g *= scale;
    //b *= scale;

	// add gamma correction for gamma=2.0
	//printf("r=%f\n", r);
	//printf("scale=%f\n", scale);
    r = sqrt(scale*r);
	//printf("rsqrt=%f\n", r);
	g = sqrt(scale*g);
	b = sqrt(scale*b);
	

    // Write the translated [0,255] value of each color component.
    printf("%d %d %d\n",
	   (int)(256 * clamp(r, 0.0, 0.999)),
	   (int)(256 * clamp(g, 0.0, 0.999)),
	   (int)(256 * clamp(b, 0.0, 0.999)));
}


