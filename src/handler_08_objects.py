#!/usr/bin/env python3

import src.file_io    as io
import data.artifacts as ad  # Artifact details
import data.creatures as cd  # Creature details
import data.heroes    as hd  # Hero details
import data.objects   as od  # Object details
import data.skills    as skd # Skill details
import data.spells    as spd # Spell details

from src.handler_06_rumors_and_events import parse_events, write_events

from enum import IntEnum

# The object definitions of a map are stored as follows:
#
# TODO

# The object data of a map is stored as follows:
#
# TODO

def parse_object_defs() -> list:
    info = []

    for _ in range(io.read_int(4)): # Amount of objects
        obj = {}
        obj["sprite"] = io.read_str(io.read_int(4))
        obj["red_squares"]        = io.read_bits(6)
        obj["yellow_squares"]     = io.read_bits(6)
        obj["placeable_terrain"]  = io.read_bits(2)
        obj["editor_section"]     = io.read_bits(2)

        obj["type"]    = od.ID(io.read_int(4))
        obj["subtype"] = get_subtype(obj["type"], io.read_int(4))

        obj["editor_group"] =      io.read_int(1)
        obj["below_ground"] = bool(io.read_int(1))
        obj["null_bytes"]   =      io.read_raw(16)
        info.append(obj)

    return info

def write_object_defs(info: list) -> None:
    io.write_int(len(info), 4)

    for obj in info:
        io.write_int(len(obj["sprite"]), 4)
        io.write_str(    obj["sprite"])
        io.write_bits(   obj["red_squares"])
        io.write_bits(   obj["yellow_squares"])
        io.write_bits(   obj["placeable_terrain"])
        io.write_bits(   obj["editor_section"])
        io.write_int(    obj["type"], 4)
        io.write_int(    obj["subtype"], 4)
        io.write_int(    obj["editor_group"], 1)
        io.write_int(    obj["below_ground"], 1)
        io.write_raw(    obj["null_bytes"])

def get_subtype(obj_type: int, i: int) -> int:
    match obj_type:
        case od.ID.Artifact:                  return ad.ID(i)
        case od.ID.Border_Guard:              return od.Border_Color(i)
        case od.ID.Keymasters_Tent:           return od.Border_Color(i)
        case od.ID.Cartographer:              return od.Cartographer(i)
        case od.ID.Creature_Bank:             return od.Creature_Bank(i)
        case od.ID.Creature_Generator_1:      return od.Dwelling(i)
        case od.ID.Creature_Generator_4:      return od.Dwelling_Multi(i)
        case od.ID.Hero:                      return hd.Classes(i)
        case od.ID.Hill_Fort:                 return od.Hill_Fort(i)
        case od.ID.Monolith_One_Way_Entrance: return od.One_Way_Monolith(i)
        case od.ID.Monolith_One_Way_Exit:     return od.One_Way_Monolith(i)
        case od.ID.Two_Way_Monolith:          return od.Two_Way_Monolith(i)
        case od.ID.Mine:                      return od.Resource(i)
        case od.ID.Monster:                   return cd.ID(i)
        case od.ID.Resource:                  return od.Resource(i)
        case od.ID.Town:                      return od.Town(i)
        case od.ID.HotA_Decoration_1:         return od.HotA_Decoration_1(i)
        case od.ID.HotA_Decoration_2:         return od.HotA_Decoration_2(i)
        case od.ID.HotA_Ground:               return od.HotA_Ground(i)
        case od.ID.HotA_Warehouse:            return od.Resource(i)
        case od.ID.HotA_Visitable_1:          return od.HotA_Visitable_1(i)
        case od.ID.HotA_Collectible:          return od.HotA_Collectible(i)
        case od.ID.HotA_Visitable_2:          return od.HotA_Visitable_2(i)
        case od.ID.Border_Gate:               return od.Border_Color(i)
    return i

def parse_object_data(object_defs: list) -> list:
    info = []

    for _ in range(io.read_int(4)): # Amount of objects
        obj = { "coords": [0, 0, 0] }
        obj["coords"][0] = io.read_int(1)
        obj["coords"][1] = io.read_int(1)
        obj["coords"][2] = io.read_int(1)

        obj["def_id"] = io.read_int(4)
        io.seek(5)

        obj["type"]    = object_defs[obj["def_id"]]["type"]
        obj["subtype"] = object_defs[obj["def_id"]]["subtype"]

        match obj["type"]:
            case od.ID.Pandoras_Box:       obj = parse_pandoras_box(obj)
            case od.ID.Black_Market:       obj = parse_black_market(obj)
            case od.ID.Campfire:           obj = parse_campfire(obj)
            case od.ID.Corpse:             obj = parse_corpse(obj)
            case od.ID.Event:              obj = parse_event(obj)
            case od.ID.Flotsam:            obj = parse_flotsam(obj)
            case od.ID.Lean_To:            obj = parse_lean_to(obj)
            case od.ID.Pyramid:            obj = parse_pyramid(obj)
            case od.ID.Scholar:            obj = parse_scholar(obj)
            case od.ID.Sea_Chest:          obj = parse_sea_chest(obj)
            case od.ID.Seers_Hut:          obj = parse_seers_hut(obj)
            case od.ID.Shipwreck_Survivor: obj = parse_shipwreck_survivor(obj)
            case od.ID.Treasure_Chest:     obj = parse_treasure_chest(obj)
            case od.ID.Tree_of_Knowledge:  obj = parse_tree_of_knowledge(obj)
            case od.ID.University:         obj = parse_university(obj)
            case od.ID.Wagon:              obj = parse_wagon(obj)
            case od.ID.Warriors_Tomb:      obj = parse_warriors_tomb(obj)

            case od.ID.Random_Dwelling:         obj = parse_dwelling(obj)
            case od.ID.Random_Dwelling_Leveled: obj = parse_leveled(obj)
            case od.ID.Random_Dwelling_Faction: obj = parse_faction(obj)

            case od.ID.Quest_Guard: obj["quest"]  = parse_quest()
            case od.ID.Grail:       obj["radius"] = io.read_int(4)
            case od.ID.Witch_Hut:   obj["skills"] = io.read_bits(4)

            case od.ID.HotA_Collectible: obj = parse_hota_collectible(obj)
            case od.ID.Abandoned_Mine:   obj = parse_abandoned_mine(obj)

            case od.ID.Mine:
                if obj["subtype"] == od.Resource.Abandoned:
                    obj = parse_abandoned_mine(obj)
                else: obj["owner"] = io.read_int(4)

            case od.ID.HotA_Visitable_2:
                if obj["subtype"] == 0: # HotA Seafaring_Academy
                    obj = parse_university(obj)

            # Some of the HotA objects are implemented in a pretty hacky way.
            case od.ID.Border_Gate:
                if obj["subtype"] == 1000: # HotA Quest Gate
                    obj["quest"] = parse_quest()
                elif obj["subtype"] == 1001: # HotA Grave
                    obj = parse_grave(obj)

            case od.ID.Town:        obj = parse_town(obj)
            case od.ID.Random_Town: obj = parse_town(obj, random=True)

            case (od.ID.Resource | od.ID.Random_Resource):
                obj = parse_resource(obj)

            case (od.ID.Hero | od.ID.Prison | od.ID.Random_Hero):
                obj = parse_hero(obj)

            case (od.ID.Monster          | od.ID.Random_Monster   |
                  od.ID.Random_Monster_1 | od.ID.Random_Monster_2 |
                  od.ID.Random_Monster_3 | od.ID.Random_Monster_4 |
                  od.ID.Random_Monster_5 | od.ID.Random_Monster_6 |
                  od.ID.Random_Monster_7):
                obj = parse_monster(obj)

            case (od.ID.Artifact                 | od.ID.Random_Artifact |
                  od.ID.Random_Treasure_Artifact | od.ID.Random_Minor_Artifact |
                  od.ID.Random_Major_Artifact    | od.ID.Random_Relic):
                obj = parse_artifact(obj)

            case (od.ID.Ocean_Bottle | od.ID.Sign):
                obj["message"] = io.read_str(io.read_int(4))
                io.seek(4)

            case (od.ID.Creature_Generator_1 | od.ID.Lighthouse |
                  od.ID.Creature_Generator_4 | od.ID.Shipyard):
                obj["owner"] = io.read_int(4)

            case (od.ID.Garrison | od.ID.Garrison_Vertical):
                obj = parse_garrison(obj)

            # The level 4 HotA Shrine is just a subtype of the level 1 Shrine.
            case (od.ID.Shrine_of_Magic_Incantation |
                  od.ID.Shrine_of_Magic_Gesture     |
                  od.ID.Shrine_of_Magic_Thought):
                obj["spell"] = spd.ID(io.read_int(4))

            case od.ID.Spell_Scroll:
                obj = parse_spell_scroll(obj)

            case od.ID.Hero_Placeholder:
                obj = parse_hero_placeholder(obj)

            case (od.ID.Creature_Bank | od.ID.Derelict_Ship |
                  od.ID.Dragon_Utopia | od.ID.Crypt | od.ID.Shipwreck):
                obj = parse_bank(obj)

        info.append(obj)

    return info

