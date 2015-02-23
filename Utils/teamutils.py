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
            return self.__attacks[item]
        else:
            raise KeyError('Key must be between 1 and 4')


class IVs:
    """
    Store the ivs from each team member, it also updates the actual stats when iv value is updated
    """

    def __init__(self):
        self.__hp = 31
        self.__attack = 31
        self.__defense = 31
        self.__sp_attack = 31
        self.__sp_defense = 31
        self.__speed = 31

    def __getitem__(self, item):
        """Get IV given by item
        :param item: Name of IV
        :type item: str
        :return: the iv asked
        :rtype: int
        """
        get = {'HP': self.get_hp(), 'Attack': self.get_attack(), 'Defense': self.get_defense(),
               'Sp Attack': self.get_sp_attack(), 'Sp Defense': self.get_sp_defense(), 'Speed': self.get_speed()}
        return get[item]

    def __setitem__(self, key, value):
        """Set IV key with value
        :param key: The IV to be changed
        :type key: str
        :param value: The new value
        :type value: int
        """
        set_ = {'HP': self.set_hp, 'Attack': self.set_attack, 'Defense': self.set_defense,
                'Sp Attack': self.set_sp_attack, 'Sp Defense': self.set_sp_defense, 'Speed': self.set_speed}
        set_[key](value)

    def set_hp(self, hp):
        """Set the IV HP, value must be between 0 and 31, if not, value won't change
        :param hp: The new value of the IV
        :type hp: int
        """
        assert isinstance(hp, int)
        if 0 < hp < 31:
            self.__hp = hp
            # Call update on stats

    def get_hp(self):
        """Get the HP IVs
        :return: The HP IV
        :rtype: int
        """
        return self.__hp

    def set_attack(self, attack):
        """Set the IV Attack, value must be between 0 and 31, if not, value won't change
        :param attack: The new value of the IV
        :type attack: int
        """
        assert isinstance(attack, int)
        if 0 < attack < 31:
            self.__attack = attack
            # Call update on stats

    def get_attack(self):
        """Get the Attack IVs
        :return: The Attack IV
        :rtype: int
        """
        return self.__attack

    def set_defense(self, defense):
        """Set the IV Attack, value must be between 0 and 31, if not, value won't change
        :param defense: The new value of the IV
        :type defense: int
        """
        assert isinstance(defense, int)
        if 0 < defense < 31:
            self.__defense = defense
            # Call update on stats

    def get_defense(self):
        """Get the Defense IVs
        :return: The Defense IV
        :rtype: int
        """
        return self.__defense

    def set_sp_attack(self, sp_attack):
        """Set the IV Sp Attack, value must be between 0 and 31, if not, value won't change
        :param sp_attack: The new value of the IV
        :type attack: int
        """
        assert isinstance(sp_attack, int)
        if 0 < sp_attack < 31:
            self.__sp_attack = sp_attack
            # Call update on stats

    def get_sp_attack(self):
        """Get the Sp Attack IVs
        :return: The Sp Attack IV
        :rtype: int
        """
        return self.__sp_attack

    def set_sp_defense(self, sp_defense):
        """Set the IV Sp Defense, value must be between 0 and 31, if not, value won't change
        :param sp_defense: The new value of the IV
        :type sp_defense: int
        """
        assert isinstance(sp_defense, int)
        if 0 < sp_defense < 31:
            self.__sp_defense = sp_defense
            # Call update on stats

    def get_sp_defense(self):
        """Get the Sp Defense IVs
        :return: The Sp Defense IV
        :rtype: int
        """
        return self.__sp_defense

    def set_speed(self, speed):
        """Set the IV Speed, value must be between 0 and 31, if not, value won't change
        :param speed: The new value of the IV
        :type speed: int
        """
        assert isinstance(speed, int)
        if 0 < speed < 31:
            self.__speed = speed
            # Call update on stats

    def get_speed(self):
        """Get the Speed IVs
        :return: The Speed IV
        :rtype: int
        """
        return self.__speed


