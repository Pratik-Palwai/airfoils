import airfoil_library
import matplotlib.pyplot as plt

draw_filepath = airfoil_library.root_dir + "airfoils\\6414.dat"
filename = draw_filepath.split("\\")[-1]

airfoil_envelope = airfoil_library.readDat(dat_path=draw_filepath)
airfoil_envelope = airfoil_library.setChord(airfoil_envelope, chord=1)
airfoil_envelope_transpose = [[], []]

for i in range(len(airfoil_envelope)):
    airfoil_envelope_transpose[0].append(airfoil_envelope[i][0])
    airfoil_envelope_transpose[1].append(airfoil_envelope[i][1])

plt.plot(airfoil_envelope_transpose[0], airfoil_envelope_transpose[1])
plt.xlim(-0.1, 1.1)
plt.gca().set_aspect("equal")

plt.title("Airfoil: " + filename)
plt.show()