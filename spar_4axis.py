import airfoil_library

spar_radius = 10 # mm
spar_y = -25 # center of spar will be this far away from current position of wire

output_file_path = airfoil_library.root_dir + "gcodes\\spar_" + str(int(airfoil_library.time.time())) + "_4axis.cnc"
gcode_file = open(output_file_path, "w")

