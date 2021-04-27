cdef class Ray():
    """Documentation for Ray
    Inputs: 
    origin: type numpy of origin point
    direction: type numpy of direction vector 

    """
    def __init__(self, origin, direction):
        super(Ray, self).__init__()
        cdef Vec3 origin
        cdef Vec3 direction
        self.origin = origin
        self.direction = direction

    cdef origin(self):
        # replace name with get_origin()?
        return self.origin

    cdef direction(self):
        # replace name with get_direction()?
        return self.direction

    cdef at(self, t):
        cdef double t
        # t of type float
        return self.origin+self.direction*t
    

