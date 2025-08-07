import airfoil_library

file_airfoil = airfoil_library.root_dir + "airfoils\\6415.afl"

chord_root = 400 # mm
chord_outboard = 300 # mm
outboard_offset = 25 # mm
half_span = 609.6 # mm

feedrate = 2000 # mm/min
chord_height = 24.5 # mm
tower_distance = 914.4 # mm
root_plane = 0 # 0 places root on XY tower, 1 places root on AZ tower

output_file_path = airfoil_library.root_dir + "gcodes\\wing_" + str(int(airfoil_library.time.time())) + "_polar_4axis.cnc"
gcode_file = open(output_file_path, "w")
file_extension = file_airfoil.split(".")[-1]

points_root = airfoil_library.readFoil(afl_path=file_airfoil)[2]
points_root = airfoil_library.setChord(airfoil_points=points_root, chord=chord_root)
points_root = airfoil_library.applyOffset(airfoil_points=points_root, y_offset=chord_height)

points_outboard = airfoil_library.readFoil(afl_path=file_airfoil)[2]
points_outboard = airfoil_library.setChord(airfoil_points=points_outboard, chord=chord_outboard)
points_outboard = airfoil_library.applyOffset(airfoil_points=points_outboard, x_offset=outboard_offset, y_offset=chord_height)

points_opposite = []

for i in range(len(points_root)):
    outboard_point = [points_outboard[i][0], points_outboard[i][1], half_span]
    root_point = [points_root[i][0], points_root[i][1], 0]
    
    opposite_point = airfoil_library.oppositePoint(root_point, outboard_point, tower_distance)
    points_opposite.append(opposite_point)

gcode_file.write("; Airfoil: NACA " + file_airfoil[-8:-4] + "\n")
gcode_file.write("; Root chord: " + str(chord_root) + " mm\n")
gcode_file.write("; Outboard chord: " + str(chord_outboard) + " mm | Outboard offset: " + str(outboard_offset) + " mm\n")
gcode_file.write("; Requested feedrate: " + str(feedrate) + "mm/s | Chord height: " + str(chord_height) + " mm\n\n")

gcode_file.write("G21 ; Set units to millimeters\n")
# gcode_file.write("G30 ; Home XYAZ axes\n")
gcode_file.write("G93 ; Activate inverse time motion mode\n")
gcode_file.write("G90 ; Activate absolute coordinate system mode\n")
# gcode_file.write("M3 S100; Set hot wire to 10% power\n")

if root_plane == 0:
    points_left = points_root
    points_right = points_opposite
elif root_plane == 1:
    points_left = points_opposite
    points_right = points_root

[x_i, y_i] = [points_left[0][0], points_left[0][1]]
[a_i, z_i] = [points_right[0][0], points_right[0][1]]
t_i = airfoil_library.inverseTime(delta_x=x_i, delta_y=y_i, delta_z=z_i, delta_a=a_i, middle_feedrate=2000)
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

    gcode_file.write(airfoil_library.moveCommand(x, y, a, z, feedrate))

gcode_file.write("\n")
gcode_file.write("M5 ; Turn hotwire off\n")

print("Wing g-code file:", output_file_path)
gcode_file.close()