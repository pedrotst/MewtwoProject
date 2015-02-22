from bs4 import BeautifulSoup
from pokemon import *
import requests
import os

def runTest(xi=1,xf=721):
    
    for i in range(xi,xf):
        run(i)

def run(i):
    if(i<10):
        file = 'Pages/page00'+str(i)+'.html'
    elif(i<100):
        file = 'Pages/page0'+str(i)+'.html'
    else:
        file = 'Pages/page0'+str(i)+'.html'
    c = importSerebii()
##    c.downloadHTML(i)
    c.getLocalHTML(file)
    print(i)
    c.parseSerebii()
    poke = Pokemon(c.getPoke())
    poke.createPokemonEvoChainDatabase()
##    poke.createAbilityDatabase()
##    poke.createPokemonAbilityDatabase()
##    poke.createAttacksDatabase()
##    poke.createPokemonAttacksDatabase()
##    poke.createPokemonItemsDatabase()
##    poke.createPokemonDexNavItemsDatabase()
##    poke.createPokemonEVWorthDatabase()
##    poke.createPokemonDatabase()
    
class importSerebii():
    def __init__(self):
        self.__poke = {}
        self.__serebiiUrl = 'http://serebii.net'
        self.__urlStart = 'http://serebii.net/pokedex-xy/'
        self.__urlEnd = '.shtml'
        self.__html = ''
        self.__soup = ''
        self.__imgDir = 'PokeData/'
        
##--------------------------------------------------------------------------------
    ##Print Pokémon data
    def __str__(self):
        p = self.__poke
        print(p['Name'])
        print(p['No'])
        print(p['Gender'])
        print(p['Types'])
        print(p['Classification'])
        print(p['Height'])
        print(p['Weight'])
        print(p['Capture Rate'])
        print(p['Base Egg Steps'])
        print(p['Abilities'])
        print(p['Experience Growth'])
        print(p['Base Happiness'])
        print(p['Effort Values Earned'])
        print(p['Eligible for Sky Battle?'])
        print(p['Weaknesses'])
        print(p['Wild Hold Item'])
        print(p['Egg Groups'])
        print(p['Evo Chain'])
        ##Continuar
        print(p['Location'])
        print(p['Flavour Text'])
        ##Attacks e Stats
        return ''
    
##--------------------------------------------------------------------------------
    ##Reference to Pokémon Data
    def getPoke(self):
        return self.__poke
    
##--------------------------------------------------------------------------------
    ##Download HTLM from Serebii.net
    def downloadHTML(self,i):
        url = ''
        if(i<10):
            url = self.__urlStart + '00' +str(i)+self.__urlEnd
        elif(i<100):
            url = self.__urlStart + '0' +str(i)+self.__urlEnd
        else:
            url = self.__urlStart +str(i)+self.__urlEnd
        r = requests.get(url)
        if (r.status_code != 200):
            raise  Exception('Download failed')
        self.__html = r.text.encode('utf-8')

    def getLocalHTML(self,file):
        with open(file,mode='r',encoding='latin1') as f:
            for line in f:
                self.__html += line + '\n'
        
##--------------------------------------------------------------------------------
    ##Parsing the HTML provided by downloadHTML
    def parseSerebii(self):
        soup = BeautifulSoup(self.__html)
        self.__isMega(soup)
        self.__getBasicInfo(soup)
        self.__getPicture(soup)
        self.__getBattleInfo(soup)
        self.__getWeaknesses(soup)
        self.__getItemEggGroup(soup)
        self.__getEvoChain(soup)
        self.__getLocationAndFlavourText(soup)
        self.__getAttacks(soup)
        self.__getStats(soup)
        

    def __isMega(self,soup):
        if soup.find('a',{'name':'mega'}) is not None:
            self.__hasMega = 1
        else:
            self.__hasMega = 0
            
        
##--------------------------------------------------------------------------------
    ##Get Pokemon basic info and save in dictionary
    def __getBasicInfo(self,soup):
        ##Parse to first line
        info = soup.find("td", {"class":"fooinfo"}).findNextSibling()

        info = self.__getName(info)

        info = self.__getNum(info)

        info = self.__getGender(info)

        info = self.__getType(info)

        ##Parse to second line
        name = info.findParent().findNextSibling()
        info = name.findNextSibling()
        names = name.findAll('td')
        infos = info.findAll('td')
        ##Retrieve rest of the information
        for name,info in zip(names,infos):
            self.__poke[name.get_text()] = [info.get_text()]

            
