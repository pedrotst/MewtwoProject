from pokemonUtils import *
from database import *
import os

""" Pokemon Class for Database--------------------------------------------------
"""
class Pokemon:
    def __init__(self,poke=0):
        if isinstance(poke,dict):
            ##Get Name
            self.__setName(poke)

            ##Get Dex numbers
            self.__setNum(poke)

            ##Get Gender
            self.__setGender(poke)

            ##Get Pokemon Type
            self.__setTypes(poke)

            ##Get Pokemon Classification
            self.__setClassification(poke)

            ##Get Pokemon Height
            self.__setHeight(poke)

            ##Get Pokemon Weight
            self.__setWeight(poke)

            ##Get Capture Rate
            self.__setCaptureRate(poke)
            
            ##Get Base Egg Step Count
            self.__setBaseEggSteps(poke)

            ##Get Image Path
            self.__setImagePath(poke)
            
            ##Get Abilities
            self.__setAbilities(poke)

            ##Get Experience Growth
            self.__setExpGrowth(poke)

            ##Get Base Happiness
            self.__setBaseHappiness(poke)

            ##Get EV Worth
            self.__setEvWorth(poke)

            ##Get SkyBattle
            self.__setSkyBattle(poke)

            ##Get Weaknesses
            self.__setWeaknesses(poke)

            ##Get Wild Items
            self.__setWildItems(poke)

            ##Get EggGroup
            self.__setEggGroup(poke)

            ##Get EvoChain
            self.__setEvoChain(poke)

            ##Get Location
            self.__setLocation(poke)

            ##Get DexText
            self.__setDexText(poke)

            ##Get Attacks
            self.__setAttacks(poke)

            ##Get Stats
            self.__setStats(poke)

            
            
        else:
            self.__name = ''
            self.__num = DexNum()
            self.__gender = PokeGender()
            self.__types = PokeTypes()
            self.__classification = ''
            self.__height = PokeHeight()
            self.__weight = PokeWeight()
            self.__captureRate = 0
            self.__baseEggSteps = 0
            self.__img = PokeImage()
##            self.__abilities = PokeAbilities()
            self.__stats = Stats()

    def __str__(self):
        string =  str(self.__name)
##        string += '\n'+str(self.__num)
##        string += '\n'+str(self.__gender)
##        string += '\n'+str(self.__types)
##        string += '\n'+str(self.__classification)
##        string += '\n'+str(self.__height)
##        string += '\n'+str(self.__weight)
##        string += '\n'+str(self.__captureRate)
##        string += '\n'+str(self.__baseEggSteps)
##        string += '\n'+str(self.__img)
##        string += '\n'+str(self.__abilities)
##        string += '\n'+str(self.__expGrowth)
##        string += '\n'+str(self.__baseHappiness)
##        string += '\n'+str(self.__evWorth)
##        string += '\n'+str(self.__skyBattle)
##        string += '\n'+str(self.__weaknesses)
        
        return string

    def __repr__(self):
        return self.__str__()

    ##Save Pokemon
    def createAbilityDatabase(self):
        manager = AbilitiesManager()
        manager.createTableAbilities()
        for ability in self.__abilities.getAbilities()+self.__abilities.getHiddenAbilities():
            try:
                manager.insertAbility(ability = ability)
            except sqlite3.IntegrityError:
                pass

    def createPokemonAbilityDatabase(self):
        manager = PokemonAbilitiesManager()
        managerHidden = PokemonHiddenAbilitiesManager()
        for ability in self.__abilities.getAbilities():
            try:
                manager.insertAbility(self.__name,ability = ability)
            except sqlite3.IntegrityError:
                pass
        for ability in self.__abilities.getHiddenAbilities():
            try:
                managerHidden.insertAbility(self.__name,ability = ability)
            except sqlite3.IntegrityError:
                pass

    def createAttacksDatabase(self):
        manager = AttacksManager()
        manager.createTableAttacks()
        for key in self.__attacks.getAttackGroups():
            for attack in self.__attacks.getAttackGroup(key):
                try:
                    manager.insertAttack(attack = attack)
                except sqlite3.IntegrityError:
                    pass
                    
    def createPokemonAttacksDatabase(self):
        managerAtt = AttacksManager()
        managerPkAtts = PokeAttacksManager()
        for key in self.__attacks.getAttackGroups():
            for attack in self.__attacks.getAttackGroup(key):
                try:
                    managerPkAtts.insertPokeAttacks(self.__name, attack.getName(), key, str(attack.getCondition()))
                except sqlite3.IntegrityError:
                    pass

        
    ##Load Pokemon
    def load(self,name):
        dirName = 'PokeData/'+name+'/'
        with open(dirName+name+'.pkm','r') as f:
            data = f.readlines()[2:]
            self.__name = data[0].strip()
            self.__num = DexNum(data[1].split(':')[1].strip(),
                                data[2].split(':')[1].strip(),
                                data[3].split(':')[1].strip(),
                                data[4].split(':')[1].strip(),
                                data[5].split(':')[1].strip())
            if(data[6].find('Male')!=-1):
                self.__gender = PokeGender(float(data[6].split(':')[1].strip().strip('%')),
                                           float(data[7].split(':')[1].strip().strip('%')))
                genderless = 0
            else:
                self.__gender = PokeGender()
                genderless = 1
                
            self.__types = PokeTypes(data[8-genderless].split(':')[1].strip(),
                                     data[9-genderless].split(':')[1].strip())
            self.__classification = data[10-genderless].strip()
            self.__height = PokeHeight(data[11-genderless].split(':')[1].strip(),
                                     data[12-genderless].split(':')[1].strip())
            self.__weight = PokeWeight(data[13-genderless].split(':')[1].strip(),
                                     data[14-genderless].split(':')[1].strip())
            self.__captureRate = int(data[15-genderless].strip())
            self.__baseEggSteps = int(data[16-genderless].strip())
            self.__img = PokeImage(data[17-genderless].strip(),
                                   data[18-genderless].strip())
            
            return self
        
    ##Ensures that directory f exists
    def __ensure_dir(self,f):
        d = os.path.dirname(f)
        if not os.path.exists(d):
            os.makedirs(d)        
