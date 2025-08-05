import airfoil_library

spar_radius = 12.5 # mm
spar_y = 25 # distance below current position of wire (mm)
# ensure machine is already homed and wire is placed above or below desired spar location

output_file_path = airfoil_library.root_dir + "gcodes//spar_" + str(int(airfoil_library.time.time())) + "_4axis.cnc"
gcode_file = open(output_file_path, "w")

gcode_file.write("Spar radius: " + str(spar_radius) + " mm | Y location: " + str(spar_y) + " mm\n\n")

gcode_file.write("G21 ; Set machine units to millimeters\n")
gcode_file.write("G94 ; Activate units/min motion mode\n")
gcode_file.write("G90 ; Activate incremental coordinate system mode\n\n")

points = 50 # number of points to approximate spar circle. 50 points is usually enough
theta = 3 * airfoil_library.numpy.pi / 2.0
delta = (2 * airfoil_library.numpy.pi) / points

x_i = 0
y_i = spar_y + spar_radius
gcode_file.write("G1 X" + str(x_i) + " Y" + str(y_i) + " A" + str(x_i) + " Z" + str(y_i) + "\n")

for p in range(points):
    theta = theta + delta

    x_f = spar_radius * airfoil_library.numpy.cos(theta)
    y_f = spar_y + (spar_radius * airfoil_library.numpy.sin(theta))

    dx = round(x_f - x_i, 4)
    dy = round(y_f - y_i, 4)

    [x_i, y_i] = [x_f, x_i]

    gcode_file.write("G1 X" + str(dx) + " Y" + str(dy) + " A" + str(dx) + " Z" + str(dy) + "\n")

print("Spar g-code file: " + output_file_path)
gcode_file.close()