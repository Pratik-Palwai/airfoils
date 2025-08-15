import airfoil_library

file_airfoil = airfoil_library.root_dir + "airfoils\\4414.dat"

chord_left = 400 # mm
chord_right = 300 # mm
offset_left = 0 # mm
offset_right = 25 # mm
# one of the leading edge airfoil offsets should be zero. if both offsets are zero the leading edge will be straight.

feedrate = 2000 # in/min
chord_height = 50 # height of the chord line above the bed

output_file_path = airfoil_library.root_dir + "gcodes\\wing_" + str(int(airfoil_library.time.time())) + "_trapezoidal_4axis.cnc"
gcode_file = open(output_file_path, "w")
file_extension = file_airfoil.split(".")[-1]
file_name = file_airfoil.split("\\")[-1]

points_left = airfoil_library.readDat(dat_path=file_airfoil)
points_right = airfoil_library.readDat(dat_path=file_airfoil)

points_left = airfoil_library.setChord(airfoil_points=points_left, chord=chord_left)
points_left = airfoil_library.applyOffset(airfoil_points=points_left, x_offset=offset_left, y_offset=chord_height)
points_left = airfoil_library.applyOffset(airfoil_points=points_left, x_offset=1)

points_right = airfoil_library.setChord(airfoil_points=points_right, chord=chord_right)
points_right = airfoil_library.applyOffset(airfoil_points=points_right, x_offset=offset_right, y_offset=chord_height)
points_right = airfoil_library.applyOffset(airfoil_points=points_right, x_offset=1)

gcode_file.write("; Airfoil: " + file_name + "\n")
gcode_file.write("; Left chord: " + str(chord_left) + " mm | Left offset: " + str(offset_left) + " mm\n")
gcode_file.write("; Right chord: " + str(chord_right) + " mm | Right offset: " + str(offset_right) + " mm\n")
gcode_file.write("; Requested feedrate: " + str(feedrate) + "mm/s | Chord height: " + str(chord_height) + " mm\n\n")

gcode_file.write(airfoil_library.gcodeHeader(feed_mode="inverse", wire_power=10))

[x_i, y_i] = [points_left[0][0], points_left[0][1]]
[a_i, z_i] = [points_right[0][0], points_right[0][1]]
t_i = airfoil_library.inverseTime(x_i, y_i, z_i, a_i, 2000)
gcode_file.write(airfoil_library.moveCommand(x_i, y_i, a_i, z_i, t_i))

for i in range(1, len(points_left)):
    [x, y] = [points_left[i][0], points_left[i][1]]
    [a, z] = [points_right[i][0], points_right[i][1]]

    [x_p, y_p] = [points_left[i - 1][0], points_left[i - 1][1]]
    [a_p, z_p] = [points_right[i - 1][0], points_right[i - 1][1]]

    dx = abs(x - x_p)
    dy = abs(y - y_p)
    da = abs(a - a_p)
    dz = abs(z - z_p)
    dt = airfoil_library.inverseTime(dx, dy, dz, da, feedrate)

    gcode_file.write(airfoil_library.moveCommand(x, y, a, z, dt))

gcode_file.write("\n")
gcode_file.write("M5 ; Turn hotwire off\n")

print("Wing g-code file:", output_file_path)
gcode_file.close()