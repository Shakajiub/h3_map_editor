#!/usr/bin/env python3

import src.file_io    as io
import data.objects   as od # Object details
import data.creatures as cd # Creature details
import data.artifacts as ad # Artifact details

def parse_objects() -> list:
    info = []

    for _ in range(io.read_int(4)): # Amount of objects
        obj = {}
        obj["sprite"] = io.read_str(io.read_int(4))
        obj["red_squares"]       =  io.read_bits(6)
        obj["yellow_squares"]    =  io.read_bits(6)
        obj["placeable_terrain"] =  io.read_bits(2)
        obj["editor_section"]    =  io.read_bits(2)
        obj["type"] =         od.ID(io.read_int(4))
        obj["subtype"]           =  io.read_int(4)

        # TODO: A full function for getting subtype IntEnum
        if obj["type"] == od.ID.Resource:
            obj["subtype"] = od.Resource(obj["subtype"])
        elif obj["type"] == od.ID.Artifact:
            obj["subtype"] = ad.ID(obj["subtype"])

        obj["editor_group"] =      io.read_int(1)
        obj["below_ground"] = bool(io.read_int(1))
        obj["null_bytes"]   =      io.read_raw(16)
        info.append(obj)

    return info

def write_objects(info: list) -> None:
    io.write_int(len(info), 4)

    for obj in info:
        io.write_int(len(obj["sprite"]), 4)
        io.write_str(    obj["sprite"])
        io.write_bits(   obj["red_squares"])
        io.write_bits(   obj["yellow_squares"])
        io.write_bits(   obj["placeable_terrain"])
        io.write_bits(   obj["editor_section"])
        io.write_int(    obj["type"], 4)
        io.write_int(    obj["subtype"], 4)
        io.write_int(    obj["editor_group"], 1)
        io.write_int(    obj["below_ground"], 1)
        io.write_raw(    obj["null_bytes"])

def parse_object_data(objects: list) -> list:
    info = []

    for _ in range(io.read_int(4)): # Amount of objects
#        io.peek(80)

        obj = { "coords": [0, 0, 0] }
        obj["coords"][0] = io.read_int(1)
        obj["coords"][1] = io.read_int(1)
        obj["coords"][2] = io.read_int(1)

        temp_id = io.read_int(4)
        obj["id"] = temp_id
        io.seek(5)

        obj_type = objects[temp_id]["type"]

        match obj_type:
            case od.ID.Artifact:     obj = parse_artifact(obj)
            case od.ID.Pandoras_Box: obj = parse_pandoras_box(obj)
            case od.ID.Event:        obj = parse_event(obj)
            case od.ID.Resource:     obj = parse_resource(obj)

            case (od.ID.Creature_Generator_1 |
                  od.ID.Creature_Generator_4):
                obj = parse_owner(obj)

            case _ if obj_type in od.CREATURE_BANKS:
                obj = parse_bank(obj)

            case (od.ID.Altar_of_Sacrifice | od.ID.Arena |
                  od.ID.Black_Market       | od.ID.Boat  |
                  od.ID.Border_Guard       | od.ID.Keymasters_Tent |
                  od.ID.Buoy               | od.ID.Campfire  |
                  od.ID.Cartographer       | od.ID.Swan_Pond |
                  od.ID.Cover_of_Darkness  | od.ID.Cursed_Ground_RoE |
                  od.ID.Cursed_Ground      | od.ID.Magic_Plains_RoE  |
                  od.ID.Magic_Plains       | od.ID.Clover_Field |
                  od.ID.Evil_Fog           | od.ID.Fiery_Fields |
                  od.ID.Holy_Ground        | od.ID.Lucid_Pools  |
                  od.ID.Magic_Clouds       | od.ID.Rocklands |
                  od.ID.HotA_Ground        | od.ID.Corpse    |
                  od.ID.Marletto_Tower):
                pass
            case _:
                raise NotImplementedError(objects[temp_id]["type"], obj["coords"])

        info.append(obj)

    return info

def write_object_data(objects: list, info: list) -> None:
    io.write_int(len(info), 4)

    for obj in info:
        io.write_int(obj["coords"][0], 1)
        io.write_int(obj["coords"][1], 1)
        io.write_int(obj["coords"][2], 1)

        temp_id = obj["id"]
        io.write_int(temp_id, 4)
        io.write_int(0, 5)

        obj_type = objects[temp_id]["type"]

        match obj_type:
            case od.ID.Artifact:     write_artifact(obj)
            case od.ID.Pandoras_Box: write_pandoras_box(obj)
            case od.ID.Event:        write_event(obj)
            case od.ID.Resource:     write_resource(obj)

            case (od.ID.Creature_Generator_1 |
                  od.ID.Creature_Generator_4):
                write_owner(obj)

            case _ if obj_type in od.CREATURE_BANKS:
                write_bank(obj)

def parse_owner(obj: dict) -> dict:
    obj["owner"] = io.read_int(4)
    return obj

def write_owner(obj: dict) -> None:
    io.write_int(obj["owner"], 4)

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

def parse_common(obj: dict) -> dict:
    message_length = io.read_int(4)

    if message_length > 0:
        obj["message"] = io.read_str(message_length)
    if io.read_int(1):
        obj["guards"] = parse_guards()

    io.seek(4)
    return obj

