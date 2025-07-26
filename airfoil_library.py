import numpy
import time

root_dir = "C:\\Users\\palwa\\Desktop\\code\\software\\python\\dbf\\"

def createFoil(max_camber, max_camber_pos, relative_thickness, num_points):
    """Returns a list with two sets of points: [[x, camber], [x, envelope]]"""
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
    return [camber_points, envelope_points]

def readFoil(afl_path):
    """Returns a list of airfoil points: [[chord points], [camber line points], [airfoil envelope points]]"""
    afl_file = open(afl_path, "r")
    segments = [[], [], []]
    state = 0 # 0 state is chord line, 1 state is camber line, 2 state is airfoil envelope

    for line in afl_file.readlines()[2:]:
        if line[0] == "_":
            state = state + 1
            continue

        position_vector = []
        for coordinate in line.split():
            position_vector.append(float(coordinate))
        if position_vector != []:
            segments[state].append(position_vector)
        
    afl_file.close()    
    return segments

def readDat(dat_path):
    """Returns a list of airfoil points from a dat file, without chord or camber line data"""
    dat_file = open(dat_path, "r")
    envelope_points = []

    for line in dat_file.readlines()[1:]:
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

def applyKerfOffset(airfoil_points, kerf_offset=0):
    """Apply given kerf radius offset to airfoil points"""
    kerf_points = [] * len(airfoil_points)
    kerf_points.append([airfoil_points[0][0], airfoil_points[0][1] + kerf_offset])

    for i in range(1, len(airfoil_points) - 1):
        previous = airfoil_points[i - 1]
        next = airfoil_points[i + 1]

        dy = next[1] - previous[1]
        dx = next[0] - previous[0]
        angle = numpy.arctan2(dy, dx)
        
        theta_f = angle + (numpy.pi / 2)
        normal_vector = [numpy.cos(theta_f), numpy.sin(theta_f)]
        
        x_f = airfoil_points[i][0] + (kerf_offset * normal_vector[0])
        y_f = airfoil_points[i][1] + (kerf_offset * normal_vector[1])

        kerf_points.append([x_f, y_f])
    
    kerf_points.append(kerf_points[0])

    return kerf_points

def inverseTime(delta_x, delta_y, delta_a, delta_z, middle_feedrate):
    """Returns the amount of time it should take to complete the move based on requested feedrate (mm/s) at center of wire"""
    delta_x_mid = (delta_x + delta_a) / 2.0
    delta_y_mid = (delta_y + delta_z) / 2.0
    displacement_mid = ((delta_x_mid ** 2) + (delta_y_mid ** 2)) ** 0.5

    delta_t = displacement_mid / middle_feedrate
    delta_t = delta_t / 60
    delta_t = 1 / delta_t

    return round(delta_t, 6)