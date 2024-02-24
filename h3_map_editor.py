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

#######################
## HANDLE USER INPUT ##
#######################

def main() -> None:
    global map_data

    # Print some block of text as an introduction to the editor.
    # This should contain some common info, tips and maybe some news.
    print("\n##############################")
    print(  "##                          ##")
    print(  "##  h3_map_editor.py v.170  ##")
    print(  "##                          ##")
    print(  "##############################")

    # First argument passed when launching the editor can be a map file.
    if len(argv) > 1:
        print("")
        open_map(argv[1])

    while True:
        command = input("\n[Enter command] > ")
        match command.split():
            case ["open", filename]: open_map(filename)
            case ["save"]:           save_map()
            case ["save", filename]: save_map(filename)

            case ["print", key] | ["show", key]:
                if key in map_data:
                    print(map_data[key])
                else: print("Unrecognized key.")

            case ["count"] | ["list"]:
                scripts.count_objects(map_data["object_data"])

            case ["guards"]:
                map_data["object_data"] = scripts.generate_guards(map_data["object_data"])

            case ["temp"]:
                map_data["object_data"] = scripts.temp(map_data["object_data"])

            case ["q"] | ["quit"] | ["exit"]: break
            case _: print("Unrecognized command.")

################
## OPEN A MAP ##
################

def open_map(filename: str) -> None:
    global map_data

    # Make sure that the filename ends with ".h3m". For convenience,
    # users should be able to open maps without typing the extension.
    if filename[-4:] != ".h3m":
        filename += ".h3m"

    print(f"Reading map '{filename}' ...", end=' ')

    # Make sure that the file actually exists.
    try:
        with open(filename, 'rb'):
            pass
    except FileNotFoundError:
        print(f"ERROR - Could not find '{filename}'")
        return

    # Parse file data byte by byte.
    # Refer to the separate handlers for documentation.
    with open(filename, 'rb') as io.in_file:
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

    print(f"DONE - '{map_data['general']['name']}':")
    print(f"\n{map_data['general']['description']}")

################
## SAVE A MAP ##
################

def save_map(filename: str = "output.h3m") -> None:
    global map_data

    # Make sure that the filename ends with ".h3m". For convenience,
    # users should be able to save maps without typing the extension.
    if len(filename) > 4:
        if filename[-4:] != ".h3m":
            filename += ".h3m"
    else: filename += ".h3m"

    print(f"Writing map '{filename}' ...", end=' ')

    # Save the map byte by byte.
    with open(filename, 'wb') as io.out_file:
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

    print("DONE")

if __name__ == "__main__":
    main()
