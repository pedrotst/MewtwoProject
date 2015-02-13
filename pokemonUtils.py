from pokemonConstants import *
from numbers import Number
import re

##def split_uppercase(string):
##    return re.sub(r'([a-z])([A-Z])', r'\1 \2',string)

def split_uppercase(string):
    split = re.split(r'([a-z][A-Z])',string)
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

def split_percUppercase(string):
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
def handleUnicodeProblens(string):
    return string.replace('\u2019','\'').replace('\u201c','"').replace('\u201d','"')
    

class DexNum:
    def __init__(self,National = 0,Central = 0,Coastal = 0,Mountain = 0,Hoenn = 0):
        try:
            self.__National = int(National)
        except ValueError:
            self.__National = 0
        try:
            self.__Central = int(Central)
        except ValueError:
            self.__Central = 0
        try:
            self.__Coastal = int(Coastal)
        except ValueError:
            self.__Coastal = 0
        try:
            self.__Mountain = int(Mountain)
        except ValueError:
            self.__Mountain = 0
        try:
            self.__Hoenn = int(Hoenn)
        except ValueError:
            self.__Hoenn = 0
            
    def __str__(self):
        string = 'National No: ' + str(self.__National)
        string += '\nCentral No: ' + str(self.__Central)
        string += '\nCoastal No: ' + str(self.__Coastal)
        string += '\nMountain No: ' + str(self.__Mountain)
        string += '\nHoenn No: ' + str(self.__Hoenn)
        return string
        
    def __repr__(self):
        return self.__str__()

    def getNational(self):
        return self.__National

    def getCentral(self):
        return self.__Central

    def getCoastal(self):
        return self.__Coastal

    def getMountain(self):
        return self.__Mountain

    def getHoenn(self):
        return self.__Hoenn
    
""" Gender Class for Database--------------------------------------------------
"""
class GenderException(Exception):
    pass

class PokeGender:
    def __init__(self,maleRate = 0,femaleRate = 0):
        if not (isinstance(maleRate,Number) and isinstance(femaleRate,Number)):
            raise TypeError('Rate must be a \'Number\'')
        self.__male = maleRate
        self.__female = femaleRate
        self.__genderless = 0
        if(self.__male==self.__female==0):
            self.__genderless = 1

    def __str__(self):
        try:
            string = 'Male Rate :'+str(self.getMaleRate())+'%'
            string += '\nFemale Rate :'+str(self.getFemaleRate())+'%'
        except GenderException:
            string = 'No gender'
        return string

    def __repr__(self):
        return self.__str__()

    def getMaleRate(self):
        if(self.__genderless):
            raise GenderException('No Gender')
        return self.__male

    def getFemaleRate(self):
        if(self.__genderless):
            raise GenderException('No Gender')
        return self.__female

""" Stats Class for Database--------------------------------------------------
"""
class PokeStats:
    def __init__(self,stats):
        self.__setHp(int(stats[1]))
        self.__setAttack(int(stats[2]))
        self.__setDefense(int(stats[3]))
        self.__setSpAttack(int(stats[4]))
        self.__setSpDefense(int(stats[5]))
        self.__setSpeed(int(stats[6]))

    def __str__(self):
        string = 'HP: '+str(self.__Hp)
        string+= ' Atk: '+str(self.__Attack)
        string+= ' Def: '+str(self.__Defense)
        string+= ' Sp.Atk: '+str(self.__SpAttack)
        string+= ' Sp.Def: '+str(self.__SpDefense)
        string+= ' Spd: '+str(self.__Speed)
        return string

    def __rpr__(self):
        return string
        
    def __setHp(self,hp):
        self.__Hp = hp

    def getHp(self):
        return self.__Hp

    def __setAttack(self,Attack):
        self.__Attack = Attack

    def getAttack(self):
        return self.__Attack

    def __setDefense(self,Defense):
        self.__Defense = Defense

    def getDefense(self):
        return self.__Defense

    def __setSpAttack(self,SpAttack):
        self.__SpAttack = SpAttack

    def getSpAttack(self):
        return self.__SpAttack

    def __setSpDefense(self,SpDefense):
        self.__SpDefense = SpDefense

    def getSpDefense(self):
        return self.__SpDefense

    def __setSpeed(self,Speed):
        self.__Speed = Speed

    def getSpeed(self):
        return self.__Speed

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
    
    def getPathImg(self):
        return self.__pathImg

    def getSPathImg(self):
        return self.__pathSImg

    def show(self):
        import tkinter as tk
        root = tk.Tk()
        root.title('Pokemon')
        photo = tk.PhotoImage(file = self.__pathImg)
        cv = tk.Canvas()
        cv.pack(side='top',fill = 'both',expand= 'yes')
        cv.create_image(10,10,image=photo,anchor='nw')
        root.mainloop()

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

    def getType1(self):
        return self.__type1

    def getType2(self):
        return self.__type2
        
