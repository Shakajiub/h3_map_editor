#!/usr/bin/env python3

import src.file_io    as io
import data.heroes    as hd
import data.spells    as sd
import data.artifacts as ad

from src.handler_01_general import MapFormat

def parse_starting_heroes(general_info: dict) -> dict:
    info = {
        "total_heroes"   : 0,
        "hero_flags"     : [],
        "placeholders"   : [],
        "custom_heroes"  : [],
        "unhandled_bytes": b''
    }

    if general_info["map_format"] == MapFormat.HotA:
        info["total_heroes"] = io.read_int(4)
        info["hero_flags"]   = io.read_bits(25)

    elif general_info["map_format"] == MapFormat.SoD:
        info["hero_flags"] = io.read_bits(20)

    for _ in range(io.read_int(4)): # Amount of placeholder heroes
        info["placeholders"].append(hd.ID(io.read_int(1)))

    for _ in range(io.read_int(1)): # Amount of custom heroes
        hero = {}
        hero["id"] = io.read_int(1)
        hero["face"] = io.read_int(1)
        hero["name"] = io.read_str(io.read_int(4))
        hero["may_be_hired_by"] = io.read_int(1)
        info["custom_heroes"].append(hero)

    info["unhandled_bytes"] = io.read_raw(57)

    return info

def write_starting_heroes(info: dict) -> None:
    if info["total_heroes"] != 0:
        io.write_int(info["total_heroes"], 4)

    io.write_bits(info["hero_flags"])

    io.write_int(len(info["placeholders"]), 4)
    for hero in info["placeholders"]:
        io.write_int(hero, 1)

    io.write_int(len(info["custom_heroes"]), 1)

    for hero in info["custom_heroes"]:
        io.write_int(    hero["id"], 1)
        io.write_int(    hero["face"], 1)
        io.write_int(len(hero["name"]), 4)
        io.write_str(    hero["name"])
        io.write_int(    hero["may_be_hired_by"], 1)

    io.write_raw(info["unhandled_bytes"])

def parse_hero_data() -> list:
    info = []

    hero_amount = io.read_int(4)

    for i in range(hero_amount):
        if not io.read_int(1):
            info.append({})
            continue

        hero = {
            "experience"        : -1,
            "secondary_custom"  : False,
            "secondary_skills"  : [],
            "artifacts_equipped": {},
            "artifacts_backpack": [],
            "biography"         : "",
            "gender"            : 255,
            "spells"            : b'',
            "primary_skills"    : {},
            "always_add_skills" : True,
            "cannot_gain_xp"    : False,
            "level"             : 1
        }

        if io.read_int(1): # Is experience set?
            hero["experience"] = io.read_int(4)

        if io.read_int(1): # Are secondary skills set?
            hero["secondary_custom"] = True
            for _ in range(io.read_int(4)):
                skill = {}
                skill["id"]    = io.read_int(1)
                skill["level"] = io.read_int(1)
                hero["secondary_skills"].append(skill)

        if io.read_int(1): # Are artifacts set?
            hero["artifacts_equipped"]["head"]          = parse_artifact()
            hero["artifacts_equipped"]["shoulders"]     = parse_artifact()
            hero["artifacts_equipped"]["neck"]          = parse_artifact()
            hero["artifacts_equipped"]["right_hand"]    = parse_artifact()
            hero["artifacts_equipped"]["left_hand"]     = parse_artifact()
            hero["artifacts_equipped"]["torso"]         = parse_artifact()
            hero["artifacts_equipped"]["right_ring"]    = parse_artifact()
            hero["artifacts_equipped"]["left_ring"]     = parse_artifact()
            hero["artifacts_equipped"]["feet"]          = parse_artifact()
            hero["artifacts_equipped"]["misc_1"]        = parse_artifact()
            hero["artifacts_equipped"]["misc_2"]        = parse_artifact()
            hero["artifacts_equipped"]["misc_3"]        = parse_artifact()
            hero["artifacts_equipped"]["misc_4"]        = parse_artifact()
            hero["artifacts_equipped"]["war_machine_1"] = parse_artifact()
            hero["artifacts_equipped"]["war_machine_2"] = parse_artifact()
            hero["artifacts_equipped"]["war_machine_3"] = parse_artifact()
            hero["artifacts_equipped"]["war_machine_4"] = parse_artifact()
            hero["artifacts_equipped"]["spellbook"]     = parse_artifact()
            hero["artifacts_equipped"]["misc_5"]        = parse_artifact()
            
            for _ in range(io.read_int(2)):
                hero["artifacts_backpack"].append(parse_artifact())

        if io.read_int(1): # Is biography set?
            hero["biography"] = io.read_str(io.read_int(4))

        hero["gender"] = io.read_int(1)

        if io.read_int(1): # Are spells set?
            hero["spells"] = io.read_bits(9)

        if io.read_int(1): # Are primary skills set?
            hero["primary_skills"]["attack"]      = io.read_int(1)
            hero["primary_skills"]["defense"]     = io.read_int(1)
            hero["primary_skills"]["spell_power"] = io.read_int(1)
            hero["primary_skills"]["knowledge"]   = io.read_int(1)

        info.append(hero)

    # Added by HotA 1.7.0 at the end of normal hero data:
    #
    # 1 byte  - Always add skills.
    # 1 byte  - Cannot gain XP.
    # 4 bytes - Level.
    #
    # For every hero.

    for i in range(hero_amount):
        info[i]["always_add_skills"] = bool(io.read_int(1))
        info[i]["cannot_gain_xp"]    = bool(io.read_int(1))
        info[i]["level"]             =      io.read_int(4)

    return info

