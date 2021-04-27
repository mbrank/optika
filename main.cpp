#include "rtweekend.h"
#include "camera.h"
#include "color.h"
#include "hittable_list.h"
#include "sphere.h"

#include <iostream>

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

color ray_color(const ray& r, const hittable& world, int depth) {
    hit_record rec;

    // If we're exceeded the ray bounce limit, no more light is gathered
    if (depth <= 0)
        return color(0,0,0);

    if (world.hit(r, 0, infinity, rec)) {
        point3 target = rec.p + rec.normal + random_in_unit_sphere();
        return 0.5 * ray_color(ray(rec.p, target - rec.p), world, depth-1);
    }
    //std::cout << "t<0:" << t << "\n";
    vec3 unit_direction = unit_vector(r.direction());
    //std::cout << "ray_color.unit_direction:" << unit_direction << "\n";
    auto t = 0.5*(unit_direction.y() + 1.0);
    //std::cout << "ray_color.t:" << new_t << "\n";
    //std::cout << "ray_color.return:" << (1.0-t)*color(1.0, 1.0, 1.0) + t*color(0.5, 0.7, 1.0) << "\n";    
    return (1.0-t)*color(1.0, 1.0, 1.0) + t*color(0.5, 0.7, 1.0);
}

int main() {

    // Image
    const auto aspect_ratio = 16.0 / 9.0;
    const int image_width = 400;
    const int image_height = static_cast<int>(image_width / aspect_ratio);
    const int samples_per_pixel = 5;
    const int max_depth = 5;
    
    // World
    hittable_list world;
    world.add(make_shared<sphere>(point3(0,0,-1), 0.5));
    world.add(make_shared<sphere>(point3(0,-100.5,-1), 100));

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
            for (int s = 0; s < samples_per_pixel; ++s) {
                auto u = (i + random_double()) / (image_width-1);
                auto v = (j + random_double()) / (image_height-1);
                ray r = cam.get_ray(u, v);
                pixel_color += ray_color(r, world, max_depth);
            }
            write_color(std::cout, pixel_color, samples_per_pixel);
        }
    }

    std::cerr << "\nDone.\n";
}
