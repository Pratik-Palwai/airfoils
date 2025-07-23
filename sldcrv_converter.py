import airfoil_library

suffix = "6414.afl"

input_path = airfoil_library.root_dir + "airfoils\\" + suffix
crv_path = airfoil_library.root_dir + "curves\\" + suffix[:4] + ".sldcrv"
crv_file = open(crv_path, "w")

zero_index = 0 
# Index of 0 means X-zero, curve is on right plane (preferred for wings and horizontal tails)
# Index of 1 means Y-zero, curve is on top plane (preferred for vertical tail)
# Index of 2 means Z-zero, curve is on front plane

if input_path[-3:] == "afl":
    points = airfoil_library.readFoil(afl_path=input_path)[2]
elif input_path[-3:] == "dat":
    points = airfoil_library.readDat(dat_path=input_path)

for point in points:
    point.insert(zero_index, 0.000000)
    crv_file.write("    ".join([str(round(coordinate, 6)) for coordinate in point]))
    crv_file.write("\n")

print("Sldcrv path:", crv_path)
crv_file.close()