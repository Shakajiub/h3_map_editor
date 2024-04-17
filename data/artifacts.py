#!/usr/bin/env python3

from enum import IntEnum

class ID(IntEnum):
    Empty_1_Byte  = 255
    Empty_2_Bytes = 65535
    Empty_Unknown = 2637180971
    Empty_4_Bytes = 4294967295
#
# Byte 1 ... (0-7)
#
    Spell_Book     = 0
    Spell_Scroll   = 1
    The_Grail      = 2
    Catapult       = 3
    Ballista       = 4
    Ammo_Cart      = 5
    First_Aid_Tent = 6
    Centaurs_Axe   = 7
#
# Byte 2 ... (8-15)
#
    Blackshard_of_the_Dead_Knight =  8
    Greater_Gnolls_Flail          =  9
    Ogres_Club_of_Havoc           = 10
    Sword_of_Hellfire             = 11
    Titans_Gladius                = 12
    Shield_of_the_Dwarven_Lords   = 13
    Shield_of_the_Yawning_Dead    = 14
    Buckler_of_the_Gnoll_King     = 15
#
# Byte 3 ... (16-23)
#
    Targ_of_the_Rampaging_Ogre    = 16
    Shield_of_the_Damned          = 17
    Sentinels_Shield              = 18
    Helm_of_the_Alabaster_Unicorn = 19
    Skull_Helmet                  = 20
    Helm_of_Chaos                 = 21
    Crown_of_the_Supreme_Magi     = 22
    Hellstorm_Helmet              = 23
#
# Byte 4 ... (24-31)
#
    Thunder_Helmet                 = 24
    Breastplate_of_Petrified_Wood  = 25
    Rib_Cage                       = 26
    Scales_of_the_Greater_Basilisk = 27
    Tunic_of_the_Cyclops_King      = 28
    Breastplate_of_Brimstone       = 29
    Titans_Cuirass                 = 30
    Armor_of_Wonder                = 31
#
# Byte 5 ... (32-39)
#
    Sandals_of_the_Saint           = 32
    Celestial_Necklace_of_Bliss    = 33
    Lions_Shield_of_Courage        = 34
    Sword_of_Judgement             = 35
    Helm_of_Heavenly_Enlightenment = 36
    Quiet_Eye_of_the_Dragon        = 37
    Red_Dragon_Flame_Tongue        = 38
    Dragon_Scale_Shield            = 39
#
# Byte 6 ... (40-47)
#
    Dragon_Scale_Armor      = 40
    Dragonbone_Greaves      = 41
    Dragon_Wing_Tabard      = 42
    Necklace_of_Dragonteeth = 43
    Crown_of_Dragontooth    = 44
    Still_Eye_of_the_Dragon = 45
    Clover_of_Fortune       = 46
    Cards_of_Prophecy       = 47
#
# Byte 7 ... (48-55)
#
    Ladybird_of_Luck         = 48
    Badge_of_Courage         = 49
    Crest_of_Valor           = 50
    Glyph_of_Gallantry       = 51
    Speculum                 = 52
    Spyglass                 = 53
    Amulet_of_the_Undertaker = 54
    Vampires_Cowl            = 55
#
# Byte 8 ... (56-63)
#
    Dead_Mans_Boots                = 56
    Garniture_of_Interference      = 57
    Surcoat_of_Counterpoise        = 58
    Boots_of_Polarity              = 59
    Bow_of_Elven_Cherrywood        = 60
    Bowstring_of_the_Unicorns_Mane = 61
    Angel_Feather_Arrows           = 62
    Bird_of_Perception             = 63
#
# Byte 9 ... (64-71)
#
    Stoic_Watchman             = 64
    Emblem_of_Cognizance       = 65
    Statesmans_Medal           = 66
    Diplomats_Ring             = 67
    Ambassadors_Sash           = 68
    Ring_of_the_Wayfarer       = 69
    Equestrians_Gloves         = 70
    Necklace_of_Ocean_Guidance = 71
#
# Byte 10 ... (72-79)
#
    Angel_Wings          = 72
    Charm_of_Mana        = 73
    Talisman_of_Mana     = 74
    Mystic_Orb_of_Mana   = 75
    Collar_of_Conjuring  = 76
    Ring_of_Conjuring    = 77
    Cape_of_Conjuring    = 78
    Orb_of_the_Firmament = 79
