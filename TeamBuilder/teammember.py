from Pokedex.pokemon import Pokemon
import Utils.teamutils


class TeamMember:
    def __init__(self, pkm_name):
        # Get data from Database
        pkm = Pokemon(pkm_name)

        # Retrieve important data
        self.__name = pkm.get_name()
        self.__base_stats = pkm.get_stats()
        self.__types = pkm.get_types()
        self.__abilities = pkm.get_abilities()
        self.__attacks_possible = pkm.get_attacks()
        self.__weaknesses = pkm.get_weaknesses()
        self.__attacks = Utils.teamutils