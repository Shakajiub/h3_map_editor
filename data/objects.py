#!/usr/bin/env python3

from enum import IntEnum

class ID(IntEnum):
    Nothing                     =   0
    #                               1
    Altar_of_Sacrifice          =   2
    Anchor_Point                =   3
    Arena                       =   4
    Artifact                    =   5
    Pandoras_Box                =   6
    Black_Market                =   7
    Boat                        =   8
    Border_Guard                =   9
    Keymasters_Tent             =  10
    Buoy                        =  11
    Campfire                    =  12
    Cartographer                =  13
    Swan_Pond                   =  14
    Cover_of_Darkness           =  15
    Creature_Bank               =  16
    Creature_Generator_1        =  17
    Creature_Generator_2        =  18
    Creature_Generator_3        =  19
    Creature_Generator_4        =  20
    Cursed_Ground_RoE           =  21
    Corpse                      =  22
    Marletto_Tower              =  23
    Derelict_Ship               =  24
    Dragon_Utopia               =  25
    Event                       =  26
    Eye_of_the_Magi             =  27
    Faerie_Ring                 =  28
    Flotsam                     =  29
    Fountain_of_Fortune         =  30
    Fountain_of_Youth           =  31
    Garden_of_Revelation        =  32
    Garrison                    =  33
    Hero                        =  34
    Hill_Fort                   =  35
    Grail                       =  36
    Hut_of_the_Magi             =  37
    Idol_of_Fortune             =  38
    Lean_To                     =  39
    #                              40
    Library_of_Enlightenment    =  41
    Lighthouse                  =  42
    Monolith_One_Way_Entrance   =  43
    Monolith_One_Way_Exit       =  44
    Two_Way_Monolith            =  45
    Magic_Plains_RoE            =  46
    School_of_Magic             =  47
    Magic_Spring                =  48
    Magic_Well                  =  49
    Market_of_Time              =  50
    Mercenary_Camp              =  51
    Mermaids                    =  52
    Mine                        =  53
    Monster                     =  54
    Mystical_Garden             =  55
    Oasis                       =  56
    Obelisk                     =  57
    Redwood_Observatory         =  58
    Ocean_Bottle                =  59
    Pillar_of_Fire              =  60
    Star_Axis                   =  61
    Prison                      =  62
    Pyramid                     =  63
    Rally_Flag                  =  64
    Random_Artifact             =  65
    Random_Treasure_Artifact    =  66
    Random_Minor_Artifact       =  67
    Random_Major_Artifact       =  68
    Random_Relic                =  69
    Random_Hero                 =  70
    Random_Monster              =  71
    Random_Monster_1            =  72
    Random_Monster_2            =  73
    Random_Monster_3            =  74
    Random_Monster_4            =  75
    Random_Resource             =  76
    Random_Town                 =  77
    Refugee_Camp                =  78
    Resource                    =  79
    Sanctuary                   =  80
    Scholar                     =  81
    Sea_Chest                   =  82
    Seers_Hut                   =  83
    Crypt                       =  84
    Shipwreck                   =  85
    Shipwreck_Survivor          =  86
    Shipyard                    =  87
    Shrine_of_Magic_Incantation =  88
    Shrine_of_Magic_Gesture     =  89
    Shrine_of_Magic_Thought     =  90
    Sign                        =  91
    Sirens                      =  92
    Spell_Scroll                =  93
    Stables                     =  94
    Tavern                      =  95
    Temple                      =  96
    Den_of_Thieves              =  97
    Town                        =  98
    Trading_Post                =  99
    Learning_Stone              = 100
    Treasure_Chest              = 101
    Tree_of_Knowledge           = 102
    Subterranean_Gate           = 103
    University                  = 104
    Wagon                       = 105
    War_Machine_Factory         = 106
    School_of_War               = 107
    Warriors_Tomb               = 108
    Water_Wheel                 = 109
    Watering_Hole               = 110
    Whirlpool                   = 111
    Windmill                    = 112
    Witch_Hut                   = 113
    Brush                       = 114
    Bush                        = 115
    Cactus                      = 116
    Canyon                      = 117
    Crater                      = 118
    Dead_Vegetation             = 119
    Flowers                     = 120
    Frozen_Lake                 = 121
    Hedge                       = 122
    Hill                        = 123
    Hole                        = 124
    Kelp                        = 125
    Lake                        = 126
    Lava_Flow                   = 127
    Lava_Lake                   = 128
    Mushrooms                   = 129
    Log                         = 130
    Mandrake                    = 131
    Moss                        = 132
    Mound                       = 133
    Mountain                    = 134
    Oak_Trees                   = 135
    Outcropping                 = 136
    Pine_Trees                  = 137
    Plant                       = 138
    HotA_Decoration_1           = 139 # HotA
    HotA_Decoration_2           = 140 # HotA
    HotA_Ground                 = 141 # HotA
    HotA_Warehouse              = 142 # HotA
    River_Delta                 = 143
    HotA_Visitable_1            = 144 # HotA
    HotA_Collectible            = 145 # HotA
    HotA_Visitable_2            = 146 # HotA
    Rock                        = 147
    Sand_Dune                   = 148
    Sand_Pit                    = 149
    Shrub                       = 150
    Skull                       = 151
    Stalagmite                  = 152
    Stump                       = 153
    Tar_Pit                     = 154
    Trees                       = 155
    Vine                        = 156
    Volcanic_Vent               = 157
    Volcano                     = 158
    Willow_Trees                = 159
    Yucca_Trees                 = 160
    Reef                        = 161
    Random_Monster_5            = 162
    Random_Monster_6            = 163
    Random_Monster_7            = 164
    Brush_2                     = 165
    Bush_2                      = 166
    Cactus_2                    = 167
    Canyon_2                    = 168
    Crater_2                    = 169
    Dead_Vegetation_2           = 170
    Flowers_2                   = 171
    Frozen_Lake_2               = 172
    Hedge_2                     = 173
    Hill_2                      = 174
    Hole_2                      = 175
    Kelp_2                      = 176
    Lake_2                      = 177
    Lava_Flow_2                 = 178
    Lava_Lake_2                 = 179
    Mushrooms_2                 = 180
    Log_2                       = 181
    Mandrake_2                  = 182
    Moss_2                      = 183
    Mound_2                     = 184
    Mountain_2                  = 185
    Oak_Trees_2                 = 186
    Outcropping_2               = 187
    Pine_Trees_2                = 188
    Plant_2                     = 189
    River_Delta_2               = 190
    Rock_2                      = 191
    Sand_Dune_2                 = 192
    Sand_Pit_2                  = 193
    Shrub_2                     = 194
    Skull_2                     = 195
    Stalagmite_2                = 196
    Stump_2                     = 197
    Tar_Pit_2                   = 198
    Trees_2                     = 199
    Vine_2                      = 200
    Volcanic_Vent_2             = 201
    Volcano_2                   = 202
    Willow_Trees_2              = 203
    Yucca_Trees_2               = 204
    Reef_2                      = 205
    Desert_Hills                = 206
    Dirt_Hills                  = 207
    Grass_Hills                 = 208
    Rough_Hills                 = 209
    Subterranean_Rocks          = 210
    Swamp_Foliage               = 211
    Border_Gate                 = 212
    Freelancers_Guild           = 213
    Hero_Placeholder            = 214
    Quest_Guard                 = 215
    Random_Dwelling             = 216
    Random_Dwelling_Leveled     = 217
    Random_Dwelling_Faction     = 218
    Garrison_Vertical           = 219
    Abandoned_Mine              = 220
    Trading_Post_Snow           = 221
    Clover_Field                = 222
    Cursed_Ground               = 223
    Evil_Fog                    = 224
    Favorable_Winds             = 225
    Fiery_Fields                = 226
    Holy_Ground                 = 227
    Lucid_Pools                 = 228
    Magic_Clouds                = 229
    Magic_Plains                = 230
    Rocklands                   = 231
    #                             232
    #                             233
    #                             234
    #                             235
    #                             236
    #                             237
    #                             238
    #                             239
    #                             240
    #                             241
    #                             242
    #                             243
    #                             244
    #                             245
    #                             246
    #                             247
    #                             248
    #                             249
    #                             250
    #                             251
    #                             252
    #                             253
    #                             254
    #                             255

