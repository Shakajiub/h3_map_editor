#!/usr/bin/env python3

import src.file_io as io

def parse_artifacts() -> dict:
    info = {
        "artifact_flags": []
    }

    info["artifact_flags"] = io.read_bits(21)

    return info

def write_artifacts(info: dict) -> None:
    io.write_bits(info["artifact_flags"])
