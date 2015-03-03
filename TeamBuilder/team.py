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
        self.__img = pkm.get_image_path()
        self.__lvl = 100
        self.__gender = pkm.get_gender().get_most_common()
        self.__is_shinny = False
        self.__base_stats = pkm.get_stats()
        self.__types = pkm.get_types()
        self.__abilities_possible = pkm.get_abilities()
        self.__attacks_possible = pkm.get_attacks()
        self.__weaknesses = pkm.get_weaknesses()
        self.__ability = None
        self.__attacks = Utils.teamutils.Attacks()
        self.__ivs = Utils.teamutils.IVs()
        self.__evs = Utils.teamutils.EVs()
        self.__nature = constants.Nature.NoNature
        self.__stats = Utils.teamutils.Stats(self.__lvl,
                                             self.__base_stats,
                                             self.__ivs,
                                             self.__evs,
                                             self.__nature)

    def get_name(self):
        """
        Return the name of the member
        :return:
        """
        return self.__name

    def get_nickname(self):
        """
        Return the nichname, if no nickname was set, return the pokemon name
        :return:
        """
        if self.__nickname == '':
            return self.__name
        else:
            return self.__nickname

    def set_nickname(self, n_nickname):
        """
        Set a new nickname with the value n_nickname
        :param n_nickname: str
        :return:
        """
        self.__nickname = n_nickname

    def get_img(self):
        """
        Get the paths of the imgs
        :return: The PokeImg class
        """
        return self.__img

    def get_lvl(self):
        """
        Return the lvl
        :return:
        """
        return self.__lvl

    def set_lvl(self, n_lvl):
        """
        Set a new level with the value n_lvl
        :param n_lvl: str
        :return:
        """
        self.__lvl = n_lvl

    def get_types(self):
        """
        Return the types of the pokemon
        :return: The pokemon types
        """
        return self.__types

    def set_ability(self, ability_name):
        """
        Set one of the possible abilities
        """
        ability = self.__abilities_possible.has_ability(ability_name)
        assert isinstance(ability, Utils.pkmutils.PokeAbility)
        self.__ability = ability

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

    def get_gender(self):
        """
        Return the pokemon gender
        :return:
        """
        return self.__gender

    def set_gender(self, poke_gender):
        """
        Set the pokemon gender
        :param poke_gender:
        :return:
        """
        self.__gender = poke_gender

    def is_shinny(self):
        """
        Return if the pokemon is shinny or not
        :return: A bool
        """
        return self.__is_shinny

    def set_shinny(self, shinny):
        """
        Set if the pokemon is shinny
        :param shinny:
        :return:
        """
        self.__is_shinny = shinny


class MemberAnalyser:
    # TODO Criar outras analises
    def __init__(self, member):
        self.__member = member
        self.__coverage = Utils.teamutils.Coverage(member)
        self.__resistance = Utils.teamutils.Resistance(member.get_weaknesses())

    def get_coverage(self):
        """
        Returns the coverage of the member
        :return:
        """
        return self.__coverage

    def get_resistance(self):
        """
        Returns the resistance of the member
        :return:
        """
        return self.__resistance


