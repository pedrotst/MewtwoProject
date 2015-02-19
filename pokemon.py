from pokemonUtils import *
from database import *
import os

""" Pokemon Class for Database--------------------------------------------------
"""
class Pokemon:
    def __init__(self,poke=None):
        if isinstance(poke,dict):
            ##Get Name
            self.__setFromDictName(poke)

            ##Get Dex numbers
            self.__setFromDictNum(poke)

            ##Get Gender
            self.__setFromDictGender(poke)

            ##Get Pokemon Type
            self.__setFromDictTypes(poke)

            ##Get Pokemon Classification
            self.__setFromDictClassification(poke)

            ##Get Pokemon Height
            self.__setFromDictHeight(poke)

            ##Get Pokemon Weight
            self.__setFromDictWeight(poke)

            ##Get Capture Rate
            self.__setFromDictCaptureRate(poke)
            
            ##Get Base Egg Step Count
            self.__setFromDictBaseEggSteps(poke)

            ##Get Image Path
            self.__setFromDictImagePath(poke)
            
            ##Get Abilities
            self.__setFromDictAbilities(poke)

            ##Get Experience Growth
            self.__setFromDictExpGrowth(poke)

            ##Get Base Happiness
            self.__setFromDictBaseHappiness(poke)

            ##Get EV Worth
            self.__setFromDictEvWorth(poke)

            ##Get SkyBattle
            self.__setFromDictSkyBattle(poke)

            ##Get Weaknesses
            self.__setFromDictWeaknesses(poke)

            ##Get Wild Items
            self.__setFromDictWildItems(poke)

            ##Get EggGroup
            self.__setFromDictEggGroup(poke)

            ##Get EvoChain
            self.__setFromDictEvoChain(poke)

            ##Get Location
            self.__setFromDictLocation(poke)

            ##Get DexText
            self.__setFromDictDexText(poke)

            ##Get Attacks
            self.__setFromDictAttacks(poke)

            ##Get Stats
            self.__setFromDictStats(poke)

        if isinstance(poke,str):
            name = poke
            db = DatabaseManager()
            data = db.getPokemonByName(name)

            pokeData = data[0]
            pokeAbilities = data[1]
            pokeHiddenAbilities = data[2]
            pokeAttacks = data[3]
            pokeItems = data[4]
            pokeDexNavItems = data[5]
            pokeEvWorth = data[6]

            ##Get Name
            self.__setFromDbName(pokeData[0])

            ##Get Dex numbers
            self.__setFromDbNum(pokeData[1],
                                pokeData[2],
                                pokeData[3],
                                pokeData[4],
                                pokeData[5])

            ##Get Gender
            self.__setFromDbGender(pokeData[6],
                                   pokeData[7])

            ##Get Pokemon Type
            self.__setFromDbTypes(pokeData[9],
                                  pokeData[10])

            ##Get Pokemon Classification
            self.__setFromDbClassification(pokeData[11])

            ##Get Pokemon Height
            self.__setFromDbHeight(pokeData[12],
                                   pokeData[13])

            ##Get Pokemon Weight
            self.__setFromDbWeight(pokeData[14],
                                   pokeData[15])

            ##Get Capture Rate
            self.__setFromDbCaptureRate(pokeData[16],
                                        pokeData[17])
            
            ##Get Base Egg Step Count
            self.__setFromDbBaseEggSteps(pokeData[18])

            ##Get Image Path
            self.__setFromDbImagePath(pokeData[19],
                                        pokeData[20])
            
            ##Get Abilities
            self.__setFromDbAbilities(pokeAbilities,pokeHiddenAbilities)

            ##Get Experience Growth
            self.__setFromDbExpGrowth(pokeData[21],
                                      pokeData[22])

            ##Get Base Happiness
            self.__setFromDbBaseHappiness(pokeData[23])

            ##Get EV Worth
            self.__setFromDbEvWorth(pokeEvWorth)

            ##Get SkyBattle
            self.__setFromDbSkyBattle(pokeData[24])

            ##Get Weaknesses
            self.__setFromDbWeaknesses(pokeData[25],
                                       pokeData[26],
                                       pokeData[27],
                                       pokeData[28],
                                       pokeData[29],
                                       pokeData[30],
                                       pokeData[31],
                                       pokeData[32],
                                       pokeData[33],
                                       pokeData[34],
                                       pokeData[35],
                                       pokeData[36],
                                       pokeData[37],
                                       pokeData[38],
                                       pokeData[39],
                                       pokeData[40],
                                       pokeData[41],
                                       pokeData[42])

            ##Get Wild Items
            self.__setFromDbWildItems(pokeItems,pokeDexNavItems)

            ##Get EggGroup
            self.__setFromDbEggGroup(pokeData[43],pokeData[44])
