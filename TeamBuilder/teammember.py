from Pokedex.pokemon import Pokemon
import Utils.teamutils
import Utils.pkmconstants as constants


class AttackNotFoundError(Exception):
    pass


class TeamMember:
    """
    Class used to represent each team member of a pokemon team
    """
    def __init__(self, pkm_name=None, poke=None):
        if pkm_name:
            # Get data from Database
            pkm = Pokemon(pkm_name)
        elif isinstance(poke, Pokemon):
            pkm = poke
        else:
            raise TypeError('Type is not consistent')

        # Retrieve important data
        self.__name = pkm.get_name()
        self.__nickname = ''
        self.__lvl = 100
        self.__base_stats = pkm.get_stats()
        self.__types = pkm.get_types()
        self.__abilities = pkm.get_abilities()
        self.__attacks_possible = pkm.get_attacks()
        self.__weaknesses = pkm.get_weaknesses()
        self.__attacks = Utils.teamutils.Attacks()
        self.__ivs = Utils.teamutils.IVs()
        self.__evs = Utils.teamutils.EVs()
        self.__nature = constants.Nature.NoNature
        self.__stats = Utils.teamutils.Stats(self.__lvl,
                                             self.__base_stats,
                                             self.__ivs,
                                             self.__evs,
                                             self.__nature)

    def get_weaknesses(self):
        """
        Getter of the weaknesses of the pokemon
        :return: The weaknesses
        """
        return self.__weaknesses

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

    def set_iv(self, name, value):
        """ Set the pokemon iv of the type name with value
        :param name: Name of the iv to be set
        :type name: str or int or constants.Stat
        :param value: The new value os the iv
        :type value: int
        """
        self.__ivs[name] = value
        self.__stats.calculate_stats()

    def get_iv(self, name):
        """ Return the value of IV name
        :param name: The name of the iv to be get
        :type name: str or int or constants.Stat
        :return: The value of the iv
        :rtype: int
        """
        return self.__ivs[name]

    def set_ev(self, name, value):
        """ Set the pokemon ev of the type name with value
        :param name: Name of the ev to be set
        :type name: str
        :param value: The new value os the ev
        :type value: int
        """
        self.__evs[name] = value
        self.__stats.calculate_stats()

    def get_ev(self, name):
        """ Return the value of IV name
        :param name: The name of the ev to be get
        :type name: str
        :return: The value of the ev
        :rtype: int
        """
        return self.__evs[name]

    def set_nature(self, nature):
        """
        Set the nature of the pokemon
        :param nature: The nature to be set
        :type nature: constants.Nature
        """
        assert isinstance(nature, constants.Nature)
        self.__nature = nature
        self.__stats.set_nature(nature)
        self.__stats.calculate_stats()

    def get_nature(self):
        """
        Return the nature of the pokemon
        :return: The nature of the pokemon
        :rtype constants.Nature
        """
        return self.__nature

    def get_stats(self):
        """
        return a reference to pokemon stats
        :return: The pokemon Stats
        """
        return self.__stats

if __name__ == '__main__':
    c = TeamMember('Blaziken')

    c.set_iv('HP', 31)
    c.set_iv('Attack', 31)
    c.set_iv('Defense', 31)
    c.set_iv('Sp. Attack', 31)
    c.set_iv('Sp. Defense', 31)
    c.set_iv('Speed', 31)

    c.set_ev('HP', 4)
    c.set_ev('Attack', 252)
    c.set_ev('Defense', 0)
    c.set_ev('Sp. Attack', 0)
    c.set_ev('Sp. Defense', 0)
    c.set_ev('Speed', 252)

    print(c.get_iv('HP'))
    print(c.get_ev('Total'))
    c.set_nature(constants.Nature.Jolly)
    print(c.get_nature())
    print(c.get_stats()['HP'])
    print(c.get_stats()['Attack'])
    print(c.get_stats()['Defense'])
    print(c.get_stats()['Sp. Attack'])
    print(c.get_stats()['Sp. Defense'])
    print(c.get_stats()['Speed'])