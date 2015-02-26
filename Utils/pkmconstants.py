from enum import Enum

""" Stats Enum for Database--------------------------------------------------
"""


class Type(Enum):
    def __str__(self):
        names = {0: 'NoType',
                 1: 'Bug',
                 2: 'Dark',
                 3: 'Dragon',
                 4: 'Electric',
                 5: 'Fairy',
                 6: 'Fighting',
                 7: 'Fire',
                 8: 'Flying',
                 9: 'Ghost',
                 10: 'Grass',
                 11: 'Ground',
                 12: 'Ice',
                 13: 'Normal',
                 14: 'Poison',
                 15: 'Psychic',
                 16: 'Rock',
                 17: 'Steel',
                 18: 'Water'}
        return names[self._value_]

    def __repr__(self):
        return self.__str__()

    def __fromStr__(string):
        names = {'NoType': 0, 'Bug': 1,
                 'Dark': 2, 'Dragon': 3,
                 'Electric': 4, 'Fairy': 5,
                 'Fighting': 6, 'Fire': 7,
                 'Flying': 8, 'Ghost': 9,
                 'Grass': 10, 'Ground': 11,
                 'Ice': 12, 'Normal': 13,
                 'Poison': 14, 'Psychic': 15,
                 'Rock': 16, 'Steel': 17,
                 'Water': 18}
        try:
            return Type(names[string])
        except KeyError:
            return Type.NoType

    def img_h(self):
        names = {'NoType': None,
                 'Bug': 'Images/Tipos/BugH.png',
                 'Dark': 'Images/Tipos/DarkH.png',
                 'Dragon': 'Images/Tipos/DragonH.png',
                 'Electric': 'Images/Tipos/ElectricH.png',
                 'Fairy': 'Images/Tipos/FairyH.png',
                 'Fighting': 'Images/Tipos/FightingH.png',
                 'Fire': 'Images/Tipos/FireH.png',
                 'Flying': 'Images/Tipos/FlyingH.png',
                 'Ghost': 'Images/Tipos/GhostH.png',
                 'Grass': 'Images/Tipos/GrassH.png',
                 'Ground': 'Images/Tipos/GroundH.png',
                 'Ice': 'Images/Tipos/IceH.png',
                 'Normal': 'Images/Tipos/NormalH.png',
                 'Poison': 'Images/Tipos/PoisonH.png',
                 'Psychic': 'Images/Tipos/PsychicH.png',
                 'Rock': 'Images/Tipos/RockH.png',
                 'Steel': 'Images/Tipos/SteelH.png',
                 'Water': 'Images/Tipos/WaterH.png'}
        return names[str(self)]

    def img_v(self):
        names = {'NoType': None,
                 'Bug': 'Images/Tipos/BugV.png',
                 'Dark': 'Images/Tipos/DarkV.png',
                 'Dragon': 'Images/Tipos/DragonV.png',
                 'Electric': 'Images/Tipos/ElectricV.png',
                 'Fairy': 'Images/Tipos/FairyV.png',
                 'Fighting': 'Images/Tipos/FightingV.png',
                 'Fire': 'Images/Tipos/FireV.png',
                 'Flying': 'Images/Tipos/FlyingV.png',
                 'Ghost': 'Images/Tipos/GhostV.png',
                 'Grass': 'Images/Tipos/GrassV.png',
                 'Ground': 'Images/Tipos/GroundV.png',
                 'Ice': 'Images/Tipos/IceV.png',
                 'Normal': 'Images/Tipos/NormalV.png',
                 'Poison': 'Images/Tipos/PoisonV.png',
                 'Psychic': 'Images/Tipos/PsychicV.png',
                 'Rock': 'Images/Tipos/RockV.png',
                 'Steel': 'Images/Tipos/SteelV.png',
                 'Water': 'Images/Tipos/WaterV.png'}
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
        names = {0: 'NoType',
                 1: 'HP',
                 2: 'Attack',
                 3: 'Defense',
                 4: 'Sp. Attack',
                 5: 'Sp. Defense',
                 6: 'Speed'}
        return names[self._value_]

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_str(string):
        """
        :param string:
        :type string: str
        :return:
        """
        names = {'NoType': 0,
                 'HP': 1,
                 'Attack': 2,
                 'Defense': 3,
                 'Sp. Attack': 4,
                 'Sp. Defense': 5,
                 'Speed': 6}
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
        names = {0: 'NoType',
                 1: 'Not Breedable',
                 2: 'Bug',
                 3: 'Flying',
                 4: 'Human-like',
                 5: 'Mineral',
                 6: 'Amorphous',
                 7: 'Ditto',
                 8: 'Dragon',
                 9: 'Fairy',
                 10: 'Field',
                 11: 'Grass',
                 12: 'Monster',
                 13: 'Water 1',
                 14: 'Water 2',
                 15: 'Water 3'}
        return names[self._value_]

    def __repr__(self):
        return self.__str__()

    def __fromStr__(string):
        names = {'NoType': 0,
                 'Not Breedable': 1,
                 'Bug': 2,
                 'Flying': 3,
                 'Human-like': 4,
                 'Mineral': 5,
                 'Amorphous': 6,
                 'Ditto': 7,
                 'Dragon': 8,
                 'Fairy': 9,
                 'Field': 10,
                 'Grass': 11,
                 'Monster': 12,
                 'Water 1': 13,
                 'Water 2': 14,
                 'Water 3': 15}
        try:
            return EggGroup(names[string])
        except KeyError:
            return EggGroup.NoType


    NoType = 0
    NotBreedable = 1
    Bug = 2
    Flying = 3
    Humanlike = 4
    Mineral = 5
    Amorphous = 6
    Ditto = 7
    Dragon = 8
    Fairy = 9
    Field = 10
    Grass = 11
    Monster = 12
    Water1 = 13
    Water2 = 14
    Water3 = 15