def write_common(obj: dict) -> None:
    io.write_int(1, 1)

    if "message" in obj:
        io.write_int(len(obj["message"]), 4)
        io.write_str(    obj["message"])
    else: io.write_int(0, 4)

    if "guards" in obj:
        io.write_int(1, 1)
        write_guards(obj["guards"])
    else: io.write_int(0, 1)

    io.write_int(0, 4)

def parse_contents(obj: dict) -> dict:
    obj["contents"] = {
        "Experience"      : 0,
        "Spell_Points"    : 0,
        "Morale"          : 0,
        "Luck"            : 0,
        "Resources"       : [],
        "Primary_Skills"  : [],
        "Secondary_Skills": [],
        "Artifacts"       : [],
        "Spells"          : [],
        "Creatures"       : []
    }

    obj["contents"]["Experience"]   = io.read_int(4)
    obj["contents"]["Spell_Points"] = io.read_int(4)
    obj["contents"]["Morale"]       = io.read_int(1)
    obj["contents"]["Luck"]         = io.read_int(1)

    for _ in range(7):
        obj["contents"]["Resources"].append(io.read_int(4))

    for _ in range(4):
        obj["contents"]["Primary_Skills"].append(io.read_int(1))

    for _ in range(io.read_int(1)):
        skill = {}
        skill["id"] = io.read_int(1)
        skill["level"] = io.read_int(1)
        obj["contents"]["Secondary_Skills"].append(skill)

    for _ in range(io.read_int(1)):
        obj["contents"]["Artifacts"].append(io.read_int(2))

    for _ in range(io.read_int(1)):
        obj["contents"]["Spells"].append(io.read_int(1))

    for _ in range(io.read_int(1)):
        creature = {}
        creature["id"] = cd.ID(io.read_int(2))
        creature["amount"]   = io.read_int(2)
        obj["contents"]["Creatures"].append(creature)

    io.seek(8)
    return obj

def write_contents(contents: dict) -> None:
    io.write_int(contents["Experience"], 4)
    io.write_int(contents["Spell_Points"], 4)
    io.write_int(contents["Morale"], 1)
    io.write_int(contents["Luck"], 1)

    for value in contents["Resources"]:
        io.write_int(value, 4)

    for value in contents["Primary_Skills"]:
        io.write_int(value, 1)

    io.write_int(len(contents["Secondary_Skills"]), 1)
    for skill in contents["Secondary_Skills"]:
        io.write_int(skill["id"], 1)
        io.write_int(skill["level"], 1)

    io.write_int(len(contents["Artifacts"]), 1)
    for value in contents["Artifacts"]:
        io.write_int(value, 2)

    io.write_int(len(contents["Spells"]), 1)
    for value in contents["Spells"]:
        io.write_int(value, 1)

    io.write_int(len(contents["Creatures"]), 1)
    for creature in contents["Creatures"]:
        io.write_int(creature["id"], 2)
        io.write_int(creature["amount"], 2)

    io.write_int(0, 8)

def parse_artifact(obj: dict) -> dict:
    if io.read_int(1):
        return parse_common(obj)
    return obj

def write_artifact(obj: dict) -> None:
    if len(obj) > 2:
        write_common(obj)
    else: io.write_int(0, 1)

def parse_pandoras_box(obj: dict) -> dict:
    if io.read_int(1):
        obj = parse_common(obj)
    obj = parse_contents(obj)
    return obj

def write_pandoras_box(obj: dict) -> None:
    if len(obj) > 3:
        write_common(obj)
    else: io.write_int(0, 1)
    write_contents(obj["contents"])

def parse_event(obj: dict) -> dict:
    if io.read_int(1):
        obj = parse_common(obj)
    obj = parse_contents(obj)

    obj["allowed_players"] =      io.read_bits(1)
    obj["allow_ai"]        = bool(io.read_int(1))
    obj["cancel_event"]    = bool(io.read_int(1))
    io.seek(4)
    obj["allow_human"]     = bool(io.read_int(1))

    return obj

def write_event(obj: dict) -> None:
    if len(obj) > 7:
        write_common(obj)
    else: io.write_int(0, 1)

    write_contents(obj["contents"])

    io.write_bits(obj["allowed_players"])
    io.write_int( obj["allow_ai"], 1)
    io.write_int( obj["cancel_event"], 5)
    io.write_int( obj["allow_human"], 1)

def parse_bank(obj: dict) -> dict:
    obj["difficulty"]     = io.read_int(4)
    obj["upgraded_stack"] = io.read_int(1)
    obj["rewards"]        = []

    for _ in range(io.read_int(4)):
        obj["rewards"].append(ad.ID(io.read_int(4)))

    return obj

def write_bank(obj: dict) -> None:
    io.write_int(obj["difficulty"], 4)
    io.write_int(obj["upgraded_stack"], 1)

    io.write_int(len(obj["rewards"]), 4)
    for reward in obj["rewards"]:
        io.write_int(reward, 4)

def parse_resource(obj: dict) -> dict:
    if io.read_int(1):
        obj = parse_common(obj)

    obj["amount"] = io.read_int(4)
    io.seek(4)
    return obj

def write_resource(obj: dict) -> None:
    if len(obj) > 3:
        write_common(obj)
    else: io.write_int(0, 1)

    io.write_int(obj["amount"], 4)
    io.write_int(0, 4)
