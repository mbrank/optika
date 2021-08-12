import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure()
ax = Axes3D(fig)
x_white_bottom = [0,555,555,0]
y_white_bottom = [200,200,200,200]
z_white_bottom = [0,0,555,555]
verts = [list(zip(x_white_bottom,
                  y_white_bottom,
                  z_white_bottom))]

bottom = Poly3DCollection(verts)
bottom.set_color("r")
ax.add_collection3d(bottom)

x_white_light = [213,343,343,213]
y_white_light = [300,300,300,300]
z_white_light = [227,227,332,332]
verts_light = [list(zip(x_white_light,
                  y_white_light,
                  z_white_light))]

light = Poly3DCollection(verts_light)
light.set_color("b")
ax.add_collection3d(light)
f = open("test5.ppm", 'r')
f.readline()
f.readline()
f.readline()

for i in range(100):
    f.readline()
    rec_p_x = float(f.readline().split()[1]) #277.301190
    rec_p_y = float(f.readline().split()[1]) #200.000000
    rec_p_z = float(f.readline().split()[1]) #292.734187
    rec_normal_x = float(f.readline().split()[1]) #0.000000
    rec_normal_y = float(f.readline().split()[1]) #1.000000
    rec_normal_z = float(f.readline().split()[1]) #0.000000
    mat_scattered_origin_x = float(f.readline().split()[1]) #277.301190
    mat_scattered_origin_y = float(f.readline().split()[1]) #200.000000
    mat_scattered_origin_z = float(f.readline().split()[1]) #292.734187
    mat_scattered_direction_x = float(f.readline().split()[1]) #-0.325318
    mat_scattered_direction_y = float(f.readline().split()[1]) #1.080068
    mat_scattered_direction_z = float(f.readline().split()[1]) #0.942209
    mat_attenuation_x = float(f.readline().split()[1]) #1110.730000
    mat_attenuation_y = float(f.readline().split()[1]) #1110.730000
    mat_attenuation_z = float(f.readline().split()[1]) #10.730000
    ax.scatter(rec_p_x, rec_p_y, rec_p_z, color='k')
    ax.plot([mat_scattered_origin_x, mat_scattered_origin_x+(mat_scattered_direction_x)*200],
            [mat_scattered_origin_y, mat_scattered_origin_y+(mat_scattered_direction_y)*200],
            [mat_scattered_origin_z, mat_scattered_origin_z+(mat_scattered_direction_z)*200])

f.close()
ax.set_xlim3d(-500, 500)
ax.set_ylim3d(-500, 500)
ax.set_zlim3d(-500, 500) 

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

plt.show()
