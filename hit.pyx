import Cython

center = np.array([0, 0, -1])
radius = 0.5
#def sphere_hit(self, r, t_min, t_max, rec):
def hit(self, r, t_min, t_max, rec):
    oc = r.origin - center
    #a = r.direction.length_squared()
    a = np.sum(r.direction**2)
    half_b = np.dot(oc, r.direction)
    #c = oc.length_squared() - self.radius*self.radius
    c = np.sum(oc**2) - radius*radius
    discriminant = half_b*half_b - a*c
    if discriminant < 0:
        return False
    sqrtd = math.sqrt(discriminant)

    # Find the nearest root that lies in acceptable range
    root = (-half_b-sqrtd)/a
    if root < t_min or t_max < root:
        root = (-half_b+sqrtd)/a
        if root < t_min or t_max < root:
            return False

    #rec.t = root
    #rec.p = r.at(rec.t)
    #rec.normal = (rec.p-center)/radius
    ## Add surface side determination to class
    #outward_normal = (rec.p-center)/radius
    #rec.set_face_normal(r, outward_normal)

    return True
