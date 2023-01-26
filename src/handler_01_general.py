#!/usr/bin/env python3

import src.map_io as io

def parse_general():
    info = {
        "format"  : 0,     "hota_version": 0,     "hota_data" : b'',
        "name"    : "",    "description" : "",    "size"      : 0,
        "has_hero": False, "two_level"   : False, "difficulty": 0
    }
    info["format"] = io.read_int(4)
    
    if info["format"] == 32:
        info["hota_version"] = io.read_int(1)
        
        if info["hota_version"] == 1:
            info["hota_data"] = io.read_raw(5)
        elif info["hota_version"] == 3:
            info["hota_data"] = io.read_raw(9)
        else:
            print("Unhandled HotA version!")
            return info
            
    info["has_hero"]    = bool(io.read_int(1))
    info["size"]        =      io.read_int(4)
    info["two_level"]   = bool(io.read_int(1))
    info["name"]        =      io.read_str(io.read_int(4))
    info["description"] =      io.read_str(io.read_int(4))
    info["difficulty"]  =      io.read_int(1)

    return info
    
def write_general(info):
    io.write_int(    info["format"], 4)
    
    if info["format"] == 32:
        io.write_int(info["hota_version"], 1)
        io.write_raw(info["hota_data"])

    io.write_int(    info["has_hero"], 1)
    io.write_int(    info["size"], 4)
    io.write_int(    info["two_level"], 1)
    io.write_int(len(info["name"]), 4)
    io.write_str(    info["name"])
    io.write_int(len(info["description"]), 4)
    io.write_str(    info["description"])
    io.write_int(    info["difficulty"], 1)
