#!/usr/bin/env python3

import src.file_io as io

from enum import IntEnum

class Tile(IntEnum):
    TerrainType    = 0
    TerrainPicture = 1
    RiverType      = 2
    RiverPicture   = 3
    RoadType       = 4
    RoadPicture    = 5
    Mirroring      = 6

class TerrainType(IntEnum):
    Dirt         =  0
    Sand         =  1
    Grass        =  2
    Snow         =  3
    Swamp        =  4
    Rough        =  5
    Subterranean =  6
    Lava         =  7
    Water        =  8
    Rock         =  9
    Highlands    = 10
    Wasteland    = 11

class RiverType(IntEnum):
    Empty = 0
    Clear = 1
    Icy   = 2
    Muddy = 3
    Lava  = 4

class RoadType(IntEnum):
    Empty       = 0
    Dirt        = 1
    Gravel      = 2
    Cobblestone = 3

def parse_terrain(size: int, is_two_level: bool) -> list:
    info = []

    for _ in range(size*size*2 if is_two_level else size*size):
        info.append([
            TerrainType(io.read_int(1)),
            io.read_int(1), # Terrain picture
            RiverType(io.read_int(1)),
            io.read_int(1), # River picture
            RoadType(io.read_int(1)),
            io.read_int(1), # Road picture
            io.read_int(1)  # Tile mirroring
        ])

    return info

def write_terrain(info: list) -> None:
    for tile in info:
        for i in tile:
            io.write_int(i, 1)
