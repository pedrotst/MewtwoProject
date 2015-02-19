from tkinter import *
from pokemon import *
    
class DexShow:
    def __init__(self,PokemonName):
        
        self.__background = 'LightSteelBlue4'
        self.__pokemon = Pokemon(PokemonName)
        
        
        self.__config()
        #self.__loadData()

    def __config(self):
        self.__top = Tk()
        self.__configTop()
        self.__configTitle()
        self.__configPokeImg()
        self.__configPokeImgShinny()
        self.__configName()
        self.__configHeight()
        self.__configWeight()
        self.__configClassification()
        self.__configType()
        self.__configNo()
        self.__configGender()

    def __configTop(self):
        self.__top.title('Pokédex')
        self.__top.minsize(width=1440,height=720)
        self.__top.configure(background=self.__background)

    def __configTitle(self):
        self.__name = StringVar()

        f = ('Helvetica',36,'bold')
        self.__labelTitle = Label(self.__top,textvariable = self.__name,font=f,bg = self.__background)
        self.__labelTitle.grid(row = 0, column =0, columnspan = 2)

    def __configPokeImg(self):
        self.__pokeImgPath = self.__pokemon.getImagePath().getPathImg()
        self.__pokeImg = PhotoImage(file = self.__pokeImgPath)  
        imgHeight = self.__pokeImg.height()
        imgWidth = self.__pokeImg.width()

        self.__pokeImgCanvas = Canvas(self.__top,bg='LightSteelBlue3',height=imgHeight,width=imgWidth)
        self.__pokeImgCanvas.grid(row = 1, column = 0,rowspan=4)
        self.__pokeImgCanvas.configure(highlightbackground='black')
        
        self.__pokeImgCanvas.create_image(0,0,anchor = NW, image = self.__pokeImg)

    def __configPokeImgShinny(self):
        self.__pokeImgShinnyPath = self.__pokemon.getImagePath().getSPathImg()
        self.__pokeImgShinny = PhotoImage(file = self.__pokeImgShinnyPath)
        imgHeight = self.__pokeImgShinny.height()
        imgWidth = self.__pokeImgShinny.width()

        self.__pokeImgShinnyCanvas = Canvas(self.__top,bg='LightSteelBlue3',height=imgHeight,width=imgWidth)
        self.__pokeImgShinnyCanvas.grid(row = 1, column = 1,rowspan=4)
        self.__pokeImgShinnyCanvas.configure(highlightbackground='black')


        self.__pokeImgShinnyCanvas.create_image(0,0,anchor = NW, image = self.__pokeImgShinny)


    def __configName(self):
        ##Make label
        self.__labelName = Label(self.__top,text = 'Name: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelName.grid(row = 1, column =2,sticky=E)
        ##Make info
        self.__labelNameInfo = Label(self.__top,textvariable = self.__name,bg = self.__background,font = ('Helvetica',12))
        self.__labelNameInfo.grid(row = 1, column = 3,sticky=W)

        self.__name.set(self.__pokemon.getName())
        

    def __configHeight(self):
        ##Make label
        self.__labelHeight = Label(self.__top,text = 'Height: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelHeight.grid(row = 2, column =2,sticky=E)
        ##Make info
        self.__height = StringVar()
        self.__labelHeightInfo = Label(self.__top,textvariable = self.__height,bg = self.__background,font = ('Helvetica',12))
        self.__labelHeightInfo.grid(row = 2, column = 3,sticky=W)

        self.__height.set(str(self.__pokemon.getHeight()))
        
    def __configWeight(self):
        ##Make label
        self.__labelWeight = Label(self.__top,text = 'Weight: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelWeight.grid(row = 3, column =2,sticky=E)
        ##Make info
        self.__weight = StringVar()
        self.__labelWeightInfo = Label(self.__top,textvariable = self.__weight,bg = self.__background,font = ('Helvetica',12))
        self.__labelWeightInfo.grid(row = 3, column = 3,sticky=W)

        self.__weight.set(str(self.__pokemon.getWeight()))
    
    def __configClassification(self):
        ##Make label
        self.__labelClassification = Label(self.__top,text = 'Classification: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelClassification.grid(row = 4, column =2,sticky=E)
        ##Make info
        self.__classification = StringVar()
        self.__labelClassificationInfo = Label(self.__top,textvariable = self.__classification,bg = self.__background,font = ('Helvetica',12))
        self.__labelClassificationInfo.grid(row = 4, column = 3,sticky=W)

        self.__classification.set(self.__pokemon.getClassification())

    def __configType(self):
        ##Make label
        self.__labelType = Label(self.__top,text = 'Type: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelType.grid(row = 1, column =4,sticky=W)
        ##Make info
        
    def __configNo(self):
        pass
    
    def __configGender(self):
        pass
    
    def run(self):
        self.__top.mainloop()
