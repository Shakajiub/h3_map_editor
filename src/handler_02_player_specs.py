#!/usr/bin/env python3

import src.map_io as io

def parse_player_specs(version):
    specs = []

    for i in range(8):
        info = {
            "mastery": 0, "control_human": False, "control_ai": False,
            "behaviour": 0, "custom_alignments": False, "alignments": b'',
            "random_alignment": False, "has_main_town": False,
            "create_hero": False, "town_type": b'', "town_coords": [],
            "unknown_bytes": b''
        }
        
        if version == 32: # HotA

            for u in range(8):
                data = io.read_raw(15)
                s = ""
                for b in data:
                    s += str(b) + ", "
                print(s)
        
            print(io.read_raw(32))
            return info

        elif version == 28: # SoD
            info["mastery"]           =      io.read_int(1)
            info["control_human"]     = bool(io.read_int(1))
            info["control_ai"]        = bool(io.read_int(1))
            info["behaviour"]         =      io.read_int(1)
            info["custom_alignments"] = bool(io.read_int(1))
            info["alignments"]        =      io.read_int(2)
            info["random_alignment"]  = bool(io.read_int(1))
            info["has_main_town"]     = bool(io.read_int(1))

            if info["has_main_town"]:
                info["create_hero"] = bool(io.read_int(1))
                info["town_type"]   =      io.read_int(1)
                info["town_coords"].append(io.read_int(1))
                info["town_coords"].append(io.read_int(1))
                info["town_coords"].append(io.read_int(1))
                
            info["unknown_bytes"] = io.read_raw(6)

        specs.append(info)

    return specs
    
def write_player_specs(info):
    pass
