import airfoil_library

airfoil_file_path = airfoil_library.root_dir + "airfoils\\4412.afl"
output_file_path = airfoil_library.root_dir + "gcodes\\wing_" + str(airfoil_library.time.time()) + "_polar.cnc"

chord_root = 400 # mm
chord_outboard = 300 # mm
half_span = 914.4 # mm
offset_outboard = 50 # positive values will put the outboard leading edge ahead of the root leading edge (mm)
root_plane = 0 # 0 will put root chord on left tower (XY) and 1 will put it on right tower (AZ)

feedrate = 2000 # mm/min
chord_height = 25.4 # height of the chord line above the bed
tower_distance = 914.4 # distance between tower XY/AZ planes (mm)

output_file_path = airfoil_library.root_dir + "gcodes\\wing_" + str(int(airfoil_library.time.time())) + "_polar.cnc"
gcode_file = open(output_file_path, "w")

points_root = airfoil_library.readFoil(afl_path=airfoil_file_path)[2]
points_outboard = airfoil_library.readFoil(afl_path=airfoil_file_path)[2]

points_root = airfoil_library.setChord(airfoil_points=points_root, chord=chord_root)
points_outboard = airfoil_library.setChord(airfoil_points=points_outboard, chord=chord_root)

points_root = airfoil_library.applyOffset(airfoil_points=points_root, y_offset=chord_height)
points_outboard = airfoil_library.applyOffset(airfoil_points=points_outboard, x_offset=offset_outboard, y_offset=chord_height)

cartesian_points_root = []
cartesian_points_outboard = []

for i in range(len(points_root)):
    cartesian_points_root.append([points_root[i][0], points_root[i][1], 0])
    cartesian_points_outboard.append([points_outboard[i][0], points_outboard[i][1], half_span])

gcode_file.write("; Airfoil: NACA " + airfoil_file_path[-8:-4] + "\n")
gcode_file.write("; Root chord: " + str(chord_root) + " mm\n")
gcode_file.write("; Outboard chord: " + str(chord_outboard) + " mm | Outboard offset: " + str(offset_outboard) + " mm\n")
gcode_file.write("; Requested feedrate: " + str(feedrate) + "mm/s\n\n")

gcode_file.write("G21 ; Set units to millimeters\n")
# gcode_file.write("G30 ; Home XYZA axes\n")
gcode_file.write("G93 ; Activate inverse time motion mode\n")
gcode_file.write("G90 ; Activate absolute coordinate system mode\n")
# gcode_file.write("M3 S100; Set hot wire to 10% power\n")
# gcode_file.write("G10 L20 P0 X0.000 Y0.000 A0.000 Z0.000 ; Set absolute coordinate system origin\n\n")

[x_i, y_i] = [points_root[0][0], points_root[0][1]]
[x_t, y_t] = [points_outboard[0][0], points_outboard[0][1]]
[a_i, z_i] = airfoil_library.oppositePoint(point_root=cartesian_points_root[0], point_outboard=cartesian_points_outboard[0], plane_distance=tower_distance)
delta = airfoil_library.inverseTime(delta_x=x_i, delta_y=y_i, delta_z=z_i, delta_a=a_i, middle_feedrate=2000)

gcode_file.write(airfoil_library.moveCommand(dx=x_i, dy=y_i, da=a_i, dz=z_i, f=delta))

for i in range(1, len(points_root)):
    [x, y] = [points_root[i][0], points_root[i][1]]
    [x_t, y_t] = [points_outboard[i][0], points_outboard[i][1]]
    [a, z] = airfoil_library.oppositePoint(point_root=cartesian_points_root[i], point_outboard=cartesian_points_outboard[i], plane_distance=tower_distance)

    [x_p, y_p] = [points_root[i - 1][0], points_root[i - 1][1]]
    [x_p_t, y_p_t] = [points_outboard[i - 1][0], points_outboard[i - 1][1]]
    [a_p, z_p] = airfoil_library.oppositePoint(point_root=cartesian_points_root[i - 1], point_outboard=cartesian_points_outboard[i - 1], plane_distance=tower_distance)

    dx = abs(x - x_p)
    dy = abs(y - y_p)
    da = abs(a - a_p)
    dz = abs(z - z_p)
    dt = airfoil_library.inverseTime(dx, dy, da, dz, feedrate)

    gcode_file.write(airfoil_library.moveCommand(dx, dy, da, dz, dt))

gcode_file.write("\n")
gcode_file.write("M5 ; Turn hotwire off\n")

print("Wing g-code file:", output_file_path)
gcode_file.close()