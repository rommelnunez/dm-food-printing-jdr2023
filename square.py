#
# David Cendejas, Josette Content, Rommel Nunez
#

FEEDRATE = 200
EXTRUSION = 1
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
    lines.append(f"G1 E1" + eol) # Extrude a small amount (prime nozzle)
    lines.append(f"G1 X0                Y{side_length}  Z0 E{EXTRUSION} F{FEEDRATE}" + eol)
    lines.append(f"G1 X{side_length}    Y{side_length}  Z0 E{EXTRUSION} F{FEEDRATE}" + eol)
    lines.append(f"G1 X{side_length}                Y0  Z0 E{EXTRUSION} F{FEEDRATE}" + eol)
    lines.append(f"G1 X0                Y0              Z0 E{EXTRUSION} F{FEEDRATE}" + eol)
    lines.append("G1 Z5 E-2 F200" + eol) # move up & retract plunger a bit
    lines.append("G1 X25 F400 " + eol) # move away from the print
    lines.append("G28") # Home printer
    # write lines to file
    with open('square.gcode', 'w') as f:
        f.writelines(lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create G-Code for square')
    parser.add_argument('side_length', metavar='l', nargs='?', type=int, default = 25,
                        help='Pass an integer for side length in mm')

    args = parser.parse_args()
    main(args.side_length)