from numbers import Number
import re

from Utils.pkmconstants import *


##def split_uppercase(string):
##    return re.sub(r'([a-z])([A-Z])', r'\1 \2',string)

def split_uppercase(string):
    split = re.split(r'([a-z|0-9][A-Z])',string)
    for c in split:
        try:
            completeC = c+split[split.index(c)+1][0]
            split[split.index(c)] = completeC
            c = completeC
            split[split.index(c)+2] = split[split.index(c)+1][1]+split[split.index(c)+2]
            split.remove(split[split.index(c)+1])
        except IndexError:
            pass
    return split

def replace_uppercase(string):
    split = split_uppercase(string)
    string = ''
    for c in split:
        string+=c+', '
    return string.strip(' ,')

#Return string splited where %[A-Z] is found
def split_perc_uppercase(string):
    split = re.split(r'(%[A-Z])',string)
    for c in split:
        try:
            completeC = c+split[split.index(c)+1][0]
            split[split.index(c)] = completeC
            c = completeC
            split[split.index(c)+2] = split[split.index(c)+1][1]+split[split.index(c)+2]
            split.remove(split[split.index(c)+1])
        except IndexError:
            pass
    return split

""" Num Class for Database--------------------------------------------------
"""
def handle_unicode_problems(string):
    return string.replace('\u2019','\'').replace('\u201c','"').replace('\u201d','"')
    

class DexNum:
    def __init__(self,national= 0,central = 0,coastal = 0,mountain = 0,hoenn = 0):
        try:
            self.__national = int(national)
        except ValueError:
            self.__national = 0
        try:
            self.__central = int(central)
        except ValueError:
            self.__central = 0
        try:
            self.__coastal = int(coastal)
        except ValueError:
            self.__coastal = 0
        try:
            self.__mountain = int(mountain)
        except ValueError:
            self.__mountain = 0
        try:
            self.__hoenn = int(hoenn)
        except ValueError:
            self.__hoenn = 0
            
    def __str__(self):
        string = 'National No: ' + str(self.__national)
        string += '\nCentral No: ' + str(self.__central)
        string += '\nCoastal No: ' + str(self.__coastal)
        string += '\nMountain No: ' + str(self.__mountain)
        string += '\nHoenn No: ' + str(self.__hoenn)
        return string
        
    def __repr__(self):
        return self.__str__()

    def get_national(self):
        return self.__national

    def get_central(self):
        return self.__central

    def get_coastal(self):
        return self.__coastal

    def get_mountain(self):
        return self.__mountain

    def get_hoenn(self):
        return self.__hoenn
    
""" Gender Class for Database--------------------------------------------------
"""
class GenderException(Exception):
    pass
#gender percentage
class PokeGender:
    def __init__(self,maleRate = 0,femaleRate = 0):
        if not (isinstance(maleRate,Number) and isinstance(femaleRate,Number)):
            raise TypeError('Rate must be a \'Number\'')
        self.__male = maleRate
        self.__female = femaleRate
        self.__genderless = False
        if self.__male==self.__female==0:
            self.__genderless = True

    def __str__(self):
        if not self.__genderless:
            string = 'Male Rate :'+str(self.get_male_rate())+'%'
            string += '\nFemale Rate :'+str(self.get_female_rate())+'%'
        else:
            string = 'No gender'
        return string

    def __repr__(self):
        return self.__str__()

    def get_male_rate(self):
        return self.__male

    def get_female_rate(self):
        return self.__female

    def is_genderless(self):
        return self.__genderless

