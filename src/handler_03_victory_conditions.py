#!/usr/bin/env python3

import src.file_io as io

from enum import IntEnum

class VictoryType(IntEnum):
    NONE                 = 255
    ACQUIRE_ARTIFACT     = 0
    ACCUMULATE_CREATURES = 1
    ACCUMULATE_RESOURCES = 2
    UPGRADE_TOWN         = 3
    BUILD_THE_GRAIL      = 4
    DEFEAT_HERO          = 5
    CAPTURE_TOWN         = 6
    DEFEAT_MONSTER       = 7
    FLAG_DWELLINGS       = 8
    FLAG_MINES           = 9
    TRANSPORT_ARTIFACT   = 10
    ELIMINATE_MONSTERS   = 11
    SURVIVE              = 12
    
class LossType(IntEnum):
    NONE         = 255
    LOSE_TOWN    = 0
    LOSE_HERO    = 1
    TIME_EXPIRES = 2

def parse_victory_conditions() -> None:
    info = {
        "victory_condition"   : VictoryType.NONE,
        "allow_normal_win"    : False,
        "allow_ai_special_win": False,
        "objective_value_one" : 0,
        "objective_value_two" : 0,
        "objective_coords"    : [0, 0, 0],
        "loss_condition"      : LossType.NONE,
        "loss_coords"         : [0, 0, 0],
        "loss_timer"          : 0,
        "mystery_byte"        : b''
    }

    info["mystery_byte"] = io.read_raw(1)
    vc =       VictoryType(io.read_int(1))
    info["victory_condition"] = vc
    
    if vc != VictoryType.NONE:
        info["allow_normal_win"]     = bool(io.read_int(1))
        info["allow_ai_special_win"] = bool(io.read_int(1))

        match vc:
            case VictoryType.ACQUIRE_ARTIFACT:
                info["objective_value_one"] = io.read_int(2)
            case VictoryType.ACCUMULATE_CREATURES:
                info["objective_value_one"] = io.read_int(2)
                info["objective_value_two"] = io.read_int(4)
            case VictoryType.ACCUMULATE_RESOURCES:
                info["objective_value_one"] = io.read_int(1)
                info["objective_value_two"] = io.read_int(4)
            case VictoryType.UPGRADE_TOWN:
                info["objective_coords"][0] = io.read_int(1)
                info["objective_coords"][1] = io.read_int(1)
                info["objective_coords"][2] = io.read_int(1)
                info["objective_value_one"] = io.read_int(1)
                info["objective_value_two"] = io.read_int(1)
            case (VictoryType.BUILD_THE_GRAIL | VictoryType.DEFEAT_HERO |
                  VictoryType.CAPTURE_TOWN    | VictoryType.DEFEAT_MONSTER):
                info["objective_coords"][0] = io.read_int(1)
                info["objective_coords"][1] = io.read_int(1)
                info["objective_coords"][2] = io.read_int(1)
            case VictoryType.TRANSPORT_ARTIFACT:
                info["objective_value_one"] = io.read_int(1)
                info["objective_coords"][0] = io.read_int(1)
                info["objective_coords"][1] = io.read_int(1)
                info["objective_coords"][2] = io.read_int(1)
            case VictoryType.SURVIVE:
                info["objective_value_one"] = io.read_int(4)
    
    lc = LossType(io.read_int(1))
    info["loss_condition"] = lc

    if lc == LossType.TIME_EXPIRES:
        info["loss_timer"] = io.read_int(2)
    elif lc != LossType.NONE:
        info["loss_coords"][0] = io.read_int(1)
        info["loss_coords"][1] = io.read_int(1)
        info["loss_coords"][2] = io.read_int(1)

    return info
    
def write_victory_conditions(info: dict) -> None:
    io.write_raw(info["mystery_byte"])
    vc = info["victory_condition"]
    io.write_int(vc, 1)
    
    if vc != VictoryType.NONE:
        io.write_int(info["allow_normal_win"], 1)
        io.write_int(info["allow_ai_special_win"], 1)

        match vc:
            case VictoryType.ACQUIRE_ARTIFACT:
                io.write_int(info["objective_value_one"], 2)
            case VictoryType.ACCUMULATE_CREATURES:
                io.write_int(info["objective_value_one"], 2)
                io.write_int(info["objective_value_two"], 4)
            case VictoryType.ACCUMULATE_RESOURCES:
                io.write_int(info["objective_value_one"], 1)
                io.write_int(info["objective_value_two"], 4)
            case VictoryType.UPGRADE_TOWN:
                io.write_int(info["objective_coords"][0], 1)
                io.write_int(info["objective_coords"][1], 1)
                io.write_int(info["objective_coords"][2], 1)
                io.write_int(info["objective_value_one"], 1)
                io.write_int(info["objective_value_two"], 1)
            case (VictoryType.BUILD_THE_GRAIL | VictoryType.DEFEAT_HERO |
                  VictoryType.CAPTURE_TOWN    | VictoryType.DEFEAT_MONSTER):
                io.write_int(info["objective_coords"][0], 1)
                io.write_int(info["objective_coords"][1], 1)
                io.write_int(info["objective_coords"][2], 1)
            case VictoryType.TRANSPORT_ARTIFACT:
                io.write_int(info["objective_value_one"], 1)
                io.write_int(info["objective_coords"][0], 1)
                io.write_int(info["objective_coords"][1], 1)
                io.write_int(info["objective_coords"][2], 1)
            case VictoryType.SURVIVE:
                io.write_int(info["objective_value_one"], 4)
        
    lc = info["loss_condition"]
    io.write_int(lc, 1)
    
    if lc == LossType.TIME_EXPIRES:
        io.write_int(info["loss_timer"], 2)
    elif lc != LossType.NONE:
        io.write_int(info["loss_coords"][0], 1)
        io.write_int(info["loss_coords"][1], 1)
        io.write_int(info["loss_coords"][2], 1)
