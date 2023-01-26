#!/usr/bin/env python3

import src.file_io as io

def parse_player_specs():
    specs = []

    for i in range(8):
        info = {
            "mastery_cap"          : 0,
            "playability_human"    : False,
            "playability_ai"       : False,
            "ai_behavior"          : 0,
            "alignments_customized": False,
            "alignments_allowed"   : 0,
            "alignment_is_random"  : False,
            "has_main_town"        : False,
            "generate_hero"        : False,
            "town_type"            : 0,
            "town_coords"          : [],
            "unhandled_bytes"      : b''
        }
        
        info["mastery_cap"]           =      io.read_int(1)
        info["playability_human"]     = bool(io.read_int(1))
        info["playability_ai"]        = bool(io.read_int(1))
        info["ai_behavior"]           =      io.read_int(1)
        info["alignments_customized"] = bool(io.read_int(1))
        info["alignments_allowed"]    =      io.read_int(2)
        info["alignment_is_random"]   = bool(io.read_int(1))
        info["has_main_town"]         = bool(io.read_int(1))

        if info["has_main_town"]:
            info["generate_hero"] = bool(io.read_int(1))
            info["town_type"]     =      io.read_int(1)
            info["town_coords"].append(  io.read_int(1))
            info["town_coords"].append(  io.read_int(1))
            info["town_coords"].append(  io.read_int(1))
            
        info["unhandled_bytes"] = io.read_raw(6)
        specs.append(info)
        
    return specs
    
def write_player_specs(specs):
    for info in specs:
        io.write_int(info["mastery_cap"], 1)
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

        io.write_raw(info["unhandled_bytes"])
