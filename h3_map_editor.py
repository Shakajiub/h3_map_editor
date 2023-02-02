#!/usr/bin/env python3

import sys
import gzip

import src.file_io as io

import src.handler_01_general            as h1
import src.handler_02_players_and_teams  as h2
import src.handler_03_victory_conditions as h3
import src.handler_04_heroes             as h4
import src.handler_05_artifacts          as h5
import src.handler_06_rumors             as h6
import src.handler_07_terrain            as h7

#import data.heroes    as hero_data
#import data.artifacts as art_data

def main() -> None:
    with gzip.open(sys.argv[1], 'rb') as io.in_file:
        general    = h1.parse_general()
        players    = h2.parse_player_specs()
        conditions = h3.parse_victory_conditions()
        teams      = h2.parse_teams()
        hero_flags = h4.parse_hero_flags(general["map_format"])
        artifacts  = h5.parse_artifacts()
        rumors     = h6.parse_rumors()
        hero_data  = h4.parse_hero_data()
        terrain    = h7.parse_terrain(general["map_size"],
                                      general["is_two_level"])

        unhandled  = io.in_file.read()

    print("\nGeneral:\n\n", general)
    print("\nPlayer Specs:")
    for i in range(8):
        print("\nPlayer", i+1)
        print(players[i])
    print("\nTeams:\n\n", teams)
    print("\nVictory/Loss Conditions:\n\n", conditions)
    print("\nHeroes:\n\n", hero_flags, "\n\n", hero_data)
    print("\nArtifacts:\n\n", artifacts)
    print("\nRumors:\n\n", rumors)

    with gzip.open("output.h3m", 'wb') as io.out_file:
        h1.write_general(general)
        h2.write_player_specs(players)
        h3.write_victory_conditions(conditions)
        h2.write_teams(teams)
        h4.write_hero_flags(hero_flags)
        h5.write_artifacts(artifacts)
        h6.write_rumors(rumors)
        h4.write_hero_data(hero_data)
        h7.write_terrain(terrain)
        io.out_file.write(unhandled)

if __name__ == "__main__":
    main()
