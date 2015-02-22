from pkmutils import *
from database import *
import os

""" Pokemon Class for Database--------------------------------------------------
"""
class Pokemon:
    def __init__(self,poke=None):
        if isinstance(poke,dict):
            ##Get Name
            self.__set_from_dict_name(poke)

            ##Get Dex numbers
            self.__set_from_dict_num(poke)

            ##Get Gender
            self.__set_from_dict_gender(poke)

            ##Get Pokemon Type
            self.__set_from_dict_types(poke)

            ##Get Pokemon Classification
            self.__set_from_dict_classification(poke)

            ##Get Pokemon Height
            self.__set_from_dict_height(poke)

            ##Get Pokemon Weight
            self.__set_from_dict_weight(poke)

            ##Get Capture Rate
            self.__set_from_dict_capture_rate(poke)
            
            ##Get Base Egg Step Count
            self.__set_from_dict_base_egg_steps(poke)

            ##Get Image Path
            self.__set_from_dict_image_path(poke)
            
            ##Get Abilities
            self.__set_from_dict_abilities(poke)

            ##Get Experience Growth
            self.__set_from_dict_exp_growth(poke)

            ##Get Base Happiness
            self.__set_from_dict_base_happiness(poke)

            ##Get EV Worth
            self.__set_from_dict_ev_worth(poke)

            ##Get SkyBattle
            self.__set_from_dict_sky_battle(poke)

            ##Get Weaknesses
            self.__set_from_dict_weaknesses(poke)

            ##Get Wild Items
            self.__set_from_dict_wildItems(poke)

            ##Get EggGroup
            self.__set_from_dict_egg_group(poke)

            ##Get EvoChain
            self.__set_from_dict_evo_chain(poke)

            ##Get Location
            self.__set_from_dict_location(poke)

            ##Get DexText
            self.__set_from_dict_dex_text(poke)

            ##Get Attacks
            self.__set_from_dict_attacks(poke)

            ##Get Stats
            self.__set_from_dict_stats(poke)

        if isinstance(poke,str):
            name = poke
            db = DatabaseManager()
            data = db.get_pokemon_by_name(name)

            pokeData = data[0]
            pokeAbilities = data[1]
            pokeHiddenAbilities = data[2]
            pokeAttacks = data[3]
            pokeItems = data[4]
            pokeDexNavItems = data[5]
            pokeEvWorth = data[6]
            pokeEvoChain = data[7]

            ##Get Name
            self.__set_from_db_name(pokeData[0])

            ##Get Dex numbers
            self.__set_from_db_num(pokeData[1], pokeData[2], pokeData[3], pokeData[4], pokeData[5])

            ##Get Gender
            self.__set_from_db_gender(pokeData[6], pokeData[7])

            ##Get Pokemon Type
            self.__set_from_db_types(pokeData[9], pokeData[10])

            ##Get Pokemon Classification
            self.__set_from_db_classification(pokeData[11])

            ##Get Pokemon Height
            self.__set_from_db_height(pokeData[12], pokeData[13])

            ##Get Pokemon Weight
            self.__set_from_db_weight(pokeData[14], pokeData[15])

            ##Get Capture Rate
            self.__set_from_db_capture_rate(pokeData[16], pokeData[17])
            
            ##Get Base Egg Step Count
            self.__set_from_db_base_egg_steps(pokeData[18])

            ##Get Image Path
            self.__set_from_db_image_path(pokeData[19], pokeData[20])
            
            ##Get Abilities
            self.__set_from_db_abilities(pokeAbilities, pokeHiddenAbilities)

            ##Get Experience Growth
            self.__set_from_db_exp_growth(pokeData[21], pokeData[22])

            ##Get Base Happiness
            self.__set_from_db_base_happiness(pokeData[23])

            ##Get EV Worth
            self.__set_from_db_ev_worth(pokeEvWorth)

            ##Get SkyBattle
            self.__set_from_db_sky_battle(pokeData[24])

            ##Get Weaknesses
            self.__set_from_db_weaknesses(pokeData[25], pokeData[26], pokeData[27], pokeData[28], pokeData[29],
                                          pokeData[30], pokeData[31], pokeData[32], pokeData[33], pokeData[34],
                                          pokeData[35], pokeData[36], pokeData[37], pokeData[38], pokeData[39],
                                          pokeData[40], pokeData[41], pokeData[42])

            ##Get Wild Items
            self.__set_from_db_wild_items(pokeItems, pokeDexNavItems)

            ##Get EggGroup
            self.__set_from_db_egg_group(pokeData[43], pokeData[44])

            ##Get EvoChain
            self.__set_from_db_evo_chain(pokeEvoChain)

            ##Get Location
            self.__set_from_db_location(pokeData[45], pokeData[46], pokeData[47], pokeData[48])

            ##Get DexText
            self.__set_from_db_dex_text(pokeData[49], pokeData[50], pokeData[51], pokeData[52])

            ##Get Attacks
            self.__set_from_db_attacks(pokeAttacks)

            ##Get Stats
            self.__set_from_db_stats(pokeData[53], pokeData[54], pokeData[55], pokeData[56], pokeData[57], pokeData[58],
                                     pokeData[59])


    def __str__(self):
        string =  str(self.__name)
        return string

    def __repr__(self):
        return self.__str__()
            
    ##Save Pokemon
    def create_ability_database(self):
        manager = AbilitiesManager()
        manager.create_table_abilities()
        for ability in self.__abilities.get_abilities() + self.__abilities.get_hidden_abilities():
            try:
                manager.insert_ability(ability=ability)
            except sqlite3.IntegrityError:
                pass

    def create_pokemon_ability_database(self):
        manager = PokemonAbilitiesManager()
        managerHidden = PokemonHiddenAbilitiesManager()
        for ability in self.__abilities.get_abilities():
            try:
                manager.insert_ability(self.__name, ability=ability)
            except sqlite3.IntegrityError:
                pass
        for ability in self.__abilities.get_hidden_abilities():
            try:
                managerHidden.insert_ability(self.__name, ability=ability)
            except sqlite3.IntegrityError:
                pass

    def create_attacks_database(self):
        manager = AttacksManager()
        manager.create_table_attacks()
        for key in self.__attacks.get_attack_groups():
            for attack in self.__attacks.get_attack_group(key):
                try:
                    manager.insert_attack(attack=attack)
                except sqlite3.IntegrityError:
                    pass
                    
    def create_pokemon_attacks_database(self):
        managerPkAtts = PokeAttacksManager()
        for key in self.__attacks.get_attack_groups():
            for attack in self.__attacks.get_attack_group(key):
                try:
                    managerPkAtts.insert_poke_attacks(self.__name, attack.get_name(), key, str(attack.get_condition()))
                except sqlite3.IntegrityError:
                    pass

    def create_pokemon_items_database(self):
        managerPkItems = PokeItemsManager()
        for item in self.__wildItems.get_normal_items():
            if(item != 'None' and item != ''):
                parts = item.split(' - ')
                itemName = parts[0].strip()
                itemChance = int(parts[1].strip(' %(SuperSize)'))
                try:
                    managerPkItems.insert_poke_item(self.__name, itemName, itemChance)
                except sqlite3.IntegrityError:
                    pass
