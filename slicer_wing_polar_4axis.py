import airfoil_library

file_airfoil = airfoil_library.root_dir + "airfoils\\6412.dat"

chord_root = 200 # mm
chord_outboard = 100 # mm
outboard_offset = 100 # mm
wingspan = 17.5 * 25.4 # mm

feedrate = 250 # mm/min
chord_height = 7 # mm
root_plane = 0 # 0 places root on XY tower, 1 places root on AZ tower
halfspan = wingspan / 2

output_file_path = airfoil_library.root_dir + "gcodes\\wing_" + airfoil_library.cur_time + "_polar_4axis.cnc"
gcode_file = open(output_file_path, "w")
file_extension = file_airfoil.split(".")[-1]
file_name = file_airfoil.split("\\")[-1]

points_root = airfoil_library.readDat(dat_path=file_airfoil)
points_root = airfoil_library.setChord(airfoil_points=points_root, chord=chord_root)
points_root = airfoil_library.applyOffset(airfoil_points=points_root, y_offset=chord_height)

points_outboard = airfoil_library.readDat(dat_path=file_airfoil)
points_outboard = airfoil_library.setChord(airfoil_points=points_outboard, chord=chord_outboard)
points_outboard = airfoil_library.applyOffset(airfoil_points=points_outboard, x_offset=outboard_offset, y_offset=chord_height)

def oppositePoint(point_root, point_outboard):
    wire_vector = [0, 0, 0]

    for i in range(len(point_root)):
        wire_vector[i] = (point_outboard[i] - point_root[i])

    scalar = 914.4 / wire_vector[2]
    wire_vector = [i * scalar for i in wire_vector]

    return [wire_vector[0] + point_root[0], wire_vector[1] + point_root[1]]

points_opposite = []

for i in range(len(points_root)):
    outboard_point = [points_outboard[i][0], points_outboard[i][1], wingspan]
    root_point = [points_root[i][0], points_root[i][1], 0]
    
    opposite_point = oppositePoint(root_point, outboard_point)
    points_opposite.append(opposite_point)

min_x = 0
for i in range(len(points_root)):
    min_x = min(points_root[i][0], points_opposite[i][0], min_x)

points_root = airfoil_library.applyOffset(airfoil_points=points_root, x_offset=-min_x)
points_opposite = airfoil_library.applyOffset(airfoil_points=points_opposite, x_offset=-min_x)

gcode_file.write("; Airfoil: " + file_name + "\n")
gcode_file.write("; Root chord: " + str(chord_root) + " mm | Wing span: " + str(wingspan) + " mm\n")
gcode_file.write("; Outboard chord: " + str(chord_outboard) + " mm | Outboard offset: " + str(outboard_offset) + " mm\n")
gcode_file.write("; Requested feedrate: " + str(feedrate) + " mm/min | Chord height: " + str(chord_height) + " mm\n\n")

gcode_file.write(airfoil_library.gcodeHeader(feed_mode="inverse"))

if root_plane == 0:
    points_left = points_root
    points_right = points_opposite
elif root_plane == 1:
    points_left = points_opposite
    points_right = points_root

[x_trailing, y_trailing] = [points_left[0][0], points_left[0][1]]
[a_trailing, z_trailing] = [points_right[0][0], points_right[0][1]]
gcode_file.write(airfoil_library.moveCommand(x_trailing, y_trailing, a_trailing, z_trailing, 2000, rapid=True))
gcode_file.write("\n")

for i in range(1, len(points_left)):
    [x, y] = [points_left[i][0], points_left[i][1]]
    [a, z] = [points_right[i][0], points_right[i][1]]

    [x_p, y_p] = [points_left[i - 1][0], points_left[i - 1][1]]
    [a_p, z_p] = [points_right[i - 1][0], points_right[i - 1][1]]

    dt = airfoil_library.inverseTime(x_p, x, y_p, y, a_p, a, z_p, z, feedrate, halfspan)

    gcode_file.write(airfoil_library.moveCommand(x, y, a, z, dt))

gcode_file.write("\n")
gcode_file.write("G94 ; Return to units/mm motion mode\n")

print("Wing g-code file:", output_file_path)
gcode_file.close()