##
##            ##Get EvoChain
##            self.__setFromDbEvoChain(poke)

            ##Get Location
            self.__setFromDbLocation(pokeData[45],
                                     pokeData[46],
                                     pokeData[47],
                                     pokeData[48])

            ##Get DexText
            self.__setFromDbDexText(pokeData[49],
                                    pokeData[50],
                                    pokeData[51],
                                    pokeData[52])

            ##Get Attacks
            self.__setFromDbAttacks(pokeAttacks)

            ##Get Stats
            self.__setFromDbStats(pokeData[53],
                                  pokeData[54],
                                  pokeData[55],
                                  pokeData[56],
                                  pokeData[57],
                                  pokeData[58],
                                  pokeData[59])            


    def __str__(self):
        string =  str(self.__name)
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
        managerPkAtts = PokeAttacksManager()
        for key in self.__attacks.getAttackGroups():
            for attack in self.__attacks.getAttackGroup(key):
                try:
                    managerPkAtts.insertPokeAttacks(self.__name, attack.getName(), key, str(attack.getCondition()))
                except sqlite3.IntegrityError:
                    pass

    def createPokemonItemsDatabase(self):
        managerPkItems = PokeItemsManager()
        for item in self.__wildItems.getNormalItems():
            if(item != 'None' and item != ''):
                parts = item.split(' - ')
                itemName = parts[0].strip()
                itemChance = int(parts[1].strip(' %(SuperSize)'))
                try:
                    managerPkItems.insertPokeItem(self.__name, itemName,itemChance)
                except sqlite3.IntegrityError:
                    pass

    def createPokemonDexNavItemsDatabase(self):
        managerPkItems = PokeDexNavItemsManager()
        dexNavItems = self.__wildItems.getDexNavItems()
        if dexNavItems:
            for item in self.__wildItems.getDexNavItems():
                item = item.strip(' %')
                if(item != 'None' and item != ''):
                    try:
                        managerPkItems.insertPokeDexNavItem(self.__name, item)
                    except sqlite3.IntegrityError:
                        pass

    def createPokemonEVWorthDatabase(self):
        manager = PokemonEVWorthManager()
        for ev in self.getEVWorth().getEVs():
            print(ev)
            try:
                manager.insertPokeEvWorth(self.__name,ev)
            except sqlite3.IntegrityError:
                pass

    def createPokemonDatabase(self):
        manager = PokemonManager()
        manager.insertPokemon(self)

        
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
    def  __setFromDictName(self,poke):
        self.__name = poke['Name']
        try:
            print(self.__name)
        except UnicodeEncodeError:
            print(self.__name.encode('utf-8','ignore'))

    def  __setFromDbName(self,name):
        self.__name = name
        try:
            print(self.__name)
        except UnicodeEncodeError:
            print(self.__name.encode('utf-8','ignore'))


##Get Name----------------------------------------------------------------------
    def getName(self):
        return self.__name

##Set Num----------------------------------------------------------------------
    def __setFromDictNum(self,poke):
        self.__num = DexNum(poke['No']['National'][1:],
                            poke['No']['Central'][1:],
                            poke['No']['Coastal'][1:],
                            poke['No']['Mountain'][1:],
                            poke['No']['Hoenn'][1:])

    def __setFromDbNum(self,national,central,coastal,mountain,hoenn):
        self.__num = DexNum(national,
                            central,
                            coastal,
                            mountain,
                            hoenn)


##Get Num----------------------------------------------------------------------
    def getDexNum(self):
        return self.__num

##Set Gender----------------------------------------------------------------------
    def __setFromDictGender(self,poke):
        try:
            male = poke['Gender']['Male']
            female = poke['Gender']['Female']
            self.__gender = PokeGender(float(male[:-1])
                                       ,float(female[:-1]))
        except (KeyError,TypeError):
            self.__gender = PokeGender()

    def __setFromDbGender(self,mRate,fRate):
            self.__gender = PokeGender(mRate,fRate)


##Get Gender----------------------------------------------------------------------
    def getGender(self):
        return self.__gender

