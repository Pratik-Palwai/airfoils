import airfoil_library

spar_y = -25 # Distance below the wire's current position the spar should be located (mm) (should be negative)
spar_x = 175 # X location of the spar, measured forwards from the trailing edge (mm)
# If the wing is swept the zero point is the trailing edge of the back-most airfoil, usually the tip airfoil
# NACA 4-digit airfoils have max thickness at 30% chord (70% from the trailing edge)

spar_radius = 50 # Millimeters
feedrate = 75 # Millimeters per minute
points = 50 # Number of points that make up the spar circle approximation, 50 points is plenty

gcode_path = airfoil_library.root_dir + "gcodes\\spar_" + str(int(airfoil_library.time.time())) + "_4axis.cnc"
gcode_file = open(gcode_path, "w")

gcode_file.write("; Spar diameter: " + str(spar_radius * 2) + " mm | X location: " + str(spar_x) + " mm | Y location: " + str(spar_y) + " mm\n")

# gcode_file.write("G90 ; Activate relative coordinate system mode\n")
gcode_file.write("G94 ; Activate units/min motion mode\n")
gcode_file.write("M3 S100; Set hot wire to 10% power\n\n")

theta_i = airfoil_library.numpy.pi / 2.0
theta = theta_i
delta = (2 * airfoil_library.numpy.pi) / points

for p in range(points + 1):
    [x, y] = [spar_radius * airfoil_library.numpy.cos(theta), spar_radius * airfoil_library.numpy.sin(theta)]
    [x, y] = [x + spar_x, y + spar_y]
    
    gcode_file.write("G1 X" + str(x) + " Y" + str(y) + " A" + str(x) + " Z" + str(y) + " F" + str(feedrate))
    gcode_file.write("\n")

    theta = theta + delta

gcode_file.write("M5 ; Turn hot wire off\n")
gcode_file.close()

print("Spar g-code file:", gcode_path)