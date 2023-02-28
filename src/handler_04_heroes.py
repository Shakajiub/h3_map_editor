#!/usr/bin/env python3

import src.file_io as io
import data.heroes as hd

from src.handler_01_general import MapFormat

def parse_hero_flags(version: int) -> dict:
    info = {
        "hota_data"      : b'',
        "hero_flags"     : [],
        "placeholders"   : [],
        "custom_heroes"  : [],
        "unhandled_bytes": b''
    }

    if version == MapFormat.HotA:
        info["hota_data"]  = io.read_raw(4)
        info["hero_flags"] = io.read_bits(23)

    elif version == MapFormat.SoD:
        info["hero_flags"] = io.read_bits(20)

    for _ in range(io.read_int(4)): # Amount of placeholder heroes
        info["placeholders"].append(hd.ID(io.read_int(1)))

    for _ in range(io.read_int(1)):
        hero = {}
        hero["id"]   = io.read_int(1)
        hero["face"] = io.read_int(1)
        hero["name"] = io.read_str(io.read_int(4))
        hero["may_be_hired_by"]  = io.read_int(1)
        info["custom_heroes"].append(hero)

    info["unhandled_bytes"] = io.read_raw(49)

    return info

def write_hero_flags(info: dict) -> None:
    if info["hota_data"] != b'':
        io.write_raw(info["hota_data"])

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
    
    for _ in range(io.read_int(4)): # Amount of heroes
        if not io.read_int(1):
            info.append(0)
            continue

        hero = {
            "experience"        : -1,
            "secondary_skills"  : [],
            "artifacts_equipped": {},
            "artifacts_backpack": [],
            "biography"         : "",
            "gender"            : 255,
            "spells"            : b'',
            "primary_skills"    : {}
        }

        if io.read_int(1): # Is experience set?
            hero["experience"] = io.read_int(4)

        if io.read_int(1): # Are secondary skills set?
            for _ in range(io.read_int(4)):
                skill = {}
                skill["id"]    = io.read_int(1)
                skill["level"] = io.read_int(1)
                hero["secondary_skills"].append(skill)

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

        info.append(hero)

    return info

def write_hero_data(info: list) -> None:
    io.write_int(len(info), 4)
    
    for hero in info:
        if hero == 0:
            io.write_int(0, 1)
            continue
        io.write_int(1, 1)

        #
        if hero["experience"] >= 0:
            io.write_int(1, 1)
            io.write_int(hero["experience"], 4)
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
