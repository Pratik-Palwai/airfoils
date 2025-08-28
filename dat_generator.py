import airfoil_library

M = 0.06
P = 0.40
K = 0.12
# for example, a NACA 4412 airfoil will have a max camber of 4% chord (M = 0.04), max camber at 40% chord (P = 0.40), and max thickness of 12% chord (K = 0.12)

theta_coords = airfoil_library.numpy.linspace(0, airfoil_library.numpy.pi, 100)
cosine_coords = []
camber_points = []
envelope_quadrants = [[], [], [], []]

for b in theta_coords:
    location = 0.5 * (1 - airfoil_library.numpy.cos(b))
    cosine_coords.append(location)

for x in cosine_coords:
    thickness = (5 * K) * ((0.2969 * (x ** 0.5)) + (-0.1260 * x) + (-0.3516 * (x ** 2)) + (0.2843 * (x ** 3)) + (-0.1036 * (x ** 4)))

    if x < P:
        camber = (M / (P ** 2)) * ((2 * P * x) - (x ** 2))
        camber_points.append([x, camber])

        dy_c = (2 * M / (P ** 2)) * (P - x)
        theta = airfoil_library.numpy.arctan(dy_c) + (airfoil_library.numpy.pi / 2)

        gradient = [airfoil_library.numpy.cos(theta), airfoil_library.numpy.sin(theta)]
        k_vector = [(thickness * i) for i in gradient]

        top_envelope_vector = [(x + k_vector[0]), (camber + k_vector[1])]
        bottom_envelope_vector = [(x - k_vector[0]), (camber - k_vector[1])]

        envelope_quadrants[1].append(top_envelope_vector)
        envelope_quadrants[2].append(bottom_envelope_vector)
    
    else:
        camber = (M / ((1 - P) ** 2)) * (1 - (2 * P) + (2 * P * x) - (x ** 2))
        camber_points.append([x, camber])

        dy_c = ((2 * M) / ((1 - P) ** 2)) * (P - x)
        theta = airfoil_library.numpy.arctan(dy_c) + (airfoil_library.numpy.pi / 2)

        gradient = [airfoil_library.numpy.cos(theta), airfoil_library.numpy.sin(theta)]
        k_vector = [(thickness * i) for i in gradient]

        top_envelope_vector = [(x + k_vector[0]), (camber + k_vector[1])]
        bottom_envelope_vector = [(x - k_vector[0]), (camber - k_vector[1])]

        envelope_quadrants[0].append(top_envelope_vector)
        envelope_quadrants[3].append(bottom_envelope_vector)

envelope_points = envelope_quadrants[0][::-1] + envelope_quadrants[1][::-1] + envelope_quadrants[2][1:] + envelope_quadrants[3]

airfoil_code = str(int(M * 100)) + str(int(P * 10)) + str(int(K * 100))
dat_path = airfoil_library.root_dir + "airfoils\\" + airfoil_code + ".dat"
dat_file = open(dat_path, "w")

if M == 0.00:
    P = 0.01 # camber correction for symmetric airfoil cosine spacing. does not affect the geometry of the airfoil

dat_file.write("_Airfoil: " + airfoil_code + "\n")
dat_file.write(airfoil_library.saveDat(points=envelope_points))

dat_file.close()
print("Airfoil path:", dat_path)