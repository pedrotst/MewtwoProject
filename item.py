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