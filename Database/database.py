import sqlite3

from Utils.pkmutils import *
import pokemon as pkm


class Manager:
    def __init__(self):
        self._databasePath = '../Database/Pokemon.db'
        self._connection = None

    def __exit__(self):
        if self._connection:
            self._connection.close()
            print('Closing')

    def _certify_connection(self):
        if self._connection is None:
            self._connect_to_database()

    def _connect_to_database(self):
        self._connection = sqlite3.connect(self._databasePath)


class DatabaseManager(Manager):
    def __init__(self):
        super()
        self.__abMan = AbilitiesManager()
        self.__pkmAbMan = PokemonAbilitiesManager()
        self.__pkmHiddenAbMan = PokemonHiddenAbilitiesManager()
        self.__atkMan = AttacksManager()
        self.__pkmAtkMan = PokeAttacksManager()
        self.__pkmItemsMan = PokeItemsManager()
        self.__pkmDNItemsMan = PokeDexNavItemsManager()
        self.__pkmEVMan = PokemonEVWorthManager()
        self.__pkmEvoMan = PokemonEvoChainManager()
        self.__pkmMan = PokemonManager()

    def get_pokemons_by_dex_num(self):
        return self.__pkmMan.get_pokemon_by_dex_num()

    def get_pokemon_by_name(self,name):
        pokeData = self.__pkmMan.get_pokemon_by_name(name)
        pokemonName = pokeData[0]
        pokeAbilities = self.__pkmAbMan.get_pokemon_abilities(pokemonName)
        try:
            pokeHiddenAbilities = self.__pkmHiddenAbMan.get_pokemon_hidden_abilities(pokemonName)
        except Exception:
            pokeHiddenAbilities = None         
        pokeAttacks = self.__pkmAtkMan.get_pokemon_attacks(pokemonName)
        pokeItems = self.__pkmItemsMan.get_pokemon_items(pokemonName)
        pokeDexNavItems = self.__pkmDNItemsMan.get_pokemon_dex_nav_items(pokemonName)
        pokeEvWorth = self.__pkmEVMan.get_pokemon_ev_worth(pokemonName)
        pokeEvoChain = self.__pkmEvoMan.get_pokemon_evo_chain(pokemonName)
        return (pokeData,
                pokeAbilities,
                pokeHiddenAbilities,
                pokeAttacks,
                pokeItems,
                pokeDexNavItems,
                pokeEvWorth,
                pokeEvoChain)


    def find_pokemon_name(self, text):
        """
        Try to find in the pokemon Database a pokemon with the name given, the name don't need to be complete
        :param text: The text to look for
        :return: The pokemon name
        """
        return self.__pkmMan.find_pokemon_name(text)



