#!/usr/bin/env python3

from enum import IntEnum

class Primary(IntEnum):
    Attack      = 0
    Defense     = 1
    Spell_Power = 2
    Knowledge   = 3

class Secondary(IntEnum):
#
# Byte 1 ... (0-7)
#
    Pathfinding  =  0
    Archery      =  1
    Logistics    =  2
    Scouting     =  3
    Diplomacy    =  4
    Navigation   =  5
    Leadership   =  6
    Wisdom       =  7
#
# Byte 2 ... (8-15)
#
    Mysticism    =  8
    Luck         =  9
    Ballistics   = 10
    Eagle_Eye    = 11
    Necromancy   = 12
    Estates      = 13
    Fire_Magic   = 14
    Air_Magic    = 15
#
# Byte 3 ... (16-23)
#
    Water_Magic  = 16
    Earth_Magic  = 17
    Scholar      = 18
    Tactics      = 19
    Artillery    = 20
    Learning     = 21
    Offense      = 22
    Armorer      = 23
#
# Byte 4 ... (24-31)
#
    Intelligence = 24
    Sorcery      = 25
    Resistance   = 26
    First_Aid    = 27
    Interference = 28
    #
    #
    #
