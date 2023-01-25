#!/usr/bin/env python3

import src.map_io as io

def parse_map_info():
    map_info = {
        "format"  : 0,     "hota_version": 0,     "hota_data" : b'',
        "name"    : "",    "description" : "",    "size"      : 0,
        "has_hero": False, "two_level"   : False, "difficulty": 0
    }
    map_info["format"] = io.read_int(4)
    
    if map_info["format"] == 32:
        map_info["hota_version"] = io.read_int(1)
        
        if map_info["hota_version"] == 1:
            map_info["hota_data"] = io.read_raw(5)
        elif map_info["hota_version"] == 3:
            map_info["hota_data"] = io.read_raw(9)
        else:
            print("Unhandled HotA version!")
            return map_info
            
    map_info["has_hero"]    = io.read_int(1)
    map_info["size"]        = io.read_int(4)
    map_info["two_level"]   = io.read_int(1)
    map_info["name"]        = io.read_str(io.read_int(4))
    map_info["description"] = io.read_str(io.read_int(4))
    map_info["difficulty"]  = io.read_int(1)

    return map_info
    
def write_map_info(info):
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
