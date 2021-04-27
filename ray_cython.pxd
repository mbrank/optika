cdef class Ray():

    cdef public Vec3 origin, direction

    cdef Vec3 origin(self)

    cdef Vec3 direction(self)

    cdef double at(self, double t)

