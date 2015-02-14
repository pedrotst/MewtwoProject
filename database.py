import sqlite3
from pokemonUtils import *

def test():
    conn = sqlite3.connect('PokemonTest.db')
    with conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE Abilities(Name TEXT PRIMARY KEY,Description TEXT)''')
##        c.execute('''CREATE TABLE IF NOT EXISTS Pokemons(Name TEXT,National INTEGER,Abilities INTEGER,FOREIGN KEY(Abilities))''')

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
            cursor.execute('''CREATE TABLE  IF NOT EXISTS PokeAttacks(PokeName TEXT, AtkName TEXT, AtkGroup TEXT, Condition TEXT, PRIMARY KEY (PokeName, AtkGroup, Condition))''')

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
        
    def getAttacksByPoke(self,name):
        self._certifyConnection()
        search = (name,)
        if not isinstance(name,str):
            raise TypeError('Pokemon\'s name must be a string')
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM PokeAttacks WHERE PokeName=? ORDER BY Condition',search)
        attackData = cursor.fetchall()
        if(attackData is not None):
            print(*attackData, sep='\n')
            #return attackData
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
            cursor.execute('''CREATE TABLE  IF NOT EXISTS PokeItems(PokeName TEXT PRIMARY KEY, ItemName Text''')

    def insertPokeItem(self, pokeName = None, itemName = None):
        if not (isinstance(pokeName,str) ):
            raise TypeError('Poke name not str')
        if not (isinstance(itemName,str) ):
            raise TypeError('atk name not str')
        self._certifyConnection()
        
        pkItemData = (pokeName,itemName) #itemname nao devia ser uma lista? to confuso. Senao ta pronto
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO PokeItems VALUES (?,?)",pkItemData)
            except sqlite3.OperationalError as error:
                self.createTablePkItems()
                cursor.execute("INSERT INTO PokeItems VALUES (?,?)",pkItemData)
        
    def getItemsByPoke(self,name): #todo
        self._certifyConnection()
        search = (name,)
        if not isinstance(name,str):
            raise TypeError('Pokemon\'s name must be a string')
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM PokeAttacks WHERE PokeName=? ORDER BY Condition',search)
        attackData = cursor.fetchall()
        if(attackData is not None):
            print(*attackData, sep='\n')
            #return attackData
        else:
            raise self.AttackNotFoundError('Pokemon was not found')
		
		
    def view(self):
        self._certifyConnection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM PokeAttacks'):
                print(row)
				
    class DescriptionError(Exception):
        pass
'''#depois eu ia montar o PokeAttacksManager
#e rodar ele pra inserir os pokemons e que ataques eles aprendem

#faz a tabela PokemonAttackers
#ela vai ter 3 columns
#a primeira é o nome do pokemon
#a segunda uma condicao
#a terceira é o nome do atk
#só que a combinacao da primeira e da terceira colunas tem que ser unica
create table t (
PokemonName text,
Condition text,
AttackName text,
primary key (PokemonName,AttackName)
)'''
if __name__ == '__main__':
    c = AttacksManager()
    c.getAttackByName("Gust")