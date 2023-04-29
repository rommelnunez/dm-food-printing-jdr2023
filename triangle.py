#
# @Title: triangle.py
# @Description: g-code generator for food printer that prints a triangle
# @Author: Philippe Wyder (PMW2125)
#

import math
import matplotlib.pyplot as plt
import numpy as np

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
    

    # Parameters
    
    A = 25  # factor by which to reduce the radius of each triangle
    z = 0 #tweaks how far the previous triangle is from the next (z-movement)
    for layer in range(0, 5, 1):
        
        lines.append(f"G1 E0.25" + eol) # Extrude a small amount (prime nozzle)
        for theta in np.linspace(0, 10*math.pi, 200):
            r = A * math.cos(-0.4 * theta)
            x = r * math.cos(theta)
            y =r * math.sin(theta)
            lines.append(f"G1 X{x}                Y{y}  Z{z} E{EXTRUSION} F{FEEDRATE}" + eol)
            
        if layer % 2 == 0:
        # Select tool number 2 and apply an offset of 18mm to the left
            lines.append(f"G1 Z{z} E-.25 F200" + eol) # move up & retract plunger a bit
            lines.append("T1 M6" + eol)
            
            lines.append(f"G1 X-18 E0 F200" + eol)
            
        else:
            lines.append(f"G1 Z{z} E-.25 F200" + eol) # move up & retract plunger a bit
            lines.append("T0 M6" + eol)
            lines.append(f"G1 X18 E0 F200" + eol)
        
        z = layer
        

    lines.append("G1 Z{z} E-2 F200" + eol) # move up & retract plunger a bit
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