class CreatureBank(IntEnum): # ID 16
    Cyclops_Stockpile    =  0
    Dwarven_Treasury     =  1
    Griffin_Conservatory =  2
    Imp_Cache            =  3
    Medusa_Stores        =  4
    Naga_Bank            =  5
    Dragon_Fly_Hive      =  6
    Shipwreck            =  7
    Derelict_Ship        =  8
    Crypt                =  9
    Dragon_Utopia        = 10
    #                      11
    #                      12
    #                      13
    #                      14
    #                      15
    #                      16
    #                      17
    #                      18
    #                      19
    #                      20
    Beholders_Sanctuary  = 21
    Temple_of_the_Sea    = 22
    Pirate_Cavern        = 23
    Mansion              = 24
    Spit                 = 25
    Red_Tower            = 26
    Black_Tower          = 27
    Ivory_Tower          = 28
    Churchyard           = 29
    Experimental_Shop    = 30
    Wolf_Raider_Picket   = 31
    Ruins                = 32

class TwoWayMonolith(IntEnum): # ID 45
    Small_Green      =  0
    Small_Brown      =  1
    Small_Violet     =  2
    Small_Orange     =  3
    Big_Green        =  4
    Big_Yellow       =  5
    Big_Red          =  6
    Big_Cyan         =  7
    Water_White      =  8
    Small_Pink       =  9
    Small_Turquoise  = 10
    Small_Yellow     = 11
    Small_Black      = 12
    Big_Chartreuse   = 13
    Big_Turquoise    = 14
    Big_Violet       = 15
    Big_Orange       = 16
    Small_Blue       = 17
    Small_Red        = 18
    Big_Pink         = 19
    Big_Blue         = 20
    Water_Red        = 21
    Water_Blue       = 22
    Water_Chartreuse = 23
    Water_Yellow     = 24

