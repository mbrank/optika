from vec3_cython import Vec3, test_add_cython
from vec3 import Vec3, test_add_python
import timeit
#from vec3_cython cimport Vec3

cy = timeit.timeit('test_add_cython(1000000)',
                   setup='from vec3_cython import Vec3, test_add_cython',
                   number=1)
py = timeit.timeit('test_add_python(1000000)',
                   setup='from vec3 import Vec3, test_add_python',
                   number=1)

#rsect = timeit.timeit('test_add_raysect(1000000)',
#                      setup='from test_raysect_vec3 import test_add_raysect',
#                      number=1)


print(cy, py)
print("Cython is {}x times faster".format(py/cy))
