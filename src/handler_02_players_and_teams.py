#!/usr/bin/env python3

import src.file_io as io
import data.heroes as hd
from data.objects import Town

from enum import IntEnum

def parse_player_specs() -> list:
    specs = []

    for _ in range(8):
        info = {
            "playability_human"    : False,
            "playability_ai"       : False,
            "ai_behavior"          : 0,
            "alignments_customized": False,
            "alignments_allowed"   : 0,
            "alignment_is_random"  : False,
            "has_main_town"        : False,
            "generate_hero"        : False,
            "town_type"            : 0,
            "town_coords"          : [0, 0, 0],
            "has_random_hero"      : False,
            "starting_hero_id"     : 255,
            "starting_hero_face"   : 255,
            "starting_hero_name"   : "",
            "available_heroes"     : [],
            "garbage_byte"         : b'\x00',
            "placeholder_heroes"   : []
        }

        info["playability_human"]     = bool(io.read_int(1))
        info["playability_ai"]        = bool(io.read_int(1))
        info["ai_behavior"]           =      io.read_int(1)
        info["alignments_customized"] = bool(io.read_int(1))
        info["alignments_allowed"]    =      io.read_int(2)
        info["alignment_is_random"]   = bool(io.read_int(1))
        info["has_main_town"]         = bool(io.read_int(1))

        if info["has_main_town"]:
            info["generate_hero"]  = bool(io.read_int(1))
            info["town_type"]      = Town(io.read_int(1))
            info["town_coords"][0] =      io.read_int(1)
            info["town_coords"][1] =      io.read_int(1)
            info["town_coords"][2] =      io.read_int(1)

        info["has_random_hero"]  =  bool(io.read_int(1))
        info["starting_hero_id"] = hd.ID(io.read_int(1))

        if info["starting_hero_id"] != hd.ID.Default:
            info["starting_hero_face"] = hd.ID(io.read_int(1))
            info["starting_hero_name"] = io.read_str(io.read_int(4))
            info["garbage_byte"]       = io.read_raw(1)

            for _ in range(io.read_int(4)):
                hero = {}
                hero["id"]   = hd.ID(io.read_int(1))
                hero["name"] = io.read_str(io.read_int(4))
                info["available_heroes"].append(hero)
        else:
            io.seek(1)
            for _ in range(io.read_int(4)): # Amount of placeholder heroes
                info["placeholder_heroes"].append(hd.ID(io.read_int(5)))

        specs.append(info)

    return specs

def write_player_specs(specs: list) -> None:
    for info in specs:
        io.write_int(info["playability_human"], 1)
        io.write_int(info["playability_ai"], 1)
        io.write_int(info["ai_behavior"], 1)
        io.write_int(info["alignments_customized"], 1)
        io.write_int(info["alignments_allowed"], 2)
        io.write_int(info["alignment_is_random"], 1)
        io.write_int(info["has_main_town"], 1)

        if info["has_main_town"]:
            io.write_int(info["generate_hero"], 1)
            io.write_int(info["town_type"], 1)
            io.write_int(info["town_coords"][0], 1)
            io.write_int(info["town_coords"][1], 1)
            io.write_int(info["town_coords"][2], 1)

        io.write_int(info["has_random_hero"], 1)
        io.write_int(info["starting_hero_id"], 1)

        if info["starting_hero_id"] != 255:
            io.write_int(    info["starting_hero_face"], 1)
            io.write_int(len(info["starting_hero_name"]), 4)
            io.write_str(    info["starting_hero_name"])
            io.write_raw(    info["garbage_byte"])
            io.write_int(len(info["available_heroes"]), 4)

            for hero in info["available_heroes"]:
                io.write_int(    hero["id"], 1)
                io.write_int(len(hero["name"]), 4)
                io.write_str(    hero["name"])
        else:
            io.write_int(0, 1)
            io.write_int(len(info["placeholder_heroes"]), 4)

            for hero in info["placeholder_heroes"]:
                io.write_int(hero, 5)

def parse_teams() -> dict:
    info = {
        "amount_of_teams": 0,
        "Player1": 0,
        "Player2": 0,
        "Player3": 0,
        "Player4": 0,
        "Player5": 0,
        "Player6": 0,
        "Player7": 0,
        "Player8": 0
    }

    info["amount_of_teams"] = io.read_int(1)

    if info["amount_of_teams"] != 0:
        info["Player1"] = io.read_int(1)
        info["Player2"] = io.read_int(1)
        info["Player3"] = io.read_int(1)
        info["Player4"] = io.read_int(1)
        info["Player5"] = io.read_int(1)
        info["Player6"] = io.read_int(1)
        info["Player7"] = io.read_int(1)
        info["Player8"] = io.read_int(1)

    return info

def write_teams(info: dict) -> None:
    io.write_int(info["amount_of_teams"], 1)

    if info["amount_of_teams"] != 0:
        io.write_int(info["Player1"], 1)
        io.write_int(info["Player2"], 1)
        io.write_int(info["Player3"], 1)
        io.write_int(info["Player4"], 1)
        io.write_int(info["Player5"], 1)
        io.write_int(info["Player6"], 1)
        io.write_int(info["Player7"], 1)
        io.write_int(info["Player8"], 1)
