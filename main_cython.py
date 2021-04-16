import numpy as np

def main():

    iw = 2560
    ih = 2560

    f = open("image_cython.ppm", "w")
    f.write("P3\n")
    f.write(str(iw) + ' ' + str(ih) + "\n255\n")
    
    #std::cout << "P3\n" << iw << ' ' << ih << "\n255\n";

    for j in range(ih-1, -1, -1):
        print("Scanlines remaining: "+str(j)+"")
        for i in range(iw):
            r = (i / (iw-1))*255.99
            g = (j / (ih-1))*255.99
            b = 0.25*255.99

            f.write(str(r) + ' ' + str(g) + ' ' + str(b) + '\n')

if __name__ == '__main__':
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('ncalls')
    stats.print_stats()
