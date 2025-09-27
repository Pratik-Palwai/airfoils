import airfoil_library

SPAR_RADIUS = 3.5 # mm
SPAR_X = -250 * 0.7 # center of spar will be this distance (+ ahead, - behind) current wire position (mm)
SPAR_Y = 5 # center of spar will be this distance (+ above, - below) current wire position (mm)
CLEARANCE_Y = -10 # wire will initially move up/down (+/-), move x amount, and then move down/up (+/-) to provide clearance (mm)
# useful for moving around the airfoil when the cut is done and the wire is at the trailing edge

FEEDRATE = 250 # mm/min
RAPID_FEEDRATE = 300 # rapid feedrate to exit spar hole after cutting (mm/min)
POINTS = 10 # number of POINTS to approximate spar circle

output_file_path = airfoil_library.root_dir + "gcodes//spar_" + airfoil_library.cur_time + "_4axis.cnc"
gcode_file = open(output_file_path, "w")

gcode_file.write("; Spar radius: " + str(SPAR_RADIUS) + "\n")
gcode_file.write("; Relative X location: " + str(SPAR_X) + " mm | Relative Y location: " + str(SPAR_Y) + " mm\n")
gcode_file.write("; Y clearance: " + str(CLEARANCE_Y) + " mm\n")
gcode_file.write("; Requested FEEDRATE: " + str(FEEDRATE) + " mm/min\n")
gcode_file.write("\n")

gcode_file.write(airfoil_library.gcodeHeader(coordinate="relative"))

theta = airfoil_library.numpy.pi / 2
delta = (2 * airfoil_library.numpy.pi) / (POINTS - 1)

gcode_file.write(airfoil_library.move2Axis(dy=CLEARANCE_Y, dt=FEEDRATE, error_check=False))
gcode_file.write(airfoil_library.move2Axis(dx=SPAR_X, dt=FEEDRATE, error_check=False))
gcode_file.write(airfoil_library.move2Axis(dy=-CLEARANCE_Y, dt=FEEDRATE, error_check=False))
gcode_file.write(airfoil_library.move2Axis(dy=SPAR_Y, dt=FEEDRATE, error_check=False))

cur_pos = [0, 0]

for p in range(POINTS):
    x = airfoil_library.numpy.cos(theta) * SPAR_RADIUS
    y = airfoil_library.numpy.sin(theta) * SPAR_RADIUS

    dx = cur_pos[0] - x
    dy = cur_pos[1] - y
    
    cur_pos = [x, y]
    theta = (theta + delta) % (2 * airfoil_library.numpy.pi)

    gcode_file.write(airfoil_library.move2Axis(dx, dy, FEEDRATE, error_check=False))

exit_y = -SPAR_Y + SPAR_RADIUS + CLEARANCE_Y
gcode_file.write(airfoil_library.move2Axis(dy=exit_y, dt=RAPID_FEEDRATE, error_check=False))
gcode_file.write(airfoil_library.move2Axis(dx=-SPAR_X, dt=RAPID_FEEDRATE, error_check=False))
gcode_file.write(airfoil_library.move2Axis(dy=-CLEARANCE_Y, dt=RAPID_FEEDRATE, error_check=False))

gcode_file.write("\n")
gcode_file.write("G94 ; Return to units/mm motion mode\n")

print("Spar g-code file: " + output_file_path)