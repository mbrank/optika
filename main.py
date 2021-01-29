import numpy as np
import math
from vec3 import Vec3, dot
from ray import Ray
from color import write_color
from hittable import Hittable, HitRecord
from hittable_list import HittableList
from sphere import Sphere

def ray_color(r, world):
    """ Input parameters:
    ray -> r of type Ray
    scene -> world of type HittableList
    """
    infinity = math.inf
    r_orig = r.origin
    r_dir = r.direction
    rec = HitRecord(r_orig, r_dir, infinity)
    if world.hittable_object(r, 0, infinity, rec):
        return (rec.normal+Vec3(1,1,1))*0.5 # Vec3 contains value for color

    vals = r.direction # if r.direction() -> error: object is not callable
    r_unit = np.array([vals.e1,
                       vals.e2,
                       vals.e3])/np.linalg.norm(np.array([vals.e1,
                                                          vals.e2,
                                                          vals.e3]))
    unit_direction = Vec3(r_unit[0], r_unit[1], r_unit[2])
    t = 0.5*(unit_direction.y() + 1)
    return Vec3(1.0, 1.0, 1.0)*(1.0-t) + Vec3(0.5, 0.7, 1.0)*t    

#def main():

# Image
aspect_ratio = 16/9
iw = 400
ih = int(iw/aspect_ratio)

#World
world = HittableList([])
world.add_to_hittable_list(Sphere(Vec3(0, 0, -1), 0.5, 'sphere1'))
world.add_to_hittable_list(Sphere(Vec3(0, -100.5, -1), 100, 'sphere2'))
world.add_to_hittable_list(Sphere(Vec3(0, 0.5, -1), 0.5, 'sphere3'))
# Camera
viewport_height = 2.0
viewport_width = aspect_ratio * viewport_height
focal_length = 1.0
origin = Vec3(0, 0, 0)
horizontal = Vec3(viewport_width, 0, 0)
vertical = Vec3(0, viewport_height, 0)

#print("viewport_width:", viewport_width)
#print("origin:", origin)
#print("horizontal/2:", horizontal/2)
#print("vertical/2:", vertical/2)

#print("focal_length:", focal_length.x(), focal_length.y(), focal_length.z())
lower_left_corner = origin - horizontal/2 - vertical/2 - Vec3(0, 0, focal_length)
#print(origin - horizontal/2 - vertical/2)
#print('lower_left_corner:', lower_left_corner)
f = open('image.ppm', 'w')
#print("Image width:", iw, "Image height:", ih)
f.write("P3\n"+str(iw)+" "+str(ih)+"\n255\n")
for j in range(ih-1, -1, -1):
    #print("\rScanlines remaining: "+str(j)+"\n")
    for i in range(iw):
        u = i / (iw-1)
        v = j / (ih-1)
        r = Ray(origin, lower_left_corner + horizontal*u + vertical*v - origin)
        rorig = r.origin
        rdir = r.direction
        pixel_color = ray_color(r, world)
        write_color(f, pixel_color)

#    print("Done!")

#if __name__ == "__main__":
#    main()
