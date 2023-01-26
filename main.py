#!/usr/bin/env python3

import sys
import gzip

import src.map_io as io
import src.handler_01_general as h1
import src.handler_02_player_specs as h2

def main():
    with gzip.open(sys.argv[1], 'rb') as io.map_file:
        general      = h1.parse_general()
        player_specs = h2.parse_player_specs()
        last_data    = io.map_file.read()
    
#    general["description"] = "I have now edited the description from here!"
#    player_specs[6]["generate_hero"] = True

    print("\nGeneral:\n\n", general)
    print("\nPlayer Specs:\n")
    for i in range(8):
        print("Player", i+1)
        print(player_specs[i], "\n")

    with gzip.open("output.h3m", 'wb') as io.out_file:
        h1.write_general(general)
        h2.write_player_specs(player_specs)
        io.out_file.write(last_data)

if __name__ == "__main__":
    main()
