import airfoil_library

FILE_AIRFOIL = airfoil_library.root_dir + "airfoils\\6412.dat"

CHORD_ROOT = 400 # mm
CHORD_OUTBOARD = 100 # mm
OUTBOARD_OFFSET = 300 # mm
WING_SPAN = 36 * 25.4 # mm

FEEDRATE = 250 # mm/min
CHORD_HEIGHT = 20 # mm
ROOT_PLANE = 0 # 0 places root on XY tower, 1 places root on AZ tower
TOOLHEAD_DISTANCE = 36 * 25.4

if WING_SPAN > TOOLHEAD_DISTANCE:
    raise ValueError("Wing span is greater than toolhead distance")
halfspan = WING_SPAN / 2

output_file_path = airfoil_library.root_dir + "gcodes\\wing_" + airfoil_library.cur_time + "_skewed_4axis.cnc"
gcode_file = open(output_file_path, "w")
file_extension = FILE_AIRFOIL.split(".")[-1]
file_name = FILE_AIRFOIL.split("\\")[-1]

points_root = airfoil_library.readDat(dat_path=FILE_AIRFOIL)
points_root = airfoil_library.setChord(airfoil_points=points_root, chord=CHORD_ROOT)
points_root = airfoil_library.applyOffset(airfoil_points=points_root, y_offset=CHORD_HEIGHT)
points_root = [[x, y, 0] for [x, y] in points_root]

points_outboard = airfoil_library.readDat(dat_path=FILE_AIRFOIL)
points_outboard = airfoil_library.setChord(airfoil_points=points_outboard, chord=CHORD_OUTBOARD)
points_outboard = airfoil_library.applyOffset(airfoil_points=points_outboard, x_offset=OUTBOARD_OFFSET, y_offset=CHORD_HEIGHT)
points_outboard = [[x, y, WING_SPAN] for [x, y] in points_outboard]

trailing_point_root = [points_root[0][0], points_root[0][1], 0]
trailing_point_outboard = [points_outboard[0][0], points_outboard[0][1], WING_SPAN]
trailing_vector = [(trailing_point_outboard[i] - trailing_point_root[i]) for i in range(len(trailing_point_root))]

print("Trailing vector:", trailing_vector)

points_opposite = []

for i in range(len(points_root)):
    outboard_point = [points_outboard[i][0], points_outboard[i][1], WING_SPAN]
    root_point = [points_root[i][0], points_root[i][1], 0]

    wire_vector = [outboard_point[i] - root_point[i] for i in range(len(outboard_point))]
    scalar = 914 / wire_vector[2]
    wire_vector = [i * scalar for i in wire_vector]

    opposite_point = [wire_vector[0] + root_point[0], wire_vector[1] + root_point[1]]
    points_opposite.append(opposite_point)

min_x = 0
for i in range(len(points_root)):
    min_x = min(points_root[i][0], points_opposite[i][0], min_x)

points_root = airfoil_library.applyOffset(airfoil_points=points_root, x_offset=-min_x)
points_opposite = airfoil_library.applyOffset(airfoil_points=points_opposite, x_offset=-min_x)

gcode_file.write("; Airfoil: " + file_name + "\n")
gcode_file.write("; Root chord: " + str(CHORD_ROOT) + " mm | Wing span: " + str(WING_SPAN) + " mm\n")
gcode_file.write("; Outboard chord: " + str(CHORD_OUTBOARD) + " mm | Outboard offset: " + str(OUTBOARD_OFFSET) + " mm\n")
gcode_file.write("; Requested FEEDRATE: " + str(FEEDRATE) + " mm/min | Chord height: " + str(CHORD_HEIGHT) + " mm\n\n")

gcode_file.write(airfoil_library.gcodeHeader(feed_mode="inverse"))