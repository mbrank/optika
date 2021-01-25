class Vec3(object):
    """Documentation for Vec3

    """
    def __init__(self, e1, e2, e3):
        super(Vec3, self).__init__()
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3

    def __add__(self, v):
        x = self.x + v.x
        y = self.y + v.y
        z = self.z + v.z
        #return [self.x, self.y, self.z]
        return Vec3(x, z, y)

    def __mul__(self, t):
        self.x = t
        self.y = t
        self.z = t

    def x(self):
        return self.e1

    def y(self):
        return self.e2

    def z(self):
        return self.e3

Vec3(1,2,3)
