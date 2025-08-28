import numpy
import time
import os

directory = os.path.abspath(__file__)
folders = directory.split("\\")[:-1]
root_dir = "\\".join(folders) + "\\"

cur_time = str(int(time.time()))

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

def inverseTime(xi, xf, yi, yf, ai, af, zi, zf, feedrate, span):
    """Returns the amount of time it should take to move to [[xf, yf], [af, zf] based on requested feedrate (mm/min) at center of center of wingspan"""
    w_i = [ai - xi, zi - yi, 914.4]
    w_f = [af - xf, zf - yf, 914.4]
    t_i = [xi, yi, 0]
    t_f = [xf, yf, 0]

    scalar = span * 2 / 914.4
    w_i = [i * scalar for i in w_i]
    w_f = [i * scalar for i in w_f]

    p_i = [w_i[i] + t_i[i] for i in range(2)]
    p_f = [w_f[i] + t_f[i] for i in range(2)]
    [dx, dy] = [p_f[0] - p_i[0], p_f[1] - p_i[1]]

    dw = ((dx ** 2) + (dy ** 2)) ** 0.5
    return feedrate / dw
    
def moveCommand(dx=0, dy=0, da=0, dz=0, dt=1, rapid=False, error_check=True):
    """Generates G1 movement command given axis coordinates and feedrate"""
    x = round(dx, 4)
    y = round(dy, 4)
    a = round(da, 4)
    z = round(dz, 4)
    t = round(dt, 6)

    warning_front = "G-code makes axis move outside of machine boundaries: "
    
    if error_check:
        if (x < 0) or (x > 475):
            print(warning_front + "X = " + str(x))
        if (y < 0) or (y > 325):
            print(warning_front + "Y = " + str(y))
        if (z < 0) or (z > 325):
            print(warning_front + "Z = " + str(z))
        if (a < 0) or (a > 475):
            print(warning_front + "A = " + str(a))

    axes = "X" + str(x) + " Y" + str(y) + " A" + str(a) + " Z" + str(z) + " F" + str(t) + "\n"
    
    if rapid:
        return "G0 " + axes
    else:
        return "G1 " + axes

def move2Axis(dx=0, dy=0, dt=1, rapid=False, error_check=True):
    """Simplified 2-axis move requiring only X Y and F sections"""
    return moveCommand(dx, dy, dx, dy, dt, rapid, error_check)

def gcodeHeader(feed_mode="conventional", coordinate="absolute", homing=False):
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

def saveDat(points):
    """Returns a string containing contents of dat file given a set of points"""
    s = ""
    
    for i in range(len(points)):
        s += "  ".join(["{:.6f}".format(x) for x in points[i]])
        s += "\n"
    
    return s