def write_object_data(info: list) -> None:
    io.write_int(len(info), 4)

    for obj in info:
        io.write_int(obj["coords"][0], 1)
        io.write_int(obj["coords"][1], 1)
        io.write_int(obj["coords"][2], 1)

        io.write_int(obj["def_id"], 4)
        io.write_int(0, 5)

        match obj["type"]:
            case od.ID.Pandoras_Box:       write_pandoras_box(obj)
            case od.ID.Black_Market:       write_black_market(obj)
            case od.ID.Campfire:           write_campfire(obj)
            case od.ID.Corpse:             write_corpse(obj)
            case od.ID.Event:              write_event(obj)
            case od.ID.Flotsam:            write_flotsam(obj)
            case od.ID.Lean_To:            write_lean_to(obj)
            case od.ID.Pyramid:            write_pyramid(obj)
            case od.ID.Scholar:            write_scholar(obj)
            case od.ID.Sea_Chest:          write_sea_chest(obj)
            case od.ID.Seers_Hut:          write_seers_hut(obj)
            case od.ID.Shipwreck_Survivor: write_shipwreck_survivor(obj)
            case od.ID.Treasure_Chest:     write_treasure_chest(obj)
            case od.ID.Tree_of_Knowledge:  write_tree_of_knowledge(obj)
            case od.ID.University:         write_university(obj)
            case od.ID.Wagon:              write_wagon(obj)
            case od.ID.Warriors_Tomb:      write_warriors_tomb(obj)

            case od.ID.Random_Dwelling:         write_dwelling(obj)
            case od.ID.Random_Dwelling_Leveled: write_leveled(obj)
            case od.ID.Random_Dwelling_Faction: write_faction(obj)

            case od.ID.Quest_Guard: write_quest(obj["quest"])
            case od.ID.Grail:       io.write_int(obj["radius"], 4)
            case od.ID.Witch_Hut:   io.write_bits(obj["skills"])

            case od.ID.HotA_Collectible: write_hota_collectible(obj)
            case od.ID.Abandoned_Mine:   write_abandoned_mine(obj)

            case od.ID.Mine:
                if obj["subtype"] == od.Resource.Abandoned:
                    write_abandoned_mine(obj)
                else: io.write_int(obj["owner"], 4)

            case od.ID.HotA_Visitable_2:
                if obj["subtype"] == 0: # HotA Seafaring_Academy
                    write_university(obj)
            case od.ID.Border_Gate:
                if obj["subtype"] == 1000: # HotA Quest Gate
                    write_quest(obj["quest"])
                elif obj["subtype"] == 1001: # HotA Grave
                    write_grave(obj)

            case od.ID.Town:        write_town(obj)
            case od.ID.Random_Town: write_town(obj, random=True)

            case (od.ID.Resource | od.ID.Random_Resource):
                write_resource(obj)

            case (od.ID.Hero | od.ID.Prison | od.ID.Random_Hero):
                write_hero(obj)

            case (od.ID.Monster          | od.ID.Random_Monster   |
                  od.ID.Random_Monster_1 | od.ID.Random_Monster_2 |
                  od.ID.Random_Monster_3 | od.ID.Random_Monster_4 |
                  od.ID.Random_Monster_5 | od.ID.Random_Monster_6 |
                  od.ID.Random_Monster_7):
                write_monster(obj)

            case (od.ID.Artifact                 | od.ID.Random_Artifact |
                  od.ID.Random_Treasure_Artifact | od.ID.Random_Minor_Artifact |
                  od.ID.Random_Major_Artifact    | od.ID.Random_Relic):
                write_artifact(obj)

            case (od.ID.Ocean_Bottle | od.ID.Sign):
                io.write_int(len(obj["message"]), 4)
                io.write_str(    obj["message"])
                io.write_int(0, 4)

            case (od.ID.Creature_Generator_1 | od.ID.Lighthouse |
                  od.ID.Creature_Generator_4 | od.ID.Shipyard):
                io.write_int(obj["owner"], 4)

            case (od.ID.Garrison | od.ID.Garrison_Vertical):
                write_garrison(obj)

            case (od.ID.Shrine_of_Magic_Incantation |
                  od.ID.Shrine_of_Magic_Gesture     |
                  od.ID.Shrine_of_Magic_Thought):
                io.write_int(obj["spell"], 4)

            case od.ID.Spell_Scroll:
                write_spell_scroll(obj)

            case od.ID.Hero_Placeholder:
                write_hero_placeholder(obj)

            case (od.ID.Creature_Bank | od.ID.Derelict_Ship |
                  od.ID.Dragon_Utopia | od.ID.Crypt | od.ID.Shipwreck):
                write_bank(obj)

