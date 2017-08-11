# Author: Chris Daw
# Date: August 10th, 2017

# Usage: python rgb888tobgr565.py hex_value
# Ex: python rrgb888tobgr565.py 0xFC8821

# This script converts rgb888 colorvalues to bgr565.
# Input as a hexadecimal rgb888 value in the format ###### or 0x######.
# rgb888 bytes are rr gg bb.
# bgr565 bits are bbbb bggg gggr rrrr.

import sys
import re
import ctypes

#--------------------------------#
#--- Convert rgb888 to rgb565 ---#
#--------------------------------#
color888 = sys.argv[1]

if not "0x" in color888[0:2]:
    color888 = "0x" + color888

isHexCode = re.compile("^0x[0-9A-Fa-f]{6}$")
if not isHexCode.match(color888):
    print("Usage: python htmlhexto565.py 0x######")
    sys.exit(1)

c_uint32 = ctypes.c_uint32
c_uint16 = ctypes.c_uint16
c_uint8 = ctypes.c_uint8

class RGB888(ctypes.LittleEndianStructure):
    _fields_ = [
            ("blue", c_uint8),
            ("green", c_uint8),
            ("red", c_uint8),
            ]

class UNION888(ctypes.Union):
    _fields_ = [
            ("rgb", RGB888),
            ("hex", c_uint32, 24),
            ]

# Form UNION888 object with the given rgb888 value
u888 = UNION888()
u888.hex = int(color888, 16)

# Initiate r, g, and b values for 888 to 565 conversion
r = u888.rgb.red
g = u888.rgb.green
b = u888.rgb.blue

int565 = ((r>>3)<<11) | ((g>>2)<<5) | (b>>3)

#--------------------------------#
#--- Convert rgb565 to bgr565 ---#
#--------------------------------#

class BGR565(ctypes.LittleEndianStructure):
    _fields_ = [
            ("red", c_uint16, 5),
            ("green", c_uint16, 6),
            ("blue", c_uint16, 5),
            ]

class RGB565(ctypes.LittleEndianStructure):
    _fields_ = [
            ("blue", c_uint16, 5),
            ("green", c_uint16, 6),
            ("red", c_uint16, 5),
            ]

class UNION(ctypes.Union):
    _fields_ = [
            ("rgb", RGB565),
            ("bgr", BGR565),
            ("int", c_uint16),
            ]

# Form Union with the given rgb565 integer value
u = UNION()
u.int = int565

# Form a BGR565 object and flip blue and red values
bgr = BGR565()
bgr.red = u.rgb.red
bgr.green = u.rgb.green
bgr.blue = u.rgb.blue

# Replace BGR565 object in the Union to change its "int"
u.bgr = bgr

print(" rgb888  --> rgb565 --> bgr565")
print("{} --> {} --> {}".format(
    color888.lower(), format(int565, '#06x'), format(u.int, '#06x')))