""" Height Class for Database--------------------------------------------------
"""
        
class PokeHeight:
    def __init__(self,meter='0m',inches='0\'00"'):
        self.__meters = meter
        self.__metersValue = float(meter[:-1])

        self.__inches = inches
        aux = inches.split('\'')
        self.__inchesValue = 12*int(aux[0])+int(aux[1][:-1])

    def __str__(self):
        string  = 'Meters: '+self.__meters
        string += '\nInches: '+self.__inches
        return string

    def __repr__(self):
        return self.__str__()
    
    def getValueInMeters(self):
        return self.__metersValue

    def getMeters(self):
        return self.__meters

    def getValueInInches(self):
        return self.__inchesValue

    def getInches(self):
        return self.__inches

""" Weight Class for Database--------------------------------------------------
"""
        
class PokeWeight:
    def __init__(self,kg='0kg',lbs='0lbs'):
        self.__kg = kg
        self.__kgValue = float(kg.strip('kg'))

        self.__lbs = lbs
        self.__lbsValue = float(lbs.strip('lbs')) 

    def __str__(self):
        string  = 'Kg: '+self.__kg
        string += '\nLbs: '+self.__lbs
        return string

    def __repr__(self):
        return self.__str__()
    
    def getValueInKg(self):
        return self.__kgValue

    def getKg(self):
        return self.__kg

    def getValueInlbs(self):
        return self.__lbsValue

    def getlbs(self):
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

    def getName(self):
        return self.__name

    def getDescription(self):
        return self.__description

class AbilityError(Exception):
    pass

class PokeAbilities:
    def __init__(self,abilities):
        self.__abilities = []
        for ability in abilities['Normal']:
            for key in ability.keys():
                self.__abilities.append(PokeAbility(key,handleUnicodeProblens(ability[key].strip('. :'))))

        self.__hiddenAbilities = []
        try:
            for ability in abilities['Hidden']:
                for key in ability.keys():
                    self.__hiddenAbilities.append(PokeAbility(key,handleUnicodeProblens(ability[key].strip('. :'))))
        except KeyError:
            pass

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
            
    def getAbility(self,i):
        return self.__abilities[i]

    def getHiddenAbility(self,i):
        return self.__hiddenAbilities[i]

    def getAbilities(self):
        return self.__abilities

    def getHiddenAbilities(self):
        return self.__hiddenAbilities

""" Exp Growth Class for Database--------------------------------------------------
"""
class PokeExpGrowth:
    def __init__(self,expG):
        expG = expG.pop()
        expG = expG.split('Points')
        self.__exp = int(expG[0].replace(',',''))
        self.__classification = expG[1]

    def __str__(self):
        string =  'Exp to lvl 100: '+str(self.__exp)
        string += '\nClassification: '+str(self.__classification)
        return string
        
    def __repr__(self):
        return self.__str__()

    def getExpGrowth(self):
        return self.__expG

    def getClassification(self):
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

    def getValue(self):
        return self.__value

    def getStat(self):
        return self.__stat
    
""" EV Worth Class for Database--------------------------------------------------
"""

        
class PokeEVWorth:
    def __init__(self,EVs):
        EVs = EVs[0].split('Point(s)')
        self.__EVs = []
        for ev in EVs:
            if ev is not '':
                n = EV(int(ev[0]),Stat.__fromStr__(ev[1:].strip()))
                self.__EVs.append(n)
  
    def getEVs(self):
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
    def __init__(self,weak):
        self.__weaknesses = {}
        for key in weak.keys():
            self.__weaknesses[key] = float(weak[key].strip(' *'))

    def __str__(self):
        string = ''
        for key in self.__weaknesses.keys():
            string += str(key) + ': '+str(self.__weaknesses[key])+'\n'
        return string[:-1]

    def __repr__(self):
        return self.__str__()

    def getWeaknesses(self):
        return self.__weaknesses

