#!/usr/bin/env python3

import src.file_io as io

from enum import IntEnum

class MapFormat(IntEnum):
    RoE  = 14
    AB   = 21
    SoD  = 28
    HotA = 32

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
        "map_format"  : 0,
        "hota_version": 0,
        "hota_data"   : b'',
        "name"        : "",
        "description" : "",
        "map_size"    : 0,
        "has_hero"    : False,
        "is_two_level": False,
        "difficulty"  : 0,
        "level_cap"   : 0
    }

    info["map_format"] = MapFormat(io.read_int(4))

    if info["map_format"] == MapFormat.HotA:
        info["hota_version"] = io.read_int(1)

        if info["hota_version"] == 1:
            info["hota_data"] = io.read_raw(5)
        elif info["hota_version"] == 3:
            info["hota_data"] = io.read_raw(9)
        else:
            print("Unhandled HotA version!")
            return info

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
        io.write_int(info["hota_version"], 1)
        io.write_raw(info["hota_data"])

    io.write_int(    info["has_hero"], 1)
    io.write_int(    info["map_size"], 4)
    io.write_int(    info["is_two_level"], 1)
    io.write_int(len(info["name"]), 4)
    io.write_str(    info["name"])
    io.write_int(len(info["description"]), 4)
    io.write_str(    info["description"])
    io.write_int(    info["difficulty"], 1)
    io.write_int(    info["level_cap"], 1)