def parse_hota_collectible(obj: dict) -> dict:
    match obj["subtype"]:
        case od.HotA_Collectible.Ancient_Lamp: obj = parse_ancient_lamp(obj)
        case od.HotA_Collectible.Sea_Barrel:   obj = parse_sea_barrel(obj)
        case od.HotA_Collectible.Jetsam:       obj = parse_flotsam(obj)
        case od.HotA_Collectible.Vial_of_Mana: obj = parse_vial_of_mana(obj)
    return obj

def write_hota_collectible(obj: dict) -> None:
    match obj["subtype"]:
        case od.HotA_Collectible.Ancient_Lamp: write_ancient_lamp(obj)
        case od.HotA_Collectible.Sea_Barrel:   write_sea_barrel(obj)
        case od.HotA_Collectible.Jetsam:       write_flotsam(obj)
        case od.HotA_Collectible.Vial_of_Mana: write_vial_of_mana(obj)

def parse_creatures(amount: int = 7) -> list:
    info = []
    for _ in range(amount):
        creature = {}
        creature["id"] = cd.ID(io.read_int(2))
        creature["amount"]   = io.read_int(2)
        info.append(creature)
    return info

def write_creatures(info: list) -> None:
    for guard in info:
        io.write_int(guard["id"], 2)
        io.write_int(guard["amount"], 2)

def parse_common(obj: dict) -> dict:
    message_length = io.read_int(4)

    if message_length > 0:
        obj["message"] = io.read_str(message_length)
    if io.read_int(1):
        obj["guards"] = parse_creatures()

    io.seek(4)
    return obj

def write_common(obj: dict) -> None:
    io.write_int(1, 1)

    if "message" in obj:
        io.write_int(len(obj["message"]), 4)
        io.write_str(    obj["message"])
    else: io.write_int(0, 4)

    if "guards" in obj:
        io.write_int(1, 1)
        write_creatures(obj["guards"])
    else: io.write_int(0, 1)

    io.write_int(0, 4)

class Movement(IntEnum):
    Give      = 0
    Take      = 1
    Nullify   = 2
    Set       = 3
    Replenish = 4

def parse_contents() -> dict:
    contents = {
        "Experience"      : 0,
        "Spell_Points"    : 0,
        "Morale"          : 0,
        "Luck"            : 0,
        "Resources"       : [],
        "Primary_Skills"  : [],
        "Secondary_Skills": [],
        "Artifacts"       : [],
        "Spells"          : [],
        "Creatures"       : []
    }

    contents["Experience"]   = io.read_int(4)
    contents["Spell_Points"] = io.read_int(4)
    contents["Morale"]       = io.read_int(1)
    contents["Luck"]         = io.read_int(1)

    for _ in range(7):
        contents["Resources"].append(io.read_int(4))

    for _ in range(4):
        contents["Primary_Skills"].append(io.read_int(1))

    for _ in range(io.read_int(1)):
        skill = {}
        skill["id"] = io.read_int(1)
        skill["level"] = io.read_int(1)
        contents["Secondary_Skills"].append(skill)

    for _ in range(io.read_int(1)):
        contents["Artifacts"].append(parse_hero_artifact())

    for _ in range(io.read_int(1)):
        contents["Spells"].append(spd.ID(io.read_int(1)))

    for _ in range(io.read_int(1)):
        creature = {}
        creature["id"] = cd.ID(io.read_int(2))
        creature["amount"]   = io.read_int(2)
        contents["Creatures"].append(creature)

    io.seek(8)
    return contents

def write_contents(contents: dict) -> None:
    io.write_int(contents["Experience"], 4)
    io.write_int(contents["Spell_Points"], 4)
    io.write_int(contents["Morale"], 1)
    io.write_int(contents["Luck"], 1)

    for value in contents["Resources"]:
        io.write_int(value, 4)

    for value in contents["Primary_Skills"]:
        io.write_int(value, 1)

    io.write_int(len(contents["Secondary_Skills"]), 1)
    for skill in contents["Secondary_Skills"]:
        io.write_int(skill["id"], 1)
        io.write_int(skill["level"], 1)

    io.write_int(len(contents["Artifacts"]), 1)
    for value in contents["Artifacts"]:
        write_hero_artifact(value)

    io.write_int(len(contents["Spells"]), 1)
    for value in contents["Spells"]:
        io.write_int(value, 1)

    io.write_int(len(contents["Creatures"]), 1)
    for creature in contents["Creatures"]:
        io.write_int(creature["id"], 2)
        io.write_int(creature["amount"], 2)

    io.write_int(0, 8)

class Pickup_Condition(IntEnum):
    Disabled   = 0
    Random     = 1
    Customized = 2

def parse_artifact(obj: dict) -> dict:
    if io.read_int(1):
        obj = parse_common(obj)

    obj["pickup_mode"] = Pickup_Condition(io.read_int(4))
    obj["pickup_conditions"] = io.read_bits(1)
    return obj

def write_artifact(obj: dict) -> None:
    if len(obj) > 2:
        write_common(obj)
    else: io.write_int(0, 1)

    io.write_int(obj["pickup_mode"], 4)
    io.write_bits(obj["pickup_conditions"])

def parse_pandoras_box(obj: dict) -> dict:
    if io.read_int(1):
        obj = parse_common(obj)
    obj["contents"] = parse_contents()

    # HotA 1.7.0 Movement Points.
    io.seek(1) # TODO - Is this something?
    obj["contents"]["Movement_Mode"] = Movement(io.read_int(4))
    obj["contents"]["Movement_Points"] = io.read_int(4)
    # HotA 1.7.1 Difficulty
    obj["difficulty"] = io.read_bits(4)
    return obj

def write_pandoras_box(obj: dict) -> None:
    if len(obj) > 3:
        write_common(obj)
    else: io.write_int(0, 1)

    write_contents(obj["contents"])

    io.write_int(0, 1)
    io.write_int(obj["contents"]["Movement_Mode"], 4)
    io.write_int(obj["contents"]["Movement_Points"], 4)
    io.write_bits(obj["difficulty"])

def parse_black_market(obj: dict) -> dict:
    obj["artifacts"] = []
    for _ in range(7):
        obj["artifacts"].append(parse_hero_artifact())
    return obj

def write_black_market(obj: dict) -> None:
    for artifact in obj["artifacts"]:
        write_hero_artifact(artifact)

def parse_campfire(obj: dict) -> dict:
    obj["null_bytes"] = io.read_raw(8)
    obj["resources"] = {}

    for _ in range(2):
        amount = io.read_int(4)
        obj["resources"][od.Resource(io.read_int(1))] = amount

    return obj

