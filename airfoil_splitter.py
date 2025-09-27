import airfoil_library
import matplotlib.pyplot as plt

AIRFOIL_SUFFIX = "6412.dat"
SPLIT_POINT = 0.70 # portion of chord airfoil will be split at
CUTOFF_ANGLE_FRONT = 25 # Angle from vertical front portion of airfoil will be cutoff (deg)
CUTOFF_ANGLE_BACK = 20 # Angle from vertical back portion of airfoil will be cutoff (deg)

filename = AIRFOIL_SUFFIX.split(".")[0]
path_main = airfoil_library.root_dir + "airfoils//" + AIRFOIL_SUFFIX
path_front = airfoil_library.root_dir + "airfoils//" + filename + "_front.dat"
path_back = airfoil_library.root_dir + "airfoils//" + filename + "_back.dat"

points_main = tuple(airfoil_library.readDat(dat_path=path_main))
points_front = []
points_back_upper = []
points_back_lower = []

back_split_index = 0
i = 0

while points_main[i][0] >= SPLIT_POINT:
    points_back_upper.append(points_main[i])
    i += 1

cutoff_point = points_back_upper[-1]

while points_main[i][0] < SPLIT_POINT:
    points_front.append(points_main[i])
    i += 1
for i in range(i, len(points_main)):
    points_back_lower.append(points_main[i])

for i in range(len(points_front) - 1, 0, -1):
    dx = points_front[i][0] - points_front[0][0]
    dy = points_front[i][1] - points_front[0][1]
    cutoff_angle = airfoil_library.vectorAngle([dx, dy, 0], [0, -1, 0])

    if cutoff_angle > CUTOFF_ANGLE_FRONT:
        points_front = points_front[:i + 1] + [points_front[0]]
        break

for i in range(1, len(points_back_lower)):
    dx = points_back_lower[i][0] - cutoff_point[0]
    dy = points_back_lower[i][1] - cutoff_point[1]
    cutoff_angle = airfoil_library.vectorAngle([dx, dy, 0], [0, -1, 0])

    if cutoff_angle > CUTOFF_ANGLE_BACK:
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