#controla a tabela Abilities que contem todas habilidades que existem e sua descrição
#só permite um tipo de query: getAbilityByName
class AbilitiesManager(Manager):
    def create_table_abilities(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
            Abilities(Name TEXT PRIMARY KEY,Description TEXT)
            ''')
            
    def insert_ability(self,name = None,description = None,ability = None):
        if ability:
            abilityData = (ability.get_name(), ability.get_description())
        else:
            if not (isinstance(name,str) and isinstance(description,str)):
                raise TypeError('Name and Description must be string')
            abilityData = (name,description)
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Abilities VALUES (?,?)",abilityData)
            except sqlite3.OperationalError as error:
                self.create_table_abilities()
                cursor.execute("INSERT INTO Abilities VALUES (?,?)",abilityData)
            except sqlite3.IntegrityError:
                pass

    def get_ability_by_name(self,name):
        self._certify_connection()
        search = (name,)
        if not isinstance(name,str):
            raise TypeError('Ability\'s name must be a string')
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Abilities WHERE Name=?',search)
        abilityData = cursor.fetchone()
        if(abilityData is not None):
            return PokeAbility(abilityData[0],abilityData[1])
        else:
            raise self.AbilityNotFoundError('Ability was not found')

    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM Abilities'):
                print(row)

    class AbilityNotFoundError(Exception):
        pass

class PokemonAbilitiesManager(Manager):
    def create_table_poke_abilities(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
                    PokemonAbilities(PokemonName TEXT PRIMARY KEY,
                    Ability1 TEXT,Ability2 TEXT)''')

    def insert_ability(self,pokemonName,name = None,description = None,ability = None):
        if ability:
            abilityData = (pokemonName,ability.get_name())
        else:
            if not (isinstance(name,str)):
                raise TypeError('Name')
            abilityData = (pokemonName,name)

        self._certify_connection()
        
        AM = AbilitiesManager()
        if AM.get_ability_by_name(abilityData[1]) is None:
            if ability:
                AM().insert_ability(ability=ability)
            elif description:
                AM().insert_ability(name, description)
            else:
                raise self.DescriptionError('Ability not in database and description is missing')
            
        with self._connection as conn:
            cursor = conn.cursor()

            try:
                cursor.execute("INSERT INTO PokemonAbilities(PokemonName,Ability1) VALUES (?,?)",abilityData)

            except sqlite3.OperationalError as error:
                self.create_table_poke_abilities()
                cursor.execute("INSERT INTO PokemonAbilities(PokemonName,Ability1) VALUES (?,?)",abilityData)

            except sqlite3.IntegrityError:
                abilitiesInRow = cursor.execute("SELECT * FROM PokemonAbilities WHERE PokemonName=?",(pokemonName,)).fetchone()
                if not abilityData[1] in abilitiesInRow:
                    if None in abilitiesInRow:
                        insertIndex = abilitiesInRow.index(None)
                        column = 'Ability'+str(insertIndex)
                        cursor.execute("UPDATE PokemonAbilities SET "+column+" = (?) WHERE PokemonName=?",(abilityData[1],pokemonName))
                    else:
                        insertIndex = len(abilitiesInRow)
                        column = 'Ability'+str(insertIndex)
                        cursor.execute("ALTER TABLE PokemonAbilities ADD COLUMN "+column+" TEXT")
                        cursor.execute("UPDATE PokemonAbilities SET "+column+" = (?) WHERE PokemonName=?",(abilityData[1],pokemonName))

    def get_pokemon_abilities(self,name):
        self._certify_connection()
        search = (name,)
        if not isinstance(name,str):
            raise TypeError('Pokemon\'s name must be a string')
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM PokemonAbilities WHERE PokemonName=?',search)
        abilityDatas = cursor.fetchone()
        if(abilityDatas is not None):
            AM = AbilitiesManager()
            abilities = []
            for abilityData,index in zip(abilityDatas,range(0,len(abilityDatas))):
                if index != 0:
                    if abilityData:
                        with self._connection as conn:
                            cursor = conn.cursor()
                            data = cursor.execute('SELECT * FROM Abilities WHERE Name=?',(abilityData,)).fetchone()
                            abilities.append(PokeAbility(data[0],data[1]))
            return abilities
        else:
            raise self.AbilityNotFoundError('Ability was not found')

    def get_pokemons_with_ability(self,name=None,ability=None):
        self._certify_connection()
        if ability:
            search = (ability.get_name(),)
        else:
            if not (isinstance(name,str)):
                raise TypeError('Name')
            search = (name,)

        with self._connection as conn:
            cursor = conn.cursor()
            abilitiesInRow = cursor.execute("SELECT * FROM PokemonAbilities WHERE PokemonName='Bulbasaur'").fetchone()
            pokemons = []
            for i in range(1,len(abilitiesInRow)):
                for pokemon in cursor.execute("SELECT PokemonName FROM PokemonAbilities WHERE Ability"+str(i)+"=(?)",search).fetchall():
                    pokemons.append(pokemon[0])
            return pokemons
        
    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokemonAbilities'):
                print(row)

                    
    class DescriptionError(Exception):
        pass