""" Stats Class for Database--------------------------------------------------
"""
class PokeStats:
    def __init__(self,stats = None ,hp = None ,
                 attack = None ,defense = None ,
                 spAttack = None ,spDefense = None ,
                 speed = None ,total = None):
        if stats:
            self.__set_hp(int(stats[1]))
            self.__set_attack(int(stats[2]))
            self.__set_defense(int(stats[3]))
            self.__set_sp_attack(int(stats[4]))
            self.__set_sp_defense(int(stats[5]))
            self.__set_speed(int(stats[6]))
            self.__set_total()
        else:
            self.__set_hp(hp)
            self.__set_attack(attack)
            self.__set_defense(defense)
            self.__set_sp_attack(spAttack)
            self.__set_sp_defense(spDefense)
            self.__set_speed(speed)
            self.__set_total(total)
            
    def __str__(self):
        string = 'HP: '+str(self.__hp)
        string+= ' Atk: '+str(self.__attack)
        string+= ' Def: '+str(self.__defense)
        string+= ' Sp.Atk: '+str(self.__spAttack)
        string+= ' Sp.Def: '+str(self.__spDefense)
        string+= ' Spd: '+str(self.__speed)
        string+= ' Total: '+str(self.__total)
        return string

    def __rpr__(self):
        return self.__str__()
        
    def __set_hp(self,hp):
        self.__hp = hp

    def get_hp(self):
        return self.__hp

    def __set_attack(self,attack):
        self.__attack = attack

    def get_attack(self):
        return self.__attack

    def __set_defense(self,defense):
        self.__defense = defense

    def get_defense(self):
        return self.__defense

    def __set_sp_attack(self,spAttack):
        self.__spAttack = spAttack

    def get_sp_attack(self):
        return self.__spAttack

    def __set_sp_defense(self,spDefense):
        self.__spDefense = spDefense

    def get_sp_defense(self):
        return self.__spDefense

    def __set_speed(self,Speed):
        self.__speed = Speed

    def get_speed(self):
        return self.__speed

    def __set_total(self,total=None):
        if total:
            self.__total = total
        else:
            self.__total = self.__hp+self.__attack+self.__defense+self.__spAttack+self.__spDefense+self.__speed

    def get_total(self):
        return self.__total

""" Image Class for Database--------------------------------------------------
"""
##Work on this class
class PokeImage:
    def __init__(self,pathImg = '',pathSImg = ''):
        if not(isinstance(pathImg,str) and isinstance(pathSImg,str)):
            raise TypeError('Path to image must be \'str\'')
        self.__pathImg = pathImg
        self.__pathSImg = pathSImg

    def __str__(self):
        return self.__pathImg + '\n' + self.__pathSImg

    def __repr__(self):
        return self.__str__()
    
    def get_path_img(self):
        return self.__pathImg

    def get_spath_img(self):
        return self.__pathSImg

""" Types Class for Database--------------------------------------------------
"""

class PokeTypes:
    def __init__(self,t1 = '',t2 = ''):
        if isinstance(t1,str):
            self.__type1 = Type.__fromStr__(t1)
        elif isinstance(t1,Type):
            self.__type1 = t1
        else:
            try:
                self.__type1 = Type(t1)
            except Exception:
                self.__type1 = Type.NoType

        if isinstance(t2,str):
            self.__type2 = Type.__fromStr__(t2)
        elif isinstance(t2,Type):
            self.__type2 = t2
        else:
            try:
                self.__type2 = Type(t2)
            except Exception:
                self.__type2 = Type.NoType

    def __str__(self):
        string = 'Type 1: '+str(self.__type1)
        string += '\nType 2: '+str(self.__type2)
        return string

    def __repr__(self):
        return self.__str__()

    def get_type1(self):
        return self.__type1

    def get_type2(self):
        return self.__type2
        
""" Height Class for Database--------------------------------------------------
"""
        
class PokeHeight:
    def __init__(self,meter='0m',inches='0\'00"'):
        if isinstance(meter,str) and isinstance(inches,str):
            self.__meters = meter
            self.__metersValue = float(meter[:-1])

            self.__inches = inches
            aux = inches.split('\'')
            self.__inchesValue = 12*int(aux[0])+int(aux[1][:-1])
        elif isinstance(meter,float) and isinstance(inches,int):
            self.__meters = str(meter)+'m'
            self.__metersValue = meter

            self.__inches = str(int(inches/12))+'\''+str(inches%12)+'"'
            self.__inchesValue = inches


    def __str__(self):
        string  = 'Meters: '+self.__meters
        string += '\nInches: '+self.__inches
        return string

    def __repr__(self):
        return self.__str__()
    
    def get_value_in_meters(self):
        return self.__metersValue

    def get_meters(self):
        return self.__meters

    def get_value_in_inches(self):
        return self.__inchesValue

    def get_inches(self):
        return self.__inches