#esses nomes tão uma bosta D:
    def create_pokemon_dex_nav_items_database(self):
        managerPkItems = PokeDexNavItemsManager()
        dexNavItems = self.__wildItems.get_dex_nav_items()
        if dexNavItems:
            for item in self.__wildItems.get_dex_nav_items():
                item = item.strip(' %')
                if(item != 'None' and item != ''):
                    try:
                        managerPkItems.insertPokeDexNavItem(self.__name, item)
                    except sqlite3.IntegrityError:
                        pass

    def create_pokemon_ev_worth_database(self):
        manager = PokemonEVWorthManager()
        for ev in self.get_ev_worth().get_evs():
            print(ev)
            try:
                manager.insert_poke_ev_worth(self.__name, ev)
            except sqlite3.IntegrityError:
                pass

    def create_pokemon_evo_chain_database(self):
        manager = PokemonEvoChainManager()
        for evoChain in self.__evoChain.get_evo_chain():
            print(evoChain)
            try:
                manager.insert_evo_node(self.__name, evoChain)
            except sqlite3.IntegrityError:
                pass

    def create_pokemon_database(self):
        manager = PokemonManager()
        manager.insert_pokemon(self)

        
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
    def  __set_from_dict_name(self,poke):
        self.__name = poke['Name']
        #try:
        #    print(self.__name)
        #except UnicodeEncodeError:
        #    print(self.__name.encode('utf-8','ignore'))

    def  __set_from_db_name(self,name):
        self.__name = name
        #try:
        #    print(self.__name)
        #except UnicodeEncodeError:
        #    print(self.__name.encode('utf-8','ignore'))