##Set Name----------------------------------------------------------------------
    def  __setName(self,poke):
        self.__name = poke['Name']
        try:
            print(self.__name)
        except UnicodeEncodeError:
            print(self.__name.encode('utf-8','ignore'))
            
##Set Num----------------------------------------------------------------------
    def __setNum(self,poke):
        self.__num = DexNum(poke['No']['National'][1:],
                            poke['No']['Central'][1:],
                            poke['No']['Coastal'][1:],
                            poke['No']['Mountain'][1:],
                            poke['No']['Hoenn'][1:])

##Set Gender----------------------------------------------------------------------
    def __setGender(self,poke):
        try:
            male = poke['Gender']['Male']
            female = poke['Gender']['Female']
            self.__gender = PokeGender(float(male[:-1])
                                       ,float(female[:-1]))
        except (KeyError,TypeError):
            self.__gender = PokeGender()

##Set Types----------------------------------------------------------------------
    def __setTypes(self,poke):
        try:
            type1 = poke['Types'][0]
            type2 = poke['Types'][1]

            self.__types = PokeTypes(type1,type2)
        except IndexError:
            self.__types = PokeTypes(type1)

##Set Classification----------------------------------------------------------------------
    def __setClassification(self,poke):
        self.__classification = poke['Classification'].pop()

##Set Height----------------------------------------------------------------------
    def __setHeight(self,poke):
        Height = poke['Height'][0]
        h = Height.split()
        if(self.__num.getNational() == 720):
            self.__height = []
            self.__height.append(PokeHeight(h[3],h[0]))
            self.__height.append(PokeHeight(h[5],h[2]))
        else:            
            self.__height = PokeHeight(h[1],h[0])

##Set Weight----------------------------------------------------------------------
    def __setWeight(self,poke):
        Weight = poke['Weight'][0]
        w = Weight.split()
        if(self.__num.getNational() == 720):
            self.__weight = []
            self.__weight.append(PokeWeight(w[3],w[0]))
            self.__weight.append(PokeWeight(w[5],w[2]))
        else:            
            self.__weight = PokeWeight(w[1],w[0])
            
##Set CaptureRate----------------------------------------------------------------------
    def __setCaptureRate(self,poke):
        self.__captureRate = PokeCR(poke['Capture Rate'])

##Set BaseEggSteps----------------------------------------------------------------------
    def __setBaseEggSteps(self,poke):
        steps = poke['Base Egg Steps'][0].replace(',','').strip()
        if(steps == ''):
            steps = 0
        self.__baseEggSteps = int(steps)

##Set Image Path----------------------------------------------------------------------
    def __setImagePath(self,poke):
        self.__img = PokeImage(poke['Picture'],poke['Picture-Shiny'])


##Set Abilities----------------------------------------------------------------------
    def __setAbilities(self,poke):
        self.__abilities = PokeAbilities(poke['Abilities'])


##Set ExpGrowth----------------------------------------------------------------------
    def __setExpGrowth(self,poke):
        self.__expGrowth = PokeExpGrowth(poke['Experience Growth'])

##Set baseHappines----------------------------------------------------------------------
    def __setBaseHappiness(self,poke):
        self.__baseHappiness = int(poke['Base Happiness'].pop())

