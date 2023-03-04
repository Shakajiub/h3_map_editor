#!/usr/bin/env python3

import src.file_io    as io
import data.objects   as od  # Object details
import data.creatures as cd  # Creature details
import data.artifacts as ad  # Artifact details
import data.heroes    as hd  # Hero details
import data.skills    as skd # Skill details
import data.spells    as spd # Spell details

from src.handler_06_rumors_and_events import parse_events, write_events

from enum import IntEnum

def parse_object_defs() -> list:
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

def write_object_defs(info: list) -> None:
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

def parse_object_data(object_defs: list) -> list:
    info = []

    for _ in range(io.read_int(4)): # Amount of objects
        obj = { "coords": [0, 0, 0] }
        obj["coords"][0] = io.read_int(1)
        obj["coords"][1] = io.read_int(1)
        obj["coords"][2] = io.read_int(1)

        obj["id"] = io.read_int(4)
        io.seek(5)

        obj["type"]    = object_defs[obj["id"]]["type"]
        obj["subtype"] = object_defs[obj["id"]]["subtype"]

        match obj["type"]:
            case od.ID.Pandoras_Box: obj = parse_pandoras_box(obj)
            case od.ID.Event:        obj = parse_event(obj)
            case od.ID.Scholar:      obj = parse_scholar(obj)
            case od.ID.Seers_Hut:    obj = parse_seers_hut(obj)

            case od.ID.Random_Dwelling:         obj = parse_dwelling(obj)
            case od.ID.Random_Dwelling_Leveled: obj = parse_leveled(obj)
            case od.ID.Random_Dwelling_Faction: obj = parse_faction(obj)

            case od.ID.Quest_Guard: obj["quest"]  = parse_quest()
            case od.ID.Grail:       obj["radius"] = io.read_int(4)
            case od.ID.Witch_Hut:   obj["skills"] = io.read_bits(4)

            case od.ID.Border_Gate:
                if obj["subtype"] == 1000: # HotA Quest Gate
                    obj["quest"] = parse_quest()

            case (od.ID.Town | od.ID.Random_Town):
                obj = parse_town(obj)

            case (od.ID.Resource | od.ID.Random_Resource):
                obj = parse_resource(obj)

            case (od.ID.Hero | od.ID.Prison | od.ID.Random_Hero):
                obj = parse_hero(obj)

            case (od.ID.Monster          | od.ID.Random_Monster   |
                  od.ID.Random_Monster_1 | od.ID.Random_Monster_2 |
                  od.ID.Random_Monster_3 | od.ID.Random_Monster_4 |
                  od.ID.Random_Monster_5 | od.ID.Random_Monster_6 |
                  od.ID.Random_Monster_7):
                obj = parse_monster(obj)

            case (od.ID.Artifact                 | od.ID.Random_Artifact |
                  od.ID.Random_Treasure_Artifact | od.ID.Random_Minor_Artifact |
                  od.ID.Random_Major_Artifact    | od.ID.Random_Relic):
                obj = parse_artifact(obj)

            case (od.ID.Ocean_Bottle | od.ID.Sign):
                obj["message"] = io.read_str(io.read_int(4))
                io.seek(4)

            case (od.ID.Creature_Generator_1 | od.ID.Lighthouse |
                  od.ID.Creature_Generator_4 | od.ID.Mine       |
                  od.ID.Shipyard):
                obj["owner"] = parse_owner()

            case (od.ID.Garrison | od.ID.Garrison_Vertical):
                obj = parse_garrison(obj)

            case od.ID.Abandoned_Mine:
                obj["resources"] = io.read_bits(1)
                io.seek(3)

            # The level 4 HotA Shrine is just a subtype of the lvl 1 Shrine.
            case (od.ID.Shrine_of_Magic_Incantation |
                  od.ID.Shrine_of_Magic_Gesture     |
                  od.ID.Shrine_of_Magic_Thought):
                obj["spell"] = spd.ID(io.read_int(4))

            case od.ID.Spell_Scroll:
                obj = parse_spell_scroll(obj)

            case od.ID.Hero_Placeholder:
                obj = parse_hero_placeholder(obj)

            case (od.ID.Creature_Bank | od.ID.Derelict_Ship |
                  od.ID.Dragon_Utopia | od.ID.Crypt | od.ID.Shipwreck):
                obj = parse_bank(obj)

        info.append(obj)

    return info