def write_campfire(obj: dict) -> None:
    io.write_raw(obj["null_bytes"])
    for k in obj["resources"].keys():
        io.write_int(obj["resources"][k], 4)
        io.write_int(k, 1)

def parse_bank(obj: dict) -> dict:
    obj["difficulty"]     = io.read_int(4)
    obj["upgraded_stack"] = io.read_int(1)
    obj["rewards"]        = []

    for _ in range(io.read_int(4)):
        obj["rewards"].append(ad.ID(io.read_int(4)))

    return obj

def write_bank(obj: dict) -> None:
    io.write_int(obj["difficulty"], 4)
    io.write_int(obj["upgraded_stack"], 1)

    io.write_int(len(obj["rewards"]), 4)
    for reward in obj["rewards"]:
        io.write_int(reward, 4)

class Corpse(IntEnum):
    Random   = 4294967295 # 4 Bytes of 255
    Nothing  = 0
    Artifact = 1

def parse_corpse(obj: dict) -> dict:
    obj["contents"] = Corpse(io.read_int(4))
    obj["value"]    =  ad.ID(io.read_int(4))
    return obj

def write_corpse(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_int(obj["value"], 4)

def parse_event(obj: dict) -> dict:
    if io.read_int(1):
        obj = parse_common(obj)
    obj["contents"] = parse_contents()

    obj["allowed_players"] =      io.read_bits(1)
    obj["allow_ai"]        = bool(io.read_int(1))
    obj["cancel_event"]    = bool(io.read_int(1))
    io.seek(4)
    obj["allow_human"]     = bool(io.read_int(1))

    # HotA 1.7.0 Movement Points.
    obj["contents"]["Movement_Mode"] = Movement(io.read_int(4))
    obj["contents"]["Movement_Points"] = io.read_int(4)
    # HotA 1.7.1 Difficulty Settings
    obj["difficulty"] = io.read_bits(4)

    return obj

def write_event(obj: dict) -> None:
    if len(obj) > 7:
        write_common(obj)
    else: io.write_int(0, 1)

    write_contents(obj["contents"])

    io.write_bits(obj["allowed_players"])
    io.write_int( obj["allow_ai"], 1)
    io.write_int( obj["cancel_event"], 5)
    io.write_int( obj["allow_human"], 1)

    io.write_int(obj["contents"]["Movement_Mode"], 4)
    io.write_int(obj["contents"]["Movement_Points"], 4)

    io.write_bits(obj["difficulty"])

def parse_flotsam(obj: dict) -> dict:
    obj["contents"] = io.read_int(4)
    obj["trash_bytes"] = io.read_int(4)
    return obj

def write_flotsam(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_int(obj["trash_bytes"], 4)

def parse_garrison(obj: dict) -> dict:
    obj["owner"]  = io.read_int(4)
    obj["guards"] = parse_creatures()
    obj["troops_removable"] = io.read_int(1)

    io.seek(8)
    return obj

def write_garrison(obj: dict) -> None:
    io.write_int(obj["owner"], 4)
    write_creatures(obj["guards"])
    io.write_int(obj["troops_removable"], 9)

def parse_hero(obj: dict) -> dict:
    # This method is pretty similar to parse_hero_data() in the heroes handler,
    # but it has some additional bytes to read all over. Maybe combine them
    # into a single method some day.

    obj["start_bytes"] = io.read_raw(4)
    obj["owner"]       = io.read_int(1)

    hero = {
        "id"                : 255,
        "name"              : "",
        "experience"        : -1,
        "portrait"          : 255,
        "secondary_skills"  : [],
        "creatures"         : [],
        "formation"         : 0,
        "artifacts_equipped": {},
        "artifacts_backpack": [],
        "patrol"            : 255,
        "biography"         : "",
        "gender"            : 255,
        "spells"            : b'',
        "primary_skills"    : {},
        "always_add_skills" : True,
        "cannot_gain_xp"    : False,
        "level"             : 1
    }

    hero["id"] = hd.ID(io.read_int(1))

    if io.read_int(1): # Is the name set?
        hero["name"] = io.read_str(io.read_int(4))

    if io.read_int(1): # Is experience set?
        hero["experience"] = io.read_int(4)

    if io.read_int(1): # Is portrait set?
        hero["portrait"] = io.read_int(1)

    if io.read_int(1): # Are secondary skills set?
        for _ in range(io.read_int(4)):
            skill = {}
            skill["id"]    = io.read_int(1)
            skill["level"] = io.read_int(1)
            hero["secondary_skills"].append(skill)

    if io.read_int(1): # Is the army set?
        hero["creatures"] = parse_creatures()

    hero["formation"] = io.read_int(1)

    if io.read_int(1): # Are artifacts set?
        hero["artifacts_equipped"]["head"]          = parse_hero_artifact()
        hero["artifacts_equipped"]["shoulders"]     = parse_hero_artifact()
        hero["artifacts_equipped"]["neck"]          = parse_hero_artifact()
        hero["artifacts_equipped"]["right_hand"]    = parse_hero_artifact()
        hero["artifacts_equipped"]["left_hand"]     = parse_hero_artifact()
        hero["artifacts_equipped"]["torso"]         = parse_hero_artifact()
        hero["artifacts_equipped"]["right_ring"]    = parse_hero_artifact()
        hero["artifacts_equipped"]["left_ring"]     = parse_hero_artifact()
        hero["artifacts_equipped"]["feet"]          = parse_hero_artifact()
        hero["artifacts_equipped"]["misc_1"]        = parse_hero_artifact()
        hero["artifacts_equipped"]["misc_2"]        = parse_hero_artifact()
        hero["artifacts_equipped"]["misc_3"]        = parse_hero_artifact()
        hero["artifacts_equipped"]["misc_4"]        = parse_hero_artifact()
        hero["artifacts_equipped"]["war_machine_1"] = parse_hero_artifact()
        hero["artifacts_equipped"]["war_machine_2"] = parse_hero_artifact()
        hero["artifacts_equipped"]["war_machine_3"] = parse_hero_artifact()
        hero["artifacts_equipped"]["war_machine_4"] = parse_hero_artifact()
        hero["artifacts_equipped"]["spellbook"]     = parse_hero_artifact()
        hero["artifacts_equipped"]["misc_5"]        = parse_hero_artifact()
        
        for _ in range(io.read_int(2)):
            hero["artifacts_backpack"].append(parse_hero_artifact())

    hero["patrol"] = io.read_int(1)

    if io.read_int(1): # Is biography set?
        hero["biography"] = io.read_str(io.read_int(4))

    hero["gender"] = io.read_int(1)

    if io.read_int(1): # Are spells set?
        hero["spells"] = io.read_bits(9)

    if io.read_int(1): # Are primary skills set?
        hero["primary_skills"]["attack"]      = io.read_int(1)
        hero["primary_skills"]["defense"]     = io.read_int(1)
        hero["primary_skills"]["spell_power"] = io.read_int(1)
        hero["primary_skills"]["knowledge"]   = io.read_int(1)

    obj["end_bytes"] = io.read_raw(16)

    hero["always_add_skills"] = bool(io.read_int(1))
    hero["cannot_gain_xp"]    = bool(io.read_int(1))
    hero["level"]             =      io.read_int(4)

    obj["hero_data"] = hero
    return obj

def write_hero(obj: dict) -> None:
    io.write_raw(obj["start_bytes"])
    io.write_int(obj["owner"], 1)

    hero = obj["hero_data"]

    #
    io.write_int(hero["id"], 1)

    #
    if hero["name"]:
        io.write_int(1, 1)
        io.write_int(len(hero["name"]), 4)
        io.write_str(hero["name"])
    else: io.write_int(0, 1)

    #
    if hero["experience"] >= 0:
        io.write_int(1, 1)
        io.write_int(hero["experience"], 4)
    else: io.write_int(0, 1)

    #
    if hero["portrait"] != 255:
        io.write_int(1, 1)
        io.write_int(hero["portrait"], 1)
    else: io.write_int(0, 1)

    #
    if hero["secondary_skills"]:
        io.write_int(1, 1)
        io.write_int(len(hero["secondary_skills"]), 4)

        for skill in hero["secondary_skills"]:
            io.write_int(skill["id"], 1)
            io.write_int(skill["level"], 1)
    else: io.write_int(0, 1)

    #
    if hero["creatures"]:
        io.write_int(1, 1)
        write_creatures(hero["creatures"])
    else: io.write_int(0, 1)

    #
    io.write_int(hero["formation"], 1)

    #
    if hero["artifacts_equipped"] or hero["artifacts_backpack"]:
        io.write_int(1, 1)

        write_hero_artifact(hero["artifacts_equipped"]["head"])
        write_hero_artifact(hero["artifacts_equipped"]["shoulders"])
        write_hero_artifact(hero["artifacts_equipped"]["neck"])
        write_hero_artifact(hero["artifacts_equipped"]["right_hand"])
        write_hero_artifact(hero["artifacts_equipped"]["left_hand"])
        write_hero_artifact(hero["artifacts_equipped"]["torso"])
        write_hero_artifact(hero["artifacts_equipped"]["right_ring"])
        write_hero_artifact(hero["artifacts_equipped"]["left_ring"])
        write_hero_artifact(hero["artifacts_equipped"]["feet"])
        write_hero_artifact(hero["artifacts_equipped"]["misc_1"])
        write_hero_artifact(hero["artifacts_equipped"]["misc_2"])
        write_hero_artifact(hero["artifacts_equipped"]["misc_3"])
        write_hero_artifact(hero["artifacts_equipped"]["misc_4"])
        write_hero_artifact(hero["artifacts_equipped"]["war_machine_1"])
        write_hero_artifact(hero["artifacts_equipped"]["war_machine_2"])
        write_hero_artifact(hero["artifacts_equipped"]["war_machine_3"])
        write_hero_artifact(hero["artifacts_equipped"]["war_machine_4"])
        write_hero_artifact(hero["artifacts_equipped"]["spellbook"])
        write_hero_artifact(hero["artifacts_equipped"]["misc_5"])
        
        io.write_int(len(hero["artifacts_backpack"]), 2)
        for artifact in hero["artifacts_backpack"]:
            write_hero_artifact(artifact)
    else: io.write_int(0, 1)

    #
    io.write_int(hero["patrol"], 1)

    #
    if hero["biography"]:
        io.write_int(1, 1)
        io.write_int(len(hero["biography"]), 4)
        io.write_str(hero["biography"])
    else: io.write_int(0, 1)

    #
    io.write_int(hero["gender"], 1)

    #
    if hero["spells"] != b'':
        io.write_int(1, 1)
        io.write_bits(hero["spells"])
    else: io.write_int(0, 1)

    #
    if hero["primary_skills"]:
        io.write_int(1, 1)
        io.write_int(hero["primary_skills"]["attack"], 1)
        io.write_int(hero["primary_skills"]["defense"], 1)
        io.write_int(hero["primary_skills"]["spell_power"], 1)
        io.write_int(hero["primary_skills"]["knowledge"], 1)
    else: io.write_int(0, 1)

    #
    io.write_raw(obj["end_bytes"])

    #
    io.write_int(hero["always_add_skills"], 1)
    io.write_int(hero["cannot_gain_xp"], 1)
    io.write_int(hero["level"], 4)

def parse_hero_artifact() -> list:
    artifact = [
        ad.ID(io.read_int(2)),
        io.read_int(2)
    ]
    if artifact[0] == ad.ID.Spell_Scroll:
        artifact[1] = spd.ID(artifact[1])
    return artifact

def write_hero_artifact(artifact: list) -> None:
    io.write_int(artifact[0], 2)
    io.write_int(artifact[1], 2)

def parse_hero_placeholder(obj: dict) -> dict:
    obj["owner"]   =       io.read_int(1)
    obj["hero_id"] = hd.ID(io.read_int(1))

    if obj["hero_id"] == hd.ID.Default:
        obj["power_rating"] = io.read_int(1)

    return obj

def write_hero_placeholder(obj: dict) -> None:
    io.write_int(obj["owner"], 1)
    io.write_int(obj["hero_id"], 1)

    if obj["hero_id"] == hd.ID.Default:
        io.write_int(obj["power_rating"], 1)

def parse_lean_to(obj: dict) -> dict:
    obj["contents"]    =          io.read_int(4)
    obj["trash_bytes"] =          io.read_int(4)
    obj["amount"]      =          io.read_int(4)
    obj["resource"] = od.Resource(io.read_int(1))
    io.seek(5)
    return obj

def write_lean_to(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_int(obj["trash_bytes"], 4)
    io.write_int(obj["amount"], 4)
    io.write_int(obj["resource"], 1)
    io.write_int(1, 5)

class Disposition(IntEnum):
    Compliant  = 0
    Friendly   = 1
    Aggressive = 2
    Hostile    = 3
    Savage     = 4
    Precise    = 5

def parse_monster(obj: dict) -> dict:
    obj["start_bytes"] = io.read_raw(4)
    obj["quantity"]    = io.read_int(2)
    obj["disposition"] = Disposition(io.read_int(1))

    if io.read_int(1):
        obj["message"] = io.read_str(io.read_int(4))
        obj["resources"] = []
        for _ in range(7):
            obj["resources"].append(io.read_int(4))
        obj["artifact"] = ad.ID(io.read_int(2))

    obj["monster_never_flees"]     = bool(io.read_int(1))
    obj["quantity_does_not_grow"]  = bool(io.read_int(1))
    obj["middle_bytes"]            =      io.read_raw(2)
    obj["precise_disposition"]     =      io.read_int(4)
    obj["join_only_for_money"]     = bool(io.read_int(1))
    obj["joining_monster_percent"] =      io.read_int(4)
    obj["upgraded_stack"]          =      io.read_int(4)
    obj["stack_count"]             =      io.read_int(4)
    obj["is_value"]                = bool(io.read_int(1))
    obj["ai_value"]                =      io.read_int(4)

    return obj

def write_monster(obj: dict) -> None:
    io.write_raw(obj["start_bytes"])
    io.write_int(obj["quantity"], 2)
    io.write_int(obj["disposition"], 1)

    if "message" in obj:
        io.write_int(1, 1)
        io.write_int(len(obj["message"]), 4)
        io.write_str(    obj["message"])
        for res in obj["resources"]:
            io.write_int(res, 4)
        io.write_int(obj["artifact"], 2)
    else: io.write_int(0, 1)

    io.write_int(obj["monster_never_flees"], 1)
    io.write_int(obj["quantity_does_not_grow"], 1)
    io.write_raw(obj["middle_bytes"])
    io.write_int(obj["precise_disposition"], 4)
    io.write_int(obj["join_only_for_money"], 1)
    io.write_int(obj["joining_monster_percent"], 4)
    io.write_int(obj["upgraded_stack"], 4)
    io.write_int(obj["stack_count"], 4)
    io.write_int(obj["is_value"], 1)
    io.write_int(obj["ai_value"], 4)

def parse_pyramid(obj: dict) -> dict:
    obj["contents"] = io.read_int(4)
    obj["spell"] = spd.ID(io.read_int(4))
    return obj

def write_pyramid(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_int(obj["spell"], 4)

def parse_town(obj: dict, random: bool = False) -> dict:
    obj["start_bytes"] = io.read_raw(4)
    obj["owner"]       = io.read_int(1)

    if io.read_int(1): # Is the name set?
        obj["name"] = io.read_str(io.read_int(4))

    if io.read_int(1): # Is the garrison customized?
        obj["garrison_guards"] = parse_creatures()

    obj["garrison_formation"] = io.read_int(1)

    if io.read_int(1): # Are the buildings customized?
        obj["buildings_built"]    =      io.read_bits(6)
        obj["buildings_disabled"] =      io.read_bits(6)
    else: obj["has_fort"]         = bool(io.read_int(1))

    obj["spells_must_appear"]  =      io.read_bits(9)
    obj["spells_cant_appear"]  =      io.read_bits(9)
    obj["spell_research"]      = bool(io.read_int(1))

    obj["buildings_special"] = []
    for _ in range(io.read_int(4)): # Amount of special buildings.
        obj["buildings_special"].append(io.read_int(1))

    obj["events"]    = parse_events(is_town=True)
    obj["alignment"] = io.read_int(1)

    io.seek(3)
    return obj

def write_town(obj: dict, random: bool = False) -> None:
    io.write_raw(obj["start_bytes"])
    io.write_int(obj["owner"], 1)

    if "name" in obj:
        io.write_int(1, 1)
        io.write_int(len(obj["name"]), 4)
        io.write_str(    obj["name"])
    else: io.write_int(0, 1)

    if "garrison_guards" in obj:
        io.write_int(1, 1)
        write_creatures(obj["garrison_guards"])
    else: io.write_int(0, 1)

    io.write_int(obj["garrison_formation"], 1)

    if "buildings_built" in obj:
        io.write_int(1, 1)
        io.write_bits(obj["buildings_built"])
        io.write_bits(obj["buildings_disabled"])
    else:
        io.write_int(0, 1)
        io.write_int(obj["has_fort"], 1)

    io.write_bits(obj["spells_must_appear"])
    io.write_bits(obj["spells_cant_appear"])
    io.write_int( obj["spell_research"], 1)

    io.write_int(len(obj["buildings_special"]), 4)
    for i in obj["buildings_special"]:
        io.write_int(i, 1)

    write_events(obj["events"], is_town=True)

    io.write_int(obj["alignment"], 1)
    io.write_int(0, 3)

def parse_resource(obj: dict) -> dict:
    if io.read_int(1):
        obj = parse_common(obj)

    obj["amount"] = io.read_int(4)
    io.seek(4)
    return obj

def write_resource(obj: dict) -> None:
    if len(obj) > 3:
        write_common(obj)
    else: io.write_int(0, 1)

    io.write_int(obj["amount"], 4)
    io.write_int(0, 4)

def parse_scholar(obj: dict) -> dict:
    obj["reward_type"] = io.read_int(1)
    
    match obj["reward_type"]:
        case 255: io.seek(1) # Random
        case 0:   obj["reward_value"] = skd.Primary(io.read_int(1))
        case 1:   obj["reward_value"] = skd.Secondary(io.read_int(1))
        case 2:   obj["reward_value"] = spd.ID(io.read_int(1))

    io.seek(6)
    return obj

def write_scholar(obj: dict) -> None:
    io.write_int(obj["reward_type"], 1)

    if "reward_value" in obj:
        io.write_int(obj["reward_value"], 1)
    else: io.write_int(0, 1)

    io.write_int(0, 6)

def parse_sea_chest(obj: dict) -> dict:
    obj["contents"] =       io.read_int(4)
    obj["artifact"] = ad.ID(io.read_int(4))
    return obj

def write_sea_chest(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_int(obj["artifact"], 4)

class Quest(IntEnum):
    NONE                        =  0
    ACHIEVE_EXPERIENCE_LEVEL    =  1
    ACHIEVE_PRIMARY_SKILL_LEVEL =  2
    DEFEAT_SPECIFIC_HERO        =  3
    DEFEAT_SPECIFIC_MONSTER     =  4
    RETURN_WITH_ARTIFACTS       =  5
    RETURN_WITH_CREATURES       =  6
    RETURN_WITH_RESOURCES       =  7
    BE_SPECIFIC_HERO            =  8
    BELONG_TO_SPECIFIC_PLAYER   =  9
    HOTA_QUEST                  = 10

class HotA_Q(IntEnum):
    BELONG_TO_SPECIFIC_CLASS = 0
    RETURN_NOT_BEFORE_DATE   = 1

def parse_quest() -> dict:
    quest = {
        "type"              : Quest.NONE,
        "value"             : 0,
        "deadline"          : 4294967295, # 4 bytes of 255
        "proposal_message"  : "",
        "progress_message"  : "",
        "completion_message": ""
    }

    quest["type"] = Quest(io.read_int(1))

    match quest["type"]:
        case Quest.NONE:
            return quest

        case Quest.ACHIEVE_EXPERIENCE_LEVEL:
            quest["value"] = io.read_int(4)

        case Quest.ACHIEVE_PRIMARY_SKILL_LEVEL:
            skills = []
            skills.append(io.read_int(1))
            skills.append(io.read_int(1))
            skills.append(io.read_int(1))
            skills.append(io.read_int(1))
            quest["value"] = skills

        case (Quest.DEFEAT_SPECIFIC_HERO | Quest.DEFEAT_SPECIFIC_MONSTER):
            # In parse_hero() and parse_monster(), these are the "start_bytes".
            # So it is most likely some identifier for the specific object.
            quest["value"] = io.read_raw(4)

        case Quest.RETURN_WITH_ARTIFACTS:
            quest["value"] = []
            for _ in range(io.read_int(1)):
                quest["value"].append([
                    ad.ID(io.read_int(2)),
                    spd.ID(io.read_int(2))
                ])

        case Quest.RETURN_WITH_CREATURES:
            quest["value"] = parse_creatures(amount=io.read_int(1))

        case Quest.RETURN_WITH_RESOURCES:
            quest["value"] = []
            for _ in range(7):
                quest["value"].append(io.read_int(4))

        case Quest.BE_SPECIFIC_HERO:
            quest["value"] = hd.ID(io.read_int(1))

        case Quest.BELONG_TO_SPECIFIC_PLAYER:
            quest["value"] = io.read_int(1)

        case Quest.HOTA_QUEST:
            quest["hota_type"] = HotA_Q(io.read_int(4))

            if quest["hota_type"] == HotA_Q.BELONG_TO_SPECIFIC_CLASS:
                quest["hota_extra"] = io.read_int(4)
                quest["value"] = io.read_bits(3)

            elif quest["hota_type"] == HotA_Q.RETURN_NOT_BEFORE_DATE:
                quest["value"] = io.read_int(4)

    quest["deadline"]           = io.read_int(4)
    quest["proposal_message"]   = io.read_str(io.read_int(4))
    quest["progress_message"]   = io.read_str(io.read_int(4))
    quest["completion_message"] = io.read_str(io.read_int(4))

    return quest

def write_quest(info: dict) -> None:
    io.write_int(info["type"], 1)

    match info["type"]:
        case Quest.NONE:
            return

        case Quest.ACHIEVE_EXPERIENCE_LEVEL:
            io.write_int(info["value"], 4)

        case Quest.ACHIEVE_PRIMARY_SKILL_LEVEL:
            for skill in info["value"]:
                io.write_int(skill, 1)

        case (Quest.DEFEAT_SPECIFIC_HERO | Quest.DEFEAT_SPECIFIC_MONSTER):
            io.write_raw(info["value"])

        case Quest.RETURN_WITH_ARTIFACTS:
            io.write_int(len(info["value"]), 1)
            for artifact in info["value"]:
                io.write_int(artifact[0], 2)
                io.write_int(artifact[1], 2)

        case Quest.RETURN_WITH_CREATURES:
            io.write_int(len(info["value"]), 1)
            write_creatures(info["value"])

        case Quest.RETURN_WITH_RESOURCES:
            for resource in info["value"]:
                io.write_int(resource, 4)

        case (Quest.BE_SPECIFIC_HERO | Quest.BELONG_TO_SPECIFIC_PLAYER):
            io.write_int(info["value"], 1)

        case Quest.HOTA_QUEST:
            io.write_int(info["hota_type"], 4)

            if info["hota_type"] == HotA_Q.BELONG_TO_SPECIFIC_CLASS:
                io.write_int(info["hota_extra"], 4)
                io.write_bits(info["value"])

            elif info["hota_type"] == HotA_Q.RETURN_NOT_BEFORE_DATE:
                io.write_int(info["value"], 4)

    io.write_int(    info["deadline"], 4)
    io.write_int(len(info["proposal_message"]), 4)
    io.write_str(    info["proposal_message"])
    io.write_int(len(info["progress_message"]), 4)
    io.write_str(    info["progress_message"])
    io.write_int(len(info["completion_message"]), 4)
    io.write_str(    info["completion_message"])

class Reward(IntEnum):
    NONE            =  0
    EXPERIENCE      =  1
    SPELL_POINTS    =  2
    MORALE          =  3
    LUCK            =  4
    RESOURCE        =  5
    PRIMARY_SKILL   =  6
    SECONDARY_SKILL =  7
    ARTIFACT        =  8
    SPELL           =  9
    CREATURES       = 10

def parse_reward() -> dict:
    reward = { "type": Reward(io.read_int(1)) }

    match reward["type"]:
        case (Reward.EXPERIENCE | Reward.SPELL_POINTS):
            reward["value"] = io.read_int(4)

        case (Reward.MORALE | Reward.LUCK):
            reward["value"] = io.read_int(1)

        case Reward.RESOURCE:
            reward["value"] = []
            reward["value"].append(od.Resource(io.read_int(1)))
            reward["value"].append(io.read_int(4))

        case Reward.PRIMARY_SKILL:
            reward["value"] = []
            reward["value"].append(skd.Primary(io.read_int(1)))
            reward["value"].append(io.read_int(1))

        case Reward.SECONDARY_SKILL:
            reward["value"] = []
            reward["value"].append(skd.Secondary(io.read_int(1)))
            reward["value"].append(io.read_int(1))

        case Reward.ARTIFACT:
            reward["value"] = [
                ad.ID(io.read_int(2)),
                spd.ID(io.read_int(2))
            ]

        case Reward.SPELL:
            reward["value"] = spd.ID(io.read_int(1))

        case Reward.CREATURES:
            reward["value"] = parse_creatures(amount=1)

    return reward

def write_reward(info: dict) -> None:
    io.write_int(info["type"], 1)

    match info["type"]:
        case (Reward.EXPERIENCE | Reward.SPELL_POINTS):
            io.write_int(info["value"], 4)

        case (Reward.MORALE | Reward.LUCK | Reward.SPELL):
            io.write_int(info["value"], 1)

        case Reward.RESOURCE:
            io.write_int(info["value"][0], 1)
            io.write_int(info["value"][1], 4)

        case (Reward.PRIMARY_SKILL | Reward.SECONDARY_SKILL):
            io.write_int(info["value"][0], 1)
            io.write_int(info["value"][1], 1)

        case Reward.ARTIFACT:
            io.write_int(info["value"][0], 2)
            io.write_int(info["value"][1], 2)

        case Reward.CREATURES:
            write_creatures(info["value"])

def parse_seers_hut(obj: dict) -> dict:
    obj["one_time_quests"]   = []
    obj["repeatable_quests"] = []

    for _ in range(io.read_int(4)): # Amount of one-time quests
        obj["one_time_quests"].append([parse_quest(), parse_reward()])

    for _ in range(io.read_int(4)): # Amount of repeatable quests
        obj["repeatable_quests"].append([parse_quest(), parse_reward()])

    io.seek(2)
    return obj

def write_seers_hut(obj: dict) -> None:
    io.write_int(len(obj["one_time_quests"]), 4)
    for quest in obj["one_time_quests"]:
        write_quest(quest[0])
        write_reward(quest[1])

    io.write_int(len(obj["repeatable_quests"]), 4)
    for quest in obj["repeatable_quests"]:
        write_quest(quest[0])
        write_reward(quest[1])

    io.write_int(0, 2)

def parse_shipwreck_survivor(obj: dict) -> dict:
    obj["contents"] =       io.read_int(4)
    obj["artifact"] = ad.ID(io.read_int(4))
    return obj

def write_shipwreck_survivor(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_int(obj["artifact"], 4)

def parse_spell_scroll(obj: dict) -> dict:
    if io.read_int(1):
        obj = parse_common(obj)
    obj["spell"] = spd.ID(io.read_int(4))
    return obj

def write_spell_scroll(obj: dict) -> None:
    if len(obj) > 3:
        write_common(obj)
    else: io.write_int(0, 1)
    io.write_int(obj["spell"], 4)

def parse_treasure_chest(obj: dict) -> dict:
    obj["contents"] = io.read_int(4)
    obj["artifact"] = io.read_int(4)
#    obj["artifact"] = ad.ID(io.read_int(4))
    return obj

def write_treasure_chest(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_int(obj["artifact"], 4)

def parse_tree_of_knowledge(obj: dict) -> dict:
    obj["contents"] = io.read_int(4)
    obj["end_bytes"] = io.read_int(4)
    return obj

def write_tree_of_knowledge(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_int(obj["end_bytes"], 4)

class University(IntEnum):
    Random = 4294967295
    Custom = 0

def parse_university(obj: dict) -> dict:
    obj["mode"]   = University(io.read_int(4))
    obj["skills"] =            io.read_bits(4)
    return obj

def write_university(obj: dict) -> None:
    io.write_int(obj["mode"], 4)
    io.write_bits(obj["skills"])

def parse_wagon(obj: dict) -> dict:
    obj["contents"] =             io.read_int(4)
    obj["artifact"] =       ad.ID(io.read_int(4))
    obj["amount"]   =             io.read_int(4)
    obj["resource"] = od.Resource(io.read_int(1))

    obj["mystery_bytes"] = io.read_raw(5)
    return obj

def write_wagon(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_int(obj["artifact"], 4)
    io.write_int(obj["amount"], 4)
    io.write_int(obj["resource"], 1)
    io.write_raw(obj["mystery_bytes"])

def parse_warriors_tomb(obj: dict) -> dict:
    obj["contents"] =       io.read_int(4)
    obj["artifact"] = ad.ID(io.read_int(4))
    return obj

def write_warriors_tomb(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_int(obj["artifact"], 4)

def parse_dwelling(obj: dict) -> dict:
    obj["owner"] = io.read_int(4)

    obj["same_as_town"] = io.read_int(4)
    if obj["same_as_town"] == 0:
        obj["alignment"] = io.read_bits(2)

    obj["minimum_level"] = io.read_int(1)
    obj["maximum_level"] = io.read_int(1)
    return obj

def write_dwelling(obj: dict) -> None:
    io.write_int(obj["owner"], 4)

    io.write_int(obj["same_as_town"], 4)
    if "alignment" in obj:
        io.write_bits(obj["alignment"])

    io.write_int(obj["minimum_level"], 1)
    io.write_int(obj["maximum_level"], 1)

def parse_leveled(obj: dict) -> dict:
    obj["owner"] = io.read_int(4)

    obj["same_as_town"] = io.read_int(4)
    if obj["same_as_town"] == 0:
        obj["alignment"] = io.read_bits(2)

    return obj

def write_leveled(obj: dict) -> None:
    io.write_int(obj["owner"], 4)

    io.write_int(obj["same_as_town"], 4)
    if "alignment" in obj:
        io.write_bits(obj["alignment"])

def parse_faction(obj: dict) -> dict:
    obj["owner"]         = io.read_int(4)
    obj["minimum_level"] = io.read_int(1)
    obj["maximum_level"] = io.read_int(1)
    return obj

def write_faction(obj: dict) -> None:
    io.write_int(obj["owner"], 4)
    io.write_int(obj["minimum_level"], 1)
    io.write_int(obj["maximum_level"], 1)

def parse_ancient_lamp(obj: dict) -> dict:
    obj["contents"]      = io.read_int(4)
    obj["trash_bytes"]   = io.read_raw(4)
    obj["amount"]        = io.read_int(4)
    obj["mystery_bytes"] = io.read_raw(6)
    return obj

def write_ancient_lamp(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_raw(obj["trash_bytes"])
    io.write_int(obj["amount"], 4)
    io.write_raw(obj["mystery_bytes"])

def parse_sea_barrel(obj: dict) -> dict:
    obj["contents"]      =             io.read_int(4)
    obj["trash_bytes"]   =             io.read_raw(4)
    obj["amount"]        =             io.read_int(4)
    obj["resource"]      = od.Resource(io.read_int(1))
    obj["mystery_bytes"] =             io.read_raw(5)
    return obj

def write_sea_barrel(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_raw(obj["trash_bytes"])
    io.write_int(obj["amount"], 4)
    io.write_int(obj["resource"], 1)
    io.write_raw(obj["mystery_bytes"])

def parse_vial_of_mana(obj: dict) -> dict:
    obj["contents"]    = io.read_int(4)
    obj["trash_bytes"] = io.read_raw(4)
    return obj

def write_vial_of_mana(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_raw(obj["trash_bytes"])

def parse_abandoned_mine(obj: dict) -> dict:
    obj["resources"] =       io.read_bits(1)
    obj["mid_bytes"] =       io.read_raw(3)
    obj["is_custom"] =  bool(io.read_int(1))
    obj["creature"]  = cd.ID(io.read_int(4))
    obj["min_val"]   =       io.read_int(4)
    obj["max_val"]   =       io.read_int(4)
    return obj

def write_abandoned_mine(obj: dict) -> None:
    io.write_bits(obj["resources"])
    io.write_raw(obj["mid_bytes"])
    io.write_int(obj["is_custom"], 1)
    io.write_int(obj["creature"], 4)
    io.write_int(obj["min_val"], 4)
    io.write_int(obj["max_val"], 4)

def parse_grave(obj: dict) -> dict:
    obj["contents"] =             io.read_int(4)
    obj["artifact"] =       ad.ID(io.read_int(4))
    obj["amount"]   =             io.read_int(4)
    obj["resource"] = od.Resource(io.read_int(1))
    obj["mystery_bytes"] =        io.read_raw(5)
    return obj

def write_grave(obj: dict) -> None:
    io.write_int(obj["contents"], 4)
    io.write_int(obj["artifact"], 4)
    io.write_int(obj["amount"], 4)
    io.write_int(obj["resource"], 1)
    io.write_raw(obj["mystery_bytes"])
