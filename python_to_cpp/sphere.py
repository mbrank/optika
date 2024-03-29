import math
from hittable import HitRecord, Hittable
from vec3 import Vec3, dot

class Sphere(Hittable):
    """Documentation for Sphere. Class to create sphere.
    Input parameters:

    center of sphere -> cen of type Vec3
    radius -> r of type Vec3
    """
    def __init__(self, center, radius, name):
        #super(Sphere, self).__init__()
        # super(Sphere, self).__init__()
        self.center = center
        self.radius = radius
        self.name = name

    #def sphere_hit(self, r, t_min, t_max, rec):
    def hit(self, r, t_min, t_max, rec):
        oc = r.origin - self.center
        a = r.direction.length_squared()
        half_b = dot(oc, r.direction)
        c = oc.length_squared() - self.radius*self.radius
        discriminant = half_b*half_b - a*c
        if discriminant < 0:
            return False
        sqrtd = math.sqrt(discriminant)

        # Find the nearest root that lies in acceptable range
        root = (-half_b-sqrtd)/a
        if root < t_min or t_max < root:
            root = (-half_b+sqrtd)/a
            if root < t_min or t_max < root:
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        rec.normal = (rec.p-self.center)/self.radius

        # Add surface side determination to class
        outward_normal = (rec.p-self.center)/self.radius
        rec.set_face_normal(r, outward_normal)

        return True
