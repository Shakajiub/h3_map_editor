#!/usr/bin/env python3

from random import choice, randint

import data.creatures as cd # Creature details
import data.objects   as od # Object details

####################
## COMMON METHODS ##
####################

AMOUNT = [
    [    5, "a few ({1-4}) "           ],
    [   10, "several ({5-9}) "         ],
    [   20, "a pack ({10-19}) of "     ],
    [   50, "lots ({20-49}) of "       ],
    [  100, "a horde ({50-99}) of "    ],
    [  250, "a throng ({100-249}) of " ],
    [  500, "a swarm ({250-499}) of "  ],
    [ 1000, "zounds ({500-999}) of "   ]
]

def get_creature_text(creature_id: int, amount: int) -> str:
    text = "a legion ({1000+}) of "
    for pair in AMOUNT:
        if amount < pair[0]:
            text = pair[1]
            break
    return text + cd.NAME[creature_id]

###################
## COUNT OBJECTS ##
###################

def count_objects(obj_data: dict) -> dict:
    info = {}

    for obj in obj_data:
        print(obj)

    return info

#####################
## DESCRIBE GUARDS ##
#####################

def describe_guards(map_data: dict) -> str:
    return ""

#####################
## GENERATE GUARDS ##
#####################

FACTIONS = {
    "Castle"    : [   0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13 ],
    "Rampart"   : [  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27 ],
    "Tower"     : [  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,  40,  41 ],
    "Inferno"   : [  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55 ],
    "Necropolis": [  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69, 141 ],
    "Dungeon"   : [  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83 ],
    "Stronghold": [  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,  96,  97 ],
    "Fortress"  : [  98,  99, 100, 101, 106, 107, 104, 105, 102, 103, 108, 109, 110, 111 ],
    "Conflux"   : [ 118, 119, 112, 127, 115, 123, 114, 129, 113, 125, 120, 121, 130, 131 ],
    "Cove"      : [ 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 151 ],
    "Neutral"   : [ 139, 138, 143, 140, 169, 142, 167, 137, 170, 116, 117, 168, 144, 136, 135, 134, 133, 132 ]
}

def generate_guards(obj_data: dict, describe_guards: bool = True) -> dict:
    print("\n---[ Generating guards (v.101) ]---\n")

    valid_types = {
        od.ID.Pandoras_Box            : "{Pandora's Box}\n",
        od.ID.Artifact                : "{Artifact}\n",
        od.ID.Random_Artifact         : "{Artifact}\n",
        od.ID.Random_Treasure_Artifact: "{Artifact}\n",
        od.ID.Random_Minor_Artifact   : "{Artifact}\n",
        od.ID.Random_Major_Artifact   : "{Artifact}\n",
        od.ID.Random_Relic            : "{Artifact}\n",
        od.ID.Event                   : "",
        od.ID.Resource                : "{Resources}\n",
        od.ID.Spell_Scroll            : "{Spell Scroll}\n",
    }

    for obj in obj_data:
        if obj["type"] not in valid_types.keys() or not "message" in obj:
            continue

        # Split the message box into a list of separate lines
        # and check if the last line contains "-guards xxx".
        obj_message = obj["message"].split('\n')
        last_line = obj_message[-1].split(' ')

        if last_line[0] != "-guards":
            continue

        if not last_line[1].isdigit():
            continue

        # If there is no message for the object (other than the desired AI
        # value, then we generate a simple title and a yes/no prompt later).
        add_prompt = False
        if obj["type"] != od.ID.Pandoras_Box:
            add_prompt = len(obj_message) == 1

        desired_guard_value = int(last_line[1])

        # Make sure we the desired guard value is large enough.
        if desired_guard_value < 1000:
            print("\nThe guard value for", obj["type"], "at", obj["coords"],
                f"is too low! ({desired_guard_value}). Min value is 1000.\n")
            continue

        # Limit the number of stacks so that the minimum
        # AI value of a single stack is at least 5000.
        max_num = max(min(round(desired_guard_value / 5000), 7), 3)
        creature_num = randint(2, max_num)
        max_creature_value = desired_guard_value / creature_num

        # Get a list of creatures from two random factions.
        creature_list = []
        creature_list += choice(list(FACTIONS.values()))
        creature_list += choice(list(FACTIONS.values()))

        obj["guards"] = []
        generated_ai_value = 0

        # Generate random creatures from the list.
        for _ in range(creature_num):
            temp_id = 65535
            temp_amount = 0

            while temp_amount == 0:
                temp_id = choice(creature_list)
                temp_amount = round(max_creature_value / cd.AI_VALUE[temp_id])

            obj["guards"].append({ "id": temp_id, "amount": temp_amount })
            generated_ai_value += cd.AI_VALUE[temp_id] * temp_amount

        if describe_guards and obj["type"] != od.ID.Event:
            # TODO - Move this into describe_guards() when it is done.

            guard_text = "Guarded by "

            # Get the total amount of each creature. (Necessary if
            # there's more than one stack of a type of creature).
            total_guards = {}
            for c in obj["guards"]:
                if c["id"] in total_guards:
                    total_guards[c["id"]] += c["amount"]
                else: total_guards[c["id"]] = c["amount"]

            # Create a sentence with all the guards with proper grammar.
            guard_list = []
            for k, v in total_guards.items():
                guard_list.append(get_creature_text(k, v))

            last_guard = " and " + guard_list.pop()
            guard_text += ", ".join(guard_list) + last_guard

            # Reconstruct the message box of the object.
            if add_prompt:
                obj_message.insert(0, valid_types[obj["type"]])

            obj_message[-1] = guard_text
            obj["message"] = "\n".join(obj_message)

            if add_prompt:
                obj["message"] += "\n\nDo you wish to fight the guards?"

        # Fill remaining guard slots (up to 7) with correct blank data.
        for _ in range(7-creature_num):
            obj["guards"].append({ "id": 65535, "amount": 65535 })

        print(f"Generated guards for", obj["type"], "at", obj["coords"],
              "for a total AI value of", generated_ai_value,
              f"({desired_guard_value} desired)")

    print("\n---[ Finished generating guards ]---\n")
    return obj_data
























