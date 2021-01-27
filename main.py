import numpy as np
from vec3 import Vec3, dot
from ray import Ray
from color import write_color
import math

def hit_sphere(center, radius, r):
    """Function, takes center given as Vec3, radius given as scalar and
    ray r given as Vec3. Returns True if discriminant > 0, i.e. ray
    hits sphere.

    """
    oc = r.origin - center
    #a = dot(r.direction, r.direction)
    #b = 2.0 * dot(oc, r.direction)
    #c = dot(oc, oc) - radius*radius
    #discriminant = b*b - 4*a*c
    a = r.direction.length_squared()
    half_b = dot(oc, r.direction)
    c = oc.length_squared() - radius*radius
    discriminant = half_b*half_b - a*c

    if discriminant < 0:
        return -1.0
    #std::cout << "hit_sphere.discriminant_else:" << (-b - sqrt(discriminant) ) / (2.0*a) << "\n";
    return (-half_b - math.sqrt(discriminant)) / a


def ray_color(r):
    point_center = Vec3(0, 0, -1)
    #if hit_sphere(point_center, 0.5, r):
    #    color = Vec3(1, 0, 0)
    #    return color
    t = hit_sphere(point_center, 0.5, r)
    if t > 0:
        #print('t', t)
        r_at = r.at(t)
        #print('r_at', r_at.__str__())
        N = r_at - Vec3(0, 0, -1)
        N_unit = np.array([N.e1,
                           N.e2,
                           N.e3])/np.linalg.norm(np.array([N.e1,
                                                           N.e2,
                                                           N.e3]))
        #print(r_unit)
        normal = Vec3(N_unit[0], N_unit[1], N_unit[2])
        #print('normal', normal.__str__())
        color = Vec3(normal.x()+1, normal.y()+1, normal.z()+1)
        #print('color', color*0.5)
        return color*0.5
    # input argumet of type Vec3, which represents a ray
    #v_hat = v / np.linalg.norm(v)
    #unit_direction = unit_vector(r.direction())
    vals = r.direction # if r.direction() -> error: object is not callable
    r_unit = np.array([vals.e1,
                       vals.e2,
                       vals.e3])/np.linalg.norm(np.array([vals.e1,
                                                          vals.e2,
                                                          vals.e3]))
    #print(r_unit)
    unit_direction = Vec3(r_unit[0], r_unit[1], r_unit[2])
    #print("ray_color.unit_direction:", unit_direction.__str__())
    t = 0.5*(unit_direction.y() + 1)
    #print("ray_color.t", t)
    return_val = Vec3(1.0, 1.0, 1.0)*(1.0-t) + Vec3(0.5, 0.7, 1.0)*t
    #print("ray_color.return:", return_val.__str__())
    return Vec3(1.0, 1.0, 1.0)*(1.0-t) + Vec3(0.5, 0.7, 1.0)*t

#def main():

# Image
aspect_ratio = 16/9
iw = 400
ih = int(iw/aspect_ratio)

# Camera

viewport_height = 2.0
viewport_width = aspect_ratio * viewport_height
focal_length = 1.0
origin = Vec3(0, 0, 0)
horizontal = Vec3(viewport_width, 0, 0)
vertical = Vec3(0, viewport_height, 0)
#focal_length = Vec3(0, 0, focal_length)
#lower_left_corner = origin.arr - horizontal.arr/2 - vertical.arr/2 - focal_length.arr

print("viewport_width:", viewport_width)
print("origin:", origin)
print("horizontal/2:", horizontal/2)
print("vertical/2:", vertical/2)

#print("focal_length:", focal_length.x(), focal_length.y(), focal_length.z())
lower_left_corner = origin - horizontal/2 - vertical/2 - Vec3(0, 0, focal_length)
print(origin - horizontal/2 - vertical/2)
print('lower_left_corner:', lower_left_corner)
f = open('image.ppm', 'w')
print("Image width:", iw, "Image height:", ih)
f.write("P3\n"+str(iw)+" "+str(ih)+"\n255\n")
for j in range(ih-1, -1, -1):
    #print("\rScanlines remaining: "+str(j)+"\n")
    for i in range(iw):
        # r = i/(iw-1)
        # g = j/(ih-1)
        # b = 0.25
        # ir = int(255.999 * r)
        # ig = int(255.999 * g)
        # ib = int(255.999 * b)
        # f.write(str(ir)+" "+str(ig)+" "+str(ib)+"\n")
        u = i / (iw-1)
        v = j / (ih-1)
        #r = Ray(origin, lower_left_corner + horizontal*u + vertical*v - origin)
        #print(lower_left_corner)
        #print(horizontal/2)
        #print(lower_left_corner + horizontal)
        r = Ray(origin, lower_left_corner + horizontal*u + vertical*v - origin)
        rorig = r.origin
        rdir = r.direction
        #print(horizontal)
        #print("ray r.origin():", rorig.__str__(), "\n")
        #print("ray r.direction():", rdir.__str__(), "\n")
        #print('u', u)
        #print('v', v)
        pixel_color = ray_color(r)
        write_color(f, pixel_color)

#    print("Done!")

#if __name__ == "__main__":
#    main()
