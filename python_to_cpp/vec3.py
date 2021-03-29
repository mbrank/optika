import numpy as np
import math
import random 

class Vec3():
    """Documentation for Vec3. Is a RGB color or point
    Use numpy array type, defined as self.arr
    """
    def __init__(self, e1, e2, e3):
        super(Vec3, self).__init__()
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3
        self.arr = np.array([self.e1, self.e2, self.e3])

    def __str__(self):
        values = str(self.e1)+" "+str(self.e2)+" "+str(self.e3)
        return "Vector with values "+values

    def __add__(self, v):
        x = self.e1 + v.e1
        y = self.e2 + v.e2
        z = self.e3 + v.e3
        #return [self.x, self.y, self.z]
        return Vec3(x, y, z)

    def __mul__(self, t):
        e1 = self.e1 * t
        e2 = self.e2 * t
        e3 = self.e3 * t
        #self.arr = np.array([self.e1, self.e2, self.e3])
        return Vec3(e1, e2, e3)

    def __sub__(self, v):
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

    def x(self):
        return self.e1

    def y(self):
        return self.e2

    def z(self):
        return self.e3

    def length_squared(self):
        return self.e1**2+self.e2**2+self.e3**2
        
    def length(self):
        return math.sqrt(self.length_squared())


def dot(u, v):
    """Function that takes tvo Vec3 vectors and returns their dot product
    in form of scalar

    """
    return u.e1 * v.e1 + u.e2 * v.e2 + u.e3 * v.e3


def vec3_random(bottom_lim, top_lim):
    """ Function that returns random vector of type Vec3
    """
    return Vec3(random.uniform(bottom_lim, top_lim),
                random.uniform(bottom_lim, top_lim),
                random.uniform(bottom_lim, top_lim))


def random_in_unit_sphere():
    while True:
        p = vec3_random(-1, 1)
        if p.length_squared() >= 1:
            continue
        return p

a = Vec3(1,2,3)
b = Vec3(1,2,3)
c = a+b
print(c.arr)
a*10
print(a.arr)
g=a/2
print(a.e1, a.e2, a.e3)
