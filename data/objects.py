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
    Cursed_Ground               =  21
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
    Magic_Plains                =  46
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
    #                             139
    #                             140
    #                             141
    #                             142
    River_Delta                 = 143
    #                             144
    #                             145
    #                             146
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
    #                             217
    #                             218
    Garrison_2                  = 219
    Mine_2                      = 220
    Trading_Post_2              = 221
    Clover_Field                = 222
    Cursed_Ground_2             = 223
    Evil_Fog                    = 224
    Favorable_Winds             = 225
    Fiery_Fields                = 226
    Holy_Ground                 = 227
    Lucid_Pools                 = 228
    Magic_Clouds                = 229
    Magic_Plains_2              = 230
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
