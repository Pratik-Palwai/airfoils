import numpy
import time
import os

directory = os.path.abspath(__file__)
folders = directory.split("\\")[:-1]

root_dir = "\\".join(folders) + "\\"

def createFoil(max_camber, max_camber_pos, relative_thickness, num_points):
    """Returns a list of airfoil envelope points starting from the trailing edge"""
    M = max_camber
    P = max_camber_pos
    T = relative_thickness

    x_coordinates = cosineSpacing(num_points=num_points)
    camber_points = []
    envelope_quadrants = [[], [], [], []]

    for x in x_coordinates:
        thickness = (5 * T) * ((0.2969 * (x ** 0.5)) + (-0.1260 * x) + (-0.3516 * (x ** 2)) + (0.2843 * (x ** 3)) + (-0.1036 * (x ** 4)))

        if x < P:
            camber = (M / (P ** 2)) * ((2 * P * x) - (x ** 2))
            camber_points.append([x, camber])

            dy_c = (2 * M / (P ** 2)) * (P - x)
            theta = numpy.arctan(dy_c) + (numpy.pi / 2)

            gradient = [numpy.cos(theta), numpy.sin(theta)]
            k_vector = [(thickness * i) for i in gradient]

            top_envelope_vector = [(x + k_vector[0]), (camber + k_vector[1])]
            bottom_envelope_vector = [(x - k_vector[0]), (camber - k_vector[1])]

            envelope_quadrants[1].append(top_envelope_vector)
            envelope_quadrants[2].append(bottom_envelope_vector)
        
        else:
            camber = (M / ((1 - P) ** 2)) * (1 - (2 * P) + (2 * P * x) - (x ** 2))
            camber_points.append([x, camber])

            dy_c = ((2 * M) / ((1 - P) ** 2)) * (P - x)
            theta = numpy.arctan(dy_c) + (numpy.pi / 2)

            gradient = [numpy.cos(theta), numpy.sin(theta)]
            k_vector = [(thickness * i) for i in gradient]

            top_envelope_vector = [(x + k_vector[0]), (camber + k_vector[1])]
            bottom_envelope_vector = [(x - k_vector[0]), (camber - k_vector[1])]

            envelope_quadrants[0].append(top_envelope_vector)
            envelope_quadrants[3].append(bottom_envelope_vector)

    envelope_points = envelope_quadrants[0][::-1] + envelope_quadrants[1][::-1] + envelope_quadrants[2][1:] + envelope_quadrants[3]
    return envelope_points

def readDat(dat_path):
    """Returns a list of airfoil points from a dat file"""
    dat_file = open(dat_path, "r")
    envelope_points = []

    for line in dat_file.readlines():
        if line[0] != "_":
            point = []

            for coordinate in line.split():
                point.append(float(coordinate))
            if point != []:
                envelope_points.append(point)
    
    return envelope_points

def setChord(airfoil_points, chord=1):
    """Scales airfoil to match given chord length"""
    for p in range(len(airfoil_points)):
        airfoil_points[p][0] *= chord
        airfoil_points[p][1] *= chord
    
    return airfoil_points

def applyOffset(airfoil_points, x_offset=0, y_offset=0):
    """Applies x and y offsets to airfoil points for tapered and swept wings"""
    for p in range(len(airfoil_points)):
        airfoil_points[p][0] += x_offset
        airfoil_points[p][1] += y_offset
    
    return airfoil_points

def cosineSpacing(num_points):
    """Returns a list of cosine-spaced x coordinates between 0 and 1 for optimal airfoil plotting: [x1, x2, x3, ...]"""
    x_coords = []
    b_coords = numpy.linspace(0, numpy.pi, num_points)

    for b in b_coords:
        location = 0.5 * (1 - numpy.cos(b))
        x_coords.append(location)
    
    return x_coords

def inverseTime(dx, dy, da, dz, middle_feedrate):
    """Returns the amount of time it should take to complete the move based on requested feedrate (mm/min) at center of wire"""
    delta_h = (dx + da) / 2.0
    delta_v = (dy + dz) / 2.0
    displacement_mid = ((delta_h ** 2) + (delta_v ** 2)) ** 0.5

    delta_t = displacement_mid / middle_feedrate
    delta_t = 1 / delta_t

    return round(delta_t, 6)

def oppositePoint(point_root, point_outboard, plane_distance):
    """Generates root-opposite point [x_o, y_o] based on the airfoil points and tower distance"""
    wire_vector = [0, 0, 0]

    for i in range(len(point_root)):
        wire_vector[i] = (point_outboard[i] - point_root[i])

    scalar = plane_distance / wire_vector[2]
    wire_vector = [i * scalar for i in wire_vector]

    return [wire_vector[0] + point_root[0], wire_vector[1] + point_root[1]]

def moveCommand(dx=0, dy=0, da=0, dz=0, dt=1, error_check=True):
    """Generates G1 movement command given axis coordinates and feedrate"""
    x = round(dx, 4)
    y = round(dy, 4)
    a = round(da, 4)
    z = round(dz, 4)
    t = round(dt, 6)

    warning_front = "G-code makes axis move outside of machine boundaries: "
    
    if error_check:
        if (x < 0) or (x > 425):
            print(warning_front + "X = " + str(x))
        if (y < 0) or (y > 325):
            print(warning_front + "Y = " + str(y))
        if (z < 0) or (z > 325):
            print(warning_front + "Z = " + str(z))
        if (a < 0) or (a > 425):
            print(warning_front + "A = " + str(a))

    return "G1 X" + str(x) + " Y" + str(y) + " A" + str(a) + " Z" + str(z) + " F" + str(t) + "\n"

def move2Axis(dx=0, dy=0, dt=1, error_check=True):
    """Simplified 2-axis move requiring only X Y and F sections"""
    return moveCommand(dx, dy, dx, dy, dt, error_check)

def gcodeHeader(feed_mode="conventional", wire_power=0, coordinate="absolute", homing=True):
    """Returns a string with the specified G-code parameters to insert at beginning of CNC file"""
    s = "G21 ; Set units to millimters\n"

    if coordinate == "absolute":
        s += "G90 ; Activate absolute coordinate system mode\n"
    elif coordinate == "relative":
        s += "G91 ; Activate relative coordinate system mode\n"

    if homing:
        s += "G30 ; Home XYAZ axes\n"
    
    s += "M3 S" + str(wire_power * 10) + " ; Set hot wire to " + str(wire_power) + " percent power\n"

    if feed_mode == "inverse":
        s += "G93 ; Activate inverse time motion mode\n"
    elif feed_mode == "conventional":
        s += "G94 ; Activate units/mm motion mode\n"
    
    return s + "\n"

def saveDat(points):
    """Returns a string containing contents of dat file given a set of points"""
    s = ""
    
    for i in range(len(points)):
        s += "  ".join(["{:.6f}".format(x) for x in points[i]])
        s += "\n"
    
    return s

def vectorAngle(v1, v2):
    """Returns angle between two 2D vectors v1 and v2"""
    dot = (v1[0] * v2[0]) + (v1[1] * v2[1])
    norm1 = ((v1[0] ** 2) + (v1[1] ** 2)) ** 0.5
    norm2 = ((v2[0] ** 2) + (v2[1] ** 2)) ** 0.5

    cosine = dot / (norm1 * norm2)
    radians = numpy.arccos(cosine)
    return (180 * radians) / numpy.pi