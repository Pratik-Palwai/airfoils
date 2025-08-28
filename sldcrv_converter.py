import airfoil_library

suffix = "7414_spar.dat"
file_extension = suffix.split(".")[-1]
file_name = suffix.split(".")[0]

zero_index = 0
# index of 0 means x-zero, curve is on right plane
# index of 1 means y-zero, curve is on top plane
# index of 2 means z-zero, curve is on front plane

input_path = airfoil_library.root_dir + "airfoils\\" + suffix

crv_path = airfoil_library.root_dir + "curves\\" + file_name + ".sldcrv"
crv_file = open(crv_path, "w")

points = airfoil_library.readDat(dat_path=input_path)

for point in points:
    point.insert(zero_index, 0.000000)
    crv_file.write("    ".join([str(round(coordinate, 6)) for coordinate in point]))
    crv_file.write("\n")

print("Sldcrv path:", crv_path)
crv_file.close()