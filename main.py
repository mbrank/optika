import numpy as np
from vec3 import Vec3
from ray import Ray
from color import write_color

def ray_color(r):
    # input argumet of type Vec3, which represents a ray
    #v_hat = v / np.linalg.norm(v)
    #unit_direction = unit_vector(r.direction())
    vals = r.direction # if r.direction() -> error: object is not callable
    r_unit = np.array([vals.e1,
                       vals.e2,
                       vals.e3])/np.linalg.norm(np.array([vals.e1,
                                                          vals.e2,
                                                          vals.e3]))
    unit_direction = Vec3(r_unit[0], r_unit[1], r_unit[2])
    t = 0.5*(unit_direction.y() + 1)
    
    return Vec3(1.0, 1.0, 1.0)*(1.0-t) + Vec3(0.5, 0.7, 1.0)*t

def main():

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
    focal_length = Vec3(0, 0, focal_length)
    #lower_left_corner = origin.arr - horizontal.arr/2 - vertical.arr/2 - focal_length.arr
    print(origin)
    print(horizontal/2)
    print(vertical/2)
    print(focal_length)
    lower_left_corner = origin - horizontal/2 - vertical/2 - focal_length
    
    f = open('image.ppm', 'w')
    print("Image width:", iw, "Image height:", ih)
    f.write("P3\n"+str(iw)+" "+str(ih)+"\n255\n")
    for j in range(ih-1, -1, -1):
        print("\rScanlines remaining: "+str(j)+"\n")
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
            print(lower_left_corner)
            print(horizontal/2)
            print(lower_left_corner + horizontal)
            r = Ray(origin, lower_left_corner + horizontal + vertical - origin)
            pixel_color = ray_color(r)
            write_color(f, pixel_color)

    print("Done!")

if __name__ == "__main__":
    main()
