#!/usr/bin/env python3

import src.file_io as io
import data.heroes as heroes

def parse_heroes(version):
    info = {
        "hota_data" : b'',
        "hero_flags": '0'*184
    }

    info["hota_data"] = io.read_raw(4)
    
    data = io.read_raw(23)
    s = ""
    for c in data:
        s += format(int(c), '#010b').removeprefix('0b')[::-1]
    
    info["hero_flags"] = s
    
#    io.seek(4) # Skip 4 empty bytes

    return info

def write_heroes(info):
    pass
