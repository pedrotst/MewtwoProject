from pokemonConstants import *
from numbers import Number
import re

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
        self.__genderless = False
        if(self.__male==self.__female==0):
            self.__genderless = True

    def __str__(self):
        if(not self.__genderless):
            string = 'Male Rate :'+str(self.getMaleRate())+'%'
            string += '\nFemale Rate :'+str(self.getFemaleRate())+'%'
        else:
            string = 'No gender'
        return string

    def __repr__(self):
        return self.__str__()

    def getMaleRate(self):
        return self.__male

    def getFemaleRate(self):
        return self.__female

    def isGenderless(self):
        return self.__genderless

""" Stats Class for Database--------------------------------------------------
"""
class PokeStats:
    def __init__(self,stats = None ,hp = None ,attack = None ,defense = None ,spAttack = None ,spDefense = None ,speed = None ,total = None):
        if(stats):
            self.__setHp(int(stats[1]))
            self.__setAttack(int(stats[2]))
            self.__setDefense(int(stats[3]))
            self.__setSpAttack(int(stats[4]))
            self.__setSpDefense(int(stats[5]))
            self.__setSpeed(int(stats[6]))
            self.__setTotal()
        else:
            self.__setHp(hp)
            self.__setAttack(attack)
            self.__setDefense(defense)
            self.__setSpAttack(spAttack)
            self.__setSpDefense(spDefense)
            self.__setSpeed(speed)
            self.__setTotal(total)
            
    def __str__(self):
        string = 'HP: '+str(self.__Hp)
        string+= ' Atk: '+str(self.__Attack)
        string+= ' Def: '+str(self.__Defense)
        string+= ' Sp.Atk: '+str(self.__SpAttack)
        string+= ' Sp.Def: '+str(self.__SpDefense)
        string+= ' Spd: '+str(self.__Speed)
        string+= ' Total: '+str(self.__Total)
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

    def __setTotal(self,total=None):
        if(total):
            self.__Total = total
        else:
            self.__Total = self.__Hp+self.__Attack+self.__Defense+self.__SpAttack+self.__SpDefense+self.__Speed

    def getTotal(self):
        return self.__Total

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
    
    def getValueInKg(self):
        return self.__kgValue

    def getKg(self):
        return self.__kg

    def getValueInLbs(self):
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
    def __init__(self,abilities = None, abilitiesList = -1, hiddenAbilitiesList = -1):
        if(abilities):
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
        elif(abilitiesList != -1 and  hiddenAbilitiesList != -1):
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
    def __init__(self,expG=None,expGrowth=None,expClassification=None):
        if(expG):
            expG = expG.pop()
            expG = expG.split('Points')
            self.__exp = int(expG[0].replace(',',''))
            self.__classification = expG[1]
        elif(expGrowth and expClassification):
            self.__exp = expGrowth
            self.__classification = expClassification
    def __str__(self):
        string =  'Exp to lvl 100: '+str(self.__exp)
        string += '\nClassification: '+str(self.__classification)
        return string
        
    def __repr__(self):
        return self.__str__()

    def getExpGrowth(self):
        return self.__exp

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
    def __init__(self,EVs = None,EvList = None):
        if(EVs):
            EVs = EVs[0].split('Point(s)')
            self.__EVs = []
            for ev in EVs:
                if ev is not '':
                    n = EV(int(ev[0]),Stat.__fromStr__(ev[1:].strip()))
                    self.__EVs.append(n)
        elif(EvList):
            self.__EVs = []
            for ev in EvList:
                n = EV(ev[2],Stat.__fromStr__(ev[1]))
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
    def __init__(self,weak = None,normal = None ,fire = None ,water = None ,electric = None ,grass = None ,ice = None ,fighting = None ,poison = None ,ground = None ,flying = None ,psychic = None ,bug = None ,rock = None ,ghost = None ,dragon = None ,dark = None ,steel = None,fairy = None):
        self.__weaknesses = {}
        if(weak):
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

    def getWeaknesses(self):
        return self.__weaknesses

""" Wild Items Class for Database--------------------------------------------------
"""
class PokeWildItems():
    def __init__(self,wI = None, items = -1, dexNavItems = -1):
        if(wI):
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
        elif(items != -1 and dexNavItems != -1):
            self.__normal = items
            self.__dexNav = dexNavItems
    def __str__(self):
        string = '\nNormal :'+str(self.__normal)+'\nDexNav :'+str(self.__dexNav)
        return string

    def __repr__(self):
        return self.__str__()
        
    def getNormalItems(self):
        return self.__normal
         
    def getDexNavItems(self):
        try:
            return self.__dexNav
        except AttributeError:
            return None
##        print(wI,'\nNormal :',self.__normal,'\nDexNav :',self.__dexNav)

""" Capture Rate Class for Database--------------------------------------------------
"""
class PokeCR:
    def __init__(self,captureRate=None,cRORAS=None,crXY=None):
        if(captureRate):
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
        elif(cRORAS and crXY):
            self.__cRORAS =cRORAS
            self.__crXY = crXY

    def __str__(self):
        string =  'CR XY: '+str(self.__crXY)+'\n'
        string += 'CR ORAS: ' + str(self.__cRORAS)
        return string
    def __repr__(self):
        return self.__str__()

    def getXY(self):
        return self.__crXY

    def getORAS(self):
        return self.__cRORAS