def write_object_data(info: list) -> None:
    io.write_int(len(info), 4)

    for obj in info:
        io.write_int(obj["coords"][0], 1)
        io.write_int(obj["coords"][1], 1)
        io.write_int(obj["coords"][2], 1)
        io.write_int(obj["id"], 4)
        io.write_int(0, 5)

        match obj["type"]:
            case od.ID.Pandoras_Box: write_pandoras_box(obj)
            case od.ID.Event:        write_event(obj)
            case od.ID.Scholar:      write_scholar(obj)
            case od.ID.Seers_Hut:    write_seers_hut(obj)

            case od.ID.Random_Dwelling:         write_dwelling(obj)
            case od.ID.Random_Dwelling_Leveled: write_leveled(obj)
            case od.ID.Random_Dwelling_Faction: write_faction(obj)

            case od.ID.Quest_Guard: write_quest(obj["quest"])
            case od.ID.Grail:       io.write_int(obj["radius"], 4)
            case od.ID.Witch_Hut:   io.write_bits(obj["skills"])

            case od.ID.Border_Gate:
                if obj["subtype"] == 1000: # HotA Quest Gate
                    write_quest(obj["quest"])

            case (od.ID.Town | od.ID.Random_Town):
                write_town(obj)

            case (od.ID.Resource | od.ID.Random_Resource):
                write_resource(obj)

            case (od.ID.Hero | od.ID.Prison | od.ID.Random_Hero):
                write_hero(obj)

            case (od.ID.Monster          | od.ID.Random_Monster   |
                  od.ID.Random_Monster_1 | od.ID.Random_Monster_2 |
                  od.ID.Random_Monster_3 | od.ID.Random_Monster_4 |
                  od.ID.Random_Monster_5 | od.ID.Random_Monster_6 |
                  od.ID.Random_Monster_7):
                write_monster(obj)

            case (od.ID.Artifact                 | od.ID.Random_Artifact |
                  od.ID.Random_Treasure_Artifact | od.ID.Random_Minor_Artifact |
                  od.ID.Random_Major_Artifact    | od.ID.Random_Relic):
                write_artifact(obj)

            case (od.ID.Ocean_Bottle | od.ID.Sign):
                io.write_int(len(obj["message"]), 4)
                io.write_str(    obj["message"])
                io.write_int(0, 4)

            case (od.ID.Creature_Generator_1 | od.ID.Lighthouse |
                  od.ID.Creature_Generator_4 | od.ID.Mine       |
                  od.ID.Shipyard):
                write_owner(obj["owner"])

            case (od.ID.Garrison | od.ID.Garrison_Vertical):
                write_garrison(obj)

            case od.ID.Abandoned_Mine:
                io.write_bits(obj["resources"])
                io.write_int(0, 3)

            case (od.ID.Shrine_of_Magic_Incantation |
                  od.ID.Shrine_of_Magic_Gesture     |
                  od.ID.Shrine_of_Magic_Thought):
                io.write_int(obj["spell"], 4)

            case od.ID.Spell_Scroll:
                write_spell_scroll(obj)

            case od.ID.Hero_Placeholder:
                write_hero_placeholder(obj)

            case (od.ID.Creature_Bank | od.ID.Derelict_Ship |
                  od.ID.Dragon_Utopia | od.ID.Crypt | od.ID.Shipwreck):
                write_bank(obj)

def parse_owner() -> int:
    # TODO: The owner is actually just one byte, usually followed by three null
    # bytes (but not always!). Remove this method and just read the owner
    # everywhere by themselves. 
    return io.read_int(4)

def write_owner(owner: int) -> None:
    io.write_int(owner, 4)

def parse_creatures(amount: int = 7) -> list:
    info = []
    for _ in range(amount):
        creature = {}
        creature["id"] = cd.ID(io.read_int(2))
        creature["amount"]   = io.read_int(2)
        info.append(creature)
    return info

