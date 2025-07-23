import airfoil_library

file_right = airfoil_library.root_dir + "airfoils\\4412.afl" 
file_left = airfoil_library.root_dir + "airfoils\\4412.afl"
# If using different airfoils make sure they have the same number of points

chord_left = 200 # Millimeters
chord_right = 200 # Millimeters
offset_left = 0 # Millimeters
offset_right = 0 # Millimeters
# One of the airfoils offsets should be zero. If both offsets are zero the trailing edge will be straight.

feedrate = 250 # Millimeters per minute
kerf = 1 # Radius of the kerf offset. Usually 1mm is accurate enough
foam_thickness = 50.8 # Trailing edge will be at half the foam thickness (millimeters). Set at zero for manual homing

file_gcode_path = airfoil_library.root_dir + "gcodes\\wing_" + str(int(airfoil_library.time.time())) + "_4axis.cnc"
gcode_file = open(file_gcode_path, "w")

points_left = airfoil_library.readFoil(afl_path=file_left)[2]
points_right = airfoil_library.readFoil(afl_path=file_right)[2]

points_left = airfoil_library.setChord(airfoil_points=points_left, chord=chord_left)
points_left = airfoil_library.applyOffset(airfoil_points=points_left, x_offset=offset_left, y_offset=(foam_thickness / 2.0))
points_right = airfoil_library.setChord(airfoil_points=points_right, chord=chord_right)
points_right = airfoil_library.applyOffset(airfoil_points=points_right, x_offset=offset_right, y_offset=(foam_thickness / 2.0))

# points_left = airfoil_library.applyKerfOffset(airfoil_points=points_left, kerf_offset=kerf)
# points_right = airfoil_library.applyKerfOffset(airfoil_points=points_right, kerf_offset=kerf)

gcode_file.write("; Left airfoil: NACA " + file_left[-8:-4] + " mm | Left chord: " + str(chord_left) + " mm | Left offset: " + str(offset_left) + "mm\n")
gcode_file.write("; Right airfoil: NACA " + file_right[-8:-4] + " mm | Right chord: " + str(chord_right) + " mm | Right offset: " + str(offset_right) + " mm\n")
gcode_file.write("; Requested feedrate: " + str(feedrate) + "mm/s | Requested feedrate: " + str(feedrate) + "mm/s\n")
gcode_file.write("; Tower plane distance: 1000 mm\n\n")

gcode_file.write("G21 ; Set units to millimeters\n")
gcode_file.write("G28 ; Home XYZA axes\n")
gcode_file.write("G93 ; Activate inverse time motion mode\n")
gcode_file.write("G90 ; Activate absolute coordinate system mode\n")
gcode_file.write("M3 S100; Set hot wire to 10% power\n\n")

[x_i, y_i] = [points_left[0][0], points_left[0][1]]
[a_i, z_i] = [points_right[0][0], points_right[0][1]]
delta = airfoil_library.inverseTime(delta_x=x_i, delta_y=y_i, delta_z=z_i, delta_a=a_i, middle_feedrate=200)
gcode_file.write("G1 X"  + str(round(x_i, 4)) + " Y" + str(round(y_i, 4)) + " A" + str(round(a_i, 4)) + " Z" + str(round(z_i, 4)) + " F" + str(delta) + "\n")

for i in range(1, len(points_left)):
    [x, y] = [points_left[i][0], points_left[i][1]]
    [a, z] = [points_right[i][0], points_right[i][1]]

    [x_p, y_p] = [points_left[i - 1][0], points_left[i - 1][1 - 1]]
    [a_p, z_p] = [points_right[i - 1][0], points_right[i - 1][1 - 1]]

    dx = abs(x - x_p)
    dy = abs(y - y_p)
    dz = abs(z - z_p)
    da = abs(a - a_p)
    dt = airfoil_library.inverseTime(dx, dy, dz, da, feedrate)

    gcode_file.write("G1 X" + str(round(x, 4)) + " Y" + str(round(y, 4)) + " A" + str(round(a, 4)) + " Z" + str(round(z, 4)) + " F" + str(dt))
    gcode_file.write("\n")

gcode_file.write("\n")
gcode_file.write("M5 ; Turn hotwire off\n")

print("Foamcut g-code file:", file_gcode_path)
gcode_file.close()