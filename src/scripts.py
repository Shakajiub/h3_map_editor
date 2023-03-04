#!/usr/bin/env python3

import data.creatures as cd # Creature details

CREATURE_MAX  = [ 5, 10, 20, 50, 100, 250, 500, 1000 ]
CREATURE_TEXT = [ "a few", "several", "a pack", "lots",
                  "a horde", "a throng", "a swarm", "zounds" ]

def indicate_guards(amount: int) -> str:
    t = "a legion"
    for i in range(8):
        if amount < CREATURE_MAX[i]:
            t = CREATURE_TEXT[i]
            break
    return f"{t} ({{{amount}}})"

def generate_guards(ai_value: int, max_amount: int = 7) -> list:
    return []
