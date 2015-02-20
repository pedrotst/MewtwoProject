from tkinter import *
from dex import *
from database import DatabaseManager
import re

class mainApplication():
    def __init__(self):
        self.__background = 'gray21'
        
        self.__config()
        
    def __config(self):
        self.__top = Tk()
        self.__configTop()
        self.__configPokeList()
        self.__configDexShow('Bulbasaur')
        


    def __configTop(self):
        self.__top.title('Pokedex')
        self.__top.minsize(width=self.__top.winfo_screenwidth() ,height=self.__top.winfo_screenheight())
        self.__top.configure(background=self.__background)
        
        
    def __configPokeList(self):
        self.__name = StringVar()
        db = DatabaseManager()
        data = db.getPokemonsByDexNum()
        OPTIONS = data
        self.__name.set(OPTIONS[0])
        self.__name.trace("w",lambda *args: self.__changePokemon(self.__name,*args))
        listbox = OptionMenu(self.__top,self.__name,*OPTIONS)
        listbox.pack()
        
    def __configDexShow(self,name):
        try:
            if(self.__l):
                self.__l.pack_forget()
                self.__l = None
        except AttributeError:
            pass
        self.__l = DexShow(self.__top,name)
        self.__l.pack()
        
    def __changePokemon(self,value,*args):
        self.__configDexShow(re.sub(r'[^a-zA-Z]','',value.get()))
        
    def run(self):
        self.__top.mainloop()
        
if __name__ == '__main__':
    mainApplication().run()
        