##Get Name----------------------------------------------------------------------
    def get_name(self):
        return self.__name

##Set Num----------------------------------------------------------------------
    def __set_from_dict_num(self,poke):
        self.__num = DexNum(poke['No']['National'][1:],
                            poke['No']['Central'][1:],
                            poke['No']['Coastal'][1:],
                            poke['No']['Mountain'][1:],
                            poke['No']['Hoenn'][1:])

    def __set_from_db_num(self,national,central,coastal,mountain,hoenn):
        self.__num = DexNum(national,
                            central,
                            coastal,
                            mountain,
                            hoenn)


##Get Num----------------------------------------------------------------------
    def get_dex_num(self):
        return self.__num

##Set Gender----------------------------------------------------------------------
    def __set_from_dict_gender(self,poke):
        try:
            male = poke['Gender']['Male']
            female = poke['Gender']['Female']
            self.__gender = PokeGender(float(male[:-1])
                                       ,float(female[:-1]))
        except (KeyError,TypeError):
            self.__gender = PokeGender()

    def __set_from_db_gender(self,mRate,fRate):
            self.__gender = PokeGender(mRate,fRate)


##Get Gender----------------------------------------------------------------------
    def get_gender(self):
        return self.__gender

##Set Types----------------------------------------------------------------------
    def __set_from_dict_types(self,poke):
        try:
            type1 = poke['Types'][0]
            type2 = poke['Types'][1]

            self.__types = PokeTypes(type1,type2)
        except IndexError:
            self.__types = PokeTypes(type1)

    def __set_from_db_types(self,type1,type2):
        self.__types = PokeTypes(type1,type2)
    

##Get Types----------------------------------------------------------------------
    def get_types(self):
        return self.__types

##Set Classification----------------------------------------------------------------------
    def __set_from_dict_classification(self,poke):
        self.__classification = poke['Classification'].pop()

    def __set_from_db_classification(self,data):
        self.__classification = data

##Get Classification----------------------------------------------------------------------
    def get_classification(self):
        return self.__classification

##Set Height----------------------------------------------------------------------
    def __set_from_dict_height(self,poke):
        Height = poke['Height'][0]
        h = Height.split()
        if(self.__num.get_national() == 720):
            self.__height = []
            self.__height.append(PokeHeight(h[3],h[0]))
            self.__height.append(PokeHeight(h[5],h[2]))
        else:            
            self.__height = PokeHeight(h[1],h[0])

    def __set_from_db_height(self,meters,inches):
        self.__height = PokeHeight(meters,inches)


##Get Height----------------------------------------------------------------------
    def get_height(self):
        if isinstance(self.__height,list):
            return self.__height[0]
        else:
            return self.__height

##Set Weight----------------------------------------------------------------------
    def __set_from_dict_weight(self,poke):
        Weight = poke['Weight'][0]
        w = Weight.split()
        if(self.__num.get_national() == 720):
            self.__weight = []
            self.__weight.append(PokeWeight(w[3],w[0]))
            self.__weight.append(PokeWeight(w[5],w[2]))
        else:            
            self.__weight = PokeWeight(w[1],w[0])

    def __set_from_db_weight(self,kg,lbs):
        self.__weight = PokeWeight(kg,lbs)


##Get Weight----------------------------------------------------------------------
    def get_weight(self):
        if isinstance(self.__weight,list):
            return self.__weight[0]
        else:
            return self.__weight

            
##Set CaptureRate----------------------------------------------------------------------
    def __set_from_dict_capture_rate(self,poke):
        self.__captureRate = PokeCR(poke['Capture Rate'])

    def __set_from_db_capture_rate(self,crORAS,crXY):
        self.__captureRate = PokeCR(cRORAS = crORAS,
                                    crXY = crXY)

##Get CaptureRate----------------------------------------------------------------------
    def get_capture_rate(self):
        return self.__captureRate

##Set BaseEggSteps----------------------------------------------------------------------
    def __set_from_dict_base_egg_steps(self,poke):
        steps = poke['Base Egg Steps'][0].replace(',','').strip()
        if(steps == ''):
            steps = 0
        self.__baseEggSteps = int(steps)

    def __set_from_db_base_egg_steps(self,steps):
        self.__baseEggSteps = steps

##Get BaseEggSteps----------------------------------------------------------------------
    def get_base_egg_steps(self):
        return self.__baseEggSteps

