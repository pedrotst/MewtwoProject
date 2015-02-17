from bs4 import BeautifulSoup
import item
import requests
import re
import os

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
                r.enconding = 'Unicode'
                self.__html = r.text
                with open(self.__itemPath,mode='w',encoding = 'utf-8') as f:
                    f.write(self.__html)
                    f.close()
            else:
                self.getItemMainHTML()

    def getItemMainHTML(self):
        with open(self.__itemPath,mode='r',encoding='utf-8') as f:
            for line in f:
                self.__html += line + '\n'

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
                    r.enconding = 'Unicode'
                    itemHtml = r.text
                    with open(itemLoc, mode = 'w', encoding = 'utf-8') as f:
                        f.write(itemHtml)
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
        with open(path,mode='r',encoding='utf-8') as f:
            for line in f:
                dest += line + '\n'
            f.close()
        return dest 

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
                        # if(root == '\.Itens\\misc'):
                        #     itType = (soup.find_all("td", {"class":"cen"}))[0]
                        # else:
                        #     itType = (soup.find_all("td", {"class":"cen"}))[1].find("a")
                        # if((itName != None) and (itType != None)):
                        #     print(itName.string, itType.string)
                    except:
                        with open(self.__itemFolder+'errorTypedb.txt', mode = 'a+') as f:
                            f.write("Get Type and Name failed for " + curFile + "\n")
                            raise

        with open("itens.txt", mode = "w", encoding = 'utf-8') as f:
            f.write(itList)
            f.close()
            # for name in dirs:
            #     print(os.path.join(root, name))
    
    
    
    def parseItems(self):
        soup = BeautifulSoup(self.__html)
        names = []
        descriptions = []
        locs = []
        itemDic = {}
        itemFound = 0
        descTime = False
        first = True
        itemName = None
        '''
        for tag in soup.find_all('a', {'href': re.compile("^/pokearth/")}):
            print(tag)
        '''
        for td in soup.find_all('td', {'class': "fooinfo"}):
            item = td.find('a', {'href': re.compile("^/itemdex/")})
            loc = td.find ('a', {'href': re.compile("^/pokearth/")})
            if(item != None):
                itemNameOld = itemName
                itemName = item.string
                itemFound += 1
                descTime = True
            elif(loc != None):
                locs.append(loc.string)
            elif(itemFound >= 1 and descTime):
                itemDesc = td.string
                descTime = False
            if(itemFound == 2):
                itemDic[itemNameOld] = (itemDesc,locs)
                locs = []
                itemFound -= 1
            
            
        print(itemDic)
        
c = importItens()
#c.downloadItensMainPage()
#c.downloadItensPages()
c.buildItemTypeDb()
#c.parseItems()
'''    if(itemFound == 2):
                itemFound = 0
                descriptions.append(td.string)
            for item in td.find_all('a', {'href': re.compile("^/itemdex/")}):
                names.append(item.string)
                itemFound += 1
                        
            for loc in td.find_all('a', {'href': re.compile("^/pokearth/")}):
                locs.append(loc.string)
            if(itemFound == 1 && first):
                first = False
'''
