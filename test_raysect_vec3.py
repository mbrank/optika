from raysect.core.math import Vector3D

def test_add_raysect(rn):
    a = Vector3D(1, 2, 3)
    b = Vector3D(1, 2, 3)
    for i in range(rn):
        c = a.add(b)