def write_creatures(info: list) -> None:
    for guard in info:
        io.write_int(guard["id"], 2)
        io.write_int(guard["amount"], 2)

def parse_common(obj: dict) -> dict:
    message_length = io.read_int(4)

    if message_length > 0:
        obj["message"] = io.read_str(message_length)
    if io.read_int(1):
        obj["guards"] = parse_creatures()

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
        write_creatures(obj["guards"])
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
    obj["guards"] = parse_creatures()
    obj["troops_removable"] = io.read_int(1)

    io.seek(8)
    return obj

def write_garrison(obj: dict) -> None:
    write_owner(obj["owner"])
    write_creatures(obj["guards"])
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

    hero["id"] = hd.ID(io.read_int(1))

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
        hero["creatures"] = parse_creatures()

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
        write_creatures(hero["creatures"])
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

def parse_hero_placeholder(obj: dict) -> dict:
    obj["owner"]   =       io.read_int(1)
    obj["hero_id"] = hd.ID(io.read_int(1))

    if obj["hero_id"] == hd.ID.Default:
        obj["power_rating"] = io.read_int(1)

    return obj

def write_hero_placeholder(obj: dict) -> None:
    io.write_int(obj["owner"], 1)
    io.write_int(obj["hero_id"], 1)

    if obj["hero_id"] == hd.ID.Default:
        io.write_int(obj["power_rating"], 1)

class Disposition(IntEnum):
    Compliant  = 0
    Friendly   = 1
    Aggressive = 2
    Hostile    = 3
    Savage     = 4
    Precise    = 5

def parse_monster(obj: dict) -> dict:
    obj["start_bytes"] = io.read_raw(4)
    obj["quantity"]    = io.read_int(2)
    obj["disposition"] = Disposition(io.read_int(1))

    if io.read_int(1):
        obj["message"] = io.read_str(io.read_int(4))
        obj["resources"] = []
        for _ in range(7):
            obj["resources"].append(io.read_int(4))
        obj["artifact"] = ad.ID(io.read_int(2))

    obj["monster_never_flees"]     = bool(io.read_int(1))
    obj["quantity_does_not_grow"]  = bool(io.read_int(1))
    obj["middle_bytes"]            =      io.read_raw(2)
    obj["precise_disposition"]     =      io.read_int(4)
    obj["join_only_for_money"]     = bool(io.read_int(1))
    obj["joining_monster_percent"] =      io.read_int(4)
    obj["upgraded_stack"]          =      io.read_int(4)
    obj["stack_count"]             =      io.read_int(4)

    return obj

def write_monster(obj: dict) -> None:
    io.write_raw(obj["start_bytes"])
    io.write_int(obj["quantity"], 2)
    io.write_int(obj["disposition"], 1)

    if "message" in obj:
        io.write_int(1, 1)
        io.write_int(len(obj["message"]), 4)
        io.write_str(    obj["message"])
        for res in obj["resources"]:
            io.write_int(res, 4)
        io.write_int(obj["artifact"], 2)
    else: io.write_int(0, 1)

    io.write_int(obj["monster_never_flees"], 1)
    io.write_int(obj["quantity_does_not_grow"], 1)
    io.write_raw(obj["middle_bytes"])
    io.write_int(obj["precise_disposition"], 4)
    io.write_int(obj["join_only_for_money"], 1)
    io.write_int(obj["joining_monster_percent"], 4)
    io.write_int(obj["upgraded_stack"], 4)
    io.write_int(obj["stack_count"], 4)

def parse_town(obj: dict) -> dict:
    obj["start_bytes"] = io.read_raw(4)
    obj["owner"]       = io.read_int(1)

    if io.read_int(1): # Is the name set?
        obj["name"] = io.read_str(io.read_int(4))

    if io.read_int(1): # Is the garrison customized?
        obj["garrison_guards"] = parse_creatures()

    obj["garrison_formation"] = io.read_int(1)

    if io.read_int(1): # Are the buildings customized?
        obj["buildings_built"]    =      io.read_bits(6)
        obj["buildings_disabled"] =      io.read_bits(6)
    else: obj["has_fort"]         = bool(io.read_int(1))

    obj["spells_must_appear"]  =      io.read_bits(9)
    obj["spells_cant_appear"]  =      io.read_bits(9)
    obj["spell_research"]      = bool(io.read_int(1))

    obj["events"]    = parse_events(is_town=True)
    obj["alignment"] = io.read_int(1)

    io.seek(3)
    return obj

