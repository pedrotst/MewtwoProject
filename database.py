import sqlite3
from pokemonUtils import *
import pokemon as pkm

class Manager:
    def __init__(self):
        self._databasePath = 'PokemonTest.db'
        self._connection = None

    def __exit__(self):
        if self._connection:
            self._connection.close()
            print('Closing')

    def _certifyConnection(self):
        if self._connection is None:
            self._connectToDatabase()        

    def _connectToDatabase(self):
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

    def getPokemonsByDexNum(self):
        return  self.__pkmMan.getPokemonByDexNum()

    def getPokemonByName(self,name):
        pokeData = self.__pkmMan.getPokemonByName(name)
        pokemonName = pokeData[0]
        pokeAbilities = self.__pkmAbMan.getPokemonAbilities(pokemonName)
        try:
            pokeHiddenAbilities = self.__pkmHiddenAbMan.getPokemonHiddenAbilities(pokemonName)
        except Exception:
            pokeHiddenAbilities = None         
        pokeAttacks = self.__pkmAtkMan.getPokemonAttacks(pokemonName)
        pokeItems = self.__pkmItemsMan.getPokemonItems(pokemonName)
        pokeDexNavItems = self.__pkmDNItemsMan.getPokemonDexNavItems(pokemonName)
        pokeEvWorth = self.__pkmEVMan.getPokemonEVWorth(pokemonName)
        pokeEvoChain = self.__pkmEvoMan.getPokemonEvoChain(pokemonName)
        return (pokeData,
                pokeAbilities,
                pokeHiddenAbilities,
                pokeAttacks,
                pokeItems,
                pokeDexNavItems,
                pokeEvWorth,
                pokeEvoChain)
                


#controla a tabela Abilities que contem todas habilidades que existem e sua descrição
#só permite um tipo de query: getAbilityByName
class AbilitiesManager(Manager):
    def createTableAbilities(self):
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS Abilities(Name TEXT PRIMARY KEY,Description TEXT)''')
            
    def insertAbility(self,name = None,description = None,ability = None):
        if ability:
            abilityData = (ability.getName(),ability.getDescription())
        else:
            if not (isinstance(name,str) and isinstance(description,str)):
                raise TypeError('Name and Description must be string')
            abilityData = (name,description)
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Abilities VALUES (?,?)",abilityData)
            except sqlite3.OperationalError as error:
                self.createTableAbilities()
                cursor.execute("INSERT INTO Abilities VALUES (?,?)",abilityData)

    def getAbilityByName(self,name):
        self._certifyConnection()
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
        self._certifyConnection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM Abilities'):
                print(row)

    class AbilityNotFoundError(Exception):
        pass

class PokemonAbilitiesManager(Manager):
    def createTablePokeAbilities(self):
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS PokemonAbilities(PokemonName TEXT PRIMARY KEY, Ability1 TEXT,Ability2 TEXT)''')

    def insertAbility(self,pokemonName,name = None,description = None,ability = None):
        if ability:
            abilityData = (pokemonName,ability.getName())
        else:
            if not (isinstance(name,str)):
                raise TypeError('Name')
            abilityData = (pokemonName,name)
            
        self._certifyConnection()
        
        AM = AbilitiesManager()
        if AM.getAbilityByName(abilityData[1]) is None:
            if ability:
                AM().insertAbility(ability = ability)
            elif description:
                AM().insertAbility(name,description)
            else:
                raise self.DescriptionError('Ability not in database and description is missing')
            
        with self._connection as conn:
            cursor = conn.cursor()

            try:
                cursor.execute("INSERT INTO PokemonAbilities(PokemonName,Ability1) VALUES (?,?)",abilityData)

            except sqlite3.OperationalError as error:
                self.createTablePokeAbilities()
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

    def getPokemonAbilities(self,name):
        self._certifyConnection()
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

    def getPokemonsWithAbility(self,name=None,ability=None):
        self._certifyConnection()
        if ability:
            search = (ability.getName(),)
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
        self._certifyConnection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokemonAbilities'):
                print(row)

                    
    class DescriptionError(Exception):
        pass