##Set Types----------------------------------------------------------------------
    def __setFromDictTypes(self,poke):
        try:
            type1 = poke['Types'][0]
            type2 = poke['Types'][1]

            self.__types = PokeTypes(type1,type2)
        except IndexError:
            self.__types = PokeTypes(type1)

    def __setFromDbTypes(self,type1,type2):
        self.__types = PokeTypes(type1,type2)
    

##Get Types----------------------------------------------------------------------
    def getTypes(self):
        return self.__types

##Set Classification----------------------------------------------------------------------
    def __setFromDictClassification(self,poke):
        self.__classification = poke['Classification'].pop()

    def __setFromDbClassification(self,data):
        self.__classification = data

##Get Classification----------------------------------------------------------------------
    def getClassification(self):
        return self.__classification

##Set Height----------------------------------------------------------------------
    def __setFromDictHeight(self,poke):
        Height = poke['Height'][0]
        h = Height.split()
        if(self.__num.getNational() == 720):
            self.__height = []
            self.__height.append(PokeHeight(h[3],h[0]))
            self.__height.append(PokeHeight(h[5],h[2]))
        else:            
            self.__height = PokeHeight(h[1],h[0])

    def __setFromDbHeight(self,meters,inches):
        self.__height = PokeHeight(meters,inches)


##Get Height----------------------------------------------------------------------
    def getHeight(self):
        if isinstance(self.__height,list):
            return self.__height[0]
        else:
            return self.__height

##Set Weight----------------------------------------------------------------------
    def __setFromDictWeight(self,poke):
        Weight = poke['Weight'][0]
        w = Weight.split()
        if(self.__num.getNational() == 720):
            self.__weight = []
            self.__weight.append(PokeWeight(w[3],w[0]))
            self.__weight.append(PokeWeight(w[5],w[2]))
        else:            
            self.__weight = PokeWeight(w[1],w[0])

    def __setFromDbWeight(self,kg,lbs):
        self.__weight = PokeWeight(kg,lbs)


##Get Weight----------------------------------------------------------------------
    def getWeight(self):
        if isinstance(self.__weight,list):
            return self.__weight[0]
        else:
            return self.__weight

            
##Set CaptureRate----------------------------------------------------------------------
    def __setFromDictCaptureRate(self,poke):
        self.__captureRate = PokeCR(poke['Capture Rate'])

    def __setFromDbCaptureRate(self,crORAS,crXY):
        self.__captureRate = PokeCR(cRORAS = crORAS,
                                    crXY = crXY)

##Get CaptureRate----------------------------------------------------------------------
    def getCaptureRate(self):
        return self.__captureRate

##Set BaseEggSteps----------------------------------------------------------------------
    def __setFromDictBaseEggSteps(self,poke):
        steps = poke['Base Egg Steps'][0].replace(',','').strip()
        if(steps == ''):
            steps = 0
        self.__baseEggSteps = int(steps)

    def __setFromDbBaseEggSteps(self,steps):
        self.__baseEggSteps = steps

##Get BaseEggSteps----------------------------------------------------------------------
    def getBaseEggSteps(self):
        return self.__baseEggSteps

##Set Image Path----------------------------------------------------------------------
    def __setFromDictImagePath(self,poke):
        self.__img = PokeImage(poke['Picture'],poke['Picture-Shiny'])

    def __setFromDbImagePath(self,path,sPath):
        self.__img = PokeImage(path,sPath)
        
##Get Image Path----------------------------------------------------------------------
    def getImagePath(self):
        return self.__img

##Set Abilities----------------------------------------------------------------------
    def __setFromDictAbilities(self,poke):
        self.__abilities = PokeAbilities(poke['Abilities'])

    def __setFromDbAbilities(self,abilities,hiddenAbilities):
        self.__abilities = PokeAbilities(abilitiesList = abilities,hiddenAbilitiesList = hiddenAbilities)
        
##Set ExpGrowth----------------------------------------------------------------------
    def __setFromDictExpGrowth(self,poke):
        self.__expGrowth = PokeExpGrowth(poke['Experience Growth'])

    def __setFromDbExpGrowth(self,expGrowth,classification):
        self.__expGrowth = PokeExpGrowth(expGrowth = expGrowth, expClassification = classification)

##Get ExpGrowth----------------------------------------------------------------------
    def getExpGrowth(self):
        return self.__expGrowth

