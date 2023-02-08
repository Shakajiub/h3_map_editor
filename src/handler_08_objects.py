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
#        io.peek(128)

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
            case od.ID.Hero:         obj = parse_hero(obj)
            case od.ID.Resource:     obj = parse_resource(obj)

            case (od.ID.Creature_Generator_1 | od.ID.Creature_Generator_4):
                obj = parse_owner(obj)

            case (od.ID.Garrison | od.ID.Garrison_Vertical):
                obj = parse_garrison(obj)

            case _ if obj_type in od.CREATURE_BANKS:
                obj = parse_bank(obj)

            # Just a temporary list to make sure I've looked at all objects.
            # This will be the default case once everything has been parsed.
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
                  od.ID.Marletto_Tower     | od.ID.Eye_of_the_Magi |
                  od.ID.Faerie_Ring        | od.ID.Flotsam |
                  od.ID.Fountain_of_Fortune | od.ID.Fountain_of_Youth |
                  od.ID.Garden_of_Revelation):
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
            case od.ID.Hero:         write_hero(obj)
            case od.ID.Resource:     write_resource(obj)

            case (od.ID.Creature_Generator_1 |
                  od.ID.Creature_Generator_4):
                write_owner(obj["owner"])

            case (od.ID.Garrison | od.ID.Garrison_Vertical):
                write_garrison(obj)

            case _ if obj_type in od.CREATURE_BANKS:
                write_bank(obj)

def parse_owner() -> int:
    return io.read_int(4)

def write_owner(owner: int) -> None:
    io.write_int(owner, 4)

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

