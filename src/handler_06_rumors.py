#!/usr/bin/env python3

import src.file_io as io

def parse_rumors() -> dict:
    info = {
        "rumors": []
    }

    for i in range(io.read_int(4)):
        rumor = {}
        rumor["name"] = io.read_str(io.read_int(4))
        rumor["text"] = io.read_str(io.read_int(4))
        info["rumors"].append(rumor)

    return info

def write_rumors(info: dict) -> None:
    io.write_int(len(info["rumors"]), 4)

    for r in info["rumors"]:
        io.write_int(len(r["name"]), 4)
        io.write_str(    r["name"])
        io.write_int(len(r["text"]), 4)
        io.write_str(    r["text"])
