#ifndef HITTABLE_H
#define HITTABLE_H

#include "ray.h"

class material;

struct hit_record {
  point3 p;
  vec3 normal;
  shared_ptr<material> mat_ptr;
  double t;
  bool front_face;
  
  inline void set_face_normal(const ray& r, const vec3& outward_normal) {
    front_face = dot(r.direction(), outward_normal) < 0; 
	std::cout << "set face normal after ->normal" << normal << "\n";
    normal = front_face ? outward_normal :-outward_normal;
	std::cout << "set face normal after ->normal" << normal << "\n";
  }
};

class hittable {
public:
  // hit is virtual method that will be overriden in every child class?
  virtual bool hit(const ray& r, double t_min, double t_max, hit_record& rec) const = 0;
};

#endif
