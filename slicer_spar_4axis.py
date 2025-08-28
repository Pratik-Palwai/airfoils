import airfoil_library

spar_radius = 3.5 # mm
spar_x = -250 * 0.7 # center of spar will be this distance (+ ahead, - behind) current wire position (mm)
spar_y = 5 # center of spar will be this distance (+ above, - below) current wire position (mm)
clearance_y = -10 # wire will initially move up/down (+/-), move x amount, and then move down/up (+/-) to provide clearance (mm)
# useful for moving around the airfoil when the cut is done and the wire is at the trailing edge

feedrate = 250 # mm/min
rapid_feedrate = 300 # rapid feedrate to exit spar hole after cutting (mm/min)
points = 10 # number of points to approximate spar circle

output_file_path = airfoil_library.root_dir + "gcodes//spar_" + airfoil_library.cur_time + "_4axis.cnc"
gcode_file = open(output_file_path, "w")

gcode_file.write("; Spar radius: " + str(spar_radius) + "\n")
gcode_file.write("; Relative X location: " + str(spar_x) + " mm | Relative Y location: " + str(spar_y) + " mm\n")
gcode_file.write("; Y clearance: " + str(clearance_y) + " mm\n")
gcode_file.write("; Requested feedrate: " + str(feedrate) + " mm/min\n")
gcode_file.write("\n")

gcode_file.write(airfoil_library.gcodeHeader(coordinate="relative"))

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

gcode_file.write("\n")
gcode_file.write("G94 ; Return to units/mm motion mode\n")

print("Spar g-code file: " + output_file_path)