##Set baseHappines----------------------------------------------------------------------
    def __setFromDictBaseHappiness(self,poke):
        self.__baseHappiness = int(poke['Base Happiness'].pop())

    def __setFromDbBaseHappiness(self,baseHappiness):
        self.__baseHappiness = baseHappiness

##Get baseHappines----------------------------------------------------------------------
    def getHappiness(self):
       return self.__baseHappiness

##Set evWorth----------------------------------------------------------------------
    def __setFromDictEvWorth(self,poke):
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

    def __setFromDbEvWorth(self,evWorth):
        self.__evWorth = PokeEVWorth(EvList = evWorth)

##Get evWorth----------------------------------------------------------------------
    def getEVWorth(self):
        if isinstance(self.__evWorth,list):
            return self.__evWorth[0]
        else:
            return self.__evWorth


##Set SkyBattle----------------------------------------------------------------------
    def __setFromDictSkyBattle(self,poke):
        self.__skyBattle = poke['Eligible for Sky Battle?'].pop().strip()

    def __setFromDbSkyBattle(self,skyBattle):
        self.__skyBattle = skyBattle

#Get SkyBattle-----------------------------------------------------------------------
    def getSkyBattle(self):
        return self.__skyBattle

##Set Weaknesses----------------------------------------------------------------------
    def __setFromDictWeaknesses(self,poke):
        self.__weaknesses = PokeWeaknesses(poke['Weaknesses'])

    def __setFromDbWeaknesses(self,normal,fire,water,electric,grass,ice,fighting,poison,ground,flying,psychic,bug,rock,ghost,dragon,dark,steel,fairy):
        self.__weaknesses = PokeWeaknesses(None,normal,fire,water,electric,grass,ice,fighting,poison,ground,flying,psychic,bug,rock,ghost,dragon,dark,steel,fairy)
       
##Get Weaknesses---------------------------------------------------------------------
    def getWeaknesses(self):
        return self.__weaknesses

##Set WildHoldItem----------------------------------------------------------------------
    def __setFromDictWildItems(self,poke):
        self.__wildItems = PokeWildItems(poke['Wild Hold Item'])

    def __setFromDbWildItems(self,items,dexnav):
        self.__wildItems = PokeWildItems(items = items, dexNavItems = dexnav)

##Set EggGroup----------------------------------------------------------------------
    def __setFromDictEggGroup(self,poke):
        self.__eggGroups = PokeEggGroup(poke['Egg Groups'])

    def __setFromDbEggGroup(self,g1,g2):
        self.__eggGroups = PokeEggGroup(group1 = EggGroup.__fromStr__(g1), group2 = EggGroup.__fromStr__(g2))

##Get EggGroup----------------------------------------------------------------------
    def getEggGroups(self):
        return  self.__eggGroups
        
##Set EvoChain----------------------------------------------------------------------
    def __setFromDictEvoChain(self,poke):
        self.__evoChain = PokeEvoChain(poke['Evo Chain'])

##Set Location----------------------------------------------------------------------
    def __setFromDictLocation(self,poke):
        self.__location = PokeLocation(poke['Location'])

    def __setFromDbLocation(self,x,y,oR,aS):
        self.__location = PokeLocation(x = x, y = y, oR = oR, aS = aS)
        
##Get Location----------------------------------------------------------------------
    def getLocation(self):
        return self.__location
        
##Set DexText----------------------------------------------------------------------
    def __setFromDictDexText(self,poke):
        self.__dexText = PokeDexText(poke['Flavour Text'])

    def __setFromDbDexText(self,x,y,oR,aS):
        self.__dexText = PokeDexText(x = x, y = y, oR = oR, aS = aS)

##Get DexText----------------------------------------------------------------------
    def getDexText(self):
        return self.__dexText

##Set Attacks----------------------------------------------------------------------
    def __setFromDictAttacks(self,poke):
        self.__attacks = PokeAttacks(poke['Attacks'])

    def __setFromDbAttacks(self,attacks):
        self.__attacks = PokeAttacks(attacks = attacks)
        
##Set Stats----------------------------------------------------------------------
    def __setFromDictStats(self,poke):
        self.__stats = PokeStats(poke['Stats'])

    def __setFromDbStats(self,hp,attack,defense,spAttack,spDefense,speed,total):
        self.__stats = PokeStats(None,hp,attack,defense,spAttack,spDefense,speed,total)
 
##Get Stats----------------------------------------------------------------------
    def getStats(self):
        return self.__stats        
