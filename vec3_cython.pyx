import numpy as np
import numpy
import math
import random 
import Cython
cimport numpy as np

cdef class Vec3():
    """Documentation for Vec3. Is a RGB color or point
    Use numpy array type, defined as self.arr
    """
    #cdef public np.ndarray arr
    def __init__(self, e1, e2, e3):
        #super(Vec3, self).__init__()
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3
        #self.arr = np.array([self.e1, self.e2, self.e3])

    def __str__(self):
        values = str(self.e1)+" "+str(self.e2)+" "+str(self.e3)
        return "Vector with values "+values

    def __add__(self, v):
        cdef double e1, e2, e3
        e1 = self.e1 + v.e1
        e2 = self.e2 + v.e2
        e3 = self.e3 + v.e3
        #return [self.x, self.y, self.z]
        return Vec3(e1, e2, e3)

    cdef Vec3 add(self, Vec3 v):
        cdef double e1, e2, e3
        e1 = self.e1 + v.e1
        e2 = self.e2 + v.e2
        e3 = self.e3 + v.e3
        #return [self.x, self.y, self.z]
        return Vec3(e1, e2, e3)

    
    def __mul__(self, t):
        cdef double e1, e2, e3
        e1 = self.e1 * t
        e2 = self.e2 * t
        e3 = self.e3 * t
        #self.arr = np.array([self.e1, self.e2, self.e3])
        return Vec3(e1, e2, e3)

    cdef mul(self, t):
        cdef double e1, e2, e3
        e1 = self.e1 * t
        e2 = self.e2 * t
        e3 = self.e3 * t
        return Vec3(e1, e2, e3)

    
    def __sub__(self, v):
        cdef double e1, e2, e3
        e1 = self.e1 - v.e1
        e2 = self.e2 - v.e2
        e3 = self.e3 - v.e3
        #self.arr = np.array([self.e1, self.e2, self.e3])        
        #return [self.x, self.y, self.z]
        return Vec3(e1, e2, e3)

    cdef sub(self, v):
        cdef double e1, e2, e3
        e1 = self.e1 - v.e1
        e2 = self.e2 - v.e2
        e3 = self.e3 - v.e3
        #self.arr = np.array([self.e1, self.e2, self.e3])        
        #return [self.x, self.y, self.z]
        return Vec3(e1, e2, e3)

    def __truediv__(self, t):
        # overload / operatorxs
        e1 = self.e1 / t
        e2 = self.e2 / t
        e3 = self.e3 / t
        #self.arr = np.array([self.e1, self.e2, self.e3])        
        #return [self.x, self.y, self.z]
        return Vec3(e1, e2, e3)

    cdef x(self):
        return self.e1

    cdef y(self):
        return self.e2

    cdef z(self):
        return self.e3

    cdef length_squared(self):
        return self.e1**2+self.e2**2+self.e3**2
        
    cdef length(self):
        return math.sqrt(self.length_squared())


cpdef test_add_cython(rn):
    cdef int i
    cdef Vec3 a, b, c
    for i in range(rn):
        a = Vec3(1, 2, 3)
        b = Vec3(1, 2, 3)
        c = a.add(b)
