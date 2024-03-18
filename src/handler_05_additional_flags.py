#!/usr/bin/env python3

import src.file_io as io

# The banned artifacts/spells/skills of a map are stored as follows:
#
# - Enabled/banned artifacts | 21 bytes (bits)
# - Enabled/banned spells    | 9 bytes (bits)
# - Enabled/banned skills    | 4 bytes (bits)

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