""" Weight Class for Database--------------------------------------------------
"""
        
class PokeWeight:
    def __init__(self,kg='0kg',lbs='0lbs'):
        if isinstance(kg,str) and isinstance(lbs,str):
            self.__kg = kg
            self.__kgValue = float(kg.strip('kg'))

            self.__lbs = lbs
            self.__lbsValue = float(lbs.strip('lbs'))
        elif isinstance(kg,float) and isinstance(lbs,float):
            self.__kg = str(kg)+'kg'
            self.__kgValue = kg

            self.__lbs = str(lbs)+'lbs'
            self.__lbsValue = lbs

    def __str__(self):
        string  = 'Kg: '+self.__kg
        string += '\nLbs: '+self.__lbs
        return string

    def __repr__(self):
        return self.__str__()
    
    def get_value_in_kg(self):
        return self.__kgValue

    def get_kg(self):
        return self.__kg

    def get_value_in_lbs(self):
        return self.__lbsValue

    def get_lbs(self):
        return self.__lbs

""" Abilities Class for Database--------------------------------------------------
"""
class PokeAbility:
    def __init__(self,name,description):
        if not (isinstance(name,str) and isinstance(description,str)):
            raise TypeError('Name and Description must be strings')
        self.__name = name
        self.__description = description

    def __str__(self):
        string =  'Name: '+self.__name
        string += '\nDescription: '+self.__description
        return string

    def __repr__(self):
        return self.__str__()

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

class AbilityError(Exception):
    pass

class PokeAbilities:
    def __init__(self,abilities = None, abilitiesList = -1, hiddenAbilitiesList = -1):
        if abilities:
            self.__abilities = []
            for ability in abilities['Normal']:
                for key in ability.keys():
                    self.__abilities.append(PokeAbility(key,handle_unicode_problems(ability[key].strip('. :'))))

            self.__hiddenAbilities = []
            try:
                for ability in abilities['Hidden']:
                    for key in ability.keys():
                        self.__hiddenAbilities.append(PokeAbility(key,handle_unicode_problems(ability[key].strip('. :'))))
            except KeyError:
                pass
        elif abilitiesList != -1 and  hiddenAbilitiesList != -1:
            self.__abilities = abilitiesList
            if hiddenAbilitiesList:
                self.__hiddenAbilities = hiddenAbilitiesList
            else:
                self.__hiddenAbilities =[]

                
    def __str__(self):
        string = ''
        for ability in self.__abilities:
            string += str(ability) + '\n'
        string += 'Hidden Abilities:\n'
        for ability in self.__hiddenAbilities:
            string += str(ability) + '\n'
        return string.strip()

    def __repr(self):
        return self.__str__()
            
    def get_ability(self,i):
        return self.__abilities[i]

    def get_hidden_ability(self,i):
        return self.__hiddenAbilities[i]

    def get_abilities(self):
        return self.__abilities

    def get_hidden_abilities(self):
        return self.__hiddenAbilities

""" Exp Growth Class for Database--------------------------------------------------
"""
class PokeExpGrowth:
    def __init__(self,expG=None,expGrowth=None,expClassification=None):
        if expG:
            expG = expG.pop()
            expG = expG.split('Points')
            self.__exp = int(expG[0].replace(',',''))
            self.__classification = expG[1]
        elif expGrowth and expClassification:
            self.__exp = expGrowth
            self.__classification = expClassification
    def __str__(self):
        string =  'Exp to lvl 100: '+str(self.__exp)
        string += '\nClassification: '+str(self.__classification)
        return string
        
    def __repr__(self):
        return self.__str__()

    def get_exp_growth(self):
        return self.__exp

    def get_classification(self):
        return self.__classification