##Set Image Path----------------------------------------------------------------------
    def __set_from_dict_image_path(self,poke):
        self.__img = PokeImage(poke['Picture'],poke['Picture-Shiny'])

    def __set_from_db_image_path(self,path,sPath):
        self.__img = PokeImage(path,sPath)
        
##Get Image Path----------------------------------------------------------------------
    def get_image_path(self):
        return self.__img

##Set Abilities----------------------------------------------------------------------
    def __set_from_dict_abilities(self,poke):
        self.__abilities = PokeAbilities(poke['Abilities'])

    def __set_from_db_abilities(self,abilities,hiddenAbilities):
        self.__abilities = PokeAbilities(abilitiesList = abilities,hiddenAbilitiesList = hiddenAbilities)
        
##Get Abilities
    def get_abilities(self):
        return self.__abilities
        
##Set ExpGrowth----------------------------------------------------------------------
    def __set_from_dict_exp_growth(self,poke):
        self.__expGrowth = PokeExpGrowth(poke['Experience Growth'])

    def __set_from_db_exp_growth(self,expGrowth,classification):
        self.__expGrowth = PokeExpGrowth(expGrowth = expGrowth, expClassification = classification)

##Get ExpGrowth----------------------------------------------------------------------
    def get_exp_growth(self):
        return self.__expGrowth

##Set baseHappines----------------------------------------------------------------------
    def __set_from_dict_base_happiness(self,poke):
        self.__baseHappiness = int(poke['Base Happiness'].pop())

    def __set_from_db_base_happiness(self,baseHappiness):
        self.__baseHappiness = baseHappiness

##Get baseHappines----------------------------------------------------------------------
    def get_happiness(self):
       return self.__baseHappiness

##Set evWorth----------------------------------------------------------------------
    def __set_from_dict_ev_worth(self,poke):
        if(self.__num.get_national() == 386):
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

        elif(self.__num.get_national() == 413):
            ev = poke['Effort Values Earned'][0].split('Plant Cloak')
            ev = ev[1].split('Sandy Cloak')
            evPlant = ev[0]
            ev = ev[1].split('Trash Cloak')
            evSandy = ev[0]
            evTrash = ev[1]
            self.__evWorth = [PokeEVWorth([evPlant]),
                              PokeEVWorth([evSandy]),
                              PokeEVWorth([evTrash])]
        elif(self.__num.get_national() == 492):
            ev = poke['Effort Values Earned'][0].split('Land Forme')
            ev = ev[1].split('Sky Forme')
            evLand = ev[0]
            evSky = ev[1]
            self.__evWorth = [PokeEVWorth([evLand]),
                              PokeEVWorth([evSky])]
        elif(self.__num.get_national() == 555):
            ev = poke['Effort Values Earned'][0].split('Standard')
            ev = ev[1].split('Zen Mode')
            evStandard = ev[0]
            evZen = ev[1]
            self.__evWorth = [PokeEVWorth([evStandard]),
                              PokeEVWorth([evZen])]
        elif(self.__num.get_national() == 641 or self.__num.get_national() == 642 or self.__num.get_national() == 645):
            ev = poke['Effort Values Earned'][0].split('Incarnate Forme')
            ev = ev[1].split('Therian Forme')
            evIncarnate = ev[0]
            evTherian = ev[1]
            self.__evWorth = [PokeEVWorth([evIncarnate]),
                              PokeEVWorth([evTherian])]
        elif(self.__num.get_national() == 646):
            ev = poke['Effort Values Earned'][0].split('Kyurem',1)
            ev = ev[1].split('Black Kyurem')
            evKyurem = ev[0]
            ev = ev[1].split('White Kyurem')
            evBKyurem = ev[0]
            evWKyurem = ev[1]
            self.__evWorth = [PokeEVWorth([evKyurem]),
                              PokeEVWorth([evBKyurem]),
                              PokeEVWorth([evWKyurem])]
        elif(self.__num.get_national() == 648):
            ev = poke['Effort Values Earned'][0].split('Aria Forme')
            ev = ev[1].split('Pirouette Forme')
            evAria = ev[0]
            evPirouette = ev[1]
            self.__evWorth = [PokeEVWorth([evAria]),
                              PokeEVWorth([evPirouette])]
        else:
            self.__evWorth = PokeEVWorth(poke['Effort Values Earned'])

    def __set_from_db_ev_worth(self,evWorth):
        self.__evWorth = PokeEVWorth(EvList = evWorth)

