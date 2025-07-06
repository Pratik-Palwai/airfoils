import airfoil_library
import time

file_prefix = "C:\\Users\\palwa\\Desktop\\code\\software\\python\\dbf\\"
file_right = file_prefix + "airfoils\\9414.afl" 
file_left = file_prefix + "airfoils\\9414.afl" # If using different airfoils make sure they have the same number of points

file_gcode_path = file_prefix + "gcodes\\gcode_" + str(int(time.time())) + "_4axis.foamcut"
gcode_file = open(file_gcode_path, "w")

points_left = airfoil_library.readFoil(afl_path=file_left)[2]
points_right = airfoil_library.readFoil(afl_path=file_right)[2]

feedrate = 250 # Millimeters per second
chord_left = 200 # Millimeters
chord_right = 120 # Millimeters
offset_left = 0 # Millimeters
offset_right = 0 # Millimeters
# One of these offsets should be zero. If both offsets are zero the trailing edge will be straight.

points_left = airfoil_library.setChord(airfoil_points=points_left, chord=chord_left)
points_left = airfoil_library.applyOffset(airfoil_points=points_left, x_offset=offset_left)
points_right = airfoil_library.setChord(airfoil_points=points_right, chord=chord_right)
points_right = airfoil_library.applyOffset(airfoil_points=points_right, x_offset=offset_right)

feedrate = round(feedrate * (1 / (2 ** 0.5)), 4) # Adjusts feedrate to be "distributed" between four axes

gcode_file.write("; Left airfoil: NACA " + file_left[-8:-4] + " Left chord: " + str(chord_left) + " | Left offset: " + str(offset_left) + "\n")
gcode_file.write("; Right airfoil: NACA " + file_right[-8:-4] + " Right chord: " + str(chord_right) + " | Right offset: " + str(offset_right) + "\n")
gcode_file.write("; Requested feedrate: " + str(feedrate) + "mm/s\n\n")

gcode_file.write("M104 T1 ; Turn hotwire on\n")
gcode_file.write("G28.4 ; Home XYAB axes\n")
gcode_file.write("ATTACH_MOTORS ; Pair stepper motors to XYAB axes\n\n")

for i in range(len(points_left)):
    [x, y] = [points_left[i][0], points_left[i][1]]
    [a, b] = [points_right[i][0], points_right[i][1]]

    gcode_file.write("G1 X" + str(round(x, 4)) + " Y" + str(round(y, 4)) + " A" + str(round(a, 4)) + " B" + str(round(b, 4)) + " F" + str(feedrate))
    gcode_file.write("\n")
    gcode_file.write("M117 X" + str(int(x)) + " Y" + str(int(y)) + " A" + str(int(a)) + " B" + str(int(b)))
    gcode_file.write("\n")

gcode_file.write("\n")
gcode_file.write("M104 T0 ; Turn hotwire off\n")
gcode_file.write("M84 ; Disable stepper motors\n")

print("Foamcut g-code file:", file_gcode_path)
gcode_file.close()