""" EV Class for Database--------------------------------------------------
"""

class EV:
    def __init__(self,value,stat):
        self.__value = value
        self.__stat = stat

    def __str__(self):
        string = str(self.__stat)+': '+str(self.__value)
        return string

    def __repr__(self):
        return self.__str__()

    def get_value(self):
        return self.__value

    def get_stat(self):
        return self.__stat
    
""" EV Worth Class for Database--------------------------------------------------
"""

        
class PokeEVWorth:
    def __init__(self,EVs = None,EvList = None):
        if EVs:
            EVs = EVs[0].split('Point(s)')
            self.__EVs = []
            for ev in EVs:
                if ev is not '':
                    n = EV(int(ev[0]), Stat.from_str(ev[1:].strip()))
                    self.__EVs.append(n)
        elif EvList:
            self.__EVs = []
            for ev in EvList:
                n = EV(ev[2], Stat.from_str(ev[1]))
                self.__EVs.append(n)
      
    def get_evs(self):
        return self.__EVs
        
    def __str__(self):
        string = ''
        for ev in self.__EVs:
            string += str(ev) + '\n'
        return string.strip()

    def __repr__(self):
        return self.__str__()

""" Weaknesses Class for Database--------------------------------------------------
"""
class PokeWeaknesses:
    def __init__(self,weak = None,normal = None ,fire = None ,
                 water = None ,electric = None ,grass = None ,
                 ice = None ,fighting = None ,poison = None ,
                 ground = None ,flying = None ,psychic = None ,
                 bug = None ,rock = None ,ghost = None ,dragon = None ,
                 dark = None ,steel = None,fairy = None):
        self.__weaknesses = {}
        if weak:
            for key in weak.keys():
                self.__weaknesses[key] = float(weak[key].strip(' *'))
        else:
            self.__weaknesses['Normal'] = normal
            self.__weaknesses['Fire'] = fire
            self.__weaknesses['Water'] = water
            self.__weaknesses['Electric'] = electric
            self.__weaknesses['Grass'] = grass
            self.__weaknesses['Ice'] = ice
            self.__weaknesses['Fighting'] = fighting
            self.__weaknesses['Poison'] = poison
            self.__weaknesses['Ground'] = ground
            self.__weaknesses['Flying'] = flying
            self.__weaknesses['Psychic'] = psychic
            self.__weaknesses['Bug'] = bug
            self.__weaknesses['Rock'] = rock
            self.__weaknesses['Ghost'] = ghost
            self.__weaknesses['Dragon'] = dragon
            self.__weaknesses['Dark'] = dark
            self.__weaknesses['Steel'] = steel
            self.__weaknesses['Fairy'] = fairy
    def __str__(self):
        string = ''
        for key in self.__weaknesses.keys():
            string += str(key) + ': '+str(self.__weaknesses[key])+'\n'
        return string[:-1]

    def __repr__(self):
        return self.__str__()

    def __getitem__(self,key):
        if isinstance(key,str):
            key = Type.__fromStr__(key)
        return self.__weaknesses[str(key)]

    def get_weaknesses(self):
        return self.__weaknesses

""" Wild Items Class for Database--------------------------------------------------
"""
class PokeWildItems():
    def __init__(self,wI = None, items = -1, dexNavItems = -1):
        if wI:
            aux = wI.strip().split('DexNav')
            self.__normal = split_perc_uppercase(aux[0])
            try:
                extras = []
                extras.clear()
                if aux[1].find('BrightPowder')>=0:
                    aux[1] = aux[1].replace('BrightPowder','')
                    extras.append('BrightPowder')
                self.__dexNav = split_uppercase(aux[1])+extras
            except IndexError:
                self.__dexNav = None
        elif items != -1 and dexNavItems != -1:
            self.__normal = items
            self.__dexNav = dexNavItems
    def __str__(self):
        string = '\nNormal :'+str(self.__normal)+'\nDexNav :'+str(self.__dexNav)
        return string

    def __repr__(self):
        return self.__str__()
        
    def get_normal_items(self):
        return self.__normal
         
    def get_dex_nav_items(self):
        try:
            return self.__dexNav
        except AttributeError:
            return None
