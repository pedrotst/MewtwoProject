import Utils.pkmconstants as constants
import Utils.pkmutils as pkmutils


class Attacks:
    """
    Class for representing a team member attacks
    """

    def __init__(self):
        self.__attacks = [None, None,
                          None, None]

    def __setitem__(self, key, value):
        """ Set the attacks of the list at key position(must be between 1 and 4)
        :param key: The number of the attack
        :type key: int
        :param value: The attack to be attributed
        :type value: Utils.pkmutils.Attack
        """
        assert isinstance(key, int)
        if 0 < key < 5:
            self.__attacks[key - 1] = value
        else:
            raise KeyError('Key must be between 1 and 4')

    def __getitem__(self, item):
        """Retrieve an attack from the attack list in item position (between 1 and 4)
        :param item: The index of the attack
        :type item: int
        :return: Returns the pokemon attack
        :rtype: Utils.pkmutils.Attack
        """
        assert isinstance(item, int)
        if 0 < item < 5:
            return self.__attacks[item - 1]
        else:
            raise KeyError('Key must be between 1 and 4')


class StatsManipulator:
    """
    Class to be imported by any class that desires to work with Stats
    """

    def __init__(self):
        self._stats = {constants.Stat.Hp: 0, constants.Stat.Atk: 0,
                       constants.Stat.Defense: 0, constants.Stat.SpAtk: 0,
                       constants.Stat.SpDef: 0, constants.Stat.Spd: 0}

    def __getitem__(self, item):
        """Get the value of the stat given by item, if item is int value must be between 0 and 5
        :param item: Name of Stat
        :type item: str or constants.Stat or int
        :return: the stat asked
        :rtype: int
        """
        if isinstance(item, str):
            key = constants.Stat.from_str(item)
        elif isinstance(item, int):
            if -1 < item < 6:
                key = constants.Stat(item + 1)
            else:
                raise IndexError
        else:
            key = item
        if 0 < key.value < 7:
            return self._stats[key]
        raise IndexError

    def __setitem__(self, key, value):
        """Set the value of the stat given by key to value
        :param key: Name of Stat
        :type key: str or constants.Stat or int
        """
        if isinstance(key, str):
            key = constants.Stat.from_str(key)
        elif isinstance(key, int):
            key = constants.Stat(key)

        self._stats[key] = value


class IVs(StatsManipulator):
    """
    Store the ivs from each team member, it also updates the actual stats when iv value is updated
    """

    def __setitem__(self, key, value):
        """Set IV key with value, the value of IV must be between 0 and 31, if not it will be adjusted to the extreme
        value that is possible
        :param key: The IV to be changed
        :type key: str
        :param value: The new value
        :type value: int
        """
        if value < 0:
            value = 0
        elif value > 31:
            value = 31
        super().__setitem__(key, value)


class EVs(StatsManipulator):
    """
    Store the evs from each team member, it also updates the actual stats when ev value is updated
    """

    def __init__(self):
        super().__init__()
        self.__total = sum(self, 1)

    def __getitem__(self, item):
        """
        Adding possibility to call Total
        :param item: The ev to be get
        :return: int or str or constants.Stat
        """
        if isinstance(item, str):
            if item == 'Total':
                return self.get_total()
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        """Set EV key with value
        :param key: The EV to be changed
        :type key: str
        :param value: The new value
        :type value: int
        """
        if value > 255:
            value = 255
        elif value < 0:
            value = 0

        if value + self.get_total() - self[key] > 510:
            value = 510 - self.get_total()

        if self.__check_total():
            super().__setitem__(key, value)
            self.__set_total()

    def __check_total(self):
        """
        Check if the total surpasses 510 or is under 0, return false if it surpasses
        :return: If the value is okay
        :rtype: bool
        """
        check = sum(self)
        if -1 < check < 511:
            return True
        return False

    def __set_total(self):
        """
        Set the EV total, the total may not surpass 510
        """
        if self.__check_total():
            self.__total = sum(self)

    def get_total(self):
        """Return the total of effort value
        :return: The total of EVs
        :rtype: int
        """
        return self.__total


