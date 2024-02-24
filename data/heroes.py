#!/usr/bin/env python3

from enum import IntEnum

class Classes(IntEnum):
#
# Byte 1 ... (0-7)
#
    Knight       =  0
    Cleric       =  1
    Ranger       =  2
    Druid        =  3
    Alchemist    =  4
    Wizard       =  5
    Demoniac     =  6
    Heretic      =  7
#
# Byte 2 ... (8-15)
#
    Death_Knight =  8
    Necromancer  =  9
    Overlord     = 10
    Warlock      = 11
    Barbarian    = 12
    Battle_Mage  = 13
    Beastmaster  = 14
    Witch        = 15
#
# Byte 3 ... (16-23)
#
    Planeswalker = 16
    Elementalist = 17
    Captain      = 18
    Navigator    = 19
    Mercenary    = 20
    Artificer    = 21
    #
    #

class ID(IntEnum):
    Default = 255
#
# Byte 1 ... (0-7)
#
    Orrin      = 0
    Valeska    = 1
    Edric      = 2
    Sylvia     = 3
    Lord_Haart = 4
    Sorsha     = 5
    Christian  = 6
    Tyris      = 7
#
# Byte 2 ... (8-15)
#
    Rion     =  8
    Adela    =  9
    Cuthbert = 10
    Adelaide = 11
    Ingham   = 12
    Sanya    = 13
    Loynis   = 14
    Caitlin  = 15
#
# Byte 3 ... (16-23)
#
    Mephala  = 16
    Ufretin  = 17
    Jenova   = 18
    Ryland   = 19
    Thorgrim = 20
    Ivor     = 21
    Clancy   = 22
    Kyrre    = 23
#
# Byte 4 ... (24-31)
#
    Coronius = 24
    Uland    = 25
    Elleshar = 26
    Gem      = 27
    Malcom   = 28
    Melodia  = 29
    Alagar   = 30
    Aeris    = 31
#
# Byte 5 ... (32-39)
#
    Piquedram = 32
    Thane     = 33
    Josephine = 34
    Neela     = 35
    Torosar   = 36
    Fafner    = 37
    Rissa     = 38
    Iona      = 39
#
# Byte 6 ... (40-47)
#
    Astral    = 40
    Halon     = 41
    Serena    = 42
    Daremyth  = 43
    Theodorus = 44
    Solmyr    = 45
    Cyra      = 46
    Aine      = 47
#
# Byte 7 ... (48-55)
#
    Fiona    = 48
    Rashka   = 49
    Marius   = 50
    Ignatius = 51
    Octavia  = 52
    Calh     = 53
    Pyre     = 54
    Nymus    = 55
#
# Byte 8 ... (56-63)
#
    Ayden  = 56
    Xyron  = 57
    Axsis  = 58
    Olema  = 59
    Calid  = 60
    Ash    = 61
    Zydar  = 62
    Xarfax = 63
#
# Byte 9 ... (64-71)
#
    Straker  = 64
    Vokial   = 65
    Moandor  = 66
    Charna   = 67
    Tamika   = 68
    Isra     = 69
    Clavius  = 70
    Galthran = 71
#
# Byte 10 ... (72-79)
#
    Septienna = 72
    Aislinn   = 73
    Sandro    = 74
    Nimbus    = 75
    Thant     = 76
    Xsi       = 77
    Vidomina  = 78
    Nagash    = 79
#
# Byte 11 ... (80-87)
#
    Lorelei = 80
    Arlach  = 81
    Dace    = 82
    Ajit    = 83
    Damacon = 84
    Gunnar  = 85
    Synca   = 86
    Shakti  = 87
#
# Byte 12 ... (88-95)
#
    Alamar     = 88
    Jaegar     = 89
    Malekith   = 90
    Jeddite    = 91
    Geon       = 92
    Deemer     = 93
    Sephinroth = 94
    Darkstorn  = 95
#
# Byte 13 ... (96-103)
#
    Yog       =  96
    Gurnisson =  97
    Jabarkas  =  98
    Shiva     =  99
    Gretchin  = 100
    Krellion  = 101
    Crag_Hack = 102
    Tyraxor   = 103
#
# Byte 14 ... (104-111)
#
    Gird    = 104
    Vey     = 105
    Dessa   = 106
    Terek   = 107
    Zubin   = 108
    Gundula = 109
    Oris    = 110
    Saurug  = 111
#
# Byte 15 ... (112-119)
#
    Bron     = 112
    Drakon   = 113
    Wystan   = 114
    Tazar    = 115
    Alkin    = 116
    Korbac   = 117
    Gerwulf  = 118
    Broghild = 119
#
# Byte 16 ... (120-127)
#
    Mirlanda = 120
    Rosic    = 121
    Voy      = 122
    Verdish  = 123
    Merist   = 124
    Styg     = 125
    Andra    = 126
    Tiva     = 127
#
# Byte 17 ... (128-135)
#
    Pasis   = 128
    Thunar  = 129
    Ignissa = 130
    Lacus   = 131
    Monere  = 132
    Erdamon = 133
    Fiur    = 134
    Kalt    = 135
#
# Byte 18 ... (136-143)
#
    Luna    = 136
    Brissa  = 137
    Ciele   = 138
    Labetha = 139
    Inteus  = 140
    Aenain  = 141
    Gelare  = 142
    Grindan = 143
#
# Byte 19 ... (144-151)
#
    Sir_Mullich = 144
    Adrienne    = 145
    Catherine   = 146
    Dracon      = 147
    Gelu        = 148
    Kilgor      = 149
    Haart_Lich  = 150
    Mutare      = 151
#
# Byte 20 ... (152-159)
#
    Roland       = 152
    Mutare_Drake = 153
    Boragus      = 154
    Xeron        = 155
    Corkes       = 156
    Jeremy       = 157
    Illor        = 158
    Derek        = 159
#
# Byte 21 ... (160-167)
#
    Leena      = 160
    Anabel     = 161
    Cassiopeia = 162
    Miriam     = 163
    Casmetra   = 164
    Eovacius   = 165
    Spint      = 166
    Andal      = 167
#
# Byte 22 ... (168-175)
#
    Manfred  = 168
    Zilare   = 169
    Astra    = 170
    Dargem   = 171
    Bidley   = 172
    Tark     = 173
    Elmore   = 174
    Beatrice = 175
#
# Byte 23 ... (176-183)
#
    Kinkeria  = 176
    Ranloo    = 177
    Giselle   = 178
    Henrietta = 179
    Sam       = 180
    Tancred   = 181
    Melchior  = 182
    Floribert = 183
#
# Byte 24 ... (184-191)
#
    Wynona    = 184
    Dury      = 185
    Morton    = 186
    Celestine = 187
    Todd      = 188
    Agar      = 189
    Bertram   = 190
    Wrathmont = 191
#
# Byte 25 ... (192-199)
#
    Ziph      = 192
    Victoria  = 193
    Eanswythe = 194
    Frederick = 195
    Tavin     = 196
    Murdoch   = 197
    #
    #
