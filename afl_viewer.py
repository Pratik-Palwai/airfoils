import airfoil_library
import turtle

draw_filepath = airfoil_library.root_dir + "airfoils\\0016.afl"

lines = airfoil_library.readFoil(afl_path=draw_filepath)
window_chord = 500

chord_line = airfoil_library.setChord(lines[0], chord=window_chord)
camber_line = airfoil_library.setChord(lines[1], chord=window_chord)
airfoil_envelope = airfoil_library.setChord(lines[2], chord=window_chord)

chord_line = airfoil_library.applyOffset(airfoil_points=chord_line, x_offset=-(window_chord / 2))
camber_line = airfoil_library.applyOffset(airfoil_points=camber_line, x_offset=-(window_chord / 2))
airfoil_envelope = airfoil_library.applyOffset(airfoil_points=airfoil_envelope, x_offset=-(window_chord / 2))

plotter = turtle.Turtle(shape="blank")
plotter.speed(0)

plotter.color(0, 0, 1)
plotter.penup()
plotter.goto(chord_line[0])
plotter.pendown()
for coord in chord_line[1:]:
    plotter.goto(coord)

plotter.color(0, 1, 0)
plotter.penup()
plotter.goto(camber_line[0])
plotter.pendown()
for coord in camber_line[1:]:
    plotter.goto(coord)

plotter.color(1, 0, 0)
plotter.penup()
plotter.goto(airfoil_envelope[0])
plotter.pendown()
for coord in airfoil_envelope[1:]:
    plotter.goto(coord)

turtle.done()