#!/usr/bin/env python3

import src.file_io as io

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
        "difficulty"  : 0
    }

    info["map_format"] = io.read_int(4)
    
    if info["map_format"] == 32: # HotA
        info["hota_version"] = io.read_int(1)
        
        if info["hota_version"] == 1:
            info["hota_data"] = io.read_raw(5)
        elif info["hota_version"] == 3:
            info["hota_data"] = io.read_raw(9)
        else:
            print("Unhandled HotA version!")
            return info
            
    info["has_hero"]     = bool(io.read_int(1))
    info["map_size"]     =      io.read_int(4)
    info["is_two_level"] = bool(io.read_int(1))
    info["name"]         =      io.read_str(io.read_int(4))
    info["description"]  =      io.read_str(io.read_int(4))
    info["difficulty"]   =      io.read_int(1)

    return info
    
def write_general(info: dict) -> None:
    io.write_int(info["map_format"], 4)
    
    if info["map_format"] == 32: # HotA
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
