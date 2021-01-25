def write_color(f, pixel_color):
    # Write the translated [0,255] value of each color component into f file.
    # input: object of class Vec3
    f.write(str(255.999 * pixel_color.x()) + ' ' +
            str(255.999 * pixel_color.y()) + ' ' +
            str(255.999 * pixel_color.z()) + '\n')
