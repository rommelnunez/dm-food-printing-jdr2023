import math
import argparse
FEEDRATE = 200
EXTRUSION = 0.5

def layer(lines, extruder, offset, x, y, z):
    eol = "\n"
    lines.append(f"T{extruder}" + eol)  # Select extruder 0
    lines.append(f"G1 X{offset}" + eol)

    lines.append(f"G1 E2" + eol)
    lines.append(f"G1 X{x[0]}                Y{y[0]}  Z{z} E{EXTRUSION} F{FEEDRATE}" + eol)
    lines.append(f"G1 X{x[1]}                Y{y[1]}  Z{z} E{EXTRUSION} F{FEEDRATE}" + eol)
    lines.append(f"G1 X{x[2]}                Y{y[2]}  Z{z} E{EXTRUSION} F{FEEDRATE}" + eol)
    lines.append(f"G1 E-2" + eol)
    lines.append("G4 P500" + eol)

def main():
    lines = []
    eol = "\n"
    lines.append("G21"+ eol) # Set units to mm
    lines.append("G92 X0 Y0 Z0 E0") # Set current position to be the origin
    lines.append("G90"+ eol) # Send absolute position commands

    # Parameters
    center_x = 0   # x-coordinate of the center of the triangles
    center_y = 0   # y-coordinate of the center of the triangles
    radius = 16   # distance from the center of the triangle to its corners
    delta = math.pi/15  # angle by which to offset the next triangle (12 degrees)
    scale_factor = 0.9  # factor by which to reduce the radius of each triangle
    theta = 0
    z = 0 #tweaks how far the previous triangle is from the next (z-movement)

    for i in range(10):  # draw 10 triangles
        # Calculate coordinates of the triangle vertices
        x1 = center_x + radius * math.cos(theta)
        y1 = center_y + radius * math.sin(theta)
        x2 = center_x + radius * math.cos(theta + 2*math.pi/3)
        y2 = center_y + radius * math.sin(theta + 2*math.pi/3)
        x3 = center_x + radius * math.cos(theta + 4*math.pi/3)
        y3 = center_y + radius * math.sin(theta + 4*math.pi/3)

        print(f"x1 = {x1}, y1 = {y1}")
        print(f"x2 = {x2}, y1 = {y2}")
        print(f"x3 = {x3}, y1 = {y3}")
        print('\n\n')

        extruder = i%2
        if extruder == 0:
            offset = 22
        else:
            offset = -22
        if extruder == 1:
            layer(lines, i%2, offset, [x1,x2,x3], [y1,y2,y3], z)
        
        # Update parameters for the next triangle
        radius *= scale_factor
        theta += delta
        z+=2

    lines.append(f"G1 Z1.0" + eol)
    lines.append("G1 Z5 E-2 F200" + eol) # move up & retract plunger a bit
    lines.append("G1 X25 F400 " + eol) # move away from the print
    lines.append("G28") # Home printer
    # write lines to file
    with open('layers.gcode', 'w') as f:
        f.writelines(lines)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Create G-Code for triangle')
    # parser.add_argument('side_length', metavar='l', nargs='?', type=int, default = 25,
    #                     help='Pass an integer for side length in mm')

    # args = parser.parse_args()
    main()