def parse_contents() -> dict:
    contents = {
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

    contents["Experience"]   = io.read_int(4)
    contents["Spell_Points"] = io.read_int(4)
    contents["Morale"]       = io.read_int(1)
    contents["Luck"]         = io.read_int(1)

    for _ in range(7):
        contents["Resources"].append(io.read_int(4))

    for _ in range(4):
        contents["Primary_Skills"].append(io.read_int(1))

    for _ in range(io.read_int(1)):
        skill = {}
        skill["id"] = io.read_int(1)
        skill["level"] = io.read_int(1)
        contents["Secondary_Skills"].append(skill)

    for _ in range(io.read_int(1)):
        contents["Artifacts"].append(io.read_int(2))

    for _ in range(io.read_int(1)):
        contents["Spells"].append(io.read_int(1))

    for _ in range(io.read_int(1)):
        creature = {}
        creature["id"] = cd.ID(io.read_int(2))
        creature["amount"]   = io.read_int(2)
        contents["Creatures"].append(creature)

    io.seek(8)
    return contents

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
    obj["contents"] = parse_contents()
    return obj

def write_pandoras_box(obj: dict) -> None:
    if len(obj) > 3:
        write_common(obj)
    else: io.write_int(0, 1)
    write_contents(obj["contents"])

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

def parse_event(obj: dict) -> dict:
    if io.read_int(1):
        obj = parse_common(obj)
    obj["contents"] = parse_contents()

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

def parse_garrison(obj: dict) -> dict:
    obj["owner"]  = parse_owner()
    obj["guards"] = parse_guards()
    obj["troops_removable"] = io.read_int(1)

    io.seek(8)
    return obj

def write_garrison(obj: dict) -> None:
    write_owner( obj["owner"])
    write_guards(obj["guards"])
    io.write_int(obj["troops_removable"], 9)

def parse_hero(obj: dict) -> dict:
    # This method is pretty similar to parse_hero_data() in the heroes handler,
    # but it has some additional bytes to read all over. Maybe combine them
    # into a single method some day.

    obj["start_bytes"] = io.read_raw(4)
    obj["owner"]       = io.read_int(1)

    hero = {
        "id"                : 255,
        "name"              : "",
        "experience"        : -1,
        "portrait"          : 255,
        "secondary_skills"  : [],
        "creatures"         : [],
        "formation"         : 0,
        "artifacts_equipped": {},
        "artifacts_backpack": [],
        "patrol"            : 255,
        "biography"         : "",
        "gender"            : 255,
        "spells"            : b'',
        "primary_skills"    : {}
    }

    hero["id"] = io.read_int(1)

    if io.read_int(1): # Is the name set?
        hero["name"] = io.read_str(io.read_int(4))

    if io.read_int(1): # Is experience set?
        hero["experience"] = io.read_int(4)

    if io.read_int(1): # Is portrait set?
        hero["portrait"] = io.read_int(1)

    if io.read_int(1): # Are secondary skills set?
        for _ in range(io.read_int(4)):
            skill = {}
            skill["id"]    = io.read_int(1)
            skill["level"] = io.read_int(1)
            hero["secondary_skills"].append(skill)

    if io.read_int(1): # Is the army set?
        hero["creatures"] = parse_guards()

    hero["formation"] = io.read_int(1)

    if io.read_int(1): # Are artifacts set?
        hero["artifacts_equipped"]["head"]          = io.read_int(2)
        hero["artifacts_equipped"]["shoulders"]     = io.read_int(2)
        hero["artifacts_equipped"]["neck"]          = io.read_int(2)
        hero["artifacts_equipped"]["right_hand"]    = io.read_int(2)
        hero["artifacts_equipped"]["left_hand"]     = io.read_int(2)
        hero["artifacts_equipped"]["torso"]         = io.read_int(2)
        hero["artifacts_equipped"]["right_ring"]    = io.read_int(2)
        hero["artifacts_equipped"]["left_ring"]     = io.read_int(2)
        hero["artifacts_equipped"]["feet"]          = io.read_int(2)
        hero["artifacts_equipped"]["misc_1"]        = io.read_int(2)
        hero["artifacts_equipped"]["misc_2"]        = io.read_int(2)
        hero["artifacts_equipped"]["misc_3"]        = io.read_int(2)
        hero["artifacts_equipped"]["misc_4"]        = io.read_int(2)
        hero["artifacts_equipped"]["war_machine_1"] = io.read_int(2)
        hero["artifacts_equipped"]["war_machine_2"] = io.read_int(2)
        hero["artifacts_equipped"]["war_machine_3"] = io.read_int(2)
        hero["artifacts_equipped"]["war_machine_4"] = io.read_int(2)
        hero["artifacts_equipped"]["spellbook"]     = io.read_int(2)
        hero["artifacts_equipped"]["misc_5"]        = io.read_int(2)
        
        for _ in range(io.read_int(2)):
            hero["artifacts_backpack"].append(io.read_int(2))

    hero["patrol"] = io.read_int(1)

    if io.read_int(1): # Is biography set?
        hero["biography"] = io.read_str(io.read_int(4))

    hero["gender"] = io.read_int(1)

    if io.read_int(1): # Are spells set?
        hero["spells"] = io.read_raw(9) # TODO: Parse spells.

    if io.read_int(1): # Are primary skills set?
        hero["primary_skills"]["attack"]      = io.read_int(1)
        hero["primary_skills"]["defense"]     = io.read_int(1)
        hero["primary_skills"]["spell_power"] = io.read_int(1)
        hero["primary_skills"]["knowledge"]   = io.read_int(1)

    obj["end_bytes"] = io.read_raw(16)
    obj["hero_data"] = hero
    return obj

def write_hero(obj: dict) -> None:
    io.write_raw(obj["start_bytes"])
    io.write_int(obj["owner"], 1)

    hero = obj["hero_data"]

    #
    io.write_int(hero["id"], 1)

    #
    if hero["name"]:
        io.write_int(1, 1)
        io.write_int(len(hero["name"]), 4)
        io.write_str(hero["name"])
    else: io.write_int(0, 1)

    #
    if hero["experience"] >= 0:
        io.write_int(1, 1)
        io.write_int(hero["experience"], 4)
    else: io.write_int(0, 1)

    #
    if hero["portrait"] != 255:
        io.write_int(1, 1)
        io.write_int(hero["portrait"], 1)
    else: io.write_int(0, 1)

    #
    if hero["secondary_skills"]:
        io.write_int(1, 1)
        io.write_int(len(hero["secondary_skills"]), 4)

        for skill in hero["secondary_skills"]:
            io.write_int(skill["id"], 1)
            io.write_int(skill["level"], 1)
    else: io.write_int(0, 1)

    #
    if hero["creatures"]:
        io.write_int(1, 1)
        write_guards(hero["creatures"])
    else: io.write_int(0, 1)

    #
    io.write_int(hero["formation"], 1)

    #
    if hero["artifacts_equipped"] or hero["artifacts_backpack"]:
        io.write_int(1, 1)

        io.write_int(hero["artifacts_equipped"]["head"], 2)
        io.write_int(hero["artifacts_equipped"]["shoulders"], 2)
        io.write_int(hero["artifacts_equipped"]["neck"], 2)
        io.write_int(hero["artifacts_equipped"]["right_hand"], 2)
        io.write_int(hero["artifacts_equipped"]["left_hand"], 2)
        io.write_int(hero["artifacts_equipped"]["torso"], 2)
        io.write_int(hero["artifacts_equipped"]["right_ring"], 2)
        io.write_int(hero["artifacts_equipped"]["left_ring"], 2)
        io.write_int(hero["artifacts_equipped"]["feet"], 2)
        io.write_int(hero["artifacts_equipped"]["misc_1"], 2)
        io.write_int(hero["artifacts_equipped"]["misc_2"], 2)
        io.write_int(hero["artifacts_equipped"]["misc_3"], 2)
        io.write_int(hero["artifacts_equipped"]["misc_4"], 2)
        io.write_int(hero["artifacts_equipped"]["war_machine_1"], 2)
        io.write_int(hero["artifacts_equipped"]["war_machine_2"], 2)
        io.write_int(hero["artifacts_equipped"]["war_machine_3"], 2)
        io.write_int(hero["artifacts_equipped"]["war_machine_4"], 2)
        io.write_int(hero["artifacts_equipped"]["spellbook"], 2)
        io.write_int(hero["artifacts_equipped"]["misc_5"], 2)
        
        io.write_int(len(hero["artifacts_backpack"]), 2)
        for art in hero["artifacts_backpack"]:
            io.write_int(art, 2)
    else: io.write_int(0, 1)

    #
    io.write_int(hero["patrol"], 1)

    #
    if hero["biography"]:
        io.write_int(1, 1)
        io.write_int(len(hero["biography"]), 4)
        io.write_str(hero["biography"])
    else: io.write_int(0, 1)

    #
    io.write_int(hero["gender"], 1)

    #
    if hero["spells"] != b'':
        io.write_int(1, 1)
        io.write_raw(hero["spells"])
    else: io.write_int(0, 1)

    #
    if hero["primary_skills"]:
        io.write_int(1, 1)
        io.write_int(hero["primary_skills"]["attack"], 1)
        io.write_int(hero["primary_skills"]["defense"], 1)
        io.write_int(hero["primary_skills"]["spell_power"], 1)
        io.write_int(hero["primary_skills"]["knowledge"], 1)
    else: io.write_int(0, 1)

    #
    io.write_raw(obj["end_bytes"])

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