##        print(wI,'\nNormal :',self.__normal,'\nDexNav :',self.__dexNav)

""" Capture Rate Class for Database--------------------------------------------------
"""
class PokeCR:
    def __init__(self,captureRate=None,cRORAS=None,crXY=None):
        if captureRate:
            try:
                self.__cRORAS = int(captureRate[0])
                self.__crXY = int(captureRate[0])
            except ValueError:
                split = re.split(r'[^0-9]',captureRate[0])
                num = []
                for element in split:
                    if element != '':
                        num.append(element)
                self.__cRORAS = int(num[1])
                self.__crXY = int(num[0])
        elif cRORAS and crXY:
            self.__cRORAS =cRORAS
            self.__crXY = crXY

    def __str__(self):
        string =  'CR XY: '+str(self.__crXY)+'\n'
        string += 'CR ORAS: ' + str(self.__cRORAS)
        return string
    def __repr__(self):
        return self.__str__()

    def get_xy(self):
        return self.__crXY

    def get_oras(self):
        return self.__cRORAS

""" Egg Group Class for Database--------------------------------------------------
"""

class PokeEggGroup:
    def __init__(self,eggGroup = None, group1 = None, group2 = None):
        if eggGroup:
            if isinstance(eggGroup,list):
                if len(eggGroup)>1:
                    self.__group1 = EggGroup.__fromStr__(eggGroup[0])
                    self.__group2 = EggGroup.__fromStr__(eggGroup[1])
                else:
                    self.__group1 = EggGroup.__fromStr__(eggGroup[0])
                    self.__group2 = EggGroup.NoType
            else:
                self.__group1 = EggGroup.__fromStr__(eggGroup)
                self.__group2 = EggGroup.NoType
        elif group1 and group2:
            self.__group1 = group1
            self.__group2 = group2

    def __str__(self):
        string =  'Group 1: '+ str(self.__group1)
        string += '\nGroup 2: '+ str(self.__group2)
        return string

    def __repr__(self):
        return self.__str__()

    def get_group1(self):
        return self.__group1

    def get_group2(self):
        return self.__group2


