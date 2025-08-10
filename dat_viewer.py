import airfoil_library
import turtle

draw_filepath = airfoil_library.root_dir + "airfoils\\4414_back.dat"

envelope = airfoil_library.readDat(dat_path=draw_filepath)
window_chord = 500

airfoil_envelope = airfoil_library.setChord(envelope, chord=window_chord)

airfoil_envelope = airfoil_library.applyOffset(airfoil_points=airfoil_envelope, x_offset=-(window_chord / 2))

plotter = turtle.Turtle(shape="blank")
plotter.speed(0)

plotter.color(1, 0, 0)
plotter.penup()
plotter.goto(airfoil_envelope[0])
plotter.pendown()
for coord in airfoil_envelope[1:]:
    plotter.goto(coord)

turtle.done()