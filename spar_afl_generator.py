import airfoil_library
import time

file_prefix = "C:\\Users\\palwa\\Desktop\\code\\software\\python\\dbf\\airfoils\\"
file_path = file_prefix + "spar.afl"
spar_file = open(file_path, "w")

num_points = 100
theta_i = airfoil_library.numpy.pi / 2.0
delta = (2 * airfoil_library.numpy.pi) / num_points

spar_file.write("_Circular spar section | Time generated: " + str(int(time.time())) + " | Number of points: " + str(num_points) + " | Start angle: " + str(round(theta_i, 4)) + " radians\n")

spar_file.write("_Chord line\n")
spar_file.write("0.000000   0.00000\n")
spar_file.write("1.000000   0.00000\n")
spar_file.write("\n")

spar_file.write("_Camber line\n")
spar_file.write("0.000000   0.00000\n")
spar_file.write("1.000000   0.00000\n")
spar_file.write("\n")

spar_file.write("_Spar envelope\n")

theta_f = theta_i
for i in range(num_points + 1):
    x_coord = (0.5 * airfoil_library.numpy.cos(theta_f)) + 0.5
    y_coord = 0.5 * airfoil_library.numpy.sin(theta_f)

    spar_file.write(str(x_coord) + "    " + str(y_coord))
    spar_file.write("\n")

    theta_f = theta_f + delta

print("Spar file:", file_path)
spar_file.close()