def write_hero_data(info: list) -> None:
    io.write_int(len(info), 4)

    for hero in info:
        if len(hero) == 3:
            io.write_int(0, 1)
            continue
        io.write_int(1, 1)

        #
        if hero["experience"] >= 0:
            io.write_int(1, 1)
            io.write_int(hero["experience"], 4)
        else: io.write_int(0, 1)

        #
        if hero["secondary_custom"]:
            io.write_int(1, 1)
            io.write_int(len(hero["secondary_skills"]), 4)

            for skill in hero["secondary_skills"]:
                io.write_int(skill["id"], 1)
                io.write_int(skill["level"], 1)
        else: io.write_int(0, 1)

        #
        if hero["artifacts_equipped"] or hero["artifacts_backpack"]:
            io.write_int(1, 1)

            write_artifact(hero["artifacts_equipped"]["head"])
            write_artifact(hero["artifacts_equipped"]["shoulders"])
            write_artifact(hero["artifacts_equipped"]["neck"])
            write_artifact(hero["artifacts_equipped"]["right_hand"])
            write_artifact(hero["artifacts_equipped"]["left_hand"])
            write_artifact(hero["artifacts_equipped"]["torso"])
            write_artifact(hero["artifacts_equipped"]["right_ring"])
            write_artifact(hero["artifacts_equipped"]["left_ring"])
            write_artifact(hero["artifacts_equipped"]["feet"])
            write_artifact(hero["artifacts_equipped"]["misc_1"])
            write_artifact(hero["artifacts_equipped"]["misc_2"])
            write_artifact(hero["artifacts_equipped"]["misc_3"])
            write_artifact(hero["artifacts_equipped"]["misc_4"])
            write_artifact(hero["artifacts_equipped"]["war_machine_1"])
            write_artifact(hero["artifacts_equipped"]["war_machine_2"])
            write_artifact(hero["artifacts_equipped"]["war_machine_3"])
            write_artifact(hero["artifacts_equipped"]["war_machine_4"])
            write_artifact(hero["artifacts_equipped"]["spellbook"])
            write_artifact(hero["artifacts_equipped"]["misc_5"])
            
            io.write_int(len(hero["artifacts_backpack"]), 2)
            for artifact in hero["artifacts_backpack"]:
                write_artifact(artifact)
        else: io.write_int(0, 1)

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
            io.write_bits(hero["spells"])
        else: io.write_int(0, 1)

        #
        if hero["primary_skills"]:
            io.write_int(1, 1)
            io.write_int(hero["primary_skills"]["attack"], 1)
            io.write_int(hero["primary_skills"]["defense"], 1)
            io.write_int(hero["primary_skills"]["spell_power"], 1)
            io.write_int(hero["primary_skills"]["knowledge"], 1)
        else: io.write_int(0, 1)

    # HotA 1.7.0.
    for hero in info:
        io.write_int(hero["always_add_skills"], 1)
        io.write_int(hero["cannot_gain_xp"], 1)
        io.write_int(hero["level"], 4)

def parse_artifact() -> list:
    artifact = [
        ad.ID(io.read_int(2)),
        io.read_int(2)
    ]
    if artifact[0] == ad.ID.Spell_Scroll:
        artifact[1] = sd.ID(artifact[1])
    return artifact

def write_artifact(artifact: list) -> None:
    io.write_int(artifact[0], 2)
    io.write_int(artifact[1], 2)