class TeamAnalyser:
    def __init__(self, team):
        self.__team = team
        self.__team_analysed = [MemberAnalyser(member) for member in team]

        self.__team_coverage = None

        self.__team_resistance = None

        self.__stats_rank = {}
        self.__team_stats = Utils.teamutils.TeamStats()

    def analyse_team_coverage(self):
        """
        Analyses the team coverage
        """
        coverages = [member.get_coverage() for member in self.__team_analysed]
        for cover in coverages:
            self.__team_coverage = cover | self.__team_coverage

    def get_physical_coverage(self):
        """
        Return a tuple with the first value being the positive and the second being the negative physical coverage
        :return: A tuple
        """
        return self.__team_coverage.get_physical_coverage()

    def get_special_coverage(self):
        """
        Return a tuple with the first value being the positive and the second being the negative special coverage
        :return: A tuple
        """
        return self.__team_coverage.get_special_coverage()

    def get_coverage(self):
        """
        Return all in concern to the complete coverage
        :return int, set, set
        :rtype int, set, set
        """
        return self.__team_coverage.get_coverage()

    def get_coverage_power(self):
        """
        A tuple with the sum of the attacks
        :return Tuple of ints
        :rtype int, int
        """
        return self.__team_coverage.get_power()

    def get_coverage_effects(self):
        """
        Get all the effects the pokemon causes with its attacks
        :return: A list of effects
        """
        self.__team_coverage.get_effects()

    def analyse_team_weaknesses(self):
        """
        Calculate the teams greatest weaknesses and resistances
        """
        resistances = [analysed.get_resistance() for analysed in self.__team_analysed]
        for resistance in resistances:
            self.__team_resistance = resistance + self.__team_resistance

    def get_weaknesses(self):
        """
        Return the weaknesses of the team
        """
        return self.__team_resistance.get_weaknesses()

    def get_greatest_weaknesses(self):
        """
        Return a tuple with the first value being the names of the greatest weaknesses and the second being the value
        :return:
        """
        return self.__team_resistance.get_greatest_weaknesses()

    def get_greatest_resistances(self):
        """
        Return a tuple with the first value being the names of the greatest resistances and the second being the value
        :return:
        """
        return self.__team_resistance.get_greatest_resistances()

    def get_type_resistance(self):
        """
        Return the resistance of the pokemon, it's a value tha represents the overall resistance against types of the
        pokemon. The greater the value the better, a resistance of 1 means that the pokemon is neutral, smaller tha one
        means that pokemon is very not resistant and greater than one mean that it is very resistance
        :return:
        """
        return self.__team_resistance.get_type_resistance()

    def analyse_stats(self):
        """
        Analyses the team stats and ranks
        :return:
        """
        for stat in Utils.pkmconstants.Stat:
            if stat == Utils.pkmutils.Stat.NoType:
                continue
            rank = sorted(self.__team, key=lambda member1: member1.get_stats()[stat], reverse=True)
            self.__stats_rank[str(stat)] = list(map(lambda name: name.get_name(), rank))
            values = map(lambda name: name.get_stats()[stat], rank)
            self.__team_stats[stat] = sum(values)

    def get_team_stats(self):
        """
        Returns the summed stats of the whole team
        :return: The TeamStats
        """
        return self.__team_stats


if __name__ == '__main__':
    p = [TeamMember('Blaziken'), TeamMember('Azumarill'), TeamMember('Galvantula'),
         TeamMember('Gliscor'), TeamMember('Ferrothorn'), TeamMember('Magnezone')]
    p[0].set_attack(1, 'Low Kick')
    p[0].set_attack(2, 'Flare Blitz')
    p[0].set_attack(3, 'Protect')
    p[0].set_attack(4, 'Knock Off')

    p[1].set_attack(1, 'Play Rough')
    p[1].set_attack(2, 'Waterfall')
    p[1].set_attack(3, 'Aqua Jet')
    p[1].set_attack(4, 'Knock Off')

    p[2].set_attack(1, 'Sticky Web')
    p[2].set_attack(2, 'Thunder')
    p[2].set_attack(3, 'Bug Buzz')
    p[2].set_attack(4, 'Thunder Wave')

    p[3].set_attack(1, 'Substitute')
    p[3].set_attack(2, 'Toxic')
    p[3].set_attack(3, 'Protect')
    p[3].set_attack(4, 'Earthquake')

    p[4].set_attack(1, 'Stealth Rock')
    p[4].set_attack(2, 'Leech Seed')
    p[4].set_attack(3, 'Gyro Ball')
    p[4].set_attack(4, 'Thunder Wave')

    p[5].set_attack(1, 'Volt Switch')
    p[5].set_attack(2, 'Hidden Power')
    p[5].set_attack(3, 'Flash Cannon')
    p[5].set_attack(4, 'Magnet Rise')

    a = TeamAnalyser(p)
    e = Utils.pkmutils.PokeWeaknesses()
    a.analyse_team_weaknesses()
    print('Team info-----------------------------------------------------------------')
    for j in range(0, 2):
        print('Name:', p[j].get_name(), 'Nickname:', p[j].get_nickname())
        for i in range(1, 5):
            print(p[j].get_attack(i).get_name())
    print('Attacks statistics-------------------------------------------------------')
    a.analyse_team_coverage()
    print('Defenses statistics------------------------------------------------------')
    print('Team Weaknesses: ', a.get_weaknesses())
    print('Greatest Weaknesses: ', a.get_greatest_weaknesses())
    print('Greatest Resistances: ', a.get_greatest_resistances())
    print(a.get_type_resistance())
    a.analyse_stats()
    print([a.get_team_stats()[i] for i in range(0, 6)])
