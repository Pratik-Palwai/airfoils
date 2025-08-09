import airfoil_library

spar_radius = 12.7 # mm
spar_x = 120 # center of spar will be this distance (+ ahead, - behind) current wire position (mm)
spar_y = 0 # center of spar will be this distance (+ above, - below) current wire position (mm)
clearance_y = -20 # wire will initially move up/down (+/-), move x amount, and then move down/up (+/-) to provide clearance (mm)
# useful for moving around the airfoil when the cut is done and the wire is at the trailing edge

feedrate = 200 # mm/min
rapid_feedrate = 500 # rapid feedrate to exit spar hole after cutting (mm/min)
points = 50 # number of points to approximate spar circle

output_file_path = airfoil_library.root_dir + "gcodes//spar_" + str(int(airfoil_library.time.time())) + "_4axis.cnc"
gcode_file = open(output_file_path, "w")

gcode_file.write("Spar radius: " + str(spar_radius) + "\n")
gcode_file.write("Relative X location: " + str(spar_x) + " mm | Relative Y location: " + str(spar_y) + " mm\n")
gcode_file.write("Y clearance: " + str(clearance_y) + " mm\n")
gcode_file.write("Requested feedrate: " + str(feedrate) + " mm/min\n")
gcode_file.write("\n")

gcode_file.write(airfoil_library.gcodeHeader(wire_power=10, coordinate="relative", homing=False))

theta = airfoil_library.numpy.pi / 2
delta = (2 * airfoil_library.numpy.pi) / (points - 1)

gcode_file.write(airfoil_library.move2Axis(dy=clearance_y, dt=feedrate, error_check=False))
gcode_file.write(airfoil_library.move2Axis(dx=spar_x, dt=feedrate, error_check=False))
gcode_file.write(airfoil_library.move2Axis(dy=-clearance_y, dt=feedrate, error_check=False))
gcode_file.write(airfoil_library.move2Axis(dy=spar_y, dt=feedrate, error_check=False))

cur_pos = [0, 0]

for p in range(points):
    x = airfoil_library.numpy.cos(theta) * spar_radius
    y = airfoil_library.numpy.sin(theta) * spar_radius

    dx = cur_pos[0] - x
    dy = cur_pos[1] - y
    
    cur_pos = [x, y]
    theta = (theta + delta) % (2 * airfoil_library.numpy.pi)

    gcode_file.write(airfoil_library.move2Axis(dx, dy, feedrate, error_check=False))

exit_y = -spar_y + spar_radius + clearance_y
gcode_file.write(airfoil_library.move2Axis(dy=exit_y, dt=rapid_feedrate, error_check=False))
gcode_file.write(airfoil_library.move2Axis(dx=-spar_x, dt=rapid_feedrate, error_check=False))
gcode_file.write(airfoil_library.move2Axis(dy=-clearance_y, dt=rapid_feedrate, error_check=False))

gcode_file.write("M5 ; Turn hotwire off\n")

print("Spar g-code file: " + output_file_path)