from ray import Ray
#from vec3 import Vec3, dot
import numpy as np

class HitRecord():
    """ Input parameters:
    point p of type Vec3
    vector normal of type Vec3
    float t to calculate length of ray
    """
    def __init__(self, p, normal, t):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = False

    def set_face_normal(self, r, outward_normal):
        self.front_face = np.dot(r.direction, outward_normal) < 0
        # normal always points out of surface
        self.normal = outward_normal if self.front_face else outward_normal*-1


class Hittable():
    """Documentation for Hittable. This is a base class for all hittable
    objects e.g. spheres, triangles, etc.

    Input parameters:

    ray -> r of type Ray,
    -> t_min, t_max of type float, if t between them, then object was hit by ray
    r,
    record of hits -> rec of type hit_record

    """
    def __init__(self, r, t_min, t_max, rec):
        super(Hittable, self).__init__()
        self.r = r
        self.t_min = t_min
        self.t_max = t_max
        self.rec = rec

    def hit(self, r, t_min, t_max, rec):
        # Virtual method, will get overriden by object class
        # Could be a function, not method?
        pass