##Set evWorth----------------------------------------------------------------------
    def __setEvWorth(self,poke):
        if(self.__num.getNational() == 386):
            ev = poke['Effort Values Earned'][0].split('Normal Forme')
            ev = ev[1].split('Attack Forme')
            evNormal = ev[0]
            ev = ev[1].split('Defense Forme')
            evAttack = ev[0]
            ev = ev[1].split('Speed Forme')
            evDefense = ev[0]
            evSpeed = ev[1]
            self.__evWorth = [PokeEVWorth([evNormal]),
                              PokeEVWorth([evAttack]),
                              PokeEVWorth([evDefense]),
                              PokeEVWorth([evSpeed])]

        elif(self.__num.getNational() == 413):
            ev = poke['Effort Values Earned'][0].split('Plant Cloak')
            ev = ev[1].split('Sandy Cloak')
            evPlant = ev[0]
            ev = ev[1].split('Trash Cloak')
            evSandy = ev[0]
            evTrash = ev[1]
            self.__evWorth = [PokeEVWorth([evPlant]),
                              PokeEVWorth([evSandy]),
                              PokeEVWorth([evTrash])]
        elif(self.__num.getNational() == 492):
            ev = poke['Effort Values Earned'][0].split('Land Forme')
            ev = ev[1].split('Sky Forme')
            evLand = ev[0]
            evSky = ev[1]
            self.__evWorth = [PokeEVWorth([evLand]),
                              PokeEVWorth([evSky])]
        elif(self.__num.getNational() == 555):
            ev = poke['Effort Values Earned'][0].split('Standard')
            ev = ev[1].split('Zen Mode')
            evStandard = ev[0]
            evZen = ev[1]
            self.__evWorth = [PokeEVWorth([evStandard]),
                              PokeEVWorth([evZen])]
        elif(self.__num.getNational() == 641 or self.__num.getNational() == 642 or self.__num.getNational() == 645):
            ev = poke['Effort Values Earned'][0].split('Incarnate Forme')
            ev = ev[1].split('Therian Forme')
            evIncarnate = ev[0]
            evTherian = ev[1]
            self.__evWorth = [PokeEVWorth([evIncarnate]),
                              PokeEVWorth([evTherian])]
        elif(self.__num.getNational() == 646):
            ev = poke['Effort Values Earned'][0].split('Kyurem',1)
            ev = ev[1].split('Black Kyurem')
            evKyurem = ev[0]
            ev = ev[1].split('White Kyurem')
            evBKyurem = ev[0]
            evWKyurem = ev[1]
            self.__evWorth = [PokeEVWorth([evKyurem]),
                              PokeEVWorth([evBKyurem]),
                              PokeEVWorth([evWKyurem])]
        elif(self.__num.getNational() == 648):
            ev = poke['Effort Values Earned'][0].split('Aria Forme')
            ev = ev[1].split('Pirouette Forme')
            evAria = ev[0]
            evPirouette = ev[1]
            self.__evWorth = [PokeEVWorth([evAria]),
                              PokeEVWorth([evPirouette])]
        else:
            self.__evWorth = PokeEVWorth(poke['Effort Values Earned'])
##Set SkyBattle----------------------------------------------------------------------
    def __setSkyBattle(self,poke):
        self.__skyBattle = poke['Eligible for Sky Battle?'].pop().strip()

##Set Weaknesses----------------------------------------------------------------------
    def __setWeaknesses(self,poke):
        self.__weaknesses = PokeWeaknesses(poke['Weaknesses'])

##Set WildHoldItem----------------------------------------------------------------------
    def __setWildItems(self,poke):
        self.__wildItems = PokeWildItems(poke['Wild Hold Item'])

##Set EggGroup----------------------------------------------------------------------
    def __setEggGroup(self,poke):
        self.__eggGroups = PokeEggGroup(poke['Egg Groups'])
        
##Set EvoChain----------------------------------------------------------------------
    def __setEvoChain(self,poke):
        self.__evoChain = PokeEvoChain(poke['Evo Chain'])

##Set Location----------------------------------------------------------------------
    def __setLocation(self,poke):
        self.__location = PokeLocation(poke['Location'])
        
##Set DexText----------------------------------------------------------------------
    def __setDexText(self,poke):
        self.__dexText = PokeDexText(poke['Flavour Text'])
        
##Set Attacks----------------------------------------------------------------------
    def __setAttacks(self,poke):
        self.__attacks = PokeAttacks(poke['Attacks'])
##Set Stats----------------------------------------------------------------------
    def __setStats(self,poke):
        self.__stats = PokeStats(poke['Stats'])
 
