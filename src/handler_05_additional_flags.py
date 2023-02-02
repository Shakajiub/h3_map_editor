#!/usr/bin/env python3

import src.file_io as io

def parse_flags() -> dict:
    info = {
        "artifacts": [],
        "spells"   : [],
        "skills"   : []
    }

    info["artifacts"] = io.read_bits(21)
    info["spells"]    = io.read_bits(9)
    info["skills"]    = io.read_bits(4)

    return info

def write_flags(info: dict) -> None:
    io.write_bits(info["artifacts"])
    io.write_bits(info["spells"])
    io.write_bits(info["skills"])