""" Poke Evo Class for Database--------------------------------------------------
""" 
class PokeEvoChain:
    def __init__(self,evoChain = None,dbChain = None):
        if evoChain:
            #print(evoChain)
            evoTable = self.__evochain_to_table(evoChain)
            evoList = []
            for row in evoTable.keys():
                for col in evoTable[row].keys():
                    if not isinstance(evoTable[row][col],str):
                        isPkm = evoTable[row][col][5]
                        if isPkm:
                            pkm = evoTable[row][col][0]
                            pkmRow = evoTable[row][col][1]
                            pkmRowspan = int(evoTable[row][col][2])
                            pkmCol = evoTable[row][col][3]
                            pkmColspan = int(evoTable[row][col][4])
                            if pkmColspan==0:
                                if pkmRowspan==0:
                                    if col+2 in evoTable[row]:
                                        method = evoTable[row][col+1][0]
                                        isMethodPokemon = evoTable[row][col+1][5]
                                        if not isMethodPokemon:
                                            evoPkm = evoTable[row][col+2][0]
                                            node = (pkm,method,evoPkm)
                                            evoList.append(node)
                                else:
                                    spanQuota = 0
                                    rowMethod = row
                                    if col+2 in evoTable[row]:
                                        while spanQuota<pkmRowspan:
                                            method = evoTable[rowMethod][col+1][0]
                                            methodSpan = int(evoTable[rowMethod][col+1][2])
                                            isMethodPokemon = evoTable[rowMethod][col+1][5]
                                            evoPkm = evoTable[rowMethod][col+2]
                                            i=0
                                            while isinstance(evoPkm,str):
                                                evoPkm = evoTable[row-i][col+2]
                                                i+=1
                                            if not isMethodPokemon:
                                                evoPkm = evoPkm[0]
                                                node = (pkm,method,evoPkm)
                                                evoList.append(node)
                                                if methodSpan == 0:
                                                    methodSpan = 1
                                                rowMethod+=methodSpan
                                                spanQuota+=methodSpan
                            else:
                                spanQuota = 0
                                colMethod = col
                                if col+2 in evoTable[row]:
                                    while spanQuota<pkmColspan:
                                        method = evoTable[row+1][colMethod][0]
                                        methodSpan = int(evoTable[row+1][colMethod][4])
                                        isMethodPokemon = evoTable[row+1][colMethod][5]
                                        evoPkm = evoTable[row+2][colMethod]
                                        if not isMethodPokemon:
                                            evoPkm = evoPkm[0]
                                            node = (pkm,method,evoPkm)
                                            evoList.append(node)
                                            if methodSpan == 0:
                                                methodSpan = 1
                                            colMethod+=methodSpan
                                            spanQuota+=methodSpan
                            #print(evoTable[row][col])
            #print(evoList)
            
            
           
            self.__evoChain = evoList
            
        else:
            self.__evoChain = list(dbChain)

    def __evochain_to_table(self,evoChain):
        table = {}
        table[0] = {}
        rowNum = 0
        colNum = 0
        for element,i in zip(evoChain,range(0,len(evoChain))):
            #print(element)
            eRow = element[1]
            eRowspan = int(element[2])
            eCol = element[3]
            eColspan = int(element[4])
            while colNum in table[rowNum]:
                #print(colNum)
                colNum+=1
            #print(rowNum,colNum)
            #print(colNum in table[rowNum])
            table[rowNum][colNum] = element
            
            for j in range(1,eRowspan):
                #print('rowspan',rowNum+j,colNum)
                if not rowNum+j in table:
                    table[rowNum+j] = {}
                table[rowNum+j][colNum] = 'rowspan'
            colNum+=1
            
            for j in range(1,eColspan):
                table[rowNum][colNum] = 'colspan'
                colNum+=1
            
            try:
                nextElement = evoChain[i+1]
                nextElementRow = nextElement[1]
            except IndexError:
                nextElementRow = rowNum
            #print(table)
            if nextElementRow!=rowNum:
                colNum=0
                rowNum+=1
                if not rowNum in table:
                    table[rowNum] = {}
        return table

    def __getByRowAndCol(self,elements,row,col):
        for element in elements:
            if element[3]==row and element[1]==col:
                return element
        return None
            

    def __str__(self):
        string = ''
        for node in self.__evoChain:
            string += str(node[0])+'\n'
        return string.strip()
        
    def get_evo_chain(self):
        return self.__evoChain
""" Poke Location for Database--------------------------------------------------
"""
class PokeLocation:
    def __init__(self,location = None,x = None,y = None, oR = None, aS = None):
        if location:
            for key in location.keys():
                if key == 'X':
                    self.__x = location[key].split('\n')[2].strip()
            
                elif key == 'Y':
                    self.__y = location[key].split('\n')[2].strip()

                elif key == 'Ruby':
                    self.__oR = location[key].split('\n')[2].strip()

                elif key == 'Sapphire':
                    self.__aS = location[key].split('\n')[2].strip()
        elif x and y and oR and aS:
            self.__x = x
            self.__y = y
            self.__oR = oR
            self.__aS = aS
            

    def __str__(self):
        string =  'X: '+ self.__x
        string += '\nY: '+ self.__y
        string += '\nOR: '+ self.__oR
        string += '\nAS: '+ self.__aS
        return string

    def __repr__(self):
        return self.__str__()

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_or(self):
        return self.__oR

    def get_as(self):
        return self.__aS


""" Poke Flavour Text for Database--------------------------------------------------
"""