def write_town(obj: dict) -> None:
    io.write_raw(obj["start_bytes"])
    io.write_int(obj["owner"], 1)

    if "name" in obj:
        io.write_int(1, 1)
        io.write_int(len(obj["name"]), 4)
        io.write_str(    obj["name"])
    else: io.write_int(0, 1)

    if "garrison_guards" in obj:
        io.write_int(1, 1)
        write_creatures(obj["garrison_guards"])
    else: io.write_int(0, 1)

    io.write_int(obj["garrison_formation"], 1)

    if "buildings_built" in obj:
        io.write_int(1, 1)
        io.write_bits(obj["buildings_built"])
        io.write_bits(obj["buildings_disabled"])
    else:
        io.write_int(0, 1)
        io.write_int(obj["has_fort"], 1)

    io.write_bits(obj["spells_must_appear"])
    io.write_bits(obj["spells_cant_appear"])
    io.write_int( obj["spell_research"], 1)

    write_events(obj["events"], is_town=True)

    io.write_int(obj["alignment"], 1)
    io.write_int(0, 3)

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

def parse_scholar(obj: dict) -> dict:
    obj["type"] = io.read_int(1)
    
    match obj["type"]:
        case 255: io.seek(1) # Random
        case 0:   obj["reward"] = skd.Primary(io.read_int(1))
        case 1:   obj["reward"] = skd.Secondary(io.read_int(1))
        case 2:   obj["reward"] = spd.ID(io.read_int(1))

    io.seek(6)
    return obj

def write_scholar(obj: dict) -> None:
    io.write_int(obj["type"], 1)

    if "reward" in obj:
        io.write_int(obj["reward"], 1)
    else: io.write_int(0, 1)

    io.write_int(0, 6)

class Quest(IntEnum):
    NONE                        =  0
    ACHIEVE_EXPERIENCE_LEVEL    =  1
    ACHIEVE_PRIMARY_SKILL_LEVEL =  2
    DEFEAT_SPECIFIC_HERO        =  3
    DEFEAT_SPECIFIC_MONSTER     =  4
    RETURN_WITH_ARTIFACTS       =  5
    RETURN_WITH_CREATURES       =  6
    RETURN_WITH_RESOURCES       =  7
    BE_SPECIFIC_HERO            =  8
    BELONG_TO_SPECIFIC_PLAYER   =  9
    HOTA_QUEST                  = 10

class HotA_Q(IntEnum):
    BELONG_TO_SPECIFIC_CLASS = 0
    RETURN_NOT_BEFORE_DATE   = 1

def parse_quest() -> dict:
    quest = {
        "type"              : Quest.NONE,
        "value"             : 0,
        "deadline"          : 4294967295, # 4 bytes of 255
        "proposal_message"  : "",
        "progress_message"  : "",
        "completion_message": ""
    }

    quest["type"] = Quest(io.read_int(1))

    match quest["type"]:
        case Quest.NONE:
            return quest

        case Quest.ACHIEVE_EXPERIENCE_LEVEL:
            quest["value"] = io.read_int(4)

        case Quest.ACHIEVE_PRIMARY_SKILL_LEVEL:
            skills = []
            skills.append(io.read_int(1))
            skills.append(io.read_int(1))
            skills.append(io.read_int(1))
            skills.append(io.read_int(1))
            quest["value"] = skills

        case (Quest.DEFEAT_SPECIFIC_HERO | Quest.DEFEAT_SPECIFIC_MONSTER):
            # In parse_hero() and parse_monster(), these are the "start_bytes".
            # So it is most likely some identifier for the specific object.
            quest["value"] = io.read_raw(4)

        case Quest.RETURN_WITH_ARTIFACTS:
            quest["value"] = []
            for _ in range(io.read_int(1)):
                quest["value"].append(ad.ID(io.read_int(2)))

        case Quest.RETURN_WITH_CREATURES:
            quest["value"] = parse_creatures(amount=io.read_int(1))

        case Quest.RETURN_WITH_RESOURCES:
            quest["value"] = []
            for _ in range(7):
                quest["value"].append(io.read_int(4))

        case Quest.BE_SPECIFIC_HERO:
            quest["value"] = hd.ID(io.read_int(1))

        case Quest.BELONG_TO_SPECIFIC_PLAYER:
            quest["value"] = io.read_int(1)

        case Quest.HOTA_QUEST:
            quest["hota_type"] = HotA_Q(io.read_int(4))

            if quest["hota_type"] == HotA_Q.BELONG_TO_SPECIFIC_CLASS:
                quest["hota_extra"] = io.read_int(4)
                quest["value"] = io.read_bits(3)

            elif quest["hota_type"] == HotA_Q.RETURN_NOT_BEFORE_DATE:
                quest["value"] = io.read_int(4)

    quest["deadline"]           = io.read_int(4)
    quest["proposal_message"]   = io.read_str(io.read_int(4))
    quest["progress_message"]   = io.read_str(io.read_int(4))
    quest["completion_message"] = io.read_str(io.read_int(4))

    return quest

