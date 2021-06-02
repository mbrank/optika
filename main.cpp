#include "rtweekend.h"
#include "camera.h"
#include "color.h"
#include "hittable_list.h"
#include "sphere.h"
#include "ray.h"
#include <iostream>
#include "material.h"

//double hit_sphere(const point3& center, double radius, const ray& r) {
//    vec3 oc = r.origin() - center;
//    auto a = r.direction().length_squared();
//    auto half_b = dot(oc, r.direction());
//    auto c = oc.length_squared() - radius*radius;
//    auto discriminant = half_b*half_b - a*c;
//    //std::cout << "hit_sphere.discriminant:" << discriminant << "\n";
//    if (discriminant < 0) {
//      return -1.0;
//    } else {
//      //std::cout << "hit_sphere.discriminant_else:" << (-b - sqrt(discriminant) ) / (2.0*a) << "\n";
//        return (-half_b - sqrt(discriminant) ) / a;
//    }
//}

color ray_color(const ray& r, const hittable& world, int depth, int i, int j) {
    hit_record rec;

    // If we're exceeded the ray bounce limit, no more light is gathered
    if (depth <= 0)
      return color(0,0,0);
    if (world.hit(r, 0, infinity, rec)) {
      //std::cout <<"depth:" << depth << ", hit -> i: "<< i << " j: " << j << "\n";
      //std::cout <<"rec center: "<<  "\n";
      ray scattered;
      color attenuation;
      if (rec.mat_ptr->scatter(r, rec, attenuation, scattered)){
	//return attenuation * ray_color(scattered, world, depth-1);
	//std::cout <<"rec attenuation: " << attenuation <<  "\n";		  
	//return attenuation;
	return attenuation*ray_color(scattered, world, depth-1, i, j);
      }
      return color(0,0,0);	  
    }

    vec3 unit_direction = unit_vector(r.direction());

    auto t = 0.5*(unit_direction.y() + 1.0);
    return (1.0-t)*color(1.0, 1.0, 1.0) + t*color(0.5, 0.7, 1.0);
}

int main() {

    // Image
    const auto aspect_ratio = 16.0 / 9.0;
    const int image_width = 400;
    const int image_height = static_cast<int>(image_width / aspect_ratio);
    const int samples_per_pixel = 1;
    const int max_depth = 3;
    
    // World
    hittable_list world;

    auto material_ground = make_shared<lambertian>(color(0.8, 0.8, 0.0));
    auto material_center = make_shared<lambertian>(color(0.7, 0.3, 0.3));
    auto material_left   = make_shared<metal>(color(0.8, 0.8, 0.8));
    auto material_right  = make_shared<metal>(color(0.8, 0.6, 0.2));

    world.add(make_shared<sphere>(point3( 0.0, -100.5, -1.0), 100.0, material_ground));
    world.add(make_shared<sphere>(point3( 0.0,    0.0, -1.0),   0.5, material_center));
    world.add(make_shared<sphere>(point3(-1.0,    0.0, -1.0),   0.5, material_left));
    world.add(make_shared<sphere>(point3( 1.0,    0.0, -1.0),   0.5, material_right));

    // Camera
    camera cam;
    //auto viewport_height = 2.0;
    //auto viewport_width = aspect_ratio * viewport_height;
    //auto focal_length = 1.0;

    //auto origin = point3(0, 0, 0);
    //auto horizontal = vec3(viewport_width, 0, 0);
    //auto vertical = vec3(0, viewport_height, 0);
    //auto lower_left_corner = origin - horizontal/2 - vertical/2 - vec3(0, 0, focal_length);

    //std::cout << "viewport_width:" << viewport_width << "\n";    
    //std::cout << "origin:" << origin << "\n";
    //std::cout << "horizontal/2:" << horizontal/2 << "\n";
    //std::cout << "vertical/2:" << vertical/2 << "\n";
    //std::cout << "focal_length:" << focal_length << "\n";
    
    //std::cout << "lower_left_corner:" << lower_left_corner << '\n'; 
    // Render

    std::cout << "P3\n" << image_width << " " << image_height << "\n255\n";

    for (int j = image_height-1; j >= 0; --j) {
		std::cerr << "\rScanlines remaining: " << j << ' ' << std::flush;
        for (int i = 0; i < image_width; ++i) {
	    color pixel_color(0, 0, 0);
		//std::cout << "j: " << j << " i: " << i << "\n";
		//std::cout <<"i: "<< i << " j: " << j << "\n";
		for (int s = 0; s < samples_per_pixel; ++s) {
                auto u = (i + random_double()) / (image_width-1);
                auto v = (j + random_double()) / (image_height-1);
                ray r = cam.get_ray(u, v);
                pixel_color += ray_color(r, world, max_depth, i, j);
            }
		write_color(std::cout, pixel_color, samples_per_pixel);
        }
    }

    std::cerr << "\nDone.\n";
}