#
# Byte 11 ... (80-87)
#
    Orb_of_Silt                = 80
    Orb_of_Tempestuous_Fire    = 81
    Orb_of_Driving_Rain        = 82
    Recanters_Cloak            = 83
    Spirit_of_Oppression       = 84
    Hourglass_of_the_Evil_Hour = 85
    Tome_of_Fire_Magic         = 86
    Tome_of_Air_Magic          = 87
#
# Byte 12 ... (88-95)
#
    Tome_of_Water_Magic  = 88
    Tome_of_Earth_Magic  = 89
    Boots_of_Levitation  = 90
    Golden_Bow           = 91
    Sphere_of_Permanence = 92
    Orb_of_Vulnerability = 93
    Ring_of_Vitality     = 94
    Ring_of_Life         = 95
#
# Byte 13 ... (96-103)
#
    Vial_of_Lifeblood       =  96
    Necklace_of_Swiftness   =  97
    Boots_of_Speed          =  98
    Cape_of_Velocity        =  99
    Pendant_of_Dispassion   = 100
    Pendant_of_Second_Sight = 101
    Pendant_of_Holiness     = 102
    Pendant_of_Life         = 103
#
# Byte 14 ... (104-111)
#
    Pendant_of_Death            = 104
    Pendant_of_Free_Will        = 105
    Pendant_of_Negativity       = 106
    Pendant_of_Total_Recall     = 107
    Pendant_of_Courage          = 108
    Everflowing_Crystal_Cloak   = 109
    Ring_of_Infinite_Gems       = 110
    Everpouring_Vial_of_Mercury = 111
#
# Byte 15 ... (112-119)
#
    Inexhaustible_Cart_of_Ore    = 112
    Eversmoking_Ring_of_Sulfur   = 113
    Inexhaustible_Cart_of_Lumber = 114
    Endless_Sack_of_Gold         = 115
    Endless_Bag_of_Gold          = 116
    Endless_Purse_of_Gold        = 117
    Legs_of_Legion               = 118
    Loins_of_Legion              = 119
#
# Byte 16 ... (120-127)
#
    Torso_of_Legion     = 120
    Arms_of_Legion      = 121
    Head_of_Legion      = 122
    Sea_Captains_Hat    = 123
    Spellbinders_Hat    = 124
    Shackles_of_War     = 125
    Orb_of_Inhibition   = 126
    Vial_of_Dragonblood = 127
#
# Byte 17 ... (128-135)
#
    Armageddons_Blade          = 128
    Angelic_Alliance           = 129
    Cloak_of_the_Undead_King   = 130
    Elixir_of_Life             = 131
    Armor_of_the_Damned        = 132
    Statue_of_Legion           = 133
    Power_of_the_Dragon_Father = 134
    Titans_Thunder             = 135
#
# Byte 18 ... (136-143)
#
    Admirals_Hat            = 136
    Bow_of_the_Sharpshooter = 137
    Wizards_Well            = 138
    Ring_of_the_Magi        = 139
    Cornucopia              = 140
    Diplomats_Cloak         = 141
    Pendant_of_Reflection   = 142
    Ironfist_of_the_Ogre    = 143
#
# Byte 19 ... (144-151)
#
    # Highlighted slot     = 144
    # Artifact lock        = 145
    Cannon                 = 146
    Trident_of_Dominion    = 147
    Shield_of_Naval_Glory  = 148
    Royal_Armor_of_Nix     = 149
    Crown_of_the_Five_Seas = 150
    Wayfarers_Boots        = 151
#
# Byte 20 ... (152-159)
#
    Runes_of_Imminency  = 152
    Demons_Horseshoe    = 153
    Shamans_Puppet      = 154
    Hideous_Mask        = 155
    Ring_of_Suppression = 156
    Pendant_of_Downfall = 157
    Ring_of_Oblivion    = 158
    Cape_of_Silence     = 159
#
# Byte 21 ... (160-167)
#
    Golden_Goose         = 160
    Horn_of_the_Abyss    = 161
    Charm_of_Eclipse     = 162
    Seal_of_Sunset       = 163
    Plate_of_Dying_Light = 164
    Sleepkeeper          = 165
    # UNUSED
    # UNUSED
