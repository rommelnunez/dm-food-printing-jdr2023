#
# @Title: triangle.py
# @Description: g-code generator for food printer that prints a triangle
# @Author: Philippe Wyder (PMW2125)
#

import math

FEEDRATE = 200
EXTRUSION = 0.5
import argparse
def main(side_length):
    lines = []
    eol = "\n"
    lines.append("T0" + eol)  # Select extruder 0
    lines.append("G21"+ eol) # Set units to mm
    lines.append("G92 X0 Y0 Z0 E0") # Set current position to be the origin
    lines.append("G90"+ eol) # Send absolute position commands
    # Controlled Movement to X,Y,Z position while Extruding 1-unit at Feedrate (speed) 50[cm/min]
    # NOTE: Z-VALUE can be omited and insteda set Z-height for single layer on printer
    lines.append(f"G1 E0.25" + eol) # Extrude a small amount (prime nozzle)

    #TEMPLATE FOR DRAWING TRIANGLE
    # lines.append(f"G1 X0                Y{side_length}  Z0 E{EXTRUSION} F{FEEDRATE}" + eol)
    # lines.append(f"G1 X{side_length}    Y{side_length}  Z0 E{EXTRUSION} F{FEEDRATE}" + eol)
    # lines.append(f"G1 X0                Y0              Z0 E{EXTRUSION} F{FEEDRATE}" + eol)
    # lines.append(f"G1 Z1.0" + eol)

    #PRINTING SECTION: this part of the code calculatest the distance from the center of triangles
    #   to the next vertex. It uses a cos/sin function to turn the next coordinate.

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

        lines.append(f"G1 X{x1}                Y{y1}  Z{z} E{EXTRUSION} F{FEEDRATE}" + eol)
        lines.append(f"G1 X{x2}                Y{y2}  Z{z} E{EXTRUSION} F{FEEDRATE}" + eol)
        lines.append(f"G1 X{x3}                Y{y3}  Z{z} E{EXTRUSION} F{FEEDRATE}" + eol)
        
        # Update parameters for the next triangle
        radius *= scale_factor
        theta += delta
        z+=3

    lines.append(f"G1 Z1.0" + eol)
    lines.append("G1 Z5 E-2 F200" + eol) # move up & retract plunger a bit
    lines.append("G1 X25 F400 " + eol) # move away from the print
    lines.append("G28") # Home printer
    # write lines to file
    with open('triangle.gcode', 'w') as f:
        f.writelines(lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create G-Code for triangle')
    parser.add_argument('side_length', metavar='l', nargs='?', type=int, default = 25,
                        help='Pass an integer for side length in mm')

    args = parser.parse_args()
    main(args.side_length)