""" Egg Group Class for Database--------------------------------------------------
"""

class PokeEggGroup:
    def __init__(self,eggGroup = None, group1 = None, group2 = None):
        if(eggGroup):
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
        elif(group1 and group2):
            self.__group1 = group1
            self.__group2 = group2

    def __str__(self):
        string =  'Group 1: '+ str(self.__group1)
        string += '\nGroup 2: '+ str(self.__group2)
        return string

    def __repr__(self):
        return self.__str__()

    def getGroup1(self):
        return self.__group1

    def getGroup2(self):
        return self.__group2


""" Poke Evo Class for Database--------------------------------------------------
""" 
class PokeEvoChain:
    def __init__(self,evoChain = None,dbChain = None):
        if evoChain:
            pkms = evoChain[0]
            methods = evoChain[1]
            j = 0
            evoList = []
            while(len(methods)>0):
                pkm = pkms[j][0]
                column = pkms[j][1]
                colspan = int(pkms[j][2])
                row = pkms[j][3]
                rowspan = int(pkms[j][4])
                if(rowspan > 0):
                    nextRows = rowspan
                    i = 0
                    currRow = 0
                    while nextRows>0:
                        #print(i,methods)
                        method = methods[i][0]
                        methodCol = methods[i][1]
                        methodRow = methods[i][3]
                        methodRowSpan = int(methods[i][4])
                        if(currRow==methodRow):
                            evoRow = methodRow
                            evoCol = methodCol+1
                            if(methodRowSpan==0):
                                nextRows -= 1
                                currRow += 1
                                if(rowspan!=0):
                                    evoCol=column+2
                                    evoRow=row
                            else:
                                nextRows -= methodRowSpan
                                currRow += methodRowSpan
                            node = (pkm,method,self.__getByRowAndCol(pkms,evoRow,evoCol))
                            evoList.append(node)
                            #print(node)
                            del methods[i]
                            i-=1
                        i+=1
                elif(colspan == 0):
                    method = methods[0][0]
                    methodCol = methods[0][1]
                    methodRow = methods[0][3]
                    if(row == methodRow):
                        node = (pkm,method,self.__getByRowAndCol(pkms,methodRow,methodCol+1))
                        del methods[0]
                        evoList.append(node)
                elif(colspan > 0):
                    nextCol = colspan
                    i = 0
                    currCol = 0
                    while nextCol>0:
                        method = methods[i][0]
                        methodCol = methods[i][1]
                        methodColSpan = int(methods[i][2])
                        methodRow = methods[i][3]
                        if(currCol==methodCol):
                            if(methodColSpan==0):
                                nextCol -= 1
                                currCol += 1
                            else:
                                nextCol -= methodColSpan
                                currCol += methodColSpan
                            node = (pkm,method,self.__getByRowAndCol(pkms,methodRow+1,methodCol))
                            evoList.append(node)
                            del methods[i]
                            i-=1
                        i+=1
                else:
                    pass
                j+=1
                #print(evoList)
            self.__evoChain = evoList
            
        else:
            self.__evoChain = list(dbChain)

    def __getByRowAndCol(self,elements,row,col):
        for element in elements:
            if element[3]==row and element[1]==col:
                return element[0]
        return None
            

    def __str__(self):
        string = ''
        for node in self.__evoChain:
            string += str(node[0])+'\n'
        return string.strip()
        
    def getEvoChain(self):
        return self.__evoChain
""" Poke Location for Database--------------------------------------------------
"""
class PokeLocation:
    def __init__(self,location = None,x = None,y = None, oR = None, aS = None):
        if(location):
            for key in location.keys():
                if key == 'X':
                    self.__x = location[key].split('\n')[2].strip()
            
                elif key == 'Y':
                    self.__y = location[key].split('\n')[2].strip()

                elif key == 'Ruby':
                    self.__oR = location[key].split('\n')[2].strip()

                elif key == 'Sapphire':
                    self.__aS = location[key].split('\n')[2].strip()
        elif(x and y and oR and aS):
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

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getOR(self):
        return self.__oR

    def getAS(self):
        return self.__aS


""" Poke Flavour Text for Database--------------------------------------------------
"""

class PokeDexText:
    def __init__(self,dexText = None,x = None,y = None, oR = None, aS = None):
        if(dexText):
            for key in dexText.keys():
                if key == 'X':
                    self.__x = dexText[key].split('\n')[2].strip()
            
                elif key == 'Y':
                    self.__y = dexText[key].split('\n')[2].strip()

                elif key == 'Ruby':
                    self.__oR = dexText[key].split('\n')[2].strip()

                elif key == 'Sapphire':
                    self.__aS = dexText[key].split('\n')[2].strip()

        elif(x and y and (oR or aS)):
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

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getOR(self):
        return self.__oR

    def getAS(self):
        return self.__aS


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
        string =  'Name: '+self.__name
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

    def setCondition(self,value):
        self.__condition = value

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
    def __init__(self,attackGroups = None, attacks = None):
        if(attackGroups):
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
        elif(attacks):
            self.__attackGroups = attacks

    def __str__(self):
        string = ''
        for key in self.getAttackGroups():
            string += key+':\n'
            for attack in self.getAttackGroup(key):
                string += str(attack)+'\n'
        return string
    
    def getAttackGroups(self):
        return self.__attackGroups.keys()

    def getAttackGroup(self,key):
        return self.__attackGroups[key]
