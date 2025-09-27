import numpy
import time
import os

directory = os.path.abspath(__file__)
folders = directory.split("\\")[:-1]
root_dir = "\\".join(folders) + "\\"

cur_time = str(int(time.time()))

def readDat(dat_path:str) -> list[list[float]]:
    """Returns a list of airfoil points from a .dat file"""
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

def setChord(airfoil_points:list[list[float]], chord:float=1.0) -> list[list[float]]:
    """Scales airfoil to match given chord length"""
    for p in range(len(airfoil_points)):
        airfoil_points[p][0] *= chord
        airfoil_points[p][1] *= chord
    
    return airfoil_points

def applyOffset(airfoil_points:list[list[float]], x_offset:float=0.0, y_offset:float=0.0) -> list[list[float]]:
    """Applies x and y offsets to airfoil points for tapered and swept wings"""
    for p in range(len(airfoil_points)):
        airfoil_points[p][0] += x_offset
        airfoil_points[p][1] += y_offset
    
    return airfoil_points

def inverseTime(xi:float, xf:float, yi:float, yf:float, ai:float, af:float, zi:float, zf:float, feedrate:float, span:float, toolhead_distance:float) -> float:
    """Returns the amount of time it should take to move to [[xf, yf], [af, zf] based on nominal feedrate at center of center of wingspan"""
    w_i = [ai - xi, zi - yi, toolhead_distance]
    w_f = [af - xf, zf - yf, toolhead_distance]
    t_i = [xi, yi, 0]
    t_f = [xf, yf, 0]

    scalar = span * 2 / toolhead_distance
    w_i = [i * scalar for i in w_i]
    w_f = [i * scalar for i in w_f]

    p_i = [w_i[i] + t_i[i] for i in range(2)]
    p_f = [w_f[i] + t_f[i] for i in range(2)]
    [dx, dy] = [p_f[0] - p_i[0], p_f[1] - p_i[1]]

    dw = numpy.sqrt((dx ** 2) + (dy ** 2))
    return feedrate / dw
    
def moveCommand(dx:float=0, dy:float=0, da:float=0, dz:float=0, dt:float=1, rapid:bool=False, error_check:bool=True) -> str:
    """Generates G1 movement command given axis coordinates and feedrate"""
    x = round(dx, 4)
    y = round(dy, 4)
    a = round(da, 4)
    z = round(dz, 4)
    t = round(dt, 6)

    warning_msg = "G-code makes axis move outside of machine boundaries: "
    
    if error_check:
        if (x < 0) or (x > 475):
            print(warning_msg + "X = " + str(x))
        if (y < 0) or (y > 325):
            print(warning_msg + "Y = " + str(y))
        if (z < 0) or (z > 325):
            print(warning_msg + "Z = " + str(z))
        if (a < 0) or (a > 475):
            print(warning_msg + "A = " + str(a))

    axes = "X" + str(x) + " Y" + str(y) + " A" + str(a) + " Z" + str(z) + " F" + str(t) + "\n"
    
    return ("G0 " + axes) if rapid else ("G1 " + axes)

def move2Axis(dx:float=0, dy:float=0, dt:float=1, rapid:bool=False, error_check:bool=True):
    """Simplified 2-axis move requiring only X Y and F parameters"""
    return moveCommand(dx, dy, dx, dy, dt, rapid, error_check)

def gcodeHeader(feed_mode:str="conventional", coordinate:str="absolute", homing:bool=False) -> str:
    """Returns a string with the specified G-code parameters to insert at beginning of CNC file"""
    s = "G21 ; Set units to millimters\n"

    if coordinate == "absolute":
        s += "G90 ; Activate absolute coordinate system mode\n"
    elif coordinate == "relative":
        s += "G91 ; Activate relative coordinate system mode\n"

    if homing:
        s += "G30 ; Home XYAZ axes\n"
    
    if feed_mode == "inverse":
        s += "G93 ; Activate inverse time motion mode\n"
    elif feed_mode == "conventional":
        s += "G94 ; Activate units/mm motion mode\n"
    
    return s + "\n"

def saveDat(points:list[list[float]]) -> str:
    """Returns a string containing contents of dat file given a set of points"""
    s = ""
    
    for i in range(len(points)):
        s += "  ".join(["{:.6f}".format(x) for x in points[i]])
        s += "\n"
    
    return s

def vectorAngle(v1:list[float], v2:list[float]) -> float:
    """Returns an angle [deg] given two three-dimensional vectors: [x1, y1, z1], [x2, y2, z2]"""
    dot = (v1[0] * v2[0]) + (v1[1] * v2[1]) + (v1[2] * v2[2])
    norm1 = ((v1[0] ** 2) + (v1[1] ** 2) + (v1[2] ** 2)) ** 0.5
    norm2 = ((v2[0] ** 2) + (v2[1] ** 2) + (v2[2] ** 2)) ** 0.5

    cosine = dot / (norm1 * norm2)
    radians = numpy.arccos(cosine)
    return (180 * radians) / numpy.pi