class PokemonHiddenAbilitiesManager(Manager):
    def createTablePokeHiddenAbilities(self):
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS PokemonHiddenAbilities(PokemonName TEXT PRIMARY KEY, Ability1 TEXT,Ability2 TEXT)''')

    def insertAbility(self,pokemonName,name = None,description = None,ability = None):
        if ability:
            abilityData = (pokemonName,ability.getName())
        else:
            if not (isinstance(name,str)):
                raise TypeError('Name')
            abilityData = (pokemonName,name)
            
        self._certifyConnection()
        
        AM = AbilitiesManager()
        if AM.getAbilityByName(abilityData[1]) is None:
            if ability:
                AM().insertAbility(ability = ability)
            elif description:
                AM().insertAbility(name,description)
            else:
                raise self.DescriptionError('Ability not in database and description is missing')
            
        with self._connection as conn:
            cursor = conn.cursor()

            try:
                cursor.execute("INSERT INTO PokemonHiddenAbilities(PokemonName,Ability1) VALUES (?,?)",abilityData)

            except sqlite3.OperationalError as error:
                self.createTablePokeHiddenAbilities()
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

    def getPokemonHiddenAbilities(self,name):
        self._certifyConnection()
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

    def getPokemonsWithHiddenAbility(self,name=None,ability=None):
        self._certifyConnection()
        if ability:
            search = (ability.getName(),)
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
        self._certifyConnection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokemonHiddenAbilities'):
                print(row)

                    
    class DescriptionError(Exception):
        pass

    class AbilityNotFoundError(Exception):
        pass

class AttacksManager(Manager):
    def createTableAttacks(self):
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS Attacks(Name TEXT PRIMARY KEY, Type TEXT,Category TEXT, Att INTEGER , Acc INTEGER, Pp INTEGER, Effect TEXT, Description TEXT)''')

    def insertAttack(self,name = None, atkType = None, cat = None , att = None, acc = None, pp = None , effect = None, description = None,attack = None):
        if attack:
            attackData = (attack.getName(),str(attack.getType()),str(attack.getCat()),attack.getAtt(),attack.getAcc(),attack.getPP(),attack.getEffect(),attack.getDescription())
        else:
            if not (isinstance(name,str) and isinstance(atkType,str)and isinstance(cat,str) and isinstance(att,int) and isinstance(acc,int) and isinstance(pp,int) and isinstance(effect,str) and isinstance(description,str)):
                raise TypeError('Type incompatibily')
            attackData = (name,atkType,cat,att,acc,pp,effect,description)
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Attacks VALUES (?,?,?,?,?,?,?,?)",attackData)
            except sqlite3.OperationalError as error:
                self.createTableAbilities()
                cursor.execute("INSERT INTO Attacks VALUES (?,?,?,?,?,?,?,?)",attackData)
        
    def getAttackByName(self,name):
        self._certifyConnection()
        search = (name,)
        if not isinstance(name,str):
            raise TypeError('Attack\'s name must be a string')
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Attacks WHERE Name=?',search)
        attackData = cursor.fetchone()
        if(attackData is not None):
            return Attack(0,attackData[0],attackData[1],attackData[2],attackData[3],attackData[4],attackData[5],attackData[6],attackData[7])
        else:
            raise self.AttackNotFoundError('Attack was not found')
		
		
    def view(self):
        self._certifyConnection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM Attacks'):
                print(row)
				
    class AttackNotFoundError(Exception):
        pass
        
class PokeAttacksManager(Manager):
    def createTablePkAttacks(self):
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS PokeAttacks(PokeName TEXT, AtkName TEXT, AtkGroup TEXT, Condition TEXT, PRIMARY KEY (PokeName, AtkName,AtkGroup))''')

    def insertPokeAttacks(self, pokeName = None, atkName = None, atkGroup = None , condition = None):
        if not (isinstance(pokeName,str) ):
            raise TypeError('Poke name not str')
        if not (isinstance(atkName,str) ):
            raise TypeError('atk name not str')
        if not (isinstance(atkGroup,str) ):
            raise TypeError('atk group not str')
        if not (isinstance(condition,str) ):
            raise TypeError('condition not str')
            
        self._certifyConnection()
        
        attackData = (pokeName,atkName, atkGroup, condition)
        AM = AttacksManager()
        if AM.getAttackByName(attackData[1]) is None:
            raise self.DescriptionError('Attack '+ atkName+ ' is not in database')
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO PokeAttacks VALUES (?,?,?,?)",attackData)
            except sqlite3.OperationalError as error:
                self.createTablePkAttacks()
                cursor.execute("INSERT INTO PokeAttacks VALUES (?,?,?,?)",attackData)
        
    def getPokemonAttacks(self,name):
        self._certifyConnection()
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
                atk = AM.getAttackByName(attack[1])
                atk.setCondition(attack[3])
                attackGroups[attack[2]].append(atk)
            return attackGroups
        else:
            raise self.AttackNotFoundError('Pokemon was not found')
		
		
    def view(self):
        self._certifyConnection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokeAttacks'):
                print(row)
				
    class DescriptionError(Exception):
        pass
        
class PokeItemsManager(Manager):
    def createTablePkItems(self):
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS PokeItems(PokeName TEXT , ItemName TEXT, ItemChance INTEGER,PRIMARY KEY(PokeName,ItemName))''')

    def insertPokeItem(self, pokeName = None, itemName = None, itemChance = None):
        if not (isinstance(pokeName,str) ):
            raise TypeError('Poke name not str')
        if not (isinstance(itemName,str) ):
            raise TypeError('item name not str')
        if not(isinstance(itemChance,int)):
            raise TypeError('item chance not int')
        self._certifyConnection()
        
        pkItemData = (pokeName,itemName,itemChance)
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO PokeItems VALUES (?,?,?)",pkItemData)
            except sqlite3.OperationalError as error:
                self.createTablePkItems()
                cursor.execute("INSERT INTO PokeItems VALUES (?,?,?)",pkItemData)
        		
    def getPokemonItems(self,pokemonName):
        self._certifyConnection()
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
        self._certifyConnection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokeItems'):
                print(row)
				
    class DescriptionError(Exception):
        pass


