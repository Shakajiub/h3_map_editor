#!/usr/bin/env python3

from enum import IntEnum

class ID(IntEnum):
#
# Byte 1 ... (0-7)
#
    Summon_Boat  = 0
    Scuttle_Boat = 1
    Visions      = 2
    View_Earth   = 3
    Disguise     = 4
    View_Air     = 5
    Fly          = 6
    Water_Walk   = 7
#
# Byte 2 ... (8-15)
#
    Dimension_Door =  8
    Town_Portal    =  9
    Quick_Sand     = 10
    Land_Mine      = 11
    Force_Field    = 12
    Fire_Wall      = 13
    Earthquake     = 14
    Magic_Arrow    = 15
#
# Byte 3 ... (16-23)
#
    Ice_Bolt        = 16
    Lightning_Bolt  = 17
    Implosion       = 18
    Chain_Lightning = 19
    Frost_Ring      = 20
    Fireball        = 21
    Inferno         = 22
    Meteor_Shower   = 23
#
# Byte 4 ... (24-31)
#
    Death_Ripple   = 24
    Destroy_Undead = 25
    Armageddon     = 26
    Shield         = 27
    Air_Shield     = 28
    Fire_Shield    = 29
    Prot_From_Air  = 30
    Prot_From_Fire = 31
#
# Byte 5 ... (32-39)
#
    Prot_From_Water = 32
    Prot_From_Earth = 33
    Anti_Magic      = 34
    Dispel          = 35
    Magic_Mirror    = 36
    Cure            = 37
    Resurrection    = 38
    Animate_Dead    = 39
#
# Byte 6 ... (40-47)
#
    Sacrifice      = 40
    Bless          = 41
    Curse          = 42
    Bloodlust      = 43
    Precision      = 44
    Weakness       = 45
    Stone_Skin     = 46
    Disrupting_Ray = 47
#
# Byte 7 ... (48-55)
#
    Prayer     = 48
    Mirth      = 49
    Sorrow     = 50
    Fortune    = 51
    Misfortune = 52
    Haste      = 53
    Slow       = 54
    Slayer     = 55
#
# Byte 8 ... (56-63)
#
    Frenzy                = 56
    Titans_Lightning_Bolt = 57
    Counterstrike         = 58
    Berserk               = 59
    Hypnotize             = 60
    Forgetfulness         = 61
    Blind                 = 62
    Teleport              = 63
#
# Byte 9 ... (64-71)
#
    Remove_Obstacle        = 64
    Clone                  = 65
    Summon_Fire_Elemental  = 66
    Summon_Earth_Elemental = 67
    Summon_Water_Elemental = 68
    Summon_Air_Elemental   = 69
#
# Creature Spells
#
    Stone            = 70
    Poison           = 71
    Bind             = 72
    Disease          = 73
    Paralyze         = 74
    Aging            = 75
    Death_Cloud      = 76
    Thunderbolt      = 77
    Dragonfly_Dispel = 78
    Death_Stare      = 79
    Acid_Breath      = 80