def write_quest(info: dict) -> None:
    io.write_int(info["type"], 1)

    match info["type"]:
        case Quest.NONE:
            return

        case Quest.ACHIEVE_EXPERIENCE_LEVEL:
            io.write_int(info["value"], 4)

        case Quest.ACHIEVE_PRIMARY_SKILL_LEVEL:
            for skill in info["value"]:
                io.write_int(skill, 1)

        case (Quest.DEFEAT_SPECIFIC_HERO | Quest.DEFEAT_SPECIFIC_MONSTER):
            io.write_raw(info["value"])

        case Quest.RETURN_WITH_ARTIFACTS:
            io.write_int(len(info["value"]), 1)
            for artifact in info["value"]:
                io.write_int(artifact, 2)

        case Quest.RETURN_WITH_CREATURES:
            io.write_int(len(info["value"]), 1)
            write_creatures(info["value"])

        case Quest.RETURN_WITH_RESOURCES:
            for resource in info["value"]:
                io.write_int(resource, 4)

        case (Quest.BE_SPECIFIC_HERO | Quest.BELONG_TO_SPECIFIC_PLAYER):
            io.write_int(info["value"], 1)

        case Quest.HOTA_QUEST:
            io.write_int(info["hota_type"], 4)

            if info["hota_type"] == HotA_Q.BELONG_TO_SPECIFIC_CLASS:
                io.write_int(info["hota_extra"], 4)
                io.write_bits(info["value"])

            elif info["hota_type"] == HotA_Q.RETURN_NOT_BEFORE_DATE:
                io.write_int(info["value"], 4)

    io.write_int(    info["deadline"], 4)
    io.write_int(len(info["proposal_message"]), 4)
    io.write_str(    info["proposal_message"])
    io.write_int(len(info["progress_message"]), 4)
    io.write_str(    info["progress_message"])
    io.write_int(len(info["completion_message"]), 4)
    io.write_str(    info["completion_message"])

class Reward(IntEnum):
    NONE            =  0
    EXPERIENCE      =  1
    SPELL_POINTS    =  2
    MORALE          =  3
    LUCK            =  4
    RESOURCE        =  5
    PRIMARY_SKILL   =  6
    SECONDARY_SKILL =  7
    ARTIFACT        =  8
    SPELL           =  9
    CREATURES       = 10

def parse_reward() -> dict:
    reward = { "type": Reward(io.read_int(1)) }

    match reward["type"]:
        case (Reward.EXPERIENCE | Reward.SPELL_POINTS):
            reward["value"] = io.read_int(4)

        case (Reward.MORALE | Reward.LUCK):
            reward["value"] = io.read_int(1)

        case Reward.RESOURCE:
            reward["value"] = []
            reward["value"].append(od.Resource(io.read_int(1)))
            reward["value"].append(io.read_int(4))

        case Reward.PRIMARY_SKILL:
            reward["value"] = []
            reward["value"].append(skd.Primary(io.read_int(1)))
            reward["value"].append(io.read_int(1))

        case Reward.SECONDARY_SKILL:
            reward["value"] = []
            reward["value"].append(skd.Secondary(io.read_int(1)))
            reward["value"].append(io.read_int(1))

        case Reward.ARTIFACT:
            reward["value"] = ad.ID(io.read_int(2))

        case Reward.SPELL:
            reward["value"] = spd.ID(io.read_int(1))

        case Reward.CREATURES:
            reward["value"] = parse_creatures(amount=1)

    return reward

