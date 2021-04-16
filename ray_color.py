import numpy as np
import math
from hittable import Hittable, HitRecord
from hittable_list import HittableList
from ray import Ray
import random

def random_in_unit_sphere(bottom_lim, top_lim):
    print("bottom_lim", bottom_lim)
    print("top_lim", top_lim)
    while True:
        #p = vec3_random(-1, 1)
        p = np.array([random.uniform(bottom_lim, top_lim),
                      random.uniform(bottom_lim, top_lim),
                      random.uniform(bottom_lim, top_lim)])
        #if p.length_squared() >= 1:
        if np.sum(p**2) >= 1:
            continue
        return p

def ray_color(r, world, depth):
    """ Input parameters:
    ray -> r of type Ray
    scene -> world of type HittableList
    """
    infinity = math.inf
    r_orig = r.origin # numpy array
    r_dir = r.direction # numpy array
    rec = HitRecord(r_orig, r_dir, infinity)
    if depth <= 0:
        #return Vec3(0, 0, 0)
        return np.zeros(3)

    if world.hittable_object(r, 0, infinity, rec):
        target = rec.p + rec.normal + random_in_unit_sphere(-1, 1)
        return ray_color(Ray(rec.p, target - rec.p), world, depth-1)*0.5

    vals = r.direction
    #r_unit = np.array([vals.e1,
    #                   vals.e2,
    #                   vals.e3])/np.linalg.norm(np.array([vals.e1,
    #                                                      vals.e2,
    #                                                      vals.e3]))
    r_unit = vals/np.linalg.norm(vals)
    #unit_direction = Vec3(r_unit[0], r_unit[1], r_unit[2])
    #t = 0.5*(unit_direction.y() + 1)
    t = 0.5*(r_unit[1] + 1)
    return np.array([1.0, 1.0, 1.0])*(1.0-t) + np.array([0.5, 0.7, 1.0])*t    
