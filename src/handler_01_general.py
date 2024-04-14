#!/usr/bin/env python3

import src.file_io as io

from enum import IntEnum

# The general information of a map is stored as follows:
#
# - Map format           | 4 bytes int
# - HotA version         | 4 bytes int
# - unknown data         | 1 byte ???
# - is_arena             | 1 byte bool
# - unknown data         | 8 bytes ???
# - allowed difficulties | 1 byte (bits)
# - has_hero             | 1 byte bool
# - map_size             | 4 bytes int
# - is_two_level         | 1 byte bool
# - name length          | 4 bytes int
# - name                 | X bytes str
# - description length   | 4 bytes int
# - description          | X bytes str
# - difficulty           | 1 byte int
# - level_cap            | 1 byte int

class MapFormat(IntEnum):
    RoE  = 14
    AB   = 21
    SoD  = 28
    CHR  = 29
    HotA = 32
    WoG  = 51

class MapSize(IntEnum):
    S  =  36
    M  =  72
    L  = 108
    XL = 144
    H  = 180
    XH = 216
    G  = 252

class Difficulty(IntEnum):
    Easy       = 0
    Normal     = 1
    Hard       = 2
    Expert     = 3
    Impossible = 4

def parse_general() -> dict:
    info = {
        "map_format"         : 0,
        "hota_version"       : 0,
        "hota_data_1"        : b'',
        "hota_data_2"        : b'',
        "name"               : "",
        "description"        : "",
        "map_size"           : 0,
        "has_hero"           : False,
        "is_two_level"       : False,
#        "allow_plague"       : True,
        "is_arena"           : False,
        "difficulty"         : 0,
        "allowed_difficulty" : [],
        "level_cap"          : 0,
    }

    info["map_format"] = MapFormat(io.read_int(4))

    if info["map_format"] == MapFormat.HotA:
        info["hota_version"] = io.read_int(4)

        if info["hota_version"] == 6:
            info["hota_data_1"]        =      io.read_raw(1)
            info["is_arena"]           = bool(io.read_int(1))
            info["hota_data_2"]        =      io.read_raw(8)
            info["allowed_difficulty"] =      io.read_bits(1)

        else: raise NotImplementedError(f"unsupported hota version: {info['hota_version']}")
    else: raise NotImplementedError(f"unsupported map format: {info['map_format']}")

    info["has_hero"]     =       bool(io.read_int(1))
    info["map_size"]     =    MapSize(io.read_int(4))
    info["is_two_level"] =       bool(io.read_int(1))
    info["name"]         =            io.read_str(io.read_int(4))
    info["description"]  =            io.read_str(io.read_int(4))
    info["difficulty"]   = Difficulty(io.read_int(1))
    info["level_cap"]    =            io.read_int(1)

    return info

def write_general(info: dict) -> None:
    io.write_int(info["map_format"], 4)

    if info["map_format"] == MapFormat.HotA:
        io.write_int( info["hota_version"], 4)
        io.write_raw( info["hota_data_1"])
        io.write_int( info["is_arena"], 1)
        io.write_raw( info["hota_data_2"])
        io.write_bits(info["allowed_difficulty"])

    io.write_int(    info["has_hero"], 1)
    io.write_int(    info["map_size"], 4)
    io.write_int(    info["is_two_level"], 1)
    io.write_int(len(info["name"]), 4)
    io.write_str(    info["name"])
    io.write_int(len(info["description"]), 4)
    io.write_str(    info["description"])
    io.write_int(    info["difficulty"], 1)
    io.write_int(    info["level_cap"], 1)