class HotA_Decoration_1(IntEnum): # ID 139
    Crate                    =  0
    Crates                   =  1
    Sack                     =  2
    Barrels                  =  3
    Jaw                      =  4
    Rope                     =  5
    Frog                     =  6
    Frogs                    =  7
    Chicken                  =  8
    Rooster                  =  9
    Bluebottle               = 10
    Ruined_Camp              = 11
    Ruined_Fountain          = 12
    Pig                      = 13
    Ancient_Altar            = 14
    Abandoned_Boat           = 15
    Fence                    = 16
    Waterfalls               = 17
    Fire                     = 18
    Ruined_Subterranean_Gate = 19
    Carnivorous_Plant        = 20
    Bridge                   = 21
    Bone                     = 22
    Sacks                    = 23
    Puddles                  = 24
    Rubble                   = 25
    Limestone_Puddles        = 26

class HotA_Decoration_2(IntEnum): # ID 140
    Stony_Sphere   = 0
    Stone          = 1
    Palms          = 2
    Ice_Block      = 3
    Pile_of_Stones = 4
    Snow_Hills     = 5
    Barchan_Dunes  = 6
    Spruces        = 7
    Limestone_Lake = 8

class HotA_Ground(IntEnum): # ID 141
    Cracked_Ice     = 0
    Dunes           = 1
    Fields_of_Glory = 2

class HotA_Visitable_1(IntEnum): # ID 144
    Temple_of_Loyalty     =  0
    Skeleton_Transformer  =  1
    Colosseum_of_the_Magi =  2
    Watering_Place        =  3
    Mineral_Spring        =  4
    Hermits_Shack         =  5
    Gazebo                =  6
    Junkman               =  7
    Derrick               =  8
    Warlocks_Lab          =  9
    Prospector            = 10
    Trailblazer           = 11

class HotA_Collectible(IntEnum): # ID 145
    Ancient_Lamp = 0
    Sea_Barrel   = 1
    Jetsam       = 2
    Vial_of_Mana = 3

class HotA_Visitable_2(IntEnum): # ID 146
    Seafaring_Academy = 0
    Observatory       = 1
    Altar_of_Mana     = 2
    Town_Gate         = 3

class BorderGate(IntEnum): # ID 212
    Light_Blue =    0
    Green      =    1
    Red        =    2
    Dark_Blue  =    3
    Brown      =    4
    Purple     =    5
    White      =    6
    Black      =    7
    Quest_Gate = 1000 # HotA
    Grave      = 1001 # HotA
