import airfoil_library

SUFFIX = "7414_spar.dat"
ZERO_INDEX = 0
# index of 0 means x-zero, curve is on right plane
# index of 1 means y-zero, curve is on top plane
# index of 2 means z-zero, curve is on front plane

file_extension = SUFFIX.split(".")[-1]
file_name = SUFFIX.split(".")[0]

input_path = airfoil_library.root_dir + "airfoils\\" + SUFFIX

crv_path = airfoil_library.root_dir + "curves\\" + file_name + ".sldcrv"
crv_file = open(crv_path, "w")

points = airfoil_library.readDat(dat_path=input_path)

for point in points:
    point.insert(ZERO_INDEX, 0.000000)
    crv_file.write("    ".join([str(round(coordinate, 6)) for coordinate in point]))
    crv_file.write("\n")

print("Sldcrv path:", crv_path)
crv_file.close()