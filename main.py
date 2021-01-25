def main():

    iw = 2560
    ih = 256

    f = open('image.ppm', 'w')
    print("Image width:", iw, "Image height:", ih)
    f.write("P3\n"+str(iw)+" "+str(ih)+"\n255\n")
    for j in range(ih-1, -1, -1):
        print("\rScanlines remaining: "+str(j)+"\n")
        for i in range(iw):
            r = i/(iw-1)
            g = j/(ih-1)
            b = 0.25
            ir = int(255.999 * r)
            ig = int(255.999 * g)
            ib = int(255.999 * b)
            f.write(str(ir)+" "+str(ig)+" "+str(ib)+"\n")

    print("Done!")

if __name__ == "__main__":
    main()
