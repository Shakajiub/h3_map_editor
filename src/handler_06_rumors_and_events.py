#!/usr/bin/env python3

import src.file_io as io

def parse_rumors() -> list:
    info = []

    for _ in range(io.read_int(4)): # Amount of rumors
        rumor = {}
        rumor["name"] = io.read_str(io.read_int(4))
        rumor["text"] = io.read_str(io.read_int(4))
        info.append(rumor)

    return info

def write_rumors(info: list) -> None:
    io.write_int(len(info), 4)

    for rumor in info:
        io.write_int(len(rumor["name"]), 4)
        io.write_str(    rumor["name"])
        io.write_int(len(rumor["text"]), 4)
        io.write_str(    rumor["text"])

def parse_events(is_town: bool = False) -> list:
    info = []

    for _ in range(io.read_int(4)): # Amount of timed events
        event = {}
        event["name"]    = io.read_str(io.read_int(4))
        event["message"] = io.read_str(io.read_int(4))

        event["resources"] = []
        for _ in range(7):
            event["resources"].append(io.read_int(4))

        event["apply_to"]         =      io.read_bits(1)
        event["apply_human"]      = bool(io.read_int(1))
        event["apply_ai"]         = bool(io.read_int(1))
        event["first_occurence"]  =      io.read_int(2)
        event["subsequent_occurences"] = io.read_int(1)
        io.seek(17)

        if is_town:
            event["buildings"] = io.read_bits(6)
            event["creatures"] = []
            for _ in range(7):
                event["creatures"].append(io.read_int(2))
            io.seek(4)

        info.append(event)

    return info

def write_events(info: list, is_town: bool = False) -> None:
    io.write_int(len(info), 4)

    for event in info:
        io.write_int(len(event["name"]), 4)
        io.write_str(    event["name"])
        io.write_int(len(event["message"]), 4)
        io.write_str(    event["message"])

        for resource in event["resources"]:
            io.write_int(resource, 4)

        io.write_bits(event["apply_to"])
        io.write_int( event["apply_human"], 1)
        io.write_int( event["apply_ai"], 1)
        io.write_int( event["first_occurence"], 2)
        io.write_int( event["subsequent_occurences"], 1)
        io.write_int(0, 17)

        if is_town:
            io.write_bits(event["buildings"])
            for creature in event["creatures"]:
                io.write_int(creature, 2)
            io.write_int(0, 4)
