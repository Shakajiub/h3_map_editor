#!/usr/bin/env python3

import src.file_io as io

from src.handler_01_general import MapFormat

def parse_heroes(version: int) -> dict:
    info = {
        "hota_data"      : b'',
        "hero_flags"     : [],
        "custom_heroes"  : [],
        "unhandled_bytes": b''
    }

    if version == MapFormat.HotA:
        info["hota_data"]  = io.read_raw(4)
        info["hero_flags"] = io.read_bits(23)

    elif version == MapFormat.SoD:
        info["hero_flags"] = io.read_bits(20)

    io.seek(4) # Skip 4 always-empty bytes

    for i in range(io.read_int(1)):
        hero = {}
        hero["id"]   = io.read_int(1)
        hero["face"] = io.read_int(1)
        hero["name"] = io.read_str(io.read_int(4))
        hero["may_be_hired_by"]  = io.read_int(1)
        info["custom_heroes"].append(hero)

    info["unhandled_bytes"] = io.read_raw(49)

    return info

def write_heroes(info: dict) -> None:
    if info["hota_data"] != b'':
        io.write_raw(info["hota_data"])

    io.write_bits(info["hero_flags"])
    io.write_int(0, 4) # Write 4 always-empty bytes
    io.write_int(len(info["custom_heroes"]), 1)

    for h in info["custom_heroes"]:
        io.write_int(    h["id"], 1)
        io.write_int(    h["face"], 1)
        io.write_int(len(h["name"]), 4)
        io.write_str(    h["name"])
        io.write_int(    h["may_be_hired_by"], 1)

    io.write_raw(info["unhandled_bytes"])