class PokemonHiddenAbilitiesManager(Manager):
    def create_table_poke_hidden_abilities(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
                PokemonHiddenAbilities(PokemonName TEXT PRIMARY KEY,
                Ability1 TEXT,Ability2 TEXT)''')

    def insert_ability(self,pokemonName,name = None,description = None,ability = None):
        if ability:
            abilityData = (pokemonName,ability.get_name())
        else:
            if not (isinstance(name,str)):
                raise TypeError('Name')
            abilityData = (pokemonName,name)

        self._certify_connection()
        
        AM = AbilitiesManager()
        if AM.get_ability_by_name(abilityData[1]) is None:
            if ability:
                AM().insert_ability(ability=ability)
            elif description:
                AM().insert_ability(name, description)
            else:
                raise self.DescriptionError('Ability not in database and description is missing')
            
        with self._connection as conn:
            cursor = conn.cursor()

            try:
                cursor.execute("INSERT INTO PokemonHiddenAbilities(PokemonName,Ability1) VALUES (?,?)",abilityData)

            except sqlite3.OperationalError as error:
                self.create_table_poke_hidden_abilities()
                cursor.execute("INSERT INTO PokemonHiddenAbilities(PokemonName,Ability1) VALUES (?,?)",abilityData)

            except sqlite3.IntegrityError:
                abilitiesInRow = cursor.execute("SELECT * FROM PokemonHiddenAbilities WHERE PokemonName=?",(pokemonName,)).fetchone()
                if not abilityData[1] in abilitiesInRow:
                    if None in abilitiesInRow:
                        insertIndex = abilitiesInRow.index(None)
                        column = 'Ability'+str(insertIndex)
                        cursor.execute("UPDATE PokemonHiddenAbilities SET "+column+" = (?) WHERE PokemonName=?",(abilityData[1],pokemonName))
                    else:
                        insertIndex = len(abilitiesInRow)
                        column = 'Ability'+str(insertIndex)
                        cursor.execute("ALTER TABLE PokemonAbilities ADD COLUMN "+column+" TEXT")
                        cursor.execute("UPDATE PokemonAbilities SET "+column+" = (?) WHERE PokemonName=?",(abilityData[1],pokemonName))

    def get_pokemon_hidden_abilities(self,name):
        self._certify_connection()
        search = (name,)
        if not isinstance(name,str):
            raise TypeError('Pokemon\'s name must be a string')
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM PokemonHiddenAbilities WHERE PokemonName=?',search)
        abilityDatas = cursor.fetchone()
        if(abilityDatas is not None):
            AM = AbilitiesManager()
            abilities = []
            for abilityData,index in zip(abilityDatas,range(0,len(abilityDatas))):
                if index != 0:
                    if abilityData:
                        with self._connection as conn:
                            cursor = conn.cursor()
                            data = cursor.execute('SELECT * FROM Abilities WHERE Name=?',(abilityData,)).fetchone()
                            abilities.append(PokeAbility(data[0],data[1]))
            return abilities
        else:
            raise self.AbilityNotFoundError('Ability was not found')

    def get_pokemons_with_hidden_ability(self,name=None,ability=None):
        self._certify_connection()
        if ability:
            search = (ability.get_name(),)
        else:
            if not (isinstance(name,str)):
                raise TypeError('Name')
            search = (name,)

        with self._connection as conn:
            cursor = conn.cursor()
            abilitiesInRow = cursor.execute("SELECT * FROM PokemonHiddenAbilities WHERE PokemonName='Bulbasaur'").fetchone()
            pokemons = []
            for i in range(1,len(abilitiesInRow)):
                for pokemon in cursor.execute("SELECT PokemonName FROM PokemonHiddenAbilities WHERE Ability"+str(i)+"=(?)",search).fetchall():
                    pokemons.append(pokemon[0])
            return pokemons


    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokemonHiddenAbilities'):
                print(row)

                    
    class DescriptionError(Exception):
        pass

    class AbilityNotFoundError(Exception):
        pass

class AttacksManager(Manager):
    def create_table_attacks(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
             Attacks(Name TEXT PRIMARY KEY, Type TEXT,Category TEXT,
              Att INTEGER , Acc INTEGER, Pp INTEGER,
               Effect TEXT, Description TEXT)''')

    def insert_attack(self,name = None, atkType = None, cat = None , att = None, acc = None, pp = None , effect = None, description = None,attack = None):
        if attack:
            attackData = (attack.get_name(),str(attack.get_item_type()),str(attack.get_cat()),attack.get_att(),attack.get_acc(),
                          attack.get_PP(), attack.get_effect(), attack.get_description())
        else:
            if not (isinstance(name,str) and isinstance(atkType,str)and isinstance(cat,str) and isinstance(att,int) and isinstance(acc,int) and isinstance(pp,int) and isinstance(effect,str) and isinstance(description,str)):
                raise TypeError('Type incompatibily')
            attackData = (name,atkType,cat,att,acc,pp,effect,description)
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Attacks VALUES (?,?,?,?,?,?,?,?)",attackData)
            except sqlite3.OperationalError as error:
                self.createTableAbilities()
                cursor.execute("INSERT INTO Attacks VALUES (?,?,?,?,?,?,?,?)",attackData)
        
    def get_attack_by_name(self,name):
        self._certify_connection()
        search = (name,)
        if not isinstance(name,str):
            raise TypeError('Attack\'s name must be a string')
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Attacks WHERE Name=?',search)
        attackData = cursor.fetchone()
        if(attackData is not None):
            return Attack(0,attackData[0],attackData[1],attackData[2],attackData[3],attackData[4],attackData[5],attackData[6],attackData[7], attackData[8])
        else:
            raise self.AttackNotFoundError('Attack was not found')

    def add_secundary_eff_col(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('ALTER TABLE Attacks ADD SecEffect TEXT')

    def add_speed_priority(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('ALTER TABLE Attacks ADD SpeedPriority INTEGER')

    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM Attacks'):
                print(row)

    def insert_sec_effect(self, attack_name, effect, speed_priority):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE Attacks'
                           ' SET SecEffect=\"{}\"'
                           ' AND SpeedPriority=\"{}\"'
                           ' WHERE NAME=\"{}\"'.format(effect, speed_priority, attack_name))

    class AttackNotFoundError(Exception):
        pass

class PokeAttacksManager(Manager):
    def create_table_pk_attacks(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
            PokeAttacks(PokeName TEXT, AtkName TEXT, AtkGroup TEXT,
            Condition TEXT, PRIMARY KEY (PokeName, AtkName,AtkGroup))''')

    def insert_poke_attacks(self, pokeName = None, atkName = None, atkGroup = None , condition = None):
        if not (isinstance(pokeName,str) ):
            raise TypeError('Poke name not str')
        if not (isinstance(atkName,str) ):
            raise TypeError('atk name not str')
        if not (isinstance(atkGroup,str) ):
            raise TypeError('atk group not str')
        if not (isinstance(condition,str) ):
            raise TypeError('condition not str')

        self._certify_connection()
        
        attackData = (pokeName,atkName, atkGroup, condition)
        AM = AttacksManager()
        if AM.get_attack_by_name(attackData[1]) is None:
            raise self.DescriptionError('Attack '+ atkName+ ' is not in database')
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO PokeAttacks VALUES (?,?,?,?)",attackData)
            except sqlite3.OperationalError as error:
                self.create_table_pk_attacks()
                cursor.execute("INSERT INTO PokeAttacks VALUES (?,?,?,?)",attackData)
        
    def get_pokemon_attacks(self,name):
        self._certify_connection()
        search = (name,)
        if not isinstance(name,str):
            raise TypeError('Pokemon\'s name must be a string')
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM PokeAttacks WHERE PokeName=? ORDER BY AtkGroup,Condition',search)
        attackData = cursor.fetchall()
        
        if(attackData is not None):
            attackGroups = {}
            for attack in attackData:
                if( attack[2] not in attackGroups.keys()):
                    attackGroups[attack[2]] = []
                AM = AttacksManager()
                atk = AM.get_attack_by_name(attack[1])
                atk.set_condition(attack[3])
                attackGroups[attack[2]].append(atk)
            return attackGroups
        else:
            raise self.AttackNotFoundError('Pokemon was not found')


    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokeAttacks'):
                print(row)

    class DescriptionError(Exception):
        pass
        
class PokeItemsManager(Manager):
    def create_table_pk_items(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
            PokeItems(PokeName TEXT , ItemName TEXT,
            ItemChance INTEGER,PRIMARY KEY(PokeName,ItemName))''')

    def insert_poke_item(self, pokeName = None, itemName = None, itemChance = None):
        if not (isinstance(pokeName,str) ):
            raise TypeError('Poke name not str')
        if not (isinstance(itemName,str) ):
            raise TypeError('item name not str')
        if not(isinstance(itemChance,int)):
            raise TypeError('item chance not int')
        self._certify_connection()
        
        pkItemData = (pokeName,itemName,itemChance)
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO PokeItems VALUES (?,?,?)",pkItemData)
            except sqlite3.OperationalError as error:
                self.create_table_pk_items()
                cursor.execute("INSERT INTO PokeItems VALUES (?,?,?)",pkItemData)

    def get_pokemon_items(self,pokemonName):
        self._certify_connection()
        search = (pokemonName,)
        if not isinstance(pokemonName,str):
            raise TypeError('Pokemon\'s name must be a string')
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT ItemName,ItemChance FROM PokeItems WHERE PokeName=?',search)
        itemData = cursor.fetchall()
        if(itemData is not None):
            return itemData
        else:
            raise self.AttackNotFoundError('Pokemon was not found')

    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokeItems'):
                print(row)

    class DescriptionError(Exception):
        pass


class PokeDexNavItemsManager(Manager):
    def create_table_pk_dex_nav_items(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
             PokeDexNavItems(PokeName TEXT , ItemName TEXT,PRIMARY KEY(PokeName,ItemName))''')

    def insert_poke_item(self, pokeName = None, itemName = None):
        if not (isinstance(pokeName,str) ):
            raise TypeError('Poke name not str')
        if not (isinstance(itemName,str) ):
            raise TypeError('item name not str')

        self._certify_connection()
        
        pkItemData = (pokeName,itemName)
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO PokeDexNavItems VALUES (?,?)",pkItemData)
            except sqlite3.OperationalError as error:
                self.createTablePkItems()
                cursor.execute("INSERT INTO PokeDexNavItems VALUES (?,?)",pkItemData)
                
    def get_pokemon_dex_nav_items(self,pokemonName):
        self._certify_connection()
        search = (pokemonName,)
        if not isinstance(pokemonName,str):
            raise TypeError('Pokemon\'s name must be a string')
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT ItemName FROM PokeDexNavItems WHERE PokeName=?',search)
        itemData = cursor.fetchall()
        if(itemData is not None):
            return itemData
        else:
            raise self.AttackNotFoundError('Pokemon was not found')
        
    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokeDexNavItems'):
                print(row)
                

class PokemonEVWorthManager(Manager):
    def create_table_pokemon_ev_worth(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
             PokemonEVWorth(PokeName TEXT , Stat TEXT, Value INTEGER,
              PRIMARY KEY(PokeName,Stat))''')

    def insert_poke_ev_worth(self,pokeName, ev = None):
        if not (isinstance(ev,EV) ):
            raise TypeError('ev not of type EV')
        if not (isinstance(pokeName,str) ):
            raise TypeError('Pokemon name not str')
        self._certify_connection()
        
        evData = (pokeName,str(ev.get_stat()), ev.get_value())
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO PokemonEVWorth VALUES (?,?,?)",evData)
            except sqlite3.OperationalError as error:
                self.create_table_pokemon_ev_worth()
                cursor.execute("INSERT INTO PokemonEVWorth VALUES (?,?,?)",evData)		

    def get_pokemon_ev_worth(self,pokemonName):
        self._certify_connection()
        search = (pokemonName,)
        if not isinstance(pokemonName,str):
            raise TypeError('Pokemon\'s name must be a string')
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM PokemonEVWorth WHERE PokeName=?',search)
        evData = cursor.fetchall()
        if(evData is not None):
            return evData
        else:
            raise self.AttackNotFoundError('Pokemon was not found')


    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokemonEVWorth'):
                print(row)

class PokemonManager(Manager):
    def create_table_pokemon(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            #THREE HOURS ORGANIZING THIS SHIT!
            #DO
            #NOT
            #MESS!
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
            Pokemon(             PokeName TEXT PRIMARY KEY,  NationalDex   INTEGER,
            CentralDex     INTEGER,    CoastalDex   INTEGER, MountainDex   INTEGER,
            HoennDex       INTEGER,    MaleRate     REAL,    FemaleRate    Real,
            Genderless     INTEGER,    Type1        TEXT,    Type2         TEXT,
            Classification TEXT,       HeightMeters REAL,    HeightInches  INTEGER,
            WeightKg       REAL,       WeightLbs    REAL,    ORASCr        INTEGER,
            XYCr           INTEGER     BaseEggSteps INTEGER, PathImg       TEXT,
            PathSImg       TEXT,       ExpGrowth    INTEGER, ExpGrowthClassification TEXT,
            BaseHappiness  INTEGER,    SkyBattle    TEXT,    Normal         REAL,
            Fire           REAL,       Water        REAL,    Electric       REAL,
            Grass          REAL,       Ice          REAL,    Fighting       REAL,
            Poison         REAL,       Ground       REAL,    Flying         REAL,
            Psychic        REAL,       Bug          REAL,    Rock           REAL,
            Ghost          REAL,       Dragon       REAL,    Dark           REAL,
            Steel          REAL,       Fairy        REAL,    EggGroup1      TEXT,
            EggGroup2      TEXT,       LocationX    TEXT,    LocationY      TEXT,
            LocationOR     TEXT,       LocationAS   TEXT,    DexTextX       TEXT,
            DexTextY       TEXT ,      DexTextOR    TEXT,    DexTextAS      TEXT,
            Hp             INTEGER,    Attack       INTEGER, Defense        INTEGER,
            SpAttack       INTEGER,    SpDefense    INTEGER, Speed          INTEGER,
            Total          INTEGER
            )''')
            #isn't it pretty now? <3

    def insert_pokemon(self, name,pokemon):
        if not (isinstance(pokemon,pkm.Pokemon) ):
            raise TypeError('Poke name not Pokemon')

        name = pokemon.get_name()
        nationalDex = pokemon.get_dex_num().get_national()
        centralDex = pokemon.get_dex_num().get_central()
        coastalDex = pokemon.get_dex_num().get_coastal()
        mountainDex = pokemon.get_dex_num().get_mountain()
        hoennDex = pokemon.get_dex_num().get_hoenn()
        maleRate = pokemon.get_gender().get_male_rate()
        femaleRate = pokemon.get_gender().get_female_rate()
        genderless = int(pokemon.get_gender().is_genderless())
        type1 = str(pokemon.get_types().get_type1())
        type2 = str(pokemon.get_types().get_type2())
        classification = pokemon.get_classification()
        heightMeters = pokemon.get_height().get_value_in_meters()
        heightInches = pokemon.get_height().get_value_in_inches()
        weightKg = pokemon.get_weight().get_value_in_kg()
        weightLbs = pokemon.get_weight().get_value_in_lbs()
        oRASCr = pokemon.get_capture_rate().get_oras()
        yXCr = pokemon.get_capture_rate().get_xy()
        baseEggSteps = pokemon.get_base_egg_steps()
        pathImg = pokemon.get_image_path().get_path_img()
        pathSImg = pokemon.get_image_path().get_spath_img()
        expGrowth = pokemon.get_exp_growth().get_exp_growth()
        expGrowthClassification = pokemon.get_exp_growth().get_classification()
        baseHappiness = pokemon.get_happiness()
        skyBattle = pokemon.get_sky_battle()
        normal = pokemon.get_weaknesses()['Normal']
        fire = pokemon.get_weaknesses()['Fire']
        water = pokemon.get_weaknesses()['Water']
        electric = pokemon.get_weaknesses()['Electric']
        grass = pokemon.get_weaknesses()['Grass']
        ice = pokemon.get_weaknesses()['Ice']
        fighting = pokemon.get_weaknesses()['Fighting']
        poison = pokemon.get_weaknesses()['Poison']
        ground = pokemon.get_weaknesses()['Ground']
        flying = pokemon.get_weaknesses()['Flying']
        psychic = pokemon.get_weaknesses()['Psychic']
        bug = pokemon.get_weaknesses()['Bug']
        rock = pokemon.get_weaknesses()['Rock']
        ghost = pokemon.get_weaknesses()['Ghost']
        dragon = pokemon.get_weaknesses()['Dragon']
        dark = pokemon.get_weaknesses()['Dark']
        steel = pokemon.get_weaknesses()['Steel']
        fairy = pokemon.get_weaknesses()['Fairy']
        eggGroup1 = str(pokemon.get_egg_groups().get_group1())
        eggGroup2 = str(pokemon.get_egg_groups().get_group2())
        locationX = pokemon.get_location().get_x()
        locationY = pokemon.get_location().get_y()
        locationOR = pokemon.get_location().get_or()
        locationAS = pokemon.get_location().get_as()
        dexTextX = pokemon.get_dex_text().get_x()
        dexTextY = pokemon.get_dex_text().get_y()
        dexTextOR = pokemon.get_dex_text().get_or()
        dexTextAS = pokemon.get_dex_text().get_as()
        hp = pokemon.get_stats().get_hp()
        attack = pokemon.get_stats().get_attack()
        defense = pokemon.get_stats().get_defense()
        spAttack = pokemon.get_stats().get_sp_attack()
        spDefense = pokemon.get_stats().get_sp_defense()
        speed = pokemon.get_stats().get_speed()
        total = hp+attack+defense+spAttack+spDefense+speed
        
        pkmData = (name, nationalDex, centralDex,
                   coastalDex, mountainDex,hoennDex,
                   maleRate,femaleRate,genderless,
                   type1,type2,classification,
                   heightMeters, heightInches, weightKg,
                   weightLbs,oRASCr,yXCr,
                   baseEggSteps,pathImg,pathSImg,expGrowth,
                   expGrowthClassification,baseHappiness,
                   skyBattle,normal,fire,
                   water,electric,grass,
                   ice,fighting,poison,
                   ground,flying,psychic ,
                   bug ,rock ,ghost ,
                   dragon ,dark ,steel ,
                   fairy ,eggGroup1,eggGroup2,
                   locationX,locationY,locationOR,
                   locationAS,dexTextX,dexTextY,
                   dexTextOR,dexTextAS,hp,
                   attack,defense,spAttack,
                   spDefense,speed,total)

        self._certify_connection()
        
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Pokemon VALUES "
                    "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
                    "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?"
                    ",?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",pkmData)
            except sqlite3.OperationalError as error:
                self.create_table_pokemon()
                cursor.execute("INSERT INTO Pokemon VALUES"
                    " (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
                    "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?"
                    ",?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",pkmData)

    def insert_pokemon_raw(self,
            name, nationalDex, centralDex,
            coastalDex, mountainDex,hoennDex,
            maleRate,femaleRate,genderless,
            type1,type2,classification,
            heightMeters, heightInches, weightKg,
            weightLbs,oRASCr,yXCr,
            baseEggSteps,pathImg,pathSImg,expGrowth,
            expGrowthClassification,baseHappiness,
            skyBattle,normal,fire,
            water,electric,grass,
            ice,fighting,poison,
            ground,flying,psychic ,
            bug ,rock ,ghost ,
            dragon ,dark ,steel ,
            fairy ,eggGroup1,eggGroup2,
            locationX,locationY,locationOR,
            locationAS,dexTextX,dexTextY,
            dexTextOR,dexTextAS,hp,
            attack,defense,spAttack,
            spDefense,speed,total):

        pkmData = (name, nationalDex, centralDex,
                   coastalDex, mountainDex,hoennDex,
                   maleRate,femaleRate,genderless,
                   type1,type2,classification,
                   heightMeters, heightInches, weightKg,
                   weightLbs,oRASCr,yXCr,
                   baseEggSteps,pathImg,pathSImg,expGrowth,
                   expGrowthClassification,baseHappiness,
                   skyBattle,normal,fire,
                   water,electric,grass,
                   ice,fighting,poison,
                   ground,flying,psychic ,
                   bug ,rock ,ghost ,
                   dragon ,dark ,steel ,
                   fairy ,eggGroup1,eggGroup2,
                   locationX,locationY,locationOR,
                   locationAS,dexTextX,dexTextY,
                   dexTextOR,dexTextAS,hp,
                   attack,defense,spAttack,
                   spDefense,speed,total)

        self._certify_connection()

        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Pokemon VALUES "
                    "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
                    "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?"
                    ",?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",pkmData)
            except sqlite3.OperationalError as error:
                self.create_table_pokemon()
                cursor.execute("INSERT INTO Pokemon VALUES"
                    " (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
                    "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?"
                    ",?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",pkmData)
            except sqlite3.IntegrityError as error:
                cursor.execute("DELETE FROM Pokemon WHERE PokeName = ?", (name,))
                print("Reinserting "+name)
                self.insert_pokemon_raw(name, nationalDex, centralDex,
                   coastalDex, mountainDex,hoennDex,
                   maleRate,femaleRate,genderless,
                   type1,type2,classification,
                   heightMeters, heightInches, weightKg,
                   weightLbs,oRASCr,yXCr,
                   baseEggSteps,pathImg,pathSImg,expGrowth,
                   expGrowthClassification,baseHappiness,
                   skyBattle,normal,fire,
                   water,electric,grass,
                   ice,fighting,poison,
                   ground,flying,psychic ,
                   bug ,rock ,ghost ,
                   dragon ,dark ,steel ,
                   fairy ,eggGroup1,eggGroup2,
                   locationX,locationY,locationOR,
                   locationAS,dexTextX,dexTextY,
                   dexTextOR,dexTextAS,hp,
                   attack,defense,spAttack,
                   spDefense,speed,total)


    def __correct_location(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT PokeName,LocationX,LocationY,LocationOR,LocationAS FROM Pokemon ORDER BY NationalDex')
            newValues = []
            for poke in cursor.fetchall():
                p = ['','','','']
                p[0] = poke[1].replace('Details','')
                p[0] = replace_uppercase(p[0])
                p[1] = poke[2].replace('Details','')
                p[1] = replace_uppercase(p[1])
                p[2] = poke[3].replace('Details','')
                p[2] = replace_uppercase(p[2])
                p[3] = poke[4].replace('Details','')
                p[3] = replace_uppercase(p[3])
                cursor.execute('''UPDATE Pokemon SET LocationX=(?),LocationY=(?),LocationOR=(?),LocationAS=(?) WHERE PokeName=(?)''',(p[0],p[1],p[2],p[3],poke[0]))
                newValues.append(p)
            print(*newValues,sep = '\n')
      
    def get_pokemon_by_dex_num(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT NationalDex,PokeName FROM Pokemon ORDER BY NationalDex')
            return cursor.fetchall()                        
                        
    def get_pokemon_by_name(self,name):
        self._certify_connection()
        search = (name,)
        if not isinstance(name,str):
            raise TypeError('Pokemon\'s name must be a string')
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Pokemon WHERE PokeName=?',search)
        pokemonData = cursor.fetchone()
        if(pokemonData is not None):
            return pokemonData
        else:
            raise self.PokemonNotFoundError('Pokemon was not found')

    class PokemonNotFoundError(Exception):
        pass



    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM Pokemon'):
                print(row)

    def find_pokemon_name(self, text):
        """
        Try to find in the pokemon Database a pokemon with the name given, the name don't need to be complete
        :param text: The text to look for
        :return: The pokemons names
        """
        search = (text+'%',)
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT PokeName FROM Pokemon WHERE PokeName LIKE ? ORDER BY NationalDex', search)
            return [name[0] for name in cursor.fetchall()]


class PokemonEvoChainManager(Manager):
    def create_table_pokemon_evo_chain(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
             PokemonEvoChain(PokeName TEXT ,EvoNode TEXT,
             PRIMARY KEY(PokeName,EvoNode))''')

    def insert_evo_node(self,pokeName, evoNode):
        if not (isinstance(pokeName,str) ):
            raise TypeError('Pokemon name not str')
        self._certify_connection()
        
        evData = (pokeName,str(evoNode))
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO PokemonEvoChain VALUES (?,?)",evData)
            except sqlite3.OperationalError as error:
                self.create_table_pokemon_evo_chain()
                cursor.execute("INSERT INTO PokemonEvoChain VALUES (?,?)",evData)
                
    def remove_node(self,pokeName,evoNode):
        if not (isinstance(pokeName,str) ):
            raise TypeError('Pokemon name not str')
        self._certify_connection()
        
        evData = (pokeName,str(evoNode))
        with self._connection as conn:
            cursor = conn.cursor()
            print(evData[1])
            cursor.execute("DELETE FROM PokemonEvoChain WHERE PokeName=(?) AND EvoNode=(?)",evData)

    def drop(self):
        self._certify_connection()
        with self._connection as conn:
            conn.cursor().execute('DROP TABLE PokemonEvoChain')
            

                
    def update_evo_node(self,pokeName,add = None,remove = None):
        if not (isinstance(pokeName,str) ):
            raise TypeError('Pokemon name not str')
        self._certify_connection()
        
        with self._connection as conn:
            cursor = conn.cursor()
            evData = (pokeName,)
            cursor.execute("SELECT EvoNode FROM PokemonEvoChain WHERE PokeName=(?)",evData)
            nodes = cursor.fetchall()
            if(nodes):
                for node in nodes:
                    print(node)
                if add:
                    self.insert_evo_node(pokeName, add)
                    print(add)
                elif remove:
                    self.remove_node(pokeName, remove)
                    

    
    def get_pokemon_evo_chain(self,pokemonName):
        self._certify_connection()
        search = (pokemonName,)
        if not isinstance(pokemonName,str):
            raise TypeError('Pokemon\'s name must be a string')
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT EvoNode FROM PokemonEvoChain WHERE PokeName=?',search)
        evData = cursor.fetchall()
        if(evData is not None):
            return evData
        else:
            raise self.AttackNotFoundError('Pokemon was not found')


    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokemonEvoChain'):
                print(row)

#deletar esta table
class ItemCategoryManager(Manager):
    def createItemCategoryTable(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
            ItemCategory(ItemName TEXT PRIMARY KEY, Category TEXT)''')

    def insertItem(self, itemName = None, category = None):
        if not (isinstance(itemName,str) ):
            raise TypeError('Poke name not str')
        if not (isinstance(category,str) ):
            raise TypeError('atk name not str')
        self._certify_connection()
        
        pkItemData = (itemName,category)
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO ItemCategory VALUES (?,?)",pkItemData)
            except sqlite3.OperationalError as error:
                self.createTablePkItems()
                cursor.execute("INSERT INTO ItemCategory VALUES (?,?)",pkItemData)

    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM ItemCategory ORDER BY Category, ItemName'):
                print(row)
    def drop(self):
        self._certify_connection()
        with self._connection as conn:
            conn.cursor().execute('DROP TABLE ItemCategory')

if __name__ == '__main__':
    PokemonEvoChainManager().update_evo_node('Gorebyss')
    input('Waiting')
    
    
    