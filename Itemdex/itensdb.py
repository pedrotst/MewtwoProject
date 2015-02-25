import sqlite3
import re
class BDManager:
    def __init__(self):
        self._databasePath = 'Itens.db'
        self._connection = None

    def __exit__(self):
        if self._connection:
            self._connection.close()
            print('Closing')

    def _certify_connection(self):
        if self._connection is None:
            self._connectToDatabase()        

    def _connectToDatabase(self):
        self._connection = sqlite3.connect(self._databasePath)

def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

class ItemManager(BDManager):
    def createItemTable(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
                Item(Name  TEXT PRIMARY KEY,
                Category   TEXT,   Type        TEXT,
                Type2      TEXT,   JapaName    TEXT,
                JapaTranls TEXT,   FlingDamage INTEGER,
                PurchPrice INTEGER,SellPrice   INTEGER,
                Effect     Text
                )''')

    def insertItem(self, name, category,
                type1, type2, japaName,
                japaTranls, flingDmg, purchPrice,
                sellPrice, effect):
        self._certify_connection()
        if not (isinstance(name, str) and isinstance(category, str)
        and isinstance(type1, str)    and isinstance(type2, str)
        and isinstance(japaName, str) and isinstance(japaTranls, str)
        and isinstance(flingDmg, int) and isinstance(purchPrice, int)
        and isinstance(sellPrice, int) and isinstance(effect, str)):
            raise TypeError('Something is the wrong type Bro')
        itemData = (name, category, type1, type2, japaName, japaTranls, flingDmg, purchPrice, sellPrice, effect)
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Item VALUES (?,?,?,?,?,?,?,?,?,?)",itemData)
            except sqlite3.OperationalError as error:
                self.createItemTable()
                self.insertItem(name, category, type1,
                                type2, japaName, japaTranls,
                                flingDmg, purchPrice,
                                sellPrice, effect)
            except sqlite3.IntegrityError as error:
                cursor.execute("DELETE FROM Item WHERE NAME = ?", (name,))
                self.insertItem(name, category, type1,
                                type2, japaName, japaTranls,
                                flingDmg, purchPrice,
                                sellPrice, effect)

    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM Item'):
                print(row)

    def getByCat(self, cat):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute(
                'SELECT Name FROM Item WHERE Category = ? ORDER BY Name', (cat,)):
                print(row)

    def get_by_name(self, name):
        self._certify_connection()
        with self._connection as conn:
            item =  conn.cursor().execute(
                'SELECT * FROM Item WHERE Name = ?', (name,))
            item = list(item)
            return item[0]

    def get_names_a_r(self):
        self._certify_connection()
        names_list = []
        with self._connection as conn:
            conn.create_function("REGEXP", 2, regexp)
            cursor = conn.cursor()
            cursor.execute('SELECT Name FROM Item WHERE Name REGEXP "^[A-R]" ORDER BY Name')
            data = cursor.fetchall()
            return(list(map(lambda x: x[0], data)))

    def get_names_h_r(self):
        self._certify_connection()
        names_list = []
        with self._connection as conn:
            conn.create_function("REGEXP", 2, regexp)
            cursor = conn.cursor()
            cursor.execute('SELECT Name FROM Item WHERE Name REGEXP "^[H-R]" ORDER BY Name')
            data = cursor.fetchall()
            return(list(map(lambda x: x[0], data)))

    def get_names_s_z(self):

        self._certify_connection()
        names_list = []
        with self._connection as conn:
            conn.create_function("REGEXP", 2, regexp)
            cursor = conn.cursor()
            cursor.execute('SELECT Name FROM Item WHERE Name REGEXP "^[S-Z]" ORDER BY Name')
            data = cursor.fetchall()
            return(list(map(lambda x: x[0], data)))


class ItemVersions(BDManager):
    def create_table(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
                ItemVersions(Name TEXT PRIMARY KEY,
                RGBY BOOLEAN, GS BOOLEAN, C BOOLEAN,
                RS BOOLEAN, E  BOOLEAN, FRLG BOOLEAN,
                DP BOOLEAN, PT BOOLEAN, HG BOOLEAN,
                SS BOOLEAN, B  BOOLEAN, W BOOLEAN,
                B2 BOOLEAN, W2 BOOLEAN, X BOOLEAN,
                Y  BOOLEAN, OR_ BOOLEAN, AS_ BOOLEAN
                )''')

    def insert_item(self, name, versions_dict):
        self._certify_connection()
        if versions_dict is not None:
            item_data = (name,  versions_dict['RGBY'], versions_dict['GS'],
                versions_dict['C'], versions_dict['RS'], versions_dict['E'],
                versions_dict['FRLG'], versions_dict['DP'], versions_dict['Pt'],
                versions_dict['HG'], versions_dict['SS'], versions_dict['B'],
                versions_dict['W'], versions_dict['B2'], versions_dict['W2'],
                versions_dict['X'], versions_dict['Y'], versions_dict['oR'],
                versions_dict['aS'])
        else:
            raise TypeError("Te proper dictionary was not provided")
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO ItemVersions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    item_data)
            except sqlite3.OperationalError as error:
                self.create_table()
                cursor.execute(
                    "INSERT INTO ItemVersions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    item_data)
            except sqlite3.IntegrityError as error:
                cursor.execute("DELETE FROM ItemVersions WHERE NAME = ?", (name,))
                self.insert_item(name, versions_dict)


    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM ItemVersions'):
                print(row)

    def getByCat(self, cat):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute(
                'SELECT Name FROM ItemVersions WHERE Category = ? ORDER BY Name', (cat,)):
                print(row)

    def get_by_name(self, name):
        self._certify_connection()
        with self._connection as conn:
            versions = conn.cursor().execute(
                'SELECT * FROM ItemVersions WHERE Name = ? ORDER BY Name', (name,))
            version = list(versions)[0]
            return version[1:]

class FlavourText(BDManager):
    def create_table(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
                FlavourText(Name TEXT PRIMARY KEY,
                GSC TEXT, RSE TEXT, FRLG TEXT,
                DPPl TEXT, HGSS  TEXT, BW TEXT,
                B2W2 TEXT, XY TEXT, ORAS TEXT
                )''')

    def insert_item(self, name, flav_dict):
        self._certify_connection()
        if len(flav_dict) == 9:
            item_data = (name,
                flav_dict['GSC'], flav_dict['RSE'], flav_dict['FRLG'],
                flav_dict['DPPl'], flav_dict['HGSS'], flav_dict['BW'],
                flav_dict['B2W2'], flav_dict['XY'], flav_dict['oRaS'])
        else:
            raise TypeError("The proper dictionary was not provided")
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO FlavourText VALUES (?,?,?,?,?,?,?,?,?,?)",
                    item_data)
            except sqlite3.OperationalError as error:
                self.create_table()
                cursor.execute(
                    "INSERT INTO FlavourText VALUES (?,?,?,?,?,?,?,?,?,?)",
                    item_data)
            except sqlite3.IntegrityError as error:
                cursor.execute("DELETE FROM FlavourText WHERE NAME = ?", (name,))
                self.insert_item(name, flav_dict)


    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM Item'):
                print(row)

    def getByCat(self, cat):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute(
                'SELECT Name FROM Item WHERE Category = ? ORDER BY Name', (cat,)):
                print(row)

    def get_by_name(self, name):
        self._certify_connection()
        with self._connection as conn:
            item_flav_list = conn.cursor().execute(
                'SELECT * FROM FlavourText WHERE Name = ? ORDER BY Name', (name,))
            item_flav = list(item_flav_list)[0]
            return item_flav[1:]

class Locations(BDManager):
    def create_table(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
                Locations(Name TEXT PRIMARY KEY,
                GSC TEXT, RSE TEXT, FRLG TEXT,
                DPPl TEXT, HGSS  TEXT, BW TEXT,
                B2W2 TEXT, XY TEXT, ORAS TEXT,
                PkWalker TEXT
                )''')

    def insert_item(self, name, loc_dict):
        self._certify_connection()
        if len(loc_dict) == 10:
            item_data = (name,
                loc_dict['GSC'], loc_dict['RSE'], loc_dict['FRLG'],
                loc_dict['DPPl'], loc_dict['HGSS'], loc_dict['BW'],
                loc_dict['B2W2'], loc_dict['XY'], loc_dict['oRaS'],
                loc_dict['PkWalker'])
        else:
            raise TypeError("The proper dictionary was not provided")
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO Locations VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    item_data)
            except sqlite3.OperationalError as error:
                self.create_table()
                cursor.execute(
                    "INSERT INTO Locations VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    item_data)
            except sqlite3.IntegrityError as error:
                cursor.execute("DELETE FROM Locations WHERE NAME = ?", (name,))
                self.insert_item(name, loc_dict)


    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM Locations'):
                print(row)

    def getByCat(self, cat):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute(
                'SELECT Name FROM Locations WHERE Category = ? ORDER BY Name', (cat,)):
                print(row)
    def get_by_name(self, name):
        self._certify_connection()
        with self._connection as conn:
            item_loc_list = conn.cursor().execute(
                'SELECT * FROM Locations WHERE Name = ? ORDER BY Name', (name,))
            item_loc = list(item_loc_list)[0]
            return item_loc[1:]

class Shop(BDManager):
    def create_table(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
                Shop(Name TEXT PRIMARY KEY,
                GSC TEXT, RSE TEXT, FRLG TEXT,
                DPPl TEXT, HGSS  TEXT, BW TEXT,
                B2W2 TEXT, XY TEXT, ORAS TEXT,
                BattleRev TEXT
                )''')

    def insert_item(self, name, shop_dict):
        self._certify_connection()
        if len(shop_dict) == 10:
            item_data = (name,
                shop_dict['GSC'], shop_dict['RSE'], shop_dict['FRLG'],
                shop_dict['DPPl'], shop_dict['HGSS'], shop_dict['BW'],
                shop_dict['B2W2'], shop_dict['XY'], shop_dict['oRaS'],
                shop_dict['BattleRev'])
        else:
            raise TypeError("The proper dictionary was not provided")
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO Shop VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    item_data)
            except sqlite3.OperationalError as error:
                self.create_table()
                cursor.execute(
                    "INSERT INTO Shop VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    item_data)
            except sqlite3.IntegrityError as error:
                cursor.execute("DELETE FROM Shop WHERE NAME = ?", (name,))
                self.insert_item(name, shop_dict)


    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT * FROM Shop'):
                print(row)

    def getByCat(self, cat):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute(
                'SELECT Name FROM Shop WHERE Category = ? ORDER BY Name', (cat,)):
                print(row)

class Pickup(BDManager):
    def create_table(self):
        self._certify_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE  IF NOT EXISTS
                Pickup(Name TEXT PRIMARY KEY,
                RS TEXT, FRLG TEXT, Emerald TEXT,
                HGSS  TEXT, BW TEXT, XY TEXT
                )''')

    def insert_item(self, name, pickup_dict):
        self._certify_connection()
        if len(pickup_dict) == 6:
            item_data = (name,
                pickup_dict['RS'], pickup_dict['FRLG'], pickup_dict['Emerald'],
                pickup_dict['HGSS'], pickup_dict['BW'], pickup_dict['XY'])
        else:
            raise TypeError("The proper dictionary was not provided")
        with self._connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO Pickup VALUES (?,?,?,?,?,?,?)",
                    item_data)
            except sqlite3.OperationalError as error:
                self.create_table()
                cursor.execute(
                    "INSERT INTO Pickup VALUES (?,?,?,?,?,?,?)",
                    item_data)
            except sqlite3.IntegrityError as error:
                cursor.execute("DELETE FROM Pickup WHERE NAME = ?", (name,))
                self.insert_item(name, pickup_dict)


    def view(self):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute('SELECT Namex FROM Pickup'):
                print(row)

    def getByCat(self, cat):
        self._certify_connection()
        with self._connection as conn:
            for row in conn.cursor().execute(
                'SELECT Name FROM Pickup WHERE Category = ? ORDER BY Name', (cat,)):
                print(row)
