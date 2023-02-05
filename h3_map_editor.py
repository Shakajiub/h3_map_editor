#!/usr/bin/env python3

import sys
import gzip

import src.file_io as io

import src.handler_01_general            as h1
import src.handler_02_players_and_teams  as h2
import src.handler_03_victory_conditions as h3
import src.handler_04_heroes             as h4
import src.handler_05_additional_flags   as h5
import src.handler_06_rumors             as h6
import src.handler_07_terrain            as h7
import src.handler_08_objects            as h8

def main() -> None:
    with gzip.open(sys.argv[1], 'rb') as io.in_file:
        general    = h1.parse_general()
        players    = h2.parse_player_specs()
        conditions = h3.parse_victory_conditions()
        teams      = h2.parse_teams()
        hero_flags = h4.parse_hero_flags(general["map_format"])
        ban_flags  = h5.parse_flags()
        rumors     = h6.parse_rumors()
        hero_data  = h4.parse_hero_data()
        terrain    = h7.parse_terrain(general["map_size"],
                                      general["is_two_level"])
        objects    = h8.parse_objects()
        obj_data   = h8.parse_object_data(objects)
        unhandled  = io.in_file.read()

#    print("\nGeneral:\n\n", general)
#    print("\nPlayer Specs:")
#    for i in range(8):
#        print("\nPlayer", i+1)
#        print(players[i])
#    print("\nTeams:\n\n", teams)
#    print("\nVictory/Loss Conditions:\n\n", conditions)
#    print("\nHeroes:\n\n", hero_flags, "\n\n", hero_data)
#    print("\nBans:\n\n", ban_flags)
#    print("\nRumors:\n\n", rumors)
#    print("\nObjects:\n\n", objects)
#    print("\nObject Data:\n\n", obj_data)

    with gzip.open("output.h3m", 'wb') as io.out_file:
        h1.write_general(general)
        h2.write_player_specs(players)
        h3.write_victory_conditions(conditions)
        h2.write_teams(teams)
        h4.write_hero_flags(hero_flags)
        h5.write_flags(ban_flags)
        h6.write_rumors(rumors)
        h4.write_hero_data(hero_data)
        h7.write_terrain(terrain)
        h8.write_objects(objects)
        h8.write_object_data(objects, obj_data)
        io.out_file.write(unhandled)

if __name__ == "__main__":
    main()
