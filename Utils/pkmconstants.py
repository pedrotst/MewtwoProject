from enum import Enum

""" Stats Enum for Database--------------------------------------------------
"""
class Type(Enum):
    def __str__(self):
        names = {0 : 'NoType',
                    1 : 'Bug',
                    2 : 'Dark',
                    3 : 'Dragon',
                    4 : 'Electric',
                    5 : 'Fairy',
                    6 : 'Fighting',
                    7 : 'Fire',
                    8 : 'Flying',
                    9 : 'Ghost',
                    10 : 'Grass',
                    11 : 'Ground',
                    12 : 'Ice',
                    13 : 'Normal',
                    14 : 'Poison',
                    15 : 'Psychic',
                    16 : 'Rock',
                    17 : 'Steel',
                    18 : 'Water'}
        return names[self._value_]
    def __repr__(self):
        return self.__str__()
    def __fromStr__(string):
        names = {'NoType' : 0, 'Bug' : 1,
                 'Dark' : 2, 'Dragon' : 3,
                 'Electric' : 4, 'Fairy' : 5,
                 'Fighting' : 6, 'Fire' : 7,
                 'Flying' : 8, 'Ghost' : 9,
                 'Grass' : 10, 'Ground' : 11,
                 'Ice' : 12, 'Normal' : 13,
                 'Poison' : 14, 'Psychic' : 15,
                 'Rock' : 16, 'Steel' : 17,
                 'Water' : 18}
        try:
            return Type(names[string])
        except KeyError:
            return Type.NoType

    def img_h(self):
        names = {'NoType' : None,
                 'Bug' : 'Images/Tipos/BugH.png',
                 'Dark' : 'Images/Tipos/DarkH.png',
                 'Dragon' : 'Images/Tipos/DragonH.png',
                 'Electric' : 'Images/Tipos/ElectricH.png',
                 'Fairy' : 'Images/Tipos/FairyH.png',
                 'Fighting' : 'Images/Tipos/FightingH.png',
                 'Fire' : 'Images/Tipos/FireH.png',
                 'Flying' : 'Images/Tipos/FlyingH.png',
                 'Ghost' : 'Images/Tipos/GhostH.png',
                 'Grass' : 'Images/Tipos/GrassH.png',
                  'Ground' : 'Images/Tipos/GroundH.png',
                  'Ice' : 'Images/Tipos/IceH.png',
                  'Normal' : 'Images/Tipos/NormalH.png',
                  'Poison' : 'Images/Tipos/PoisonH.png',
                  'Psychic' : 'Images/Tipos/PsychicH.png',
                  'Rock' : 'Images/Tipos/RockH.png',
                  'Steel' : 'Images/Tipos/SteelH.png',
                  'Water' : 'Images/Tipos/WaterH.png'}
        return names[str(self)]
        
    def img_v(self):
        names = {'NoType' : None,
                 'Bug' : 'Images/Tipos/BugV.png',
                 'Dark' : 'Images/Tipos/DarkV.png',
                 'Dragon' : 'Images/Tipos/DragonV.png',
                 'Electric' : 'Images/Tipos/ElectricV.png',
                 'Fairy' : 'Images/Tipos/FairyV.png',
                 'Fighting' : 'Images/Tipos/FightingV.png',
                 'Fire' : 'Images/Tipos/FireV.png',
                 'Flying' : 'Images/Tipos/FlyingV.png',
                 'Ghost' : 'Images/Tipos/GhostV.png',
                 'Grass' : 'Images/Tipos/GrassV.png',
                  'Ground' : 'Images/Tipos/GroundV.png',
                  'Ice' : 'Images/Tipos/IceV.png',
                  'Normal' : 'Images/Tipos/NormalV.png',
                  'Poison' : 'Images/Tipos/PoisonV.png',
                  'Psychic' : 'Images/Tipos/PsychicV.png',
                  'Rock' : 'Images/Tipos/RockV.png',
                  'Steel' : 'Images/Tipos/SteelV.png',
                  'Water' : 'Images/Tipos/WaterV.png'}
        return names[str(self)]

    NoType = 0
    Bug = 1
    Dark = 2
    Dragon = 3
    Electric = 4
    Fairy = 5
    Fighting = 6
    Fire = 7
    Flying = 8
    Ghost = 9
    Grass = 10
    Ground = 11
    Ice = 12
    Normal = 13
    Poison = 14
    Psychic = 15
    Rock = 16
    Steel = 17
    Water = 18

""" Stat Class for Database--------------------------------------------------
"""
class Stat(Enum):
    def __str__(self):
        names = {0 : 'NoType',
                    1 : 'HP',
                    2 : 'Attack',
                    3 : 'Defense',
                    4 : 'Sp. Attack',
                    5 : 'Sp. Defense',
                    6 : 'Speed'}
        return names[self._value_]
    def __repr__(self):
        return self.__str__()
    def __fromStr__(string):
        names = {'NoType' : 0,
                 'HP' : 1,
                 'Attack' : 2,
                 'Defense' : 3,
                 'Sp. Attack' : 4,
                 'Sp. Defense' : 5,
                 'Speed' : 6,}
        try:
            return Stat(names[string])
        except KeyError:
            return Stat.NoType

        
    NoType = 0
    Hp = 1
    Atk = 2
    Defense = 3
    SpAtk = 4
    SpDef = 5
    Spd = 6

""" Stat Class for Database--------------------------------------------------
"""
class EggGroup(Enum):
    def __str__(self):
        names = {0  : 'NoType',
                 1  : 'Not Breedable',
                 2  : 'Bug',
                 3  : 'Flying',
                 4  : 'Human-like',
                 5  : 'Mineral',
                 6  : 'Amorphous',
                 7  : 'Ditto',
                 8  : 'Dragon',
                 9  : 'Fairy',
                 10 : 'Field',
                 11 : 'Grass',
                 12 : 'Monster',
                 13 : 'Water 1',
                 14 : 'Water 2',
                 15 : 'Water 3'}
        return names[self._value_]
    def __repr__(self):
        return self.__str__()
    def __fromStr__(string):
        names = { 'NoType'          : 0,
                  'Not Breedable'   : 1,
                  'Bug'             : 2,
                  'Flying'          : 3,
                  'Human-like'       : 4,
                  'Mineral'         : 5,
                  'Amorphous'       : 6,
                  'Ditto'           : 7,
                  'Dragon'          : 8,
                  'Fairy'           : 9,
                  'Field'           : 10,
                  'Grass'           : 11,
                  'Monster'         : 12,
                  'Water 1'          : 13,
                  'Water 2'          : 14,
                  'Water 3'          : 15}
        try:
            return EggGroup(names[string])
        except KeyError:
            return EggGroup.NoType

        
    NoType          = 0
    NotBreedable    = 1
    Bug             = 2
    Flying          = 3
    Humanlike       = 4
    Mineral         = 5
    Amorphous       = 6
    Ditto           = 7
    Dragon          = 8
    Fairy           = 9
    Field           = 10
    Grass           = 11
    Monster         = 12
    Water1          = 13
    Water2          = 14
    Water3          = 15

""" Attack Types Class for Database--------------------------------------------------
"""
class AttackCat(Enum):
    def __str__(self):
        names = {0 : 'Other',
                    1 : 'Physical',
                    2 : 'Special'}
        return names[self._value_]
    def __repr__(self):
        return self.__str__()
    def __fromStr__(string):
        names = {'Other' : 0,
                 'Physical' : 1,
                 'Special' : 2}
        try:
            return AttackCat(names[string])
        except KeyError:
            return AttackCat.Other

        
    Other = 0
    Physical = 1
    Special = 2