""" Wild Items Class for Database--------------------------------------------------
"""
class PokeWildItems():
    def __init__(self,wI):
        aux = wI.strip().split('DexNav')
        self.__normal = split_percUppercase(aux[0])
        try:
            extras = []
            extras.clear()
            if(aux[1].find('BrightPowder')>=0):
                aux[1] = aux[1].replace('BrightPowder','')
                extras.append('BrightPowder')
            self.__dexNav = split_uppercase(aux[1])+extras
        except IndexError:
            self.__dexNav = None
##        print(wI,'\nNormal :',self.__normal,'\nDexNav :',self.__dexNav)

""" Capture Rate Class for Database--------------------------------------------------
"""
class PokeCR:
    def __init__(self,captureRate):
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

    def __str__(self):
        string =  'CR XY: '+str(self.__crXY)+'\n'
        string += 'CR ORAS: ' + str(self.__cRORAS)
        return string
    def __repr__(self):
        return self.__str__()

""" Egg Group Class for Database--------------------------------------------------
"""

class PokeEggGroup:
    def __init__(self,eggGroup):
        if isinstance(eggGroup,list):
            if(len(eggGroup)>1):
                self.__group1 = EggGroup.__fromStr__(eggGroup[0])
                self.__group2 = EggGroup.__fromStr__(eggGroup[1])
            else:
                self.__group1 = EggGroup.__fromStr__(eggGroup[0])
                self.__group2 = EggGroup.NoType
        else:
            self.__group1 = EggGroup.__fromStr__(eggGroup)
            self.__group2 = EggGroup.NoType

    def __str__(self):
        string =  'Group 1: '+ str(self.__group1)
        string += '\nGroup 2: '+ str(self.__group2)
        return string

    def __repr__(self):
        return self.__str__()

""" Poke Evo Class for Database--------------------------------------------------
"""
class Entity(Enum):
    NoType = 0
    Pokemon = 1
    MegaPokemon = 2
    Level = 3
    MegaStone = 4
    EvolutionStone = 5
    Egg = 6
    SexCondition = 7
    Condition = 8
    Trade = 9
    Local = 10
    Tyrogue = 11
    Rollout = 12
    
class PokeEvoChain:
    def __init__(self,evoChain):
        evoList = []
        for List in evoChain:
            evoEnt = []
            for ent in List:
                evoEnt.append(self.__entIdent(ent))
            evoList.append(evoEnt)
        self.__evoChain = []
        list2index = 0
        for ent,entIndex in zip(evoList[0],range(0,len(evoList[0]))):
            try:
                nextEntIndex = entIndex+1
                nextEnt = evoList[0][nextEntIndex]
                if(ent is Entity.Pokemon):
                    if(nextEnt is Entity.Pokemon or nextEnt is Entity.MegaPokemon):
                        evoNode = [evoChain[0][entIndex],evoChain[1][list2index],evoChain[0][nextEntIndex]]
                        self.__evoChain.append(evoNode)
                        list2index += 1
                    else:
                        evoNode = [evoChain[0][entIndex],evoChain[0][nextEntIndex],evoChain[0][nextEntIndex+1]]
                        self.__evoChain.append(evoNode)
            except IndexError:
                pass


    def __entIdent(self,unknown):
        conditions = ['happiness']
##        print(re.search(r'-m',unknown))
        if re.search(r'[^0-9]',unknown) is None:
            return Entity.Pokemon
        elif re.search(r'\d-\w',unknown) is not None:
            return Entity.MegaPokemon
        elif re.search(r'l\d',unknown) is not None:
            return Entity.Level
        elif re.search(r'mega\d|charizard',unknown) is not None:
            return Entity.MegaStone
        elif re.search(r'stone',unknown) is not None:
            return Entity.EvolutionStone
        elif re.search(r'egg',unknown) is not None:
            return Entity.Egg
        elif re.search(r'male|female',unknown) is not None:
            return Entity.SexCondition
        elif unknown in conditions:
            return Entity.Condition
        elif re.search(r'trade',unknown) is not None:
            return Entity.Trade
        elif re.search(r'coronet',unknown) is not None:
            return Entity.Local
        elif re.search(r'tyrogue',unknown) is not None:
            return Entity.Tyrogue
        elif re.search(r'rollout',unknown) is not None:
            return Entity.Rollout

        else:
            return Entity.NoType
