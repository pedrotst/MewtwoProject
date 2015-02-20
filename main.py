from tkinter import *
from dex import *
from database import DatabaseManager
import re
from dialog import MyDialog

class mainApplication():
    def __init__(self):
        self.__background = 'gray21'
        
        self.__config()
        
    def __config(self):
        self.__top = Tk()
        self.__configTop()
        self.__configPokeList()
        self.__configDexShow('Bulbasaur')
        self.__configErrorLog()
        self.__configPreviousButton()
        self.__configNextButton()


    def __configTop(self):
        self.__top.title('Pokedex')
        self.__top.minsize(width=self.__top.winfo_screenwidth() ,height=self.__top.winfo_screenheight())
        self.__top.configure(background=self.__background)
        
        
    def __configPokeList(self):
        self.__name = StringVar()
        db = DatabaseManager()
        data = db.getPokemonsByDexNum()
        self.__OPTIONS = data
        self.__name.set(self.__OPTIONS[0])
        self.__name.trace("w",lambda *args: self.__changePokemon(self.__name,*args))
        listbox = OptionMenu(self.__top,self.__name,*self.__OPTIONS)
        listbox.pack()
        
    def __configDexShow(self,name):
        try:
            if(self.__l):
                self.__l.pack_forget()
                self.__next.pack_forget()
                self.__previous.pack_forget()
                self.__error.pack_forget()
                self.__l = DexShow(self.__top,name)
                self.__l.pack()
                self.__next.pack(side = RIGHT)
                self.__previous.pack(side = LEFT)
                self.__error.pack()
        except AttributeError:
            pass
            self.__l = DexShow(self.__top,name)
            self.__l.pack()
        
    def __changePokemon(self,value,*args):
        data = self.__name.get().strip('()').split(',')
        data[0] = int(data[0])
        data[1] = data[1].strip(' \'')
        self.__configDexShow(data[1])
        
    def __configErrorLog(self):
        self.__error = Button(self.__top,text='Add Error',command = self.__errorLog)
        self.__error.pack()
    
    def __configPreviousButton(self):
        self.__previous = Button(self.__top,text='Previous',command = self.__goToPrevious)
        self.__previous.pack(side = LEFT)
    
    def __configNextButton(self):
        self.__next = Button(self.__top,text='Next',command = self.__goToNext)
        self.__next.pack(side = RIGHT)

    def __errorLog(self):
        errorLog = MyDialog(self.__top)

    def __goToPrevious(self):
        data = self.__name.get().strip('()').split(',')
        data[0] = int(data[0])
        data[1] = data[1].strip(' \'')
        index = self.__OPTIONS.index(tuple(data))
        if(index>0):
            next = self.__OPTIONS[index-1][1]
            self.__name.set(self.__OPTIONS[index-1])
        
    def __goToNext(self):
        data = self.__name.get().strip('()').split(',')
        data[0] = int(data[0])
        data[1] = data[1].strip(' \'')
        index = self.__OPTIONS.index(tuple(data))
        if(index<720):
            next = self.__OPTIONS[index+1][1]
            self.__name.set(self.__OPTIONS[index+1])
        
    def run(self):
        self.__top.mainloop()
        
if __name__ == '__main__':
    mainApplication().run()
        