class EVs:
    """
    Store the evs from each team member, it also updates the actual stats when ev value is updated
    """

    def __init__(self):
        self.__hp = 0
        self.__attack = 0
        self.__defense = 0
        self.__sp_attack = 0
        self.__sp_defense = 0
        self.__speed = 0
        self.__total = sum(self)

    def __getitem__(self, item):
        """Get EV given by item
        :param item: Name of EV
        :type item: str or int
        :return: the ev asked
        :rtype: int
        """
        if isinstance(item, str):
            get = {'HP': self.get_hp(), 'Attack': self.get_attack(), 'Defense': self.get_defense(),
                   'Sp Attack': self.get_sp_attack(), 'Sp Defense': self.get_sp_defense(), 'Speed': self.get_speed(),
                   'Total': self.get_total()}
        elif isinstance(item, int):
            get = [self.get_hp(), self.get_attack(), self.get_defense(),
                   self.get_sp_attack(), self.get_sp_defense(), self.get_speed()]
        return get[item]

    def __setitem__(self, key, value):
        """Set EV key with value
        :param key: The EV to be changed
        :type key: str
        :param value: The new value
        :type value: int
        """
        set_ = {'HP': self.set_hp, 'Attack': self.set_attack, 'Defense': self.set_defense,
                'Sp Attack': self.set_sp_attack, 'Sp Defense': self.set_sp_defense, 'Speed': self.set_speed}
        if value + self.get_total() - self[key] > 510:
            value = 510 - self.get_total()
        set_[key](value)

    def set_hp(self, hp):
        """Set the EV HP, value must be between 0 and 31, if not, value won't change
        :param hp: The new value of the EV
        :type hp: int
        """
        assert isinstance(hp, int)
        if 0 < hp < 255 and self.__check_total():
            self.__set_total()
            self.__hp = hp
            # Call update on stats

    def get_hp(self):
        """Get the HP EVs
        :return: The HP EV
        :rtype: int
        """
        return self.__hp

    def set_attack(self, attack):
        """Set the EV Attack, value must be between 0 and 31, if not, value won't change
        :param attack: The new value of the EV
        :type attack: int
        """
        assert isinstance(attack, int)
        if 0 < attack < 255 and self.__check_total():
            self.__attack = attack
            self.__set_total()
            # Call update on stats

    def get_attack(self):
        """Get the Attack EVs
        :return: The Attack EV
        :rtype: int
        """
        return self.__attack

    def set_defense(self, defense):
        """Set the EV Attack, value must be between 0 and 31, if not, value won't change
        :param defense: The new value of the EV
        :type defense: int
        """
        assert isinstance(defense, int)
        if 0 < defense < 255 and self.__check_total():
            self.__defense = defense
            self.__set_total()
            # Call update on stats

    def get_defense(self):
        """Get the Defense EVs
        :return: The Defense EV
        :rtype: int
        """
        return self.__defense

    def set_sp_attack(self, sp_attack):
        """Set the EV Sp Attack, value must be between 0 and 31, if not, value won't change
        :param sp_attack: The new value of the EV
        :type attack: int
        """
        assert isinstance(sp_attack, int)
        if 0 < sp_attack < 255 and self.__check_total():
            self.__sp_attack = sp_attack
            self.__set_total()
            # Call update on stats

    def get_sp_attack(self):
        """Get the Sp Attack EVs
        :return: The Sp Attack EV
        :rtype: int
        """
        return self.__sp_attack

    def set_sp_defense(self, sp_defense):
        """Set the EV Sp Defense, value must be between 0 and 31, if not, value won't change
        :param sp_defense: The new value of the EV
        :type sp_defense: int
        """
        assert isinstance(sp_defense, int)
        if 0 < sp_defense < 255 and self.__check_total():
            self.__sp_defense = sp_defense
            self.__set_total()
            # Call update on stats

    def get_sp_defense(self):
        """Get the Sp Defense EVs
        :return: The Sp Defense EV
        :rtype: int
        """
        return self.__sp_defense

    def set_speed(self, speed):
        """Set the EV Speed, value must be between 0 and 31, if not, value won't change
        :param speed: The new value of the EV
        :type speed: int
        """
        assert isinstance(speed, int)
        if 0 < speed < 255 and self.__check_total():
            self.__speed = speed
            self.__set_total()
            # Call update on stats

    def get_speed(self):
        """Get the Speed EVs
        :return: The Speed EV
        :rtype: int
        """
        return self.__speed

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