""" Poke Location for Database--------------------------------------------------
"""
class PokeLocation:
    def __init__(self,location):
        for key in location.keys():
            if key == 'X':
                self.__x = location[key].split('\n')[2].strip()
        
            elif key == 'Y':
                self.__y = location[key].split('\n')[2].strip()

            elif key == 'Ruby':
                self.__oR = location[key].split('\n')[2].strip()

            elif key == 'Sapphire':
                self.__aS = location[key].split('\n')[2].strip()

    def __str__(self):
        string =  'X: '+ self.__x
        string += '\nY: '+ self.__y
        string += '\nOR: '+ self.__oR
        string += '\nAS: '+ self.__aS
        return string

    def __repr__(self):
        return self.__str__()

""" Poke Flavour Text for Database--------------------------------------------------
"""

class PokeDexText:
    def __init__(self,dexText):
        for key in dexText.keys():
            if key == 'X':
                self.__x = dexText[key].split('\n')[2].strip()
        
            elif key == 'Y':
                self.__y = dexText[key].split('\n')[2].strip()

            elif key == 'Ruby':
                self.__oR = dexText[key].split('\n')[2].strip()

            elif key == 'Sapphire':
                self.__aS = dexText[key].split('\n')[2].strip()

    def __str__(self):
        string =  'X: '+ self.__x
        string += '\nY: '+ self.__y
        string += '\nOR: '+ self.__oR
        string += '\nAS: '+ self.__aS
        return string

    def __repr__(self):
        return self.__str__()

""" Poke Attacks for Database--------------------------------------------------
"""

class Attack:
    def __init__(self,condition=0,name='',atkType = Type.NoType,cat = AttackCat.Other,att = 0,acc = 0,pp=0,effect = '',description = '' ):
        self.__condition = condition
        self.__name = name
        self.__atkType = atkType
        self.__cat = cat
        ## Value 357 means --
        ## Value 951 means ??
        if(att == '--'):
            self.__att = 357
        elif(att == '??'):
            self.__att = 951
        else:
            self.__att = int(att)
        ## Value 357 means --
        if(acc == '--'):
            self.__acc = 357
        else:
            self.__acc = int(acc)
        self.__pp = int(pp)
        self.__effect = effect
        self.__description = description

    def __str__(self):
        return self.__name+str(self.__cat)
    def __repr__(self):
        return self.__str__()

    def getCondition(self):
        return self.__condition
    def getName(self):
        return self.__name
    def getType(self):
        return self.__atkType
    def getCat(self):
        return self.__cat
    def getAtt(self):
        return self.__att
    def getAcc(self):
        return self.__acc
    def getPP(self):
        return self.__pp
    def getEffect(self):
        return self.__effect
    def getDescription(self):
       return self.__description
    
class PokeAttacks:
    def __init__(self,attackGroups):
        self.__attackGroups = {}
        for attackGroup in attackGroups.keys():
            self.__attackGroups[attackGroup] = []
            for attack in attackGroups[attackGroup]:
                caract = []
                for element in attack:
                    caract.append(element)
                if(len(caract)==8):
                    self.__attackGroups[attackGroup].append(Attack(name = caract[0],
                                                               atkType = Type.__fromStr__(caract[1]),
                                                               cat = AttackCat.__fromStr__(caract[2]),
                                                               att = caract[3],
                                                               acc = caract[4],
                                                               pp = caract[5],
                                                               effect = caract[6],
                                                               description = caract[7]))
                elif(len(caract) == 9):
                    self.__attackGroups[attackGroup].append(Attack(condition = caract[0],
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

    def getAttackGroups(self):
        return self.__attackGroups.keys()

    def getAttackGroup(self,key):
        return self.__attackGroups[key]
