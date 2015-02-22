import itensDb

class Item():
    def __init__(self, iName, iCategory, iType, iType2, japaName, japaTransl, flingDamage, purchPrice, sellPrice, effectText, versionsAvail, flvText, loc, pickUpDet, shoppingDet):
        self.__name = iName
        self.__category = iCategory
        self.__type = iType
        self.__type2 = iType2
        self.__japaName = japaName
        self.__japaTransl = japaTransl
        self.__flingDamage = flingDamage
        self.__purchPrice = purchPrice
        self.__sellPrice = sellPrice
        self.__effectText = effectText
        self.__versionsAvail = versionsAvail
        self.__flvText = flvText
        self.__loc = loc
        self.__pickUpDet = pickUpDet
        self.__shoppingDet = shoppingDet

    def __str__(self):
        string = self.__name+": \n"
        string+= "Category: " + self.__category+"\n"
        string+= "Type: " + self.__type + ', '+self.__type2+"\n"
        string+= "JapaName: " + self.__japaName +" - "+self.__japaTransl+"\n"
        string+= "FlingDamage: " + str(self.__flingDamage)+"\n"
        string+= "Purchace Price: " + str(self.__purchPrice)+"\n"
        string+= "Sell Price: " + str(self.__sellPrice)+"\n\n"
        string+= "Effect Text: " + self.__effectText+"\n\n"
        string+= "Versions Avail: " + str(self.__versionsAvail)+"\n\n"
        string+= "Flavour Text: " + str(self.__flvText)+"\n\n"
        string+= "Location: " + str(self.__loc)+"\n\n"
        string+= "Pickup Details: " + str(self.__pickUpDet)+"\n\n"
        string+= "Shopping Details: " + str(self.__shoppingDet)
        return string

    def __repr__(self):
        return self.__str__()

    def insertDb(self):
        if(len(self.__versionsAvail) == 18):
            itenDb = itensDb.ItemManager()
            versions_db = itensDb.ItemVersions()
            flav_db = itensDb.FlavourText()
            loc_db = itensDb.Locations()
            pickup_db = itensDb.Pickup()
            shop_db = itensDb.Shop()
            
            itenDb.insertItem(self.__name, self.__category, self.__type, self.__type2, self.__japaName, self.__japaTransl, self.__flingDamage, self.__purchPrice, self.__sellPrice, self.__effectText)
            versions_db.insert_item(self.__name, self.__versionsAvail)
            flav_db.insert_item(self.__name, self.__flvText)
            loc_db.insert_item(self.__name, self.__loc)
            pickup_db.insert_item(self.__name, self.__pickUpDet)
            shop_db.insert_item(self.__name, self.__shoppingDet)
            # itenDb.view()