##--------------------------------------------------------------------------------        
    def __getPicture(self,soup):
        ##Parsing to find image link
        info = soup.find("td", {"class":"fooinfo"})
        name = soup.find("td", {"class":"fooevo"})

        ##Find all images that represent the Pokemon
        infos = info.findAll("img")

        ##Look non-shiny one
        info = infos[0]

        ##Create Image URL
        imageUrl = self.__serebiiUrl +  info['src']

        ##Download Image
##        self.__downloadImage(imageUrl,self.__poke['Name'],self.__poke['Name'])

        ##Insert path to Image in the dictionary
        self.__poke[name.text] = self.__imgDir+self.__poke['Name']+'/'+self.__poke['Name']+'.png'

        ##Get Shiny
        info = infos [1]

        ##Create Shiny Image URL
        imageUrl = self.__serebiiUrl +  info['src']

        ##Download Shiny Image
##        self.__downloadImage(imageUrl,self.__poke['Name'],self.__poke['Name']+'-Shiny')

        ##Insert path to Image in the dictionary
        self.__poke[name.text+'-Shiny'] = self.__imgDir+self.__poke['Name']+'/'+self.__poke['Name']+'-Shiny.png'

        
##-------------------------------------------------------------------------------- 
    def __getBattleInfo(self,soup):
        info = soup.find('a',{"name":"general"}).findNextSibling().findNextSibling()

        info = self.__getAbilities(info)

        name = info.findNextSibling()
        info = name.findNextSibling()
        names = name.findAll('td')
        infos = info.findAll('td')
        ##Retrieve rest of the information
        for name,info in zip(names,infos):
            self.__poke[name.get_text()] = [info.get_text()]

##--------------------------------------------------------------------------------            
    ##Retrieve name and return parsing reference
    def __getName(self,info):   
        ##Insert Pokemon name into dictionary
        self.__poke['Name'] = info.string

        ## Parsing reference
        return info

##--------------------------------------------------------------------------------            
    ##Retrieve num and return parsing reference
    def __getNum(self,info):
        ##Parsing to find Pokemon numbers
        info = info.findNextSibling().findNextSibling() 
        trs = info.findAll('tr')

        ##Dictionary for the pokedex num
        numPoke = {}

        ##In each collum search for region and num
        for tr in trs:
            region = tr.td.findNext()
            num = region.findNext()
            numPoke[region.string] = num.string
        self.__poke['No'] = numPoke

        ## Parsing reference
        return info
    
##--------------------------------------------------------------------------------            
    ##Retrieve num and return parsing reference
    def __getGender(self,info):
        
        ##Parsing to find Gender Ratio
        info = info.findNextSibling()
        tr = info.find('tr')

        try:
            ##Dictionary for the gender
            genders = {}

            ## Get Male rate
            gender = tr.td.findNext()
            ratio = gender.findNext()
            genders['Male'] = ratio.string

            ##Parse to female ratio
            tr = tr.findNextSibling()

            ##Get Female Ratio
            gender = tr.td.findNext()
            ratio = gender.findNext()
            genders['Female'] = ratio.string

            self.__poke['Gender'] = genders
        except AttributeError:
            self.__poke['Gender'] = 'Genderless'
        ## Parsing reference
        return info
##--------------------------------------------------------------------------------        
    ##Get pokemon type and return parsing reference
    def __getType(self,info):
        info = info.findNextSibling()
        As = info.findAll('a')
        types = []
        for a in As:
            types.append(a['href'][12:-6].capitalize())

        self.__poke['Types'] = types

        return info

##--------------------------------------------------------------------------------
    ##Download an image with URL url and save it in imgDir/name/name.png     
    def __downloadImage(self,url,fld,name):
        ##Request URL
        r = requests.get(url)

        ##Check status
        if r.status_code == 200:
            folder = self.__imgDir+fld+'/'

            ##Check folder existance
            self.__ensure_dir(folder)

            ##Define image location
            imgPath = folder+name+'.png'

            ##Save Image in folder
            with open(imgPath, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)

    ##Ensures that directory f exists
    def __ensure_dir(self,f):
        d = os.path.dirname(f)
        if not os.path.exists(d):
            os.makedirs(d)
##--------------------------------------------------------------------------------
    ## Get abilities
    def __getAbilities(self,info):
        info = info.findNext()
        info = info.findNextSibling()
##        print(str(info).encode('utf-8','ignore'))
        try:
            end = info.find(text = 'Hidden Ability').findNext('a')
        except AttributeError:
            end = None
