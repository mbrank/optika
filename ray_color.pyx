def random_in_unit_sphere(bottom_lim, top_lim):
    cdef int bottom_lim, top_lim
    cdef numpy.ndarray p
    while True:
        #p = vec3_random(-1, 1)
        p = np.array([random.uniform(bottom_lim, top_lim),
                      random.uniform(bottom_lim, top_lim),
                      random.uniform(bottom_lim, top_lim)])
        #if p.length_squared() >= 1:
        if np.sum(p**2) >= 1:
            continue
        return p
