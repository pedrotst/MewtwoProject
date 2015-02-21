import database

class Item:
    def __init__(self, iName, iCategory):
        self.__name = iName
        self.__category = iCategory
        
    def __str__(self):
    	string = self.__name +": "+self.__category
    	return string
	
    def insertItemCategoryDatabase(self):
        manager = database.ItemCategoryManager()
        manager.createItemCategoryTable()
        try:
        	manager.insertItem(self.getName(), self.getCategory())
        except database.sqlite3.IntegrityError:
            pass

    def __repr__(self):
    	return self.__str__()

    def getName(self):
    	return self.__name

    def getCategory(self):
    	return self.__category

class battleItem(Item):
    def __init__(self, iName, iCategory, iType, japaName, flingDamage, purchPrice, sellPrice, versions, effectText, flvText, loc, pickUpDet, shoppingDet):
        self.__name = iName
        self.__category = iCategory
        self.__type = iType
        self.__japaName = japaName
        self.__flingDamage = flingDamage
        self.__purchPrice = purchPrice
        self.__sellPrice = sellPrice
        self.__versions = versions
        self.__effectText = effectText
        self.__flvText = flvText
        self.__loc = loc
        self.__pickUpDet = pickUpDet
        self.__shoppingDet = shoppingDet

    def __str__(self):
        string = self.__name+": \n"
        string+= "Category: " + self.__category+"\n"
        string+= "Type: " + self.__type+"\n"
        string+= "JapaName: " + self.__japaName+"\n"
        string+= "FlingDamage: " + self.__flingDamage+"\n"
        string+= "Purchace Price: " + self.__purchPrice+"\n"
        string+= "Sell Price: " + self.__sellPrice+"\n\n"
        string+= "Versions: " + str(self.__versions)+"\n\n"
        string+= "Effect Text: " + self.__effectText+"\n\n"
        string+= "Flavour Text: " + str(self.__flvText)+"\n\n"
        string+= "Location: " + str(self.__loc)+"\n\n"
        string+= "Pickup Details: " + str(self.__pickUpDet)+"\n\n"
        string+= "Shopping Details: " + str(self.__shoppingDet)
        return string

    def __repr__(self):
        return self.__str__()

    # def insertDB(self):
    #     