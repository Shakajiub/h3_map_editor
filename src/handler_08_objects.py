#!/usr/bin/env python3

import src.file_io as io

def parse_objects() -> list:
    info = []

    for _ in range(io.read_int(4)):
        obj = {}
        obj["sprite"]            = io.read_str(io.read_int(4))
        obj["red_squares"]       = io.read_bits(6)
        obj["yellow_squares"]    = io.read_bits(6)
        obj["placeable_terrain"] = io.read_bits(2)
        obj["editor_section"]    = io.read_bits(2)
        obj["id"]                = io.read_int(4)
        obj["sub_id"]            = io.read_int(4)
        obj["editor_group"]      = io.read_int(1)
        obj["below_ground"] = bool(io.read_int(1))
        obj["null_bytes"]        = io.read_raw(16)
        info.append(obj)

    return info

def parse_object_details() -> dict:
    info = {}

#    io.peek(64)

#    for _ in range(io.read_int(4)):
#        pass

    return info

def write_objects(info: list) -> None:
    io.write_int(len(info), 4)

    for obj in info:
        io.write_int(len(obj["sprite"]), 4)
        io.write_str(obj["sprite"])
        io.write_bits(obj["red_squares"])
        io.write_bits(obj["yellow_squares"])
        io.write_bits(obj["placeable_terrain"])
        io.write_bits(obj["editor_section"])
        io.write_int(obj["id"], 4)
        io.write_int(obj["sub_id"], 4)
        io.write_int(obj["editor_group"], 1)
        io.write_int(obj["below_ground"], 1)
        io.write_raw(obj["null_bytes"])

def write_object_details(info: dict) -> None:
    pass
