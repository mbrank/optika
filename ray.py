#from vec3 import Vec3

class Ray():
    """Documentation for Ray
    Inputs: 
    origin: type numpy of origin point
    direction: type numpy of direction vector 

    """
    def __init__(self, origin, direction):
        super(Ray, self).__init__()
        self.origin = origin
        self.direction = direction

    def origin(self):
        # replace name with get_origin()?
        return self.origin

    def direction(self):
        # replace name with get_direction()?
        return self.direction

    def at(self, t):
        # t of type float
        return self.origin+self.direction*t
    

