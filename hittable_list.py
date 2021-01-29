from hittable import Hittable, HitRecord

class HittableList(Hittable):
    """Documentation for HittableList

    """
    def __init__(self, hittable_list):
        #Hittable.__init__(self, r, t_min, t_max, rec, hit)
        self.hittable_list = hittable_list

    def clear_hittable_list(self):
        self.hittable_list = []
        
    def add_to_hittable_list(self, hittable):
        """ Input parameter: object hittable of type Hittable, e.g. Sphere,...
        """
        self.hittable_list.append(hittable)

    def hittable_object(self, r, t_min, t_max, rec):
        temp_rec = rec
        hit_anything = False
        closest_so_far = t_max
        print('t_max', t_max)

        for obj in self.hittable_list:
            #print('test1:', obj.name)
            if obj.hit(r, t_min, closest_so_far, temp_rec):
                #print('sphere:', obj.name)
                hit_anything = True
                closest_so_far = temp_rec.t
                print('closest_so_far', closest_so_far)
                rec = temp_rec
                return hit_anything