class PokeDexNavItemsManager(Manager):
    def createTablePkDexNavItems(self):
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS PokeDexNavItems(PokeName TEXT , ItemName TEXT,PRIMARY KEY(PokeName,ItemName))''')

    def insertPokeItem(self, pokeName = None, itemName = None):
        if not (isinstance(pokeName,str) ):
            raise TypeError('Poke name not str')
        if not (isinstance(itemName,str) ):
            raise TypeError('item name not str')

        self._certifyConnection()
        
        pkItemData = (pokeName,itemName)
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO PokeDexNavItems VALUES (?,?)",pkItemData)
            except sqlite3.OperationalError as error:
                self.createTablePkItems()
                cursor.execute("INSERT INTO PokeDexNavItems VALUES (?,?)",pkItemData)
                
    def getPokemonDexNavItems(self,pokemonName):
        self._certifyConnection()
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
        self._certifyConnection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokeDexNavItems'):
                print(row)
                

class PokemonEVWorthManager(Manager):
    def createTablePokemonEVWorth(self):
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS PokemonEVWorth(PokeName TEXT , Stat TEXT, Value INTEGER, PRIMARY KEY(PokeName,Stat))''')

    def insertPokeEvWorth(self,pokeName, ev = None):
        if not (isinstance(ev,EV) ):
            raise TypeError('ev not of type EV')
        if not (isinstance(pokeName,str) ):
            raise TypeError('Pokemon name not str')
        self._certifyConnection()
        
        evData = (pokeName,str(ev.getStat()), ev.getValue())
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO PokemonEVWorth VALUES (?,?,?)",evData)
            except sqlite3.OperationalError as error:
                self.createTablePokemonEVWorth()
                cursor.execute("INSERT INTO PokemonEVWorth VALUES (?,?,?)",evData)		
		
    def getPokemonEVWorth(self,pokemonName):
        self._certifyConnection()
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
        self._certifyConnection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokemonEVWorth'):
                print(row)

