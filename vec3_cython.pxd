from cython.operator cimport dereference as deref

cdef class Vec3():

    cdef public double e1, e2, e3

    cdef Vec3 add(self, Vec3 v)

    cdef Vec3 mul(self, Vec3 v)

    cdef Vec3 sub(self, Vec3 v)

    cdef double x(self)

    cdef double y(self)

    cdef double z(self)

    cdef double length_squared(self)

    cdef double length(self)
