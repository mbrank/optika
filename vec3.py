import numpy as np

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
        return Vec3(x, z, y)

    def __mul__(self, t):
        self.e1 *= t
        self.e2 *= t
        self.e3 *= t
        self.arr = np.array([self.e1, self.e2, self.e3])
        return Vec3(self.e1, self.e2, self.e3)

    def __sub__(self, v):
        self.e1 -= v.e1
        self.e2 -= v.e2
        self.e3 -= v.e3
        self.arr = np.array([self.e1, self.e2, self.e3])        
        #return [self.x, self.y, self.z]
        return Vec3(self.e1, self.e2, self.e3)

    def __truediv__(self, t):
        # overload / operatorxs
        self.e1 /= t
        self.e2 /= t
        self.e3 /= t
        self.arr = np.array([self.e1, self.e2, self.e3])        
        #return [self.x, self.y, self.z]
        return Vec3(self.e1, self.e2, self.e3)

        
    def x(self):
        return self.e1

    def y(self):
        return self.e2

    def z(self):
        return self.e3

    def length(self):
        return self.e1**2+self.e2**2+self.e3**2
        
    def length_squared(self):
        return math.sqrt(self.length())
        
    
a = Vec3(1,2,3)
b = Vec3(1,2,3)
c = a+b
print(c.arr)
a*10
print(a.arr)
g=a/2
print(a.e1, a.e2, a.e3)
