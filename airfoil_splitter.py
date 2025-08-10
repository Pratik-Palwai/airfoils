import airfoil_library

suffix = "4414.dat"
[filename, extension] = suffix.split(".")

split_point = 0.70 # proportion of chord to place top slice point at
front_angle = 25 # angle from vertical the front section of airfoil will be split at (deg)
back_angle = 30 # angle from vertical the back section of airfoil will be split at (deg)

file_input_path = airfoil_library.root_dir + "airfoils\\" + suffix
file_front_path = airfoil_library.root_dir + "airfoils\\" + filename + "_front.dat"
file_back_path = airfoil_library.root_dir + "airfoils\\" + filename + "_back.dat"

front_file = open(file_front_path, "w")
back_file = open(file_back_path, "w")

input_points = airfoil_library.readDat(dat_path=file_input_path)
points_front = []
points_back = []

for i in range(len(input_points)):
    if input_points[i][0] >= split_point:
        points_back.append(input_points[i])
    elif input_points[i][0] < split_point:
        points_front.append(input_points[i])

points_front.append(points_front[0])

vertical_vector = [0, -1]
for i, j in enumerate(points_front[::-1][1:]):
    cutoff_vector = [j[0] - points_front[0][0], j[1] - points_front[0][1]]
    cutoff_angle = airfoil_library.theta(vertical_vector, cutoff_vector)
    
    if cutoff_angle > front_angle:
        break

points_front = points_front[:-i]
points_front.append(points_front[0])

for i, j in enumerate(points_back):
    if abs(points_back[i][1] - points_back[i + 1][1]) > 0.05:
        split_index = i
        break

for i in range(split_index + 1, len(points_back)):
    dx = points_back[i][0] - points_back[split_index][0]
    dy = points_back[i][1] - points_back[split_index][1]
    cutoff_angle = airfoil_library.theta([dx, dy], vertical_vector)

    if cutoff_angle > back_angle:
        break

points_back = points_back[:split_index] + points_back[i:]

front_file.write("_Airfoil: " + filename + " (front) | Top split location: " + str(split_point) + " | Cutoff angle: " + str(front_angle) + "\n")
front_file.write(airfoil_library.saveDat(points_front))
front_file.close()

back_file.write("_Airfoil: " + filename + " (back) | Top split location: " + str(split_point) + " | Cutoff angle: " + str(back_angle) + "\n")
back_file.write(airfoil_library.saveDat(points_back))
back_file.close()

print("Front: " + file_front_path)
print("Back: " + file_back_path)