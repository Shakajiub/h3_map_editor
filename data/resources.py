#!/usr/bin/env python3

from enum import IntEnum

class ID(IntEnum):
    Invalid = 255
#
# Byte 1 ... (0-7)
#
    Wood    = 0
    Mercury = 1
    Ore     = 2
    Sulfur  = 3
    Crystal = 4
    Gems    = 5
    Gold    = 6
    #