""" Attack Types Class for Database--------------------------------------------------
"""


class AttackCat(Enum):
    def __str__(self):
        names = {0: 'Other',
                 1: 'Physical',
                 2: 'Special'}
        return names[self._value_]

    def __repr__(self):
        return self.__str__()

    def __fromStr__(string):
        names = {'Other': 0,
                 'Physical': 1,
                 'Special': 2}
        try:
            return AttackCat(names[string])
        except KeyError:
            return AttackCat.Other


    Other = 0
    Physical = 1
    Special = 2


""" Nature Enumeration--------------------------------------------------
"""


class Nature(Enum):
    """
    Class that has the possible natures and it's boosting and hindering attacks
    """

    def get_increased_stat(self):
        """
        Returns which stat the nature influence positively
        :return: Stat
        """
        increased_stats = [Stat.NoType, Stat.NoType, Stat.Atk, Stat.Atk, Stat.Atk, Stat.Atk, Stat.Defense, Stat.NoType,
                           Stat.Defense, Stat.Defense, Stat.Defense, Stat.Spd, Stat.Spd, Stat.NoType, Stat.Spd,
                           Stat.Spd, Stat.SpAtk, Stat.SpAtk, Stat.SpAtk, Stat.NoType, Stat.SpAtk, Stat.SpDef,
                           Stat.SpDef, Stat.SpDef, Stat.SpDef, Stat.NoType]
        return increased_stats[self.value]

    def get_decreased_stat(self):
        """
        Returns which stat the nature influence negatively
        :return: Stat
        """
        increased_stats = [Stat.NoType, Stat.NoType, Stat.Defense, Stat.Spd, Stat.SpAtk, Stat.SpDef, Stat.Atk,
                           Stat.NoType, Stat.Spd, Stat.SpAtk, Stat.SpDef, Stat.Atk, Stat.Defense, Stat.NoType,
                           Stat.SpAtk, Stat.SpDef, Stat.Atk, Stat.Defense, Stat.Spd, Stat.NoType, Stat.SpDef, Stat.Atk,
                           Stat.Defense, Stat.Spd, Stat.SpAtk, Stat.NoType]
        return increased_stats[self.value]

    NoNature = 0
    Hardy = 1
    Lonely = 2
    Brave = 3
    Adamant = 4
    Naughty = 5
    Bold = 6
    Docile = 7
    Relaxed = 8
    Impish = 9
    Lax = 10
    Timid = 11
    Hasty = 12
    Serious = 13
    Jolly = 14
    Naive = 15
    Modest = 16
    Mild = 17
    Quiet = 18
    Bashful = 19
    Rash = 20
    Calm = 21
    Gentle = 22
    Sassy = 23
    Careful = 24
    Quirky = 25


""" Weaknesses Table Enumeration--------------------------------------------------
"""


