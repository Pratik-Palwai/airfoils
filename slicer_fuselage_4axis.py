import airfoil_library

file_fuselage = airfoil_library.root_dir + "airfoils\\fuselage.dat"

feedrate = 1500 # mm/min
fuselage_length = 914.4 # mm
fuselage_height = 135 # height of fuselage top above the bed (mm)
# cosmos EPS foam fuselages are 36"L x 5"H x 2.5"W and g-code starts from top rear corner

output_file_path = airfoil_library.root_dir + "gcodes\\fuselage_" + str(int(airfoil_library.time.time())) + "_4axis.cnc"
gcode_file = open(output_file_path, "w")
file_extension = file_fuselage.split(".")[-1]

if file_extension == "afl":
    points = airfoil_library.readFoil(afl_path=file_fuselage)[2]
elif file_extension == "dat":
    points = airfoil_library.readDat(dat_path=file_fuselage)

points = airfoil_library.setChord(airfoil_points=points, chord=fuselage_length)
points = airfoil_library.applyOffset(airfoil_points=points, x_offset=1, y_offset=fuselage_height)

gcode_file.write("; Fuselage 4-axis\n")
gcode_file.write("; Chord: " + str(fuselage_length) + " mm | Chord height: " + str(fuselage_height) + " mm\n")
gcode_file.write("; Requested feedrate: " + str(feedrate) + "mm/s | Chord height: " + str(fuselage_height) + " mm\n\n")

gcode_file.write(airfoil_library.gcodeHeader(feed_mode="conventional", wire_power=10))

[x_i, y_i] = [points[0][0], points[0][1]]
gcode_file.write(airfoil_library.move2Axis(x_i, y_i, feedrate))

for i in range(1, len(points)):
    [x, y] = [points[i][0], points[i][1]]
    [x_p, y_p] = [points[i - 1][0], points[i - 1][1]]

    gcode_file.write(airfoil_library.move2Axis(x, y, feedrate))

gcode_file.write("\n")
gcode_file.write("M5 ; Turn hotwire off\n")

print("Wing g-code file:", output_file_path)
gcode_file.close()