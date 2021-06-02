#ifndef MATERIAL_H
#define MATERIAL_H

#include "rtweekend.h"
#include "ray.h"
#include "hittable.h"

struct hit_record;

class material {
    public:
        virtual bool scatter(
            const ray& r_in, const hit_record& rec, color& attenuation, ray& scattered
        ) const = 0;
};


class lambertian : public material {
    public:
        lambertian(const color& a) : albedo(a) {}

        virtual bool scatter(
            const ray& r_in, const hit_record& rec, color& attenuation, ray& scattered
        ) const override {
            auto scatter_direction = rec.normal + random_unit_vector();

			// Catch degenerate scatter direction
            if (scatter_direction.near_zero())
                scatter_direction = rec.normal;
			
            scattered = ray(rec.p, scatter_direction);
            attenuation = albedo;
			//std::cout << "lambertian attenuation: " << attenuation << "\n";
            return true;
        }

    public:
        color albedo;
};

class metal : public material {
    public:
        metal(const color& a) : albedo(a) {}

        virtual bool scatter(
            const ray& r_in, const hit_record& rec, color& attenuation, ray& scattered
        ) const override {
            vec3 reflected = reflect(unit_vector(r_in.direction()), rec.normal);
            scattered = ray(rec.p, reflected);
            attenuation = albedo;
			std::cout << "unit_vec: " << unit_vector(r_in.direction())  << "\n";
			std::cout << "reflected: " << reflected  << "\n";
			std::cout << "metal r_in origin: " << r_in.origin()  << "\n";
			std::cout << " metal r_in direction: " << r_in.direction()  << "\n";
			std::cout << "  metal rec normal: " << rec.normal  << "\n";
			std::cout << "   metal rec p: " << rec.p  << "\n";			
			std::cout << "    scattered metal origin: " << scattered.origin()  << "\n";
			std::cout << "     scattered metal direction: " << scattered.direction()  << "\n";
            return (dot(scattered.direction(), rec.normal) > 0);
        }

    public:
        color albedo;
};

#endif
