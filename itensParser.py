from bs4 import BeautifulSoup
import item
import requests
import re
import os
# import html.parser
from lxml import html




class importItens():
    def __init__(self):
        self.__url = 'http://serebii.net/itemdex/'
        self.__serebii = 'http://serebii.net'
        self.__itemFolder = './Itens'
        self.__itemName = 'Itens.html'
        self.__itemPath = os.path.join(self.__itemFolder, self.__itemName)
        self.__html = ''
        self.__dirs = ''
        self.__itemDic = {}
    def downloadItensMainPage(self):
            if(not os.path.exists(self.__itemFolder)):
                os.mkdir(self.__itemFolder)
                r = requests.get(self.__url)
                if (r.status_code != 200):
                    raise  Exception('Download failed')
                self.__html = html.parser.HTMLParser().unescape(r.text)
                with open(self.__itemPath,mode='wb') as f:
                    f.write(r.content)
                    f.close()
            else:
                self.getItemMainHTML()

    


    def createItemFolder(self, formSoup):
        categoryName = formSoup['name']
        categoryPath = os.path.join(self.__itemFolder, categoryName)
        if(not os.path.exists(categoryPath)):
            os.mkdir(categoryPath)
            os.mkdir(os.path.join(categoryPath, 'Sprites'))
            categoryLoc = os.path.join(categoryPath, categoryName+'.html')
            with open(categoryLoc, mode = 'w') as f:
                f.write(formSoup.prettify())
                f.close()

    def downloadEachItem(self, formSoup):
        categoryName = formSoup['name']
        categoryPath = os.path.join(self.__itemFolder, categoryName)
        if((categoryName == 'nav') or (categoryName == 'nav4') or (categoryName == 'nav2')):
            # options = formSoup.b.find_all({'option': 'value'}) no need to download the alphabetic order stuff, redundant D:
            options = []
        else:
            options = formSoup.find_all({'option': 'value'})
        for item in options:
            try:
                itemLoc = os.path.join(categoryPath, item.string+'.html')
                if(not os.path.exists(itemLoc) and (not item.string == '======')):
                    itemHTMLloc = self.__serebii + item['value']
                    print(item.string)
                    r = requests.get(itemHTMLloc)
                    if (r.status_code != 200):
                        raise  Exception('Download failed')
                    r.encode = 'latin1'
                    parsedText = html.parser.HTMLParser().unescape(r.text)
                    with open(itemLoc, mode = 'wb') as f:
                        f.write(parsedText.encode())
                        f.close()
            except:
                with open(self.__itemFolder+'error.txt', mode = 'a+') as f:
                    f.write("Download Failed for " + item.string + "\n")
    
    def downloadItensPages(self):
        soup = BeautifulSoup(self.__html)
        for td in soup.find_all('td', {'align': "center"}):
            form = td.find('form')
            if(form != None):
                self.createItemFolder(form)
                self.downloadEachItem(form)


    #won't allow buildItemTypeDb search at main list file        
    def notMainList(self, fileName):
        dirs = next(os.walk(self.__itemFolder))[1]
        for dirName in dirs:
            if fileName.startswith(dirName):
                return True
        return False

    def getHTML(self, path):
        dest = ''
        with open(path,mode='r', encoding = 'utf-8') as f:
            for line in f.readlines():
                dest += line
            f.close()
        return(dest)

    def getItemMainHTML(self):
        xx = b''
        with open(self.__itemPath,mode='rb') as f:
            for line in f.readlines():
                xx += line
            f.close()

        self.__html = str(xx, encoding = 'latin1').encode('latin1').decode('utf-8')

    def buildItemTypeDb(self):
        itList = []
        for root, dirs, files in os.walk(self.__itemFolder, topdown=False):
            for name in files:
                if(not self.notMainList(name)):
                    curFile = os.path.join(root, name)
                    #print(curFile)
                    cufFileHtml = self.getHTML(curFile)
                    soup = BeautifulSoup(cufFileHtml)
                    try:
                        f = soup.find("table", {"class": "dextable", "align":"center"})
                        itName = f.find("tr").find("td")
                        itType = root[8:]
                        itemthingy = item.Item(itName.string, itType)
                        # itList.append(itemthingy)
                        print(itemthingy)
                        itemthingy.insertItemCategoryDatabase()
                    except:
                        with open(self.__itemFolder+'errorTypedb.txt', mode = 'a+') as f:
                            f.write("Get Type and Name failed for " + curFile + "\n")
                            raise

        with open("itens.txt", mode = "w", encoding = 'utf-8') as f:
            f.write(itList)
            f.close()
            # for name in dirs:
            #     print(os.path.join(root, name))
    def yesNoIsBool(self, yesNo):
        if yesNo == "Yes":
            return True
        return False

    def getHead(self, l):
        return l[0] if len(l) > 0 else ''

    def getFlavourTextDict(self, fileTree):
        flavours = {}
        flavours['GSC'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Flavour Text"]/tr[position()>1]/td[text()="Crystal"]/following-sibling::td/text()'))
        flavours['RSE'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Flavour Text"]/tr[position()>1]/td[text()="Emerald"]/following-sibling::td/text()'))
        flavours['FRLG'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Flavour Text"]/tr[position()>1]/td[text()="LeafGreen"]/following-sibling::td/text()'))
        flavours['DPPl'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Flavour Text"]/tr[position()>1]/td[text()="Platinum"]/following-sibling::td/text()'))
        flavours['HGSS'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Flavour Text"]/tr[position()>1]/td[text()="SoulSilver"]/following-sibling::td/text()'))
        flavours['BW'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Flavour Text"]/tr[position()>1]/td[text()="White"]/following-sibling::td/text()'))
        flavours['B2W2'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Flavour Text"]/tr[position()>1]/td[text()="White 2"]/following-sibling::td/text()'))
        flavours['XY'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Flavour Text"]/tr[position()>1]/td[text()="Y"]/following-sibling::td/text()'))
        flavours['oRaS'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Flavour Text"]/tr[position()>1]/td[text()="Alpha Sapphire"]/following-sibling::td/text()'))
        return flavours

    def getLocationsDict(self, fileTree):
        locations = {}
        locations['GSC'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Locations"]/tr[position()>1]/td[text()="Crystal"]/following-sibling::td/a[position()>0]/text()'))
        locations['RSE'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Locations"]/tr[position()>1]/td[text()="Emerald"]/following-sibling::td/a/text()'))
        locations['FRLG'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Locations"]/tr[position()>1]/td[text()="LeafGreen"]/following-sibling::td/a/text()'))
        locations['DPPl'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Locations"]/tr[position()>1]/td[text()="Platinum"]/following-sibling::td/a/text()'))
        locations['HGSS'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Locations"]/tr[position()>1]/td[text()="SoulSilver"]/following-sibling::td/a/text()'))
        locations['BW'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Locations"]/tr[position()>1]/td[text()="White"]/following-sibling::td/a/text()'))
        locations['B2W2'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Locations"]/tr[position()>1]/td[text()="White 2"]/following-sibling::td/a/text()'))
        locations['XY'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Locations"]/tr[position()>1]/td[text()="Y"]/following-sibling::td/a/text()'))
        locations['oRaS'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Locations"]/tr[position()>1]/td[text()="Alpha Sapphire"]/following-sibling::td/a/text()'))
        locations['PkWalker'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Locations"]/tr[position()>1]/td[text()="PokéWalker"]/following-sibling::td/a/text()'))
        locations['PkWalker'] += " "+ self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Locations"]/tr[position()>1]/td[text()="PokéWalker"]/following-sibling::td/i/text()'))
        return locations
                
    def getShoppingDict(self, fileTree):
        shopDet = {}
        shopDet['GSC'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Shopping Details"]/tr[position()>1]/td[text()="Crystal"]/following-sibling::td/a[position()>0]/text()'))
        shopDet['RSE'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Shopping Details"]/tr[position()>1]/td[text()="Emerald"]/following-sibling::td/a/text()'))
        shopDet['FRLG'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Shopping Details"]/tr[position()>1]/td[text()="LeafGreen"]/following-sibling::td/a/text()'))
        shopDet['DPPl'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Shopping Details"]/tr[position()>1]/td[text()="Platinum"]/following-sibling::td/a/text()'))
        shopDet['HGSS'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Shopping Details"]/tr[position()>1]/td[text()="SoulSilver"]/following-sibling::td/a/text()'))
        shopDet['BW'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Shopping Details"]/tr[position()>1]/td[text()="White"]/following-sibling::td/a/text()'))
        shopDet['B2W2'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Shopping Details"]/tr[position()>1]/td[text()="White 2"]/following-sibling::td/a/text()'))
        shopDet['XY'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Shopping Details"]/tr[position()>1]/td[text()="Y"]/following-sibling::td/a/text()'))
        shopDet['oRaS'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Shopping Details"]/tr[position()>1]/td[text()="Alpha Sapphire"]/following-sibling::td/a/text()'))
        shopDet['BattleRev'] =  self.getHead(fileTree.xpath('//table[./tr[1]/td/text() = "Shopping Details"]/tr[position()>1]/td[text()="Battle Revolution"]/following-sibling::td/text()'))
        return shopDet

    def getPickUpLocDict(self, fileTree):
        pickDet = {}
        pickDet['RS'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/a/b/text() = "PickUp"]/tr[position()>1]/td[text()="Sapphire"]/following-sibling::td/text()'))
        pickDet['FRLG'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/a/b/text() = "PickUp"]/tr[position()>1]/td[text()="LeafGreen"]/following-sibling::td/text()'))
        pickDet['Emerald'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/a/b/text() = "PickUp"]/tr[position()>1]/td[text()="Emerald"]/following-sibling::td/text()'))
        pickDet['HGSS'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/a/b/text() = "PickUp"]/tr[position()>1]/td[text()="SoulSilver"]/following-sibling::td/text()'))
        pickDet['BW'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/a/b/text() = "PickUp"]/tr[position()>1]/td[text()="White"]/following-sibling::td/font/text()'))
        pickDet['XY'] = self.getHead(fileTree.xpath('//table[./tr[1]/td/a/b/text() = "PickUp"]/tr[position()>1]/td[text()="Y"]/following-sibling::td/font/text()'))
        return pickDet

    def getAvailDict(self, fileTree):
        yesNoList = fileTree.xpath('//table[./tr[1]/td/text() = "Attainable In"]/tr[3]/td/text()')
        trueFalseList = (list(map (lambda x: True if x == 'Yes' else False, yesNoList)))
        versionsStr = ["RGBY", "GS", 'C', 'RS', 'E', "FRLG", 'DP', 'Pt', 'HG', 'SS', 'B', 'W', 'B2', 'W2', 'X', 'Y', 'oR', 'aS']
        versionsAvail = dict(zip(versionsStr, trueFalseList))
        return versionsAvail

    def getType(self, fileTree):
        iType = fileTree.xpath('//table[@class = "dextable"]/tr[./td[2]/text() = "Item Type"]/following-sibling::tr/td[2]/a/text()')
        typeQuant = len(iType)
        if(typeQuant > 0):
            if(typeQuant > 1):
                return (iType[0], iType[1])
            else:
                return (iType[0], '')
        else:
            return ('', '')

    def getName(self, fileTree):
        name = fileTree.xpath('//table[@class = "dextable" and @align = "center"]/tr[1]/td/font/b/text()')
        return name[0] if len(name) >0 else ''

    #gets the purchPrice as int, if doesn't exists, returns -1
    def getPurchPrice(self,fileTree):
        purchPrice = fileTree.xpath('//td[@class = "cen"]/table/tr[./td/b/text() = "Purchase Price"]/td[2]/text()')
        return int(purchPrice[0]) if len(purchPrice) >0 else -1
    #gets the sellPrice as int, if doesn't exists, returns -1
    def getSellPrice(self,fileTree):
        sellPrice = fileTree.xpath('//td[@class = "cen"]/table/tr[./td/b/text() = "Sell Price"]/td[2]/text()')
        return int(sellPrice[0]) if len(sellPrice) >0 else -1
    #gets the flingDamage as int, if doesn't exists, returns -1
    def getFlingDamage(self, fileTree):
        flingDamage = fileTree.xpath('//table[@class = "dextable"]/tr[./td[4]/text() = "Fling Damage"]/following-sibling::tr/td[4]/text()')
        return int(flingDamage[0]) if len(flingDamage) > 0 else -1

    def getEffectText(self,fileTree):
        effectText = fileTree.xpath('//table[@class = "dextable" and @align = "center" and ./tr/td/text() = "In-Depth Effect"]/tr[2]/td[@class = "fooinfo"]/text()')
        return effectText[0] if len(effectText) > 0 else ''

    def getJapaneseText(self, fileTree):
        japaName = self.getHead(fileTree.xpath('//table[@class = "dextable"]/tr[./td[3]/text() = "Japanese Name"]/following-sibling::tr/td[3]/text()'))
        japaTranls = self.getHead(fileTree.xpath('//table[@class = "dextable"]/tr[./td[3]/text() = "Japanese Name"]/following-sibling::tr/td[3]/i/text()'))
        return (japaName, japaTranls)

    def getImgPath(self, fileTree):
        imgPath = fileTree.xpath("//table[@class='dextable'][2]/tr[2]/td[@class='cen'][1]/table/tr/td[@class='pkmn']/img/@src")
        return imgPath[0] if len(imgPath) > 0 else ''

    def downloadSprites(self):
        for root, dirs, files in os.walk(self.__itemFolder, topdown = True):
            for f in files:
                if(f != root[6:] + '.html' and f[-5:] == '.html' and f[:-5] != root[:5]):
                    # print(os.path.join(root, f))
                    print("Downloading: " + f)
                    fileHtml = self.getHTML(os.path.join(root, f))
                    fileTree = html.fromstring(fileHtml)
                    imageUrl = self.__serebii + self.getImgPath(fileTree)
                    imagePath = os.path.join(root, 'Sprites', f[:-5])
                    if imageUrl == self.__serebii:
                        print("error with: " + f)
                    r = requests.get(imageUrl)
                    if r.status_code == 200:
                        with open(imagePath+'.png', 'wb') as pic:
                            for chunk in r.iter_content():
                                pic.write(chunk)
                            pic.close()
                    else:
                        print("error with request: " + f)
                else:
                    print("error with root-check: " + f)




    def buildItemDb(self, name):
        folderPath = os.path.join(self.__itemFolder, name)
        print(folderPath)
        for root, dirs, files in os.walk(folderPath, topdown = True):
            for f in files: 
                if f[-5:] == '.html':
                    fileHtml = self.getHTML(os.path.join(root, f))
                    fileTree = html.fromstring(fileHtml)
                    name = self.getName(fileTree)
                    category = root[len(self.__itemFolder)+1:]
                    iType, iType2 = self.getType(fileTree)
                    flingDamage = int(self.getFlingDamage(fileTree))
                    japaName, japaTransl = self.getJapaneseText(fileTree)
                    purchPrice = self.getPurchPrice(fileTree)
                    sellPrice = self.getSellPrice(fileTree)
                    effectText = self.getEffectText(fileTree)
                    versionsAvail = self.getAvailDict(fileTree)
                    flavours = self.getFlavourTextDict(fileTree)
                    locations = self.getLocationsDict(fileTree)
                    pickUpLoc = self.getPickUpLocDict(fileTree)
                    shopDet = self.getShoppingDict(fileTree)
                    theItem = item.Item(name, category, iType, iType2, japaName, japaTransl, flingDamage, purchPrice, sellPrice, effectText, versionsAvail, flavours, locations, pickUpLoc, shopDet)
                    # print(theItem)
                    print(root, name)
                    theItem.insertDb()

c = importItens()
# c.downloadItensMainPage()
# c.downloadItensPages()
#c.buildItemTypeDb()
c.buildItemDb('')
# c.downloadSprites()
# c.parseItems()