class PokemonManager(Manager):
    def createTablePokemon(self):
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS Pokemon(PokeName TEXT PRIMARY KEY, NationalDex INTEGER, CentralDex INTEGER, CoastalDex INTEGER, MountainDex INTEGER, HoennDex INTEGER, MaleRate REAL, FemaleRate Real, Genderless INTEGER, Type1 TEXT, Type2 TEXT, Classification TEXT, HeightMeters REAL, HeightInches INTEGER, WeightKg REAL, WeightLbs REAL, ORASCr INTEGER, XYCr INTEGER, BaseEggSteps INTEGER, PathImg TEXT, PathSImg TEXT, ExpGrowth INTEGER, ExpGrowthClassification TEXT, BaseHappiness INTEGER, SkyBattle TEXT, Normal REAL, Fire REAL, Water REAL, Electric REAL, Grass REAL, Ice REAL, Fighting REAL, Poison REAL, Ground REAL, Flying REAL, Psychic REAL, Bug REAL, Rock REAL, Ghost REAL, Dragon REAL, Dark REAL, Steel REAL, Fairy REAL, EggGroup1 TEXT, EggGroup2 TEXT, LocationX TEXT, LocationY TEXT, LocationOR TEXT, LocationAS TEXT, DexTextX TEXT, DexTextY TEXT , DexTextOR TEXT, DexTextAS TEXT, Hp INTEGER, Attack INTEGER, Defense INTEGER, SpAttack INTEGER, SpDefense INTEGER, Speed INTEGER, Total INTEGER)''')

    def insertPokemon(self, pokemon):
        if not (isinstance(pokemon,pkm.Pokemon) ):
            raise TypeError('Poke name not Pokemon')

        name = pokemon.getName()
        nationalDex = pokemon.getDexNum().getNational()
        centralDex = pokemon.getDexNum().getCentral()
        coastalDex = pokemon.getDexNum().getCoastal()
        mountainDex = pokemon.getDexNum().getMountain()
        hoennDex = pokemon.getDexNum().getHoenn()
        maleRate = pokemon.getGender().getMaleRate()
        femaleRate = pokemon.getGender().getFemaleRate()
        genderless = int(pokemon.getGender().isGenderless())
        type1 = str(pokemon.getTypes().getType1())
        type2 = str(pokemon.getTypes().getType2())
        classification = pokemon.getClassification()
        heightMeters = pokemon.getHeight().getValueInMeters()
        heightInches = pokemon.getHeight().getValueInInches()
        weightKg = pokemon.getWeight().getValueInKg()
        weightLbs = pokemon.getWeight().getValueInLbs()
        oRASCr = pokemon.getCaptureRate().getORAS()
        yXCr = pokemon.getCaptureRate().getXY()
        baseEggSteps = pokemon.getBaseEggSteps()
        pathImg = pokemon.getImagePath().getPathImg()
        pathSImg = pokemon.getImagePath().getSPathImg()
        expGrowth = pokemon.getExpGrowth().getExpGrowth()
        expGrowthClassification = pokemon.getExpGrowth().getClassification()
        baseHappiness = pokemon.getHappiness()
        skyBattle = pokemon.getSkyBattle()
        normal = pokemon.getWeaknesses()['Normal']
        fire = pokemon.getWeaknesses()['Fire']
        water = pokemon.getWeaknesses()['Water']
        electric = pokemon.getWeaknesses()['Electric']
        grass = pokemon.getWeaknesses()['Grass']
        ice = pokemon.getWeaknesses()['Ice']
        fighting = pokemon.getWeaknesses()['Fighting']
        poison = pokemon.getWeaknesses()['Poison']
        ground = pokemon.getWeaknesses()['Ground']
        flying = pokemon.getWeaknesses()['Flying']
        psychic = pokemon.getWeaknesses()['Psychic']
        bug = pokemon.getWeaknesses()['Bug']
        rock = pokemon.getWeaknesses()['Rock']
        ghost = pokemon.getWeaknesses()['Ghost']
        dragon = pokemon.getWeaknesses()['Dragon']
        dark = pokemon.getWeaknesses()['Dark']
        steel = pokemon.getWeaknesses()['Steel']
        fairy = pokemon.getWeaknesses()['Fairy']
        eggGroup1 = str(pokemon.getEggGroups().getGroup1())
        eggGroup2 = str(pokemon.getEggGroups().getGroup2())
        locationX = pokemon.getLocation().getX()
        locationY = pokemon.getLocation().getY()
        locationOR = pokemon.getLocation().getOR()
        locationAS = pokemon.getLocation().getAS()
        dexTextX = pokemon.getDexText().getX()
        dexTextY = pokemon.getDexText().getY()
        dexTextOR = pokemon.getDexText().getOR()
        dexTextAS = pokemon.getDexText().getAS()
        hp = pokemon.getStats().getHp()
        attack = pokemon.getStats().getAttack()
        defense = pokemon.getStats().getDefense()
        spAttack = pokemon.getStats().getSpAttack()
        spDefense = pokemon.getStats().getSpDefense()
        speed = pokemon.getStats().getSpeed()
        total = hp+attack+defense+spAttack+spDefense+speed
        
        pkmData = (name,
                   nationalDex,
                   centralDex,
                   coastalDex,
                   mountainDex,
                   hoennDex,
                   maleRate,
                   femaleRate,
                   genderless,
                   type1,
                   type2,
                   classification,
                   heightMeters,
                   heightInches,
                   weightKg,
                   weightLbs,
                   oRASCr,
                   yXCr,
                   baseEggSteps,
                   pathImg,
                   pathSImg,
                   expGrowth,
                   expGrowthClassification,
                   baseHappiness,
                   skyBattle,
                   normal,
                   fire,
                   water, 
                   electric, 
                   grass,
                   ice,
                   fighting, 
                   poison,
                   ground,
                   flying,
                   psychic ,
                   bug ,
                   rock ,
                   ghost ,
                   dragon ,
                   dark ,
                   steel ,
                   fairy ,
                   eggGroup1,
                   eggGroup2,
                   locationX,
                   locationY,
                   locationOR,
                   locationAS,
                   dexTextX,
                   dexTextY,
                   dexTextOR,
                   dexTextAS,
                   hp,
                   attack,
                   defense,
                   spAttack,
                   spDefense,
                   speed,
                   total)
        
        self._certifyConnection()
        
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Pokemon VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",pkmData)
            except sqlite3.OperationalError as error:
                self.createTablePokemon()
                cursor.execute("INSERT INTO Pokemon VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",pkmData)
             
    def __correctLocation(self):
        self._certifyConnection()
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
      
    def getPokemonByDexNum(self):
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT NationalDex,PokeName FROM Pokemon ORDER BY NationalDex')
            return cursor.fetchall()                        
                        
    def getPokemonByName(self,name):
        self._certifyConnection()
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
        self._certifyConnection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM Pokemon'):
                print(row)

    class DescriptionError(Exception):
        pass

class PokemonEvoChainManager(Manager):
    def createTablePokemonEvoChain(self):
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS PokemonEvoChain(PokeName TEXT ,EvoNode TEXT, PRIMARY KEY(PokeName,EvoNode))''')

    def insertEvoNode(self,pokeName, evoNode):
        if not (isinstance(pokeName,str) ):
            raise TypeError('Pokemon name not str')
        self._certifyConnection()
        
        evData = (pokeName,str(evoNode))
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO PokemonEvoChain VALUES (?,?)",evData)
            except sqlite3.OperationalError as error:
                self.createTablePokemonEvoChain()
                cursor.execute("INSERT INTO PokemonEvoChain VALUES (?,?)",evData)
                
    def removeNode(self,pokeName,evoNode):
        if not (isinstance(pokeName,str) ):
            raise TypeError('Pokemon name not str')
        self._certifyConnection()
        
        evData = (pokeName,str(evoNode))
        with self._connection as conn:
            cursor = conn.cursor()
            print(evData[1])
            cursor.execute("DELETE FROM PokemonEvoChain WHERE PokeName=(?) AND EvoNode=(?)",evData)

    def drop(self):
        self._certifyConnection()
        with self._connection as conn:
            conn.cursor().execute('DROP TABLE PokemonEvoChain')
            

                
    def updateEvoNode(self,pokeName,add = None,remove = None):
        if not (isinstance(pokeName,str) ):
            raise TypeError('Pokemon name not str')
        self._certifyConnection()
        
        with self._connection as conn:
            cursor = conn.cursor()
            evData = (pokeName,)
            cursor.execute("SELECT EvoNode FROM PokemonEvoChain WHERE PokeName=(?)",evData)
            nodes = cursor.fetchall()
            if(nodes):
                for node in nodes:
                    print(node)
                if add:
                    self.insertEvoNode(pokeName,add)
                    print(add)
                elif remove:
                    self.removeNode(pokeName,remove)
                    

    
    def getPokemonEvoChain(self,pokemonName):
        self._certifyConnection()
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
        self._certifyConnection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokemonEvoChain'):
                print(row)

class ItemCategoryManager(Manager):
    def createItemCategoryTable(self):
        self._certifyConnection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS ItemCategory(ItemName TEXT PRIMARY KEY, Category TEXT)''')

    def insertItem(self, itemName = None, category = None):
        if not (isinstance(itemName,str) ):
            raise TypeError('Poke name not str')
        if not (isinstance(category,str) ):
            raise TypeError('atk name not str')
        self._certifyConnection()
        
        pkItemData = (itemName,category)
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO ItemCategory VALUES (?,?)",pkItemData)
            except sqlite3.OperationalError as error:
                self.createTablePkItems()
                cursor.execute("INSERT INTO ItemCategory VALUES (?,?)",pkItemData)

    def view(self):
        self._certifyConnection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM ItemCategory ORDER BY Category, ItemName'):
                print(row)
    def drop(self):
        self._certifyConnection()
        with self._connection as conn:
            conn.cursor().execute('DROP TABLE ItemCategory')

if __name__ == '__main__':
    PokemonEvoChainManager().view()
    
    
    