class PokeDexText:
    def __init__(self,dexText = None,x = None,y = None, oR = None, aS = None):
        if dexText:
            for key in dexText.keys():
                if key == 'X':
                    self.__x = dexText[key].split('\n')[2].strip()
            
                elif key == 'Y':
                    self.__y = dexText[key].split('\n')[2].strip()

                elif key == 'Ruby':
                    self.__oR = dexText[key].split('\n')[2].strip()

                elif key == 'Sapphire':
                    self.__aS = dexText[key].split('\n')[2].strip()

        elif x and y and (oR or aS):
            self.__x = x
            self.__y = y
            self.__oR = oR
            self.__aS = aS


    def __str__(self):
        string =  'X: '+ self.__x
        string += '\nY: '+ self.__y
        string += '\nOR: '+ self.__oR
        string += '\nAS: '+ self.__aS
        return string

    def __repr__(self):
        return self.__str__()

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_or(self):
        return self.__oR

    def get_as(self):
        return self.__aS


""" Poke Attacks for Database--------------------------------------------------
"""

class Attack:
    def __init__(self,condition=0,name='',
                 atkType = Type.NoType,cat = AttackCat.Other,
                 att = 0,acc = 0,pp=0,effect = '',description = '' ):
        self.__condition = condition
        self.__name = name
        self.__atkType = atkType
        self.__cat = cat
        ## Value 357 means --
        ## Value 951 means ??
        if att == '--':
            self.__att = 357
        elif att == '??':
            self.__att = 951
        else:
            self.__att = int(att)
        ## Value 357 means --
        if acc == '--':
            self.__acc = 357
        else:
            self.__acc = int(acc)
        self.__pp = int(pp)
        self.__effect = effect
        self.__description = description

    def __str__(self):
        string =  '\nName: '+self.__name
        string += '\nCondition: '+self.__condition
        string += '\nType: '+self.__atkType
        string += '\nCategory: '+self.__cat
        string += '\nAttribute: '+str(self.__att)
        string += '\nAccuracy: '+str(self.__acc)
        string += '\nPP: '+str(self.__pp)
        string += '\nEffect: '+self.__effect
        string += '\nDescription: '+self.__description
        return string

    def __repr__(self):
        return self.__str__()

    def set_condition(self, value):
        self.__condition = value

    def get_condition(self):
        return self.__condition

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__atkType

    def get_cat(self):
        return self.__cat

    def get_att(self):
        return self.__att

    def get_acc(self):
        return self.__acc

    def get_PP(self):
        return self.__pp

    def get_effect(self):
        return self.__effect
    def get_description(self):
       return self.__description
    
class PokeAttacks:
    def __init__(self, attackGroups=None, attacks=None):
        if attackGroups:
            self.__attackGroups = {}
            for attackGroup in attackGroups.keys():
                self.__attackGroups[attackGroup] = []
                for attack in attackGroups[attackGroup]:
                    caract = []
                    for element in attack:
                        caract.append(element)
                    if len(caract)==8:
                        self.__attackGroups[attackGroup].\
                            append(Attack(name = caract[0],
                               atkType = Type.__fromStr__(caract[1]),
                               cat = AttackCat.__fromStr__(caract[2]),
                               att = caract[3],
                               acc = caract[4],
                               pp = caract[5],
                               effect = caract[6],
                               description = caract[7]))
                    elif len(caract) == 9:
                        self.__attackGroups[attackGroup].\
                            append(Attack(condition = caract[0],
                               name = caract[1],
                               atkType = Type.__fromStr__(caract[2]),
                               cat = AttackCat.__fromStr__(caract[3]),
                               att = caract[4],
                               acc = caract[5],
                               pp = caract[6],
                               effect = caract[7],
                               description = caract[8]))
                    else:
                        pass
        elif attacks:
            self.__attackGroups = attacks

    def __str__(self):
        string = ''
        for key in self.get_attack_groups():
            string += key+':\n'
            for attack in self.get_attack_group(key):
                string += str(attack)+'\n'
        return string

    # Retrieve attacks by name
    def __getitem__(self, item):
        for key in self.get_attack_groups():
            for attack in self.get_attack_group(key):
                if item == attack.get_name():
                    return attack
        return None

    def get_attack_groups(self):
        return self.__attackGroups.keys()

    def get_attack_group(self,key):
        return self.__attackGroups[key]