##Get evWorth----------------------------------------------------------------------
    def get_ev_worth(self):
        if isinstance(self.__evWorth,list):
            return self.__evWorth[0]
        else:
            return self.__evWorth


##Set SkyBattle----------------------------------------------------------------------
    def __set_from_dict_sky_battle(self,poke):
        self.__skyBattle = poke['Eligible for Sky Battle?'].pop().strip()

    def __set_from_db_sky_battle(self,skyBattle):
        self.__skyBattle = skyBattle

#Get SkyBattle-----------------------------------------------------------------------
    def get_sky_battle(self):
        return self.__skyBattle

##Set Weaknesses----------------------------------------------------------------------
    def __set_from_dict_weaknesses(self,poke):
        self.__weaknesses = PokeWeaknesses(poke['Weaknesses'])

    def __set_from_db_weaknesses(self,normal,fire,water,electric,grass,ice,fighting,poison,ground,flying,psychic,bug,rock,ghost,dragon,dark,steel,fairy):
        self.__weaknesses = PokeWeaknesses(None,normal,fire,water,electric,grass,ice,fighting,poison,ground,flying,psychic,bug,rock,ghost,dragon,dark,steel,fairy)
       
##Get Weaknesses---------------------------------------------------------------------
    def get_weaknesses(self):
        return self.__weaknesses

##Set WildHoldItem----------------------------------------------------------------------
    def __set_from_dict_wildItems(self,poke):
        self.__wildItems = PokeWildItems(poke['Wild Hold Item'])

    def __set_from_db_wild_items(self,items,dexnav):
        self.__wildItems = PokeWildItems(items = items, dexNavItems = dexnav)

##Get WildHoldItems
    def get_wild_items(self):
        return self.__wildItems
    
##Set EggGroup----------------------------------------------------------------------
    def __set_from_dict_egg_group(self,poke):
        self.__eggGroups = PokeEggGroup(poke['Egg Groups'])

    def __set_from_db_egg_group(self,g1,g2):
        self.__eggGroups = PokeEggGroup(group1 = EggGroup.__fromStr__(g1), group2 = EggGroup.__fromStr__(g2))

##Get EggGroup----------------------------------------------------------------------
    def get_egg_groups(self):
        return  self.__eggGroups
        
##Set EvoChain----------------------------------------------------------------------
    def __set_from_dict_evo_chain(self,poke):
        self.__evoChain = PokeEvoChain(poke['Evo Chain'])

    def __set_from_db_evo_chain(self,evoChain):
        self.__evoChain = PokeEvoChain(dbChain = evoChain)

##Get EvoChain----------------------------------------------------------------------
    def get_evo_chain(self):
        return self.__evoChain

##Set Location----------------------------------------------------------------------
    def __set_from_dict_location(self,poke):
        self.__location = PokeLocation(poke['Location'])

    def __set_from_db_location(self,x,y,oR,aS):
        self.__location = PokeLocation(x = x, y = y, oR = oR, aS = aS)
        
##Get Location----------------------------------------------------------------------
    def get_location(self):
        return self.__location
        
##Set DexText----------------------------------------------------------------------
    def __set_from_dict_dex_text(self,poke):
        self.__dexText = PokeDexText(poke['Flavour Text'])

    def __set_from_db_dex_text(self,x,y,oR,aS):
        self.__dexText = PokeDexText(x = x, y = y, oR = oR, aS = aS)

##Get DexText----------------------------------------------------------------------
    def get_dex_text(self):
        return self.__dexText

##Set Attacks----------------------------------------------------------------------
    def __set_from_dict_attacks(self,poke):
        self.__attacks = PokeAttacks(poke['Attacks'])

    def __set_from_db_attacks(self,attacks):
        self.__attacks = PokeAttacks(attacks = attacks)
        
##Get Attacks
    def get_attacks(self):
        return self.__attacks
        
##Set Stats----------------------------------------------------------------------
    def __set_from_dict_stats(self,poke):
        self.__stats = PokeStats(poke['Stats'])

    def __set_from_db_stats(self,hp,attack,defense,spAttack,spDefense,speed,total):
        self.__stats = PokeStats(None,hp,attack,defense,spAttack,spDefense,speed,total)
 
##Get Stats----------------------------------------------------------------------
    def get_stats(self):
        return self.__stats
    

if __name__ == '__main__':
    Pokemon('Bulbasaur')
