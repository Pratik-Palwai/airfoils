import airfoil_library

M = 0.06
P = 0.40
K = 0.14
# for example, a NACA 4412 airfoil will have a max camber of 4% chord (M = 0.04), max camber at 40% chord (P = 0.40), and max thickness of 12% chord (K = 0.12)

airfoil_code = str(int(M * 100)) + str(int(P * 10)) + str(int(K * 100))
dat_path = airfoil_library.root_dir + "airfoils\\" + airfoil_code + ".dat"
dat_file = open(dat_path, "w")

if M == 0.00:
    P = 0.01 # camber correction for symmetric airfoil cosine spacing. does not affect the geometry of the airfoil

envelope_points = airfoil_library.createFoil(max_camber=M, max_camber_pos=P, relative_thickness=K, num_points=200)

dat_file.write("_Airfoil: " + airfoil_code + "\n")
dat_file.write(airfoil_library.saveDat(points=envelope_points))

dat_file.close()
print("Airfoil path:", dat_path)