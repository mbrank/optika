import numpy as np
import math
#from vec3 import Vec3, dot, vec3_random, random_in_unit_sphere
from ray import Ray
from color import write_color
from hittable import Hittable, HitRecord
from hittable_list import HittableList
from sphere import Sphere
from camera import Camera
from rtweekend import random_double
import random

def random_in_unit_sphere(bottom_lim, top_lim):
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

# Image
aspect_ratio = 16/9
iw = 400
ih = int(iw/aspect_ratio)
samples_per_pixel = 100
max_depth = 50

#World
world = HittableList([])
#world.add_to_hittable_list(Sphere(Vec3(0, 0, -1), 0.5, 'sphere1'))
world.add_to_hittable_list(Sphere(np.array([0,0,-1]), 0.5, 'sphere1'))
#world.add_to_hittable_list(Sphere(Vec3(0, -100.5, -1), 100, 'sphere2'))
world.add_to_hittable_list(Sphere(np.array([0, -100.5, -1]), 100, 'sphere2'))
# Camera
focal_length = 1.0
viewport_height = 2.0
camera = Camera(aspect_ratio, viewport_height, focal_length)
f = open('image_numpy.ppm', 'w')
f.write("P3\n"+str(iw)+" "+str(ih)+"\n255\n")
for j in range(ih-1, -1, -1):
    print("Scanlines remaining: "+str(j)+"")
    for i in range(iw):
        #pixel_color = Vec3(0, 0, 0)
        pixel_color = np.zeros(3)
        for s in range(samples_per_pixel):
            #u = (i+random_double(0, 0.9999))/(iw-1)
            u = (i+random.uniform(0, 0.9999))/(iw-1)
            #v = (j+random_double(0, 0.9999))/(ih-1)
            v = (j+random.uniform(0, 0.9999))/(ih-1)
            r = camera.get_ray(u, v)
            pixel_color += ray_color(r, world, max_depth) 

        write_color(f, pixel_color, samples_per_pixel)

print("Done!")
