import airfoil_library
import matplotlib.pyplot as plt

airfoil_suffix = "4418.dat"
split_point = 0.70 # portion of chord airfoil will be split at
cutoff_angle_front = 25 # Angle from vertical front portion of airfoil will be cutoff (deg)
cutoff_angle_back = 20 # Angle from vertical back portion of airfoil will be cutoff (deg)

filename = airfoil_suffix.split(".")[0]
path_main = airfoil_library.root_dir + "airfoils//" + airfoil_suffix
path_front = airfoil_library.root_dir + "airfoils//" + filename + "_front.dat"
path_back = airfoil_library.root_dir + "airfoils//" + filename + "_back.dat"

points_main = tuple(airfoil_library.readDat(dat_path=path_main))
points_front = []
points_back_upper = []
points_back_lower = []

def vectorAngle(v1, v2):
    dot = (v1[0] * v2[0]) + (v1[1] * v2[1])
    norm1 = ((v1[0] ** 2) + (v1[1] ** 2)) ** 0.5
    norm2 = ((v2[0] ** 2) + (v2[1] ** 2)) ** 0.5

    cosine = dot / (norm1 * norm2)
    radians = airfoil_library.numpy.arccos(cosine)
    return (180 * radians) / airfoil_library.numpy.pi

back_split_index = 0
i = 0

while points_main[i][0] >= split_point:
    points_back_upper.append(points_main[i])
    i += 1

cutoff_point = points_back_upper[-1]

while points_main[i][0] < split_point:
    points_front.append(points_main[i])
    i += 1
for i in range(i, len(points_main)):
    points_back_lower.append(points_main[i])

for i in range(len(points_front) - 1, 0, -1):
    dx = points_front[i][0] - points_front[0][0]
    dy = points_front[i][1] - points_front[0][1]
    cutoff_angle = vectorAngle([dx, dy], [0, -1])

    if cutoff_angle > cutoff_angle_front:
        points_front = points_front[:i + 1] + [points_front[0]]
        break

for i in range(1, len(points_back_lower)):
    dx = points_back_lower[i][0] - cutoff_point[0]
    dy = points_back_lower[i][1] - cutoff_point[1]
    cutoff_angle = vectorAngle([dx, dy], [0, -1])

    if cutoff_angle > cutoff_angle_back:
        points_back = points_back_upper + points_back_lower[i:]
        break

file_front = open(path_front, "w")
file_front.write(airfoil_library.saveDat(points_front))
file_front.close()

file_back = open(path_back, "w")
file_back.write(airfoil_library.saveDat(points_back))
file_back.close()

print("Front airfoil file:", path_front)
print("Back airfoil file:", path_back)