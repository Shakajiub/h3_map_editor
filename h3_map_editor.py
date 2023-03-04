#!/usr/bin/env python3

from sys  import argv
from gzip import open

import src.file_io as io
import src.scripts as scripts

import src.handler_01_general            as h1
import src.handler_02_players_and_teams  as h2
import src.handler_03_conditions         as h3
import src.handler_04_heroes             as h4
import src.handler_05_additional_flags   as h5
import src.handler_06_rumors_and_events  as h6
import src.handler_07_terrain            as h7
import src.handler_08_objects            as h8

def main() -> None:
    map_data = {
        "general"     : {}, # General tab in Map Specifications
        "player_specs": [], # ...
        "conditions"  : {}, # Special Victory and Loss Conditions
        "teams"       : {}, # ...
        "start_heroes": {}, # Available starting heroes
        "ban_flags"   : {}, # Available artifacts, spells, and skills
        "rumors"      : [], # ...
        "hero_data"   : [], # Custom hero details (name, bio, portrait, etc.)
        "terrain"     : [], # ...
        "object_defs" : [], # Object definitions (sprite, type, squares, etc.)
        "object_data" : [], # Object details (messages, guards, quests, etc.)
        "events"      : [], # ...
        "null_bytes"  : b'' # All maps end with some null bytes
    }

##################
## OPEN THE MAP ##
##################

    with open(argv[1], 'rb') as io.in_file:
        print(f"Reading map \"{argv[1]}\" ...")
        map_data["general"]      = h1.parse_general()
        map_data["player_specs"] = h2.parse_player_specs()
        map_data["conditions"]   = h3.parse_conditions()
        map_data["teams"]        = h2.parse_teams()
        map_data["start_heroes"] = h4.parse_starting_heroes(map_data["general"])
        map_data["ban_flags"]    = h5.parse_flags()
        map_data["rumors"]       = h6.parse_rumors()
        map_data["hero_data"]    = h4.parse_hero_data()
        map_data["terrain"]      = h7.parse_terrain(map_data["general"])
        map_data["object_defs"]  = h8.parse_object_defs()
        map_data["object_data"]  = h8.parse_object_data(map_data["object_defs"])
        map_data["events"]       = h6.parse_events()
        map_data["null_bytes"]   = io.in_file.read()

########################
## RUN CUSTOM SCRIPTS ##
########################

    print("This is where you run any scripts to edit the map!")

##################
## SAVE THE MAP ##
##################

    with open("output.h3m", 'wb') as io.out_file:
        print("Writing map \"output.h3m\" ...")
        h1.write_general(        map_data["general"])
        h2.write_player_specs(   map_data["player_specs"])
        h3.write_conditions(     map_data["conditions"])
        h2.write_teams(          map_data["teams"])
        h4.write_starting_heroes(map_data["start_heroes"])
        h5.write_flags(          map_data["ban_flags"])
        h6.write_rumors(         map_data["rumors"])
        h4.write_hero_data(      map_data["hero_data"])
        h7.write_terrain(        map_data["terrain"])
        h8.write_object_defs(    map_data["object_defs"])
        h8.write_object_data(    map_data["object_data"])
        h6.write_events(         map_data["events"])
        io.out_file.write(       map_data["null_bytes"])

if __name__ == "__main__":
    main()