class Stats(StatsManipulator):
    """
    The actual stats of the pokemon
    """

    def __init__(self, lvl, base_stats, iv, ev, nature):
        super().__init__()
        assert isinstance(lvl, int) and isinstance(base_stats, pkmutils.PokeStats) and isinstance(iv, IVs) \
                and isinstance(ev, EVs) and isinstance(nature, constants.Nature)
        self.__lvl = lvl
        self.__base_stats = base_stats
        self.__iv = iv
        self.__ev = ev
        self.__nature = nature
        self.calculate_stats()

    def set_nature(self, nature):
        self.__nature = nature

    def calculate_stats(self):
        """
        Calculate the stats ic and oc are constants that change with the stat being calculated
        """
        inner_constants = [100, 0, 0, 0, 0, 0]
        outer_constants = [10, 5, 5, 5, 5, 5]
        nature_constants = self.__determine_nature_constants()
        bases = [self.__base_stats.get_hp(), self.__base_stats.get_attack(), self.__base_stats.get_defense(),
                 self.__base_stats.get_sp_attack(), self.__base_stats.get_sp_defense(), self.__base_stats.get_speed()]
        for iv, base, ev, ic, oc, nc, i in zip(self.__iv, bases, self.__ev, inner_constants, outer_constants,
                                               nature_constants, range(0, 6)):
            self[i + 1] = int((((iv + (2 * base) + ev / 4 + ic) * self.__lvl) / 100 + oc) * nc)

    def __determine_nature_constants(self):
        """
        Creates a list in which the position represents one of the stats [hp,atk,def,sp_atk,sp_def,spd] and the value
        stored is the bonus given by the nature
        exp: Naughty boosts attack hinders sp_def so [1, 1.1, 1, 1, 0.9, 1] will be return
        :return: A list with the the equivalents boosts and hinders of each nature
        """
        nature_increased_index = self.__nature.get_increased_stat()
        nature_decreased_index = self.__nature.get_decreased_stat()
        dnc = []
        for i in range(0, 6):
            if i == nature_increased_index.value - 1:
                dnc.append(1.1)
            elif i == nature_decreased_index.value - 1:
                dnc.append(0.9)
            else:
                dnc.append(1)
        return dnc


class Coverage:
    """
    A class that calculate a coverage of a given pokemon, if a member of class TeamMember is given it will be used for
    calculation, if not the values given will be used
    """

    def __init__(self, member=None,
                 pcp=None, ppc=None, npc=None,
                 scp=None, psc=None, nsc=None,
                 cp=None, pc=None, nc=None,
                 ec=None, pp=None, sp=None):
        if member:
            # Get all attacks
            attacks = [member.get_attack(i) for i in range(1, 5)]

            # Get all attacks organized in 5 lists, Physical Positive and Negative Coverages, a set with the values
            # of the types the pokemon attacks cover. Special have the same distribution and Other attacks will be a
            # list of the effects the attack causes

            self.__positive_physical_coverage, self.__negative_physical_coverage = self.__get_coverage(attacks,
                                                                                                       'Physical')

            self.__positive_special_coverage, self.__negative_special_coverage = self.__get_coverage(attacks, 'Special')

            self.__effects_coverage = [attack.get_description() for attack in attacks if attack.get_cat() == 'Other']

            # Calculate the total coverage with union of the sets

            self.__positive_coverage = self.__positive_special_coverage | self.__positive_physical_coverage

            self.__negative_coverage = self.__negative_special_coverage | self.__negative_physical_coverage

            # Calculate the sum of the raw attack power of both special and physical power

            self.__physical_power = sum([attack.get_att() for attack in attacks if attack.get_att() != 951
                                         and attack.get_cat() == 'Physical'])

            self.__special_power = sum([attack.get_att() for attack in attacks if attack.get_att() != 951
                                        and attack.get_cat() == 'Special'])

            # Calculate the percentage of the types cover by the attacks

            self.__coverage_percentage = len(self.__positive_coverage) / 18

            self.__physical_coverage_percentage = len(self.__positive_physical_coverage) / 18

            self.__special_coverage_percentage = len(self.__positive_special_coverage) / 18
        else:
            self.__physical_coverage_percentage = pcp
            self.__positive_physical_coverage = ppc
            self.__negative_physical_coverage = npc
            self.__special_coverage_percentage = scp
            self.__positive_special_coverage = psc
            self.__negative_special_coverage = nsc
            self.__coverage_percentage = cp
            self.__positive_coverage = pc
            self.__negative_coverage = nc
            self.__effects_coverage = ec
            self.__physical_power = pp
            self.__special_power = sp

    # noinspection PyMethodMayBeStatic
    def __get_coverage(self, attacks, type_of_coverage):
        """ Given a type of coverage and a list of attacks, this method will find both the positive coverage and the
        negative coverage of that list of attacks with the specified type of coverage('Physical' or 'Special')
            :param attacks: The list of attacks
            :param type_of_coverage:'Physical' or 'Special'
            :rtype : set,set
            """
        weak_table = constants.WeaknessesTable()
        list_of_attacks = [attack for attack in attacks if attack.get_cat() == type_of_coverage]
        positive_coverage = []
        negative_coverage = []
        for attack in list_of_attacks:
            type_ = attack.get_type()
            row = weak_table[type_]
            positive_coverage += [type_def for type_def in row if row[type_def] > 1]
            negative_coverage += [type_def for type_def in row if row[type_def] < 1]
        return set(positive_coverage), set(negative_coverage)

    def get_physical_coverage(self):
        """
        Return all in concern to the physical coverage
        """
        return self.__physical_coverage_percentage, self.__positive_physical_coverage, self.__negative_physical_coverage

    def get_special_coverage(self):
        """
        Return all in concern to the special coverage
        :return int, set, set
        :rtype int, set, set
        """
        return self.__special_coverage_percentage, self.__positive_special_coverage, self.__negative_special_coverage

    def get_coverage(self):
        """
        Return all in concern to the complete coverage
        :return int, set, set
        :rtype int, set, set
        """
        return self.__coverage_percentage, self.__positive_coverage, self.__negative_coverage

    def get_power(self):
        """
        A tuple with the sum of the attacks
        :return Tuple of ints
        :rtype int, int
        """
        return self.__physical_power, self.__special_power

    def get_effects(self):
        """
        Get all the effects the pokemon causes with its attacks
        :return: A list of effects
        """
        return self.__effects_coverage

    def __or__(self, other):
        """
        Make a union between this coverage and other coverage
        :param other: The coverage to be united
        :return: A new coverage
        """
        if other:
            pcp, ppc, npc = other.get_physical_coverage()
            scp, psc, nsc = other.get_special_coverage()
            effects = other.get_effects()

            n_ppc = self.__positive_physical_coverage | ppc
            n_npc = self.__negative_physical_coverage | npc

            n_psc = self.__positive_special_coverage | psc
            n_nsc = self.__negative_special_coverage | nsc

            n_ec = list(set(self.__effects_coverage) | set(effects))

            n_pc = n_psc | n_ppc
            n_nc = n_nsc | n_npc

            n_pp = self.__physical_power + other.__physical_power
            n_sp = self.__special_power + other.__special_power

            n_cp = len(n_pc) / 18

            n_pcp = len(n_ppc) / 18

            n_scp = len(n_psc) / 18

            n_coverage = Coverage(
                ppc=n_ppc, npc=n_npc, psc=n_psc, nsc=n_nsc, ec=n_ec, pc=n_pc,
                nc=n_nc, pp=n_pp, sp=n_sp, cp=n_cp, pcp=n_pcp, scp=n_scp
            )

            return n_coverage
        return self


class Resistance:
    def __init__(self, weaknesses):
        self.__weaknesses = weaknesses
        self.__type_resistance = 18 / sum(self.__weaknesses)
        self.__greatest_weaknesses = self.__weaknesses.max_values()
        self.__greatest_weaknesses_value = max(self.__weaknesses)
        self.__greatest_resistances = self.__weaknesses.min_values()
        self.__greatest_resistances_value = min(self.__weaknesses)

    def get_weaknesses(self):
        """
        Return the weaknesses of the team
        """
        return self.__weaknesses

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

    def get_type_resistance(self):
        """
        Return the resistance of the pokemon, it's a value tha represents the overall resistance against types of the
        pokemon. The greater the value the better, a resistance of 1 means that the pokemon is neutral, smaller tha one
        means that pokemon is very not resistant and greater than one mean that it is very resistance
        :return:
        """
        return self.__type_resistance

    def __add__(self, other):
        """
        Add the two weaknesses making just one multiplied by the other
        :param other: The other weakness
        :return: The new Weakness
        """
        if other:
            n_weaknesses = self.__weaknesses * other.get_weaknesses()
            return Resistance(n_weaknesses)
        return self


class TeamStats(StatsManipulator):
    """
    Class to deal with the team stats, empty at the moment, ready for expansion if needed
    """
    pass