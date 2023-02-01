#!/usr/bin/env python3

import sys
import gzip

import src.file_io as io

import src.handler_01_general as h1
import src.handler_02_players_and_teams as h2
import src.handler_03_victory_conditions as h3
import src.handler_04_heroes as h4

import data.heroes as heroes

def main() -> None:
    with gzip.open(sys.argv[1], 'rb') as io.in_file:
        general          = h1.parse_general()
        player_specs     = h2.parse_player_specs()
        conditions       = h3.parse_victory_conditions()
        teams            = h2.parse_teams()
        available_heroes = h4.parse_heroes(general["map_format"])
        unhandled_data   = io.in_file.read()

#    general["description"] = "I have now edited the description from here!"
#    player_specs[0]["starting_hero_name"] = "Hackerman"

#    conditions["victory_condition"] = h3.VictoryType.SURVIVE
#    conditions["objective_value_one"] = 21

#    available_heroes["hero_flags"][heroes.ID.Solmyr] = 1
#    available_heroes["hero_flags"][heroes.ID.Haart_Lich] = 1

    print("\nGeneral:\n\n", general)
#    print("\nPlayer Specs:")
#    for i in range(8):
#        print("\nPlayer", i+1)
#        print(player_specs[i])
#    print("\nTeams:\n\n", teams)
#    print("\nVictory/Loss Conditions:\n\n", conditions)
#    print("\nAvailable Heroes:\n\n", available_heroes)

    with gzip.open("output.h3m", 'wb') as io.out_file:
        h1.write_general(general)
        h2.write_player_specs(player_specs)
        h3.write_victory_conditions(conditions)
        h2.write_teams(teams)
        h4.write_heroes(available_heroes)
        io.out_file.write(unhandled_data)

if __name__ == "__main__":
    main()
