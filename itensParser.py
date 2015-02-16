from bs4 import BeautifulSoup
from pokemon import *
import requests
import re

class importItens():
    def __init__(self):
        self.__url = 'http://www.serebii.net/omegarubyalphasapphire/items.shtml'
        self.__itemPath = './Pages/Itens.html'
        self.__html = ''
        
    def downloadItensPage(self):
            r = requests.get(self.__url)
            if (r.status_code != 200):
                raise  Exception('Download failed')
            r.enconding = 'Unicode'
            self.__html = r.text
            with open(self.__itemPath,mode='w',encoding = 'utf-8') as f:
                print(self.__html)

                f.write(self.__html)
                f.close()

    def getItemHTML(self):
        with open(self.__itemPath,mode='r',encoding='utf-8') as f:
            for line in f:
                self.__html += line + '\n'
        
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
c.getItemHTML()
c.parseItems()
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