##        print(end)
        tags = info.findAll('a')
        abilities = {}
        abilityType = 'Normal'
        abilities[abilityType] = []
        for tag in tags:
            if tag is end:
                abilityType = 'Hidden'
                abilities[abilityType] = []
            ability = {}
            name = tag.getText()
            description = tag.next_sibling
            ability[name] = description
            abilities[abilityType].append(ability)
        self.__poke['Abilities'] = abilities
    
        return info
    
##--------------------------------------------------------------------------------
    def __getWeaknesses(self,soup):
        types = [Type.Normal,Type.Fire,Type.Water,Type.Electric,Type.Grass,Type.Ice,Type.Fighting,Type.Poison,Type.Ground,Type.Flying,Type.Psychic,Type.Bug,Type.Rock,Type.Ghost,Type.Dragon,Type.Dark,Type.Steel,Type.Fairy]
        info = soup.find('td',{'class','footype'})
        info = info.findParent()
        tags1 = info.findAll('td',{'class','footype'})
        info = info.findNextSibling()
        tags2 = info.findAll('td',{'class','footype'})
        weak = {}
        for tag1,tag2,t in zip(tags1,tags2,types):
            ##Descomentar para baixar imagens dos Tipos
            ##self.__downloadImage(self.__serebiiUrl+tag1.a.img['src'],'Tipos',t.__str__())
            weak[t]= tag2.string
        self.__poke['Weaknesses'] = weak

##--------------------------------------------------------------------------------
    def __getItemEggGroup(self,soup):

        ##Get Items
        name = soup.find('td',{'class','footwo'})
        info = name.findParent().findNextSibling().findNext()
        
        try:
            self.__poke[name.string] = info.get_text()
            imgUrl = self.__serebiiUrl + info.a.img['src']
##            self.__downloadImage(imgUrl,self.__poke['Name']+'/Wild Items',self.__poke[name.string].split('-')[0])
        except AttributeError:
            self.__poke[name.string] = 'None'

        try:
            dexnav = info.find('table',class_='dexitem')
            items = dexnav.findAll('td')
            dexnavItems = []
            for item in items:
                imgUrl = self.__serebiiUrl + item.a.img['src']
##                self.__downloadImage(imgUrl,self.__poke['Name']+'/Wild Items/DexNav',item.get_text())
        except AttributeError:
            c = 'sem erro'
        
        ##Get Egg Group
        name = name.findNextSibling()
        info = info.findNextSibling().find('table',class_='dexitem')
        try:            
            tags = info.findAll('tr')
            eggGroup = []
            for tag in tags:
                eggGroup.append(tag.find('td').findNextSibling().get_text())
            self.__poke[name.get_text()] = eggGroup
        except AttributeError:
            self.__poke[name.get_text()] = 'Not Breedable'
    
##--------------------------------------------------------------------------------
    def __getEvoChain(self,soup):
        info = soup.find('table',class_='evochain')
        tagsTr = info.findAll('tr')
        pokeEvoChain = []
        row = 0
        column = 0
        for tagTr in tagsTr:
            tagsTd = tagTr.findAll('td')
            #print(tagTr.findParent())
            column = 0
            for tagTd in tagsTd:
                try:
                    c = tagTd['class']
                    isPokemon = True
                except KeyError:
                    isPokemon = False
                try:
                    rowSpan = tagTd['rowspan']
                except KeyError:
                    rowSpan = 0
                try:
                    columnSpan = tagTd['colspan']
                except KeyError:
                    columnSpan = 0
                #print(isPokemon,column,columnSpan,row,rowSpan)
                try:
                    aux = tagTd.a.img['src'].split('/').pop().split('.')[0]
        
                except AttributeError:
                    aux = tagTd.img['src'].split('/').pop().split('.')[0]
                  
                pokeEvoChain.append((aux,row,rowSpan,column,columnSpan,isPokemon))
                
                column += 1
            row += 1
        self.__poke['Evo Chain'] = pokeEvoChain
        
##--------------------------------------------------------------------------------
    def __getAttacks(self,soup):
        info = soup.find('a',{'name':'attacks'})
        end = soup.find('a',{'name':'stats'}).findNext('table',{'class':'dextable'})
