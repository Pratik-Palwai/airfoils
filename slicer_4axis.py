import airfoil_library

airfoil_file_path = airfoil_library.root_dir + "airfoils\\4412.afl" 

chord_left = 400 # mm
chord_right = 200 # mm
offset_left = 0 # mm
offset_right = 200 # mm
# one of the leading edge airfoil offsets should be zero. if both offsets are zero the leading edge will be straight.

feedrate = 2000 # mm/min
chord_height = 25.4 # height of the chord line above the bed

output_file_path = airfoil_library.root_dir + "gcodes\\wing_" + str(int(airfoil_library.time.time())) + ".cnc"
gcode_file = open(output_file_path, "w")

points_left = airfoil_library.readFoil(afl_path=airfoil_file_path)[2]
points_right = airfoil_library.readFoil(afl_path=airfoil_file_path)[2]

points_left = airfoil_library.setChord(airfoil_points=points_left, chord=chord_left)
points_left = airfoil_library.applyOffset(airfoil_points=points_left, x_offset=offset_left, y_offset=chord_height)
points_right = airfoil_library.setChord(airfoil_points=points_right, chord=chord_right)
points_right = airfoil_library.applyOffset(airfoil_points=points_right, x_offset=offset_right, y_offset=chord_height)

gcode_file.write("; Airfoil: NACA " + airfoil_file_path[-8:-4] + "\n")
gcode_file.write("; Left chord: " + str(chord_left) + " mm | Left offset: " + str(offset_left) + " mm\n")
gcode_file.write("; Right chord: " + str(chord_right) + " mm | Right offset: " + str(offset_right) + " mm\n")
gcode_file.write("; Requested feedrate: " + str(feedrate) + "mm/s | Chord height: " + str(chord_height) + " mm\n\n")

gcode_file.write("G21 ; Set units to millimeters\n")
gcode_file.write("G30 ; Home XYZA axes\n")
gcode_file.write("G93 ; Activate inverse time motion mode\n")
gcode_file.write("G90 ; Activate absolute coordinate system mode\n")
# gcode_file.write("M3 S100; Set hot wire to 10% power\n")
# gcode_file.write("G10 L20 P0 X0.000 Y0.000 A0.000 Z0.000 ; Set absolute coordinate system origin\n\n")

[x_i, y_i] = [points_left[0][0], points_left[0][1]]
[a_i, z_i] = [points_right[0][0], points_right[0][1]]
delta = airfoil_library.inverseTime(delta_x=x_i, delta_y=y_i, delta_z=z_i, delta_a=a_i, middle_feedrate=2000)
gcode_file.write(airfoil_library.moveCommand(dx=x_i, dy=y_i, da=a_i, dz=z_i, f=delta))

for i in range(1, len(points_left)):
    [x, y] = [points_left[i][0], points_left[i][1]]
    [a, z] = [points_right[i][0], points_right[i][1]]

    [x_p, y_p] = [points_left[i - 1][0], points_left[i - 1][1 - 1]]
    [a_p, z_p] = [points_right[i - 1][0], points_right[i - 1][1 - 1]]

    dx = abs(x - x_p)
    dy = abs(y - y_p)
    da = abs(a - a_p)
    dz = abs(z - z_p)
    dt = airfoil_library.inverseTime(dx, dy, dz, da, feedrate)

    gcode_file.write(airfoil_library.moveCommand(dx, dy, da, dz, feedrate))

gcode_file.write("\n")
gcode_file.write("M5 ; Turn hotwire off\n")

print("Wing g-code file:", output_file_path)
gcode_file.close()