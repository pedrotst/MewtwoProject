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
    def __init__(self, iName, iCategory, iType, flingDamage, purchPrice, sellPrice, versions, effectText, flvText, loc, pickUpDet, shoppingDet):
        super(iName, iCategory)
        self.__type = iType
        self.__flingDamage = flingDamage
        self.__purchPrice = purchPrice
        self.__sellPrice = sellPrice
        self.__versions = versions
        self.__effectText = effectText
        self.__flvText = flvText
        self.__loc = loc
        self.__pickUpDet = pickUpDet
        self.__shoppingDet = shoppingDet