##        print(end.next)
        exceptions = ['Generation VI Level Up','X & Y Level Up','TM & HM Attacks','\u03a9R\u03b1S Level Up','X / Y Level Up - Attack Forme','\u03a9R\u03b1S Level Up - Attack Forme','X / Y Level Up - Defense Forme','\u03a9R\u03b1S Level Up - Defense Forme','X / Y Level Up - Speed Forme','\u03a9R\u03b1S Level Up - Speed Forme','X / Y Level Up - Sandy Cloak','\u03a9R\u03b1S Level Up - Sandy Cloak','X / Y Level Up - Trash Cloak','\u03a9R\u03b1S Level Up - Trash Cloack','X / Y Level Up - Sky Forme','\u03a9R\u03b1S Level Up - Sky Forme','X / Y Level Up - Zen Mode','\u03a9R\u03b1S Level Up - Zen Mode','X / Y Level Up - White Kyurem','\u03a9R\u03b1S Level Up - White Kyurem','X / Y Level Up - Black Kyurem','\u03a9R\u03b1S Level Up - Black Kyurem','X / Y Level Up - Pirouette Forme','\u03a9R\u03b1S Level Up - Pirouette Forme','X / Y Level Up - Eternal Flower','\u03a9R\u03b1S Level Up - Eternal Flower','X / Y Level Up - Female','\u03a9R\u03b1S Level Up - Female','Level Up - Hoopa Unbound']##'\0u3a9''\u03b1'
        tags = info.findAllNext('tr')
        attack = []
        attacks = {}
        attackClassName = ''
        count = 0
        for tag in tags:
            if(tag == end.next):
                break
            if(tag.td is not None):
##                print(tag.td.encode('utf-8'))
                try:
                    if(tag.td['class'][0] == 'fooevo'):
                        attackClassName = tag.td.getText()
                        attacks[attackClassName] = []
                    elif(tag.td['class'][0] == 'fooinfo'):
                        if(count == 0):
                            attack = []
##                            print(attackClassName.replace('\u03a9','2').replace('\u03b1','3'))
                            if(attackClassName in exceptions):
                                countTd = 0
                            else:
                                countTd = 1
                            for td in tag.findAll('td'):
                                if(countTd == 0):
                                    attack.append(td.getText())
                                elif(countTd == 1):
                                    attack.append(td.getText())
                                elif(countTd == 2):
                                    attack.append(td.img['src'][17:-4].capitalize())
                                elif(countTd == 3):
                                    attack.append(td.img['src'][17:-4].capitalize())
                                elif(countTd == 4):
                                    attack.append(td.getText())
                                elif(countTd == 5):
                                    attack.append(td.getText())
                                elif(countTd == 6):
                                    attack.append(td.getText())
                                elif(countTd == 7):
                                    attack.append(td.getText().replace('\u2014','-'))
                                countTd += 1
                        elif(count == 1):
                            for td in tag.findAll('td'):
                                attack.append(td.getText())
                                attacks[attackClassName].append(attack)
                        count+=1
                        if(count == 2):
                            count = 0
                except KeyError:
                    if(tag.td['colspan'][0] == '3'):
                        if(count == 1):
                            for td in tag.findAll('td'):
                                attack.append(td.getText())
                                attacks[attackClassName].append(attack)
                        count+=1
                        if(count == 2):
                            count = 0
                            
        self.__poke['Attacks'] = attacks

##--------------------------------------------------------------------------------
    def __getStats(self,soup):
        stats = []
        info = soup.find('td',{'colspan':'2','width':'14%','class':'fooinfo'})
        stats.append(info.getText())
        tags = info.findNextSiblings('td')
        for tag in tags:
            stats.append(tag.getText())
        self.__poke['Stats'] = stats
        
##--------------------------------------------------------------------------------
    def __getLocationAndFlavourText(self,soup):      
        location = {}
        flavourText = {}
        data = []

        ##X data
        infos = soup.findAll('td',{'class':'foox'})
        for info in infos:
            data.append(info.parent.getText())
        flavourText['X'] = data[1]
        location['X'] = data[0]
        data.clear()
        
        ##Y data
        infos = soup.findAll('td',{'class':'fooy'})
        for info in infos:
            data.append(info.parent.getText())
        flavourText['Y'] = data[1]
        location['Y'] = data[0]
        data.clear()
        
        ##Ruby data
        infos = soup.findAll('td',{'class':'ruby'})
        for info in infos:
            data.append(info.parent.getText())
        flavourText['Ruby'] = data[1]
        location['Ruby'] = data[0]
        data.clear()
        
        ##Shappire data
        infos = soup.findAll('td',{'class':'sapphire'})
        for info in infos:
            data.append(info.parent.getText())
        flavourText['Sapphire'] = data[1]
        location['Sapphire'] = data[0]

        self.__poke['Flavour Text'] = flavourText
        self.__poke['Location'] = location

if __name__ == '__main__':
    run(366)