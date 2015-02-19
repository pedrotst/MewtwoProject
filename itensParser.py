from bs4 import BeautifulSoup
import item
import requests
import re
import os
import win_unicode_console
import html.parser

win_unicode_console.enable()

class importItens():
    def __init__(self):
        self.__url = 'http://serebii.net/itemdex/'
        self.__serebii = 'http://serebii.net'
        self.__itemFolder = '.\Itens\\'
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

    def buildBattleItemDb(self):
        battleFolderPath = os.path.join(self.__itemFolder, 'battle')
        print(battleFolderPath)
        for root, dirs, files in os.walk(battleFolderPath, topdown = False):
            for f in files:
                fileHtml = self.getHTML(os.path.join(battleFolderPath, f))
                fileSoup = BeautifulSoup(fileHtml)
                name = fileSoup.find("table", {"class": "dextable", "align": "center"}).find("tr").find("td").find("font").text
                print(name)
                category = 'battle'
                print(category)
                table2 = fileSoup.find_all("td", {"class": "cen"})
                iType = table2[1].text
                print(iType)
                flingDamage = table2[3].text
                print(flingDamage)
                purchPrice = table2[4].find_all("td", {"width": "40%"})[0].text
                sellPrice = table2[4].find_all("td", {"width": "40%"})[1].text
                print(purchPrice)
                print(sellPrice)
                versionsAvail = {}
                versionsList = []
                yesNoList = fileSoup.find_all("td", {"class": "cen", "width": "5%"})
                if len(yesNoList) == 0 :
                    yesNoList = fileSoup.find_all("td", {"class": "cen", "width": "6%"})
                for version in yesNoList:
                    versionsList.append(self.yesNoIsBool(version.text))
                while len(versionsList) < 18:
                    versionsList.append(False)
                versionsStr = ["RGBY", "GS", 'C', 'RS', 'E', "FRLG", 'DP', 'Pt', 'HG', 'SS', 'B', 'W', 'B2', 'W2', 'X', 'Y', 'oR', 'aS']
                for i in range(18):
                    versionsAvail[versionsStr[i]] = versionsList[i]
                print(versionsAvail)
                effectText = fileSoup.find("td", {"class": "fooinfo"}).text
                print(effectText)
                flavTexts = {}
                flavTextList = fileSoup.find_all("td", {"class": "fooinfo", "width": "80%"})
                if (flav = fileSoup.find("td", {"class": "crystal"})) != None:
                    flavTexts['HS'] = exist.text
                else:
                    flavTexts['HS'] = "NODATA"
                if (exists = fileSoup.find("td", {"class": "emerald"})
                exists = fileSoup.find("td", {"class": "leafgreen"})
                exists = fileSoup.find("td", {"class": "platinum"})
                exists = fileSoup.find("td", {"class": "soulsilver"})
                exists = fileSoup.find("td", {"class": "white"})
                exists = fileSoup.find("td", {"class": "white"})
                if exists != None:

                # flavVersions = ['HS', 'RSE', 'FRLG', 'DPPl', 'HGSS', 'BW', 'B2W2']
                # flavTextList = fileSoup.find_all()

c = importItens()
c.downloadItensMainPage()
# c.downloadItensPages()
#c.buildItemTypeDb()
c.buildBattleItemDb()
#c.parseItems()