class WeaknessesTable:
    def __init__(self):
        """
        A table with the relation of [attack][defense] of the types
        """
        self.__table = {
            'Normal': {
                'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 1,
                'Ground': 1, 'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 0.5, 'Ghost': 0, 'Dragon': 1, 'Dark': 1,
                'Steel': 0.5, 'Fairy': 1
            }, 'Fire': {
                'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Electric': 1, 'Grass': 2, 'Ice': 2, 'Fighting': 1, 'Poison': 1,
                'Ground': 1, 'Flying': 1, 'Psychic': 1, 'Bug': 2, 'Rock': 0.5, 'Ghost': 1, 'Dragon': 0.5, 'Dark': 1,
                'Steel': 2, 'Fairy': 1
            }, 'Water': {
                'Normal': 1, 'Fire': 2, 'Water': 0.5, 'Electric': 1, 'Grass': 0.5, 'Ice': 1, 'Fighting': 1, 'Poison': 1,
                'Ground': 2, 'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 2, 'Ghost': 1, 'Dragon': 0.5, 'Dark': 1,
                'Steel': 1, 'Fairy': 1
            }, 'Electric': {
                'Normal': 1, 'Fire': 1, 'Water': 2, 'Electric': 0.5, 'Grass': 0.5, 'Ice': 1, 'Fighting': 1, 'Poison': 1,
                'Ground': 0, 'Flying': 2, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 0.5, 'Dark': 1,
                'Steel': 1, 'Fairy': 1
            }, 'Grass': {
                'Normal': 1, 'Fire': 0.5, 'Water': 2, 'Electric': 1, 'Grass': 0.5, 'Ice': 1, 'Fighting': 1, 'Poison': 0.5,
                'Ground': 2, 'Flying': 0.5, 'Psychic': 1, 'Bug': 0.5, 'Rock': 2, 'Ghost': 1, 'Dragon': 0.5, 'Dark': 1,
                'Steel': 0.5, 'Fairy': 1
            }, 'Ice': {
                'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Electric': 1, 'Grass': 2, 'Ice': 0.5, 'Fighting': 1, 'Poison': 1,
                'Ground': 2, 'Flying': 2, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 2, 'Dark': 1,
                'Steel': 0.5, 'Fairy': 1
            }, 'Fighting': {
                'Normal': 2, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 2, 'Fighting': 1, 'Poison': 0.5,
                'Ground': 1, 'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 'Rock': 2, 'Ghost': 0, 'Dragon': 1, 'Dark': 2,
                'Steel': 2, 'Fairy': 0.5
            }, 'Poison': {
                'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 2, 'Ice': 1, 'Fighting': 1, 'Poison': 0.5,
                'Ground': 0.5, 'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 0.5, 'Ghost': 0.5, 'Dragon': 1, 'Dark': 1,
                'Steel': 0, 'Fairy': 2
            }, 'Ground': {
                'Normal': 1, 'Fire': 2, 'Water': 1, 'Electric': 2, 'Grass': 0.5, 'Ice': 1, 'Fighting': 1, 'Poison': 2,
                'Ground': 1, 'Flying': 0, 'Psychic': 1, 'Bug': 0.5, 'Rock': 2, 'Ghost': 1, 'Dragon': 1, 'Dark': 1,
                'Steel': 2, 'Fairy': 1
            }, 'Flying': {
                'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 0.5, 'Grass': 2, 'Ice': 1, 'Fighting': 2, 'Poison': 1,
                'Ground': 1, 'Flying': 1, 'Psychic': 1, 'Bug': 2, 'Rock': 0.5, 'Ghost': 1, 'Dragon': 1, 'Dark': 1,
                'Steel': 0.5, 'Fairy': 1
            }, 'Psychic': {
                'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 2, 'Poison': 2,
                'Ground': 1, 'Flying': 1, 'Psychic': 0.5, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 0,
                'Steel': 0.5, 'Fairy': 1
            }, 'Bug': {
                'Normal': 1, 'Fire': 0.5, 'Water': 1, 'Electric': 1, 'Grass': 2, 'Ice': 1, 'Fighting': 0.5, 'Poison': 0.5,
                'Ground': 1, 'Flying': 0.5, 'Psychic': 2, 'Bug': 1, 'Rock': 1, 'Ghost': 0.5, 'Dragon': 1, 'Dark': 2,
                'Steel': 0.5, 'Fairy': 0.5
            }, 'Rock': {
                'Normal': 1, 'Fire': 2, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 2, 'Fighting': 0.5, 'Poison': 1,
                'Ground': 0.5, 'Flying': 2, 'Psychic': 1, 'Bug': 2, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 1,
                'Steel': 0.5, 'Fairy': 1
            }, 'Ghost': {
                'Normal': 0, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 1,
                'Ground': 1, 'Flying': 1, 'Psychic': 2, 'Bug': 1, 'Rock': 1, 'Ghost': 2, 'Dragon': 1, 'Dark': 0.5,
                'Steel': 1, 'Fairy': 1
            }, 'Dragon': {
                'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 1,
                'Ground': 1, 'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 2, 'Dark': 1,
                'Steel': 0.5, 'Fairy': 0
            }, 'Dark': {
                'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 0.5, 'Poison': 1,
                'Ground': 1, 'Flying': 1, 'Psychic': 2, 'Bug': 1, 'Rock': 1, 'Ghost': 2, 'Dragon': 1, 'Dark': 0.5,
                'Steel': 1, 'Fairy': 0.5
            }, 'Steel': {
                'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Grass': 1, 'Ice': 2, 'Fighting': 1, 'Poison': 1,
                'Ground': 1, 'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 2, 'Ghost': 1, 'Dragon': 1, 'Dark': 1,
                'Steel': 0.5, 'Fairy': 2
            }, 'Fairy': {
                'Normal': 1, 'Fire': 0.5, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 2, 'Poison': 0.5,
                'Ground': 1, 'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 2, 'Dark': 2,
                'Steel': 0.5, 'Fairy': 1
            }}

    def __getitem__(self, item):
        return self.__table[item]