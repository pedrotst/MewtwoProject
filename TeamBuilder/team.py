import teammember
import Pokedex.pokemon
import Utils.pkmutils


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
        :type value: str or Pokedex.pokemon.Pokemon or teammember.TeamMember
        """
        if isinstance(value, str):
            value = teammember.TeamMember(value)
        elif isinstance(value, Pokedex.pokemon):
            value = teammember.TeamMember(poke=value)
        if isinstance(value, teammember.TeamMember):
            self.__my_team[key] = value
        else:
            raise TypeError('value is not str, Pokemon or TeamMember')


class TeamAnalyser:
    def __init__(self, team):
        self.__team = team
        self.__team_weaknesses = Utils.pkmutils.PokeWeaknesses()
        self.__greatest_weaknesses = []
        self.__greatest_weaknesses_value = 0
        self.__greatest_resistances = []
        self.__greatest_resistances_value = 0

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
    c = Team(['Blaziken', 'Charizard', 'Slugma', 'Magmar', 'Magmar', 'Entei'])
    a = TeamAnalyser(c)
    e = Utils.pkmutils.PokeWeaknesses()
    a.calculate_team_weaknesses()
    print(a.get_weaknesses())
    print(a.get_greatest_weaknesses())
    print(a.get_greatest_resistances())