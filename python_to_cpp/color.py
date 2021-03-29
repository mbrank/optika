def clamp(x, xmin, xmax):
    if x < xmin:
        return xmin
    elif x > xmax:
        return xmax
    else:
        return x


def write_color(f, pixel_color, samples_per_pixel):
    # Write the translated [0,255] value of each color component into f file.
    # input: object of class Vec3
    r = pixel_color.x()
    g = pixel_color.y()
    b = pixel_color.z()

    # Divide the color of pixel by the number of samples
    scale = 1.0/samples_per_pixel
    r *= scale
    g *= scale
    b *= scale

    # Write the translated [0, 255] value mof each color component
    f.write(str(int(256 * clamp(r, 0, 0.999))) + ' ' +
            str(int(256 * clamp(g, 0, 0.999))) + ' ' +
            str(int(256 * clamp(b, 0, 0.999))) + '\n')
