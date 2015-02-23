from Pokedex.pokemon import Pokemon
import Utils.teamutils


class AttackNotFoundError(Exception):
    pass


class TeamMember:
    """
    Class used to represent each team member of a pokemon team
    """
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
        self.__attacks = Utils.teamutils.Attacks()
        self.__ivs = Utils.teamutils.IVs()

    def set_attack(self, index, atk_name):
        """Define the pokemon attacks, it checks if the pokemon can learn that attack
        :param index: The position of the attack (as in game), each pokemon can learn only 4 attacks (from 1 to 4)
        :type index: int
        :param atk_name: The name of the attack to be selected to the attack position index
        :type atk_name: str
        """
        attack = self.__attacks_possible[atk_name]
        assert isinstance(attack, Utils.pkmutils.Attack)
        self.__attacks[index] = attack

    def get_attack(self, index):
        """Retrieve attack from attacks learned
        :param index: Positions of the attack
        :type index: int
        :return: The Attack
        :rtype: Utils.pkmutils.Attack
        """
        return self.__attacks[index]

if __name__ == '__main__':
    c = TeamMember('Pikachu')
    c.set_attack(1, 'Thunder')
    d = Utils.teamutils.EVs()
    d['Sp Attack'] = 45
    d['Sp Defense'] = 252
    d['Speed'] = 252
    print(d['Speed'])
    print(d['Total'])