def write_reward(info: dict) -> None:
    io.write_int(info["type"], 1)

    match info["type"]:
        case (Reward.EXPERIENCE | Reward.SPELL_POINTS):
            io.write_int(info["value"], 4)

        case (Reward.MORALE | Reward.LUCK | Reward.SPELL):
            io.write_int(info["value"], 1)

        case Reward.RESOURCE:
            io.write_int(info["value"][0], 1)
            io.write_int(info["value"][1], 4)

        case (Reward.PRIMARY_SKILL | Reward.SECONDARY_SKILL):
            io.write_int(info["value"][0], 1)
            io.write_int(info["value"][1], 1)

        case Reward.ARTIFACT:
            io.write_int(info["value"], 2)

        case Reward.CREATURES:
            write_creatures(info["value"])

def parse_seers_hut(obj: dict) -> dict:
    obj["one_time_quests"]   = []
    obj["repeatable_quests"] = []

    for _ in range(io.read_int(4)): # Amount of one-time quests
        obj["one_time_quests"].append([parse_quest(), parse_reward()])

    for _ in range(io.read_int(4)): # Amount of repeatable quests
        obj["repeatable_quests"].append([parse_quest(), parse_reward()])

    io.seek(2)
    return obj

def write_seers_hut(obj: dict) -> None:
    io.write_int(len(obj["one_time_quests"]), 4)
    for quest in obj["one_time_quests"]:
        write_quest(quest[0])
        write_reward(quest[1])

    io.write_int(len(obj["repeatable_quests"]), 4)
    for quest in obj["repeatable_quests"]:
        write_quest(quest[0])
        write_reward(quest[1])

    io.write_int(0, 2)

def parse_spell_scroll(obj: dict) -> dict:
    if io.read_int(1):
        obj = parse_common(obj)
    obj["spell"] = spd.ID(io.read_int(4))
    return obj

def write_spell_scroll(obj: dict) -> None:
    if len(obj) > 3:
        write_common(obj)
    else: io.write_int(0, 1)
    io.write_int(obj["spell"], 4)

def parse_dwelling(obj: dict) -> dict:
    obj["owner"] = io.read_int(4)

    obj["same_as_town"] = io.read_int(4)
    if obj["same_as_town"] == 0:
        obj["alignment"] = io.read_bits(2)

    obj["minimum_level"] = io.read_int(1)
    obj["maximum_level"] = io.read_int(1)
    return obj

def write_dwelling(obj: dict) -> None:
    io.write_int(obj["owner"], 4)

    io.write_int(obj["same_as_town"], 4)
    if "alignment" in obj:
        io.write_bits(obj["alignment"])

    io.write_int(obj["minimum_level"], 1)
    io.write_int(obj["maximum_level"], 1)

def parse_leveled(obj: dict) -> dict:
    obj["owner"] = io.read_int(4)

    obj["same_as_town"] = io.read_int(4)
    if obj["same_as_town"] == 0:
        obj["alignment"] = io.read_bits(2)

    return obj

def write_leveled(obj: dict) -> None:
    io.write_int(obj["owner"], 4)

    io.write_int(obj["same_as_town"], 4)
    if "alignment" in obj:
        io.write_bits(obj["alignment"])

def parse_faction(obj: dict) -> dict:
    obj["owner"]         = io.read_int(4)
    obj["minimum_level"] = io.read_int(1)
    obj["maximum_level"] = io.read_int(1)
    return obj

def write_faction(obj: dict) -> None:
    io.write_int(obj["owner"], 4)
    io.write_int(obj["minimum_level"], 1)
    io.write_int(obj["maximum_level"], 1)











