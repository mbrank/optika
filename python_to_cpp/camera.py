from vec3 import Vec3, dot
from ray import Ray

class Camera():
    """Documentation for Camera. Defines camera and its properties.

    """
    def __init__(self, aspect_ratio, viewport_height, focal_length):
        #super(Camera, self).__init__(aspect_ratio, viewport_height, focal_length)
        self.aspect_ratio = aspect_ratio
        self.viewport_height = viewport_height
        self.focal_length = focal_length
        self.viewport_width = aspect_ratio*viewport_height

        self.origin = Vec3(0, 0, 0)
        self.horizontal = Vec3(self.viewport_width, 0, 0)
        self.vertical = Vec3(0, self.viewport_height, 0)
        self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical/2 - Vec3(0, 0, +self.focal_length)

    def get_ray(self, u, v):
        return Ray(self.origin,
                   self.lower_left_corner + self.horizontal*u + self.vertical*v - self.origin)
        
