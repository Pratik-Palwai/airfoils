import airfoil_library

M = 0.04
P = 0.40
K = 0.12
# For example, a NACA 4412 airfoil will have a max camber of 4% chord (M = 0.04), max camber at 40% chord (P = 0.40), and max thickness of 12% chord (K = 0.12)

airfoil_code = str(int(M * 100)) + str(int(P * 10)) + str(int(K * 100))
afl_path = airfoil_library.root_dir + "airfoils\\" + airfoil_code + ".afl"
afl_file = open(afl_path, "w")

[camber_line_points, envelope_points] = airfoil_library.createFoil(max_camber=M, max_camber_pos=P, relative_thickness=K, num_points=50)

afl_file.write("_Airfoil: NACA " + airfoil_code + " | Max camber: " + str(M) + " chord | Max camber at " + str(P) + " chord | Airfoil thickness: " + str(K) + " chord\n")

afl_file.write("_Chord line\n")
afl_file.write("0.000000    0.000000\n")
afl_file.write("1.000000    0.000000\n")
afl_file.write("\n")

afl_file.write("_Camber line\n")
for x in range(len(camber_line_points)):
    afl_file.write("    ".join([str(round(a, 6)) for a in camber_line_points[x]]))
    afl_file.write("\n")
afl_file.write("\n")

afl_file.write("_Airfoil envelope\n")
for vector in envelope_points:
    afl_file.write("    ".join([str(round(vector[0], 6)), str(round(vector[1], 6))]))
    afl_file.write("\n")

afl_file.close()
print("Airfoil path:", afl_path)