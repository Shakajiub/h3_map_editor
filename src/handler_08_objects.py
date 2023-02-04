#!/usr/bin/env python3

import src.file_io    as io
import data.objects   as od # Object details
import data.creatures as cd # Creature details

def parse_objects() -> list:
    info = []

    for _ in range(io.read_int(4)): # Amount of objects
        obj = {}
        obj["sprite"]            = io.read_str(io.read_int(4))
        obj["red_squares"]       = io.read_bits(6)
        obj["yellow_squares"]    = io.read_bits(6)
        obj["placeable_terrain"] = io.read_bits(2)
        obj["editor_section"]    = io.read_bits(2)
        obj["type"]              = od.ID(io.read_int(4))
        obj["subtype"]           = io.read_int(4)

        # TODO: A full function for getting subtype IntEnum
        if obj["type"] == od.ID.Resource:
            obj["subtype"] = od.Resource(obj["subtype"])

        obj["editor_group"]      = io.read_int(1)
        obj["below_ground"] = bool(io.read_int(1))
        obj["null_bytes"]        = io.read_raw(16)
        info.append(obj)

    return info

def write_objects(info: list) -> None:
    io.write_int(len(info), 4)

    for obj in info:
        io.write_int(len(obj["sprite"]), 4)

        io.write_str( obj["sprite"])
        io.write_bits(obj["red_squares"])
        io.write_bits(obj["yellow_squares"])
        io.write_bits(obj["placeable_terrain"])
        io.write_bits(obj["editor_section"])
        io.write_int( obj["type"], 4)
        io.write_int( obj["subtype"], 4)
        io.write_int( obj["editor_group"], 1)
        io.write_int( obj["below_ground"], 1)
        io.write_raw( obj["null_bytes"])

def parse_object_details(objects: list) -> list:
    info = []

    for _ in range(io.read_int(4)): # Amount of objects
        io.peek(64)

        obj = { "coords": [0, 0, 0] }
        obj["coords"][0] = io.read_int(1)
        obj["coords"][1] = io.read_int(1)
        obj["coords"][2] = io.read_int(1)

        temp_id = io.read_int(4)
        obj["id"] = temp_id

        match objects[temp_id]["type"]:
            case od.ID.Resource:
                obj = parse_resource(obj)
            case _:
                raise IndexError(objects[temp_id]["type"], obj["coords"])

        info.append(obj)

    return info

def write_object_details(objects: list, info: list) -> None:
    io.write_int(len(info), 4)

    for obj in info:
        io.write_int(obj["coords"][0], 1)
        io.write_int(obj["coords"][1], 1)
        io.write_int(obj["coords"][2], 1)

        temp_id = obj["id"]
        io.write_int(temp_id, 4)

        match objects[temp_id]["type"]:
            case od.ID.Resource:
                write_resource(obj)

def parse_guards() -> list:
    info = []
    for _ in range(7):
        guard = {}
        guard["id"] = cd.ID(io.read_int(2))
        guard["amount"]   = io.read_int(2)
        info.append(guard)
    return info

def write_guards(info: list) -> None:
    for guard in info:
        io.write_int(guard["id"], 2)
        io.write_int(guard["amount"], 2)

def parse_resource(obj: dict) -> dict:
    io.seek(5)

    # Is the resource pile customized?
    if not io.read_int(1):
        io.seek(8)
        return obj

    message_length = io.read_int(4)
    if message_length > 0:
        obj["message"] = io.read_str(message_length)

    # Is the resource pile guarded?
    if io.read_int(1):
        obj["guards"] = parse_guards()

    io.seek(4)
    obj["amount"] = io.read_int(4)
    io.seek(4)
    return obj

def write_resource(obj: dict) -> None:
    io.write_int(0, 5)

    # Non-customized resources have only 2 keys
    if len(obj) == 2:
        io.write_int(0, 9)
        return
    else: io.write_int(1, 1)

    if "message" in obj:
        io.write_int(len(obj["message"]), 4)
        io.write_str(    obj["message"])
    else: io.write_int(0, 4)

    if "guards" in obj:
        io.write_int(1, 1)
        write_guards(obj["guards"])
    else: io.write_int(0, 1)

    io.write_int(0, 4)
    io.write_int(obj["amount"], 4)
    io.write_int(0, 4)
