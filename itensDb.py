import sqlite3

class Manager:
    def __init__(self):
        self._databasePath = 'Iten.db'
        self._connection = None

    def __exit__(self):
        if self._connection:
            self._connection.close()
            print('Closing')

    def _certifyConnection(self):
        if self._connection is None:
            self._connectToDatabase()        

    def _connectToDatabase(self):
        self._connection = sqlite3.connect(self._databasePath)

class BattleItenManager(Manager):
