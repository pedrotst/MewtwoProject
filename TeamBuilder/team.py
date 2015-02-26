import Pokedex.pokemon as pokedex
import Utils.pkmutils
import Utils.pkmconstants as constants
import Utils.teamutils


class Team:
    """
    A class that represents a team of pokemon
    """

    def __init__(self, team=None):
        """
        Initialize the team, if the team if given it will be attributed
        :param team: The new team
        """
        self.__my_team = [None, None, None, None, None, None]
        if team:
            i = 0
            for member in team:
                self[i] = member
                i += 1

    def __getitem__(self, item):
        """
        Retrieve each team member
        :param item: the index of the team member
        :return: The team member
        """
        return self.__my_team[item]

    def __setitem__(self, key, value):
        """
        Set a team member in position key with the member value
        :param key: The index of the pokemon
        :type key: int
        :param value:
        :type value: str or pokedex.Pokemon.Pokemon or teammember.TeamMember
        """
        if isinstance(value, str):
            value = TeamMember(value)
        elif isinstance(value, pokedex.Pokemon):
            value = TeamMember(poke=value)
        if isinstance(value, TeamMember):
            self.__my_team[key] = value
        else:
            raise TypeError('value is not str, Pokemon or TeamMember')


class AttackNotFoundError(Exception):
    pass


class TeamMember:
    """
    Class used to represent each team member of a pokemon team
    """
    def __init__(self, pkm_name=None, poke=None):
        if pkm_name:
            # Get data from Database
            pkm = pokedex.Pokemon(pkm_name)
        elif isinstance(poke, pokedex.Pokemon):
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


class TeamAnalyser:
    def __init__(self, team):
        self.__team = team
        self.__team_weaknesses = Utils.pkmutils.PokeWeaknesses()
        self.__greatest_weaknesses = []
        self.__greatest_weaknesses_value = 0
        self.__greatest_resistances = []
        self.__greatest_resistances_value = 0
        self.__positive_physical_coverage = {}
        self.__positive_special_coverage = {}
        self.__negative_physical_coverage = {}
        self.__negative_special_coverage = {}
        self.__effects_coverage = []

    def calculate_team_coverage(self):
        """
        Calculate which types the team hits super effectively
        """
        for member in self.__team:
            for i in range(1, 5):
                attack = member.get_attack(i)
                category = attack.get_cat()
                if category == 'Physical':
                    for weak in constants.WeaknessesTable()[attack.get_type()]:
                        attack_advantage = constants.WeaknessesTable()[attack.get_type()][weak]
                        if attack_advantage > 1:
                            if weak in self.__positive_physical_coverage:
                                self.__positive_physical_coverage[weak] *= attack_advantage
                            else:
                                self.__positive_physical_coverage[weak] = attack_advantage
                        elif attack_advantage < 1:
                            if weak in self.__negative_physical_coverage:
                                self.__negative_physical_coverage[weak] *= attack_advantage
                            else:
                                self.__negative_physical_coverage[weak] = attack_advantage

                elif category == 'Special':
                    for weak in constants.WeaknessesTable()[attack.get_type()]:
                        attack_advantage = constants.WeaknessesTable()[attack.get_type()][weak]
                        if attack_advantage > 1:
                            if weak in self.__positive_special_coverage:
                                self.__positive_special_coverage[weak] *= attack_advantage
                            else:
                                self.__positive_special_coverage[weak] = attack_advantage
                        elif attack_advantage < 1:
                            if weak in self.__negative_special_coverage:
                                self.__negative_special_coverage[weak] *= attack_advantage
                            else:
                                self.__negative_special_coverage[weak] = attack_advantage

                elif category == 'Other':
                    self.__effects_coverage.append(attack.get_description())
        print('Positive Physical Coverage: ', self.__positive_physical_coverage)
        print('Negative Physical Coverage: ', self.__negative_physical_coverage)
        print('Positive Special Coverage: ', self.__positive_special_coverage)
        print('Negative Special Coverage: ', self.__negative_special_coverage)
        print('Effects: ', self.__effects_coverage)

    def get_physical_coverage(self):
        """
        Return a tuple with the first value being the positive and the second being the negative physical coverage
        :return: A tuple
        """
        return self.__positive_physical_coverage, self.__negative_physical_coverage

    def get__coverage(self):
        """
        Return a tuple with the first value being the positive and the second being the negative physical coverage
        :return: A tuple
        """
        return self.__positive_physical_coverage, self.__negative_physical_coverage

    def calculate_team_weaknesses(self):
        """
        Calculate the teams greatest weaknesses and resistances
        """
        for member in self.__team:
            if member:
                self.__team_weaknesses *= member.get_weaknesses()
        self.__greatest_weaknesses = self.__team_weaknesses.max_values()
        self.__greatest_weaknesses_value = max(self.__team_weaknesses)
        self.__greatest_resistances = self.__team_weaknesses.min_values()
        self.__greatest_resistances_value = min(self.__team_weaknesses)

    def get_weaknesses(self):
        """
        Return the weaknesses of the team
        """
        return self.__team_weaknesses

    def get_greatest_weaknesses(self):
        """
        Return a tuple with the first value being the names of the greatest weaknesses and the second being the value
        :return:
        """
        return self.__greatest_weaknesses, self.__greatest_weaknesses_value

    def get_greatest_resistances(self):
        """
        Return a tuple with the first value being the names of the greatest resistances and the second being the value
        :return:
        """
        return self.__greatest_resistances, self.__greatest_resistances_value

if __name__ == '__main__':
    p = [TeamMember('Pikachu'), TeamMember('Blaziken')]
    p[0].set_attack(1, 'Thunder')
    p[0].set_attack(2, 'Thunderbolt')
    p[0].set_attack(3, 'Slam')
    p[0].set_attack(4, 'Agility')
    p[1].set_attack(1, 'Flare Blitz')
    p[1].set_attack(2, 'Brave Bird')
    p[1].set_attack(3, 'Slash')
    p[1].set_attack(4, 'Sky Uppercut')
    a = TeamAnalyser(p)
    e = Utils.pkmutils.PokeWeaknesses()
    a.calculate_team_weaknesses()
    print('Attacks statistics-------------------------------------------------------')
    a.calculate_team_coverage()
    print('Defenses statistics------------------------------------------------------')
    print('Team Weaknesses: ', a.get_weaknesses())
    print('Greatest Weaknesses: ', a.get_greatest_weaknesses())
    print('Greatest Resistances: ', a.get_greatest_resistances())