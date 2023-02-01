#!/usr/bin/env python3

import src.file_io as io

def parse_heroes(version: int) -> dict:
    info = {
        "hota_data" : b'',
        "hero_flags": b''
    }

    temp_flags = ""
    raw_data   = b''

    if version == 32: # HotA
        info["hota_data"] = io.read_raw(4)
        raw_data = io.read_raw(23)
    elif version == 28: # SoD
        raw_data = io.read_raw(20)

    for c in raw_data:
        temp_flags += format(int(c), '#010b').removeprefix('0b')[::-1]

    info["hero_flags"] = temp_flags.encode()

#    io.seek(4) # Skip 4 always-empty bytes

    # TODO: Parse custom heroes.

    return info

def write_heroes(info: dict) -> None:
    if info["hota_data"] != b'':
        io.write_raw(info["hota_data"])
        
    temp_flags = str(info["hero_flags"])[2:-1]
    for i in range(0, len(temp_flags), 8):
        io.write_int(int(temp_flags[i:i+8][::-1], 2), 1)

#    io.write_int(0, 4) # Write 4 always-empty bytes
