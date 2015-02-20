from tkinter import *
from pokemon import *
        
class DexShow(LabelFrame):
    def __init__(self,top,PokemonName):
        LabelFrame.__init__(self,top)
        self.__background = 'gray21'
        self.__pokemon = Pokemon(PokemonName)
        
        
        self.__config()
        #self.__loadData()

    def __config(self):
        self.__top = self
        self.__configTop()
        self.__configTitle()
        
        self.__configPokeImg()
        self.__configPokeImgShinny()

        self.__configBasicInfo()
        
        self.__configBreedingInfo()
        
        self.__configTrainingInfo1()
        
        self.__configTrainingInfo2()
        
        self.__configBattleInfo()


    def __configTop(self):
        self.__top.configure(background=self.__background)

    def __configBasicInfo(self):
        self.__BasicInfo = LabelFrame(self.__top,background = 'gray21')
        self.__BasicInfo.grid(row = 1,column = 2,rowspan = 4,columnspan = 4, padx = 20,pady = 5,sticky = NSEW)
        self.__BasicInfo.configure(highlightthickness = 2,highlightbackground = 'Black', text = 'Basic Info')

        self.__configName()
        self.__configHeight()
        self.__configWeight()
        self.__configClassification()
        self.__configType()
        self.__configNo()
        self.__configGender()
        self.__configDexText()
        

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

        self.__pokeImgCanvas = Canvas(self.__top,bg='gray24',height=imgHeight,width=imgWidth)
        self.__pokeImgCanvas.grid(row = 1, column = 0,rowspan=2,padx = 5,pady = 5)
        self.__pokeImgCanvas.configure(highlightbackground='black')
        
        self.__pokeImgCanvas.create_image(0,0,anchor = NW, image = self.__pokeImg)

    def __configPokeImgShinny(self):
        self.__pokeImgShinnyPath = self.__pokemon.getImagePath().getSPathImg()
        self.__pokeImgShinny = PhotoImage(file = self.__pokeImgShinnyPath)
        imgHeight = self.__pokeImgShinny.height()
        imgWidth = self.__pokeImgShinny.width()

        self.__pokeImgShinnyCanvas = Canvas(self.__top,bg='gray24',height=imgHeight,width=imgWidth)
        self.__pokeImgShinnyCanvas.grid(row = 1, column = 1,rowspan=2,padx = 5,pady = 5)
        self.__pokeImgShinnyCanvas.configure(highlightbackground='black')


        self.__pokeImgShinnyCanvas.create_image(0,0,anchor = NW, image = self.__pokeImgShinny)


    def __configName(self):
        ##Make label
        self.__labelName = Label(self.__BasicInfo,text = 'Name: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelName.grid(row = 0, column =0,sticky=NSEW)
        ##Make info
        self.__labelNameInfo = Label(self.__BasicInfo,textvariable = self.__name,bg = self.__background,font = ('Helvetica',10))
        self.__labelNameInfo.grid(row = 0, column = 1,sticky=NSEW)

        self.__name.set(self.__pokemon.getName())
        

    def __configClassification(self):
        ##Make label
        self.__labelClassification = Label(self.__BasicInfo,text = 'Classification: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelClassification.grid(row = 1, column =0,sticky=NSEW)
        ##Make info
        self.__classification = StringVar()
        self.__labelClassificationInfo = Label(self.__BasicInfo,textvariable = self.__classification,bg = self.__background,font = ('Helvetica',10))
        self.__labelClassificationInfo.grid(row = 1, column = 1,sticky=NSEW)

        self.__classification.set(self.__pokemon.getClassification())


    def __configHeight(self):
        ##Make label
        self.__labelHeight = Label(self.__BasicInfo,text = 'Height: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelHeight.grid(row = 0, column =2,sticky=NSEW)
        ##Make info
        self.__height = StringVar()
        self.__labelHeightInfo = Label(self.__BasicInfo,textvariable = self.__height,bg = self.__background,font = ('Helvetica',10))
        self.__labelHeightInfo.grid(row = 0, column = 3,sticky=NSEW)

        self.__height.set(str(self.__pokemon.getHeight()))
        
    def __configWeight(self):
        ##Make label
        self.__labelWeight = Label(self.__BasicInfo,text = 'Weight: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelWeight.grid(row = 1, column =2,sticky=NSEW)
        ##Make info
        self.__weight = StringVar()
        self.__labelWeightInfo = Label(self.__BasicInfo,textvariable = self.__weight,bg = self.__background,font = ('Helvetica',10))
        self.__labelWeightInfo.grid(row = 1, column = 3,sticky=NSEW)

        self.__weight.set(str(self.__pokemon.getWeight()))
    

    def __configType(self):
        ##Make label
        self.__labelType = Label(self.__BasicInfo,text = 'Type: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelType.grid(row = 0, column =4,sticky=NSEW)
        ##Make info
        types = self.__pokemon.getTypes()
        ##If Two Types
        if types.getType2() != Type.NoType:
            self.__type1Img = PhotoImage(file = types.getType1().ImgH())
            self.__type2Img = PhotoImage(file = types.getType2().ImgH())
            imgHeight = self.__type1Img.height()
            imgWidth = self.__type1Img.width()
            
            self.__type1Canvas = Canvas(self.__BasicInfo,bg='LightSteelBlue3',height=2*imgHeight,width=imgWidth)
            self.__type1Canvas.grid(row = 0, column = 5)
            self.__type1Canvas.configure(highlightthickness=0)


            self.__type1Canvas.create_image(0,0,anchor = NW, image = self.__type1Img)
            self.__type1Canvas.create_image(0,imgHeight,anchor = NW, image = self.__type2Img)
            
            
            

        ##If Only One Type    
        else:
            self.__type1Img = PhotoImage(file = types.getType1().ImgH())
            imgHeight = self.__type1Img.height()
            imgWidth = self.__type1Img.width()
            
            self.__type1Canvas = Canvas(self.__BasicInfo,bg='LightSteelBlue3',height=imgHeight,width=imgWidth)
            self.__type1Canvas.grid(row = 0, column = 5)
            self.__type1Canvas.configure(highlightthickness=0)


            self.__type1Canvas.create_image(0,0,anchor = NW, image = self.__type1Img)
       
    def __configGender(self):
         ##Make label
        self.__labelGender = Label(self.__BasicInfo,text = 'Gender: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelGender.grid(row = 1, column =4,sticky=NSEW)
        
        ##Make info
        self.__gender = StringVar()
        self.__labelGenderInfo = Label(self.__BasicInfo,textvariable = self.__gender,bg = self.__background,font = ('Helvetica',10))
        
        self.__labelGenderInfo.grid(row = 1, column =5)
        
        self.__gender.set(self.__pokemon.getGender())
       
        
    def __configNo(self):
        ##Make label
        self.__labelNo = Label(self.__BasicInfo,text = 'Dex No: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelNo.grid(row = 0, column =6,rowspan = 2,sticky=NSEW)
    
        ##Make frame for dexNums    
        self.__NoFrame = Frame(self.__BasicInfo,background = self.__background)
        ##Label For Each Num
        self.__labelNational = Label(self.__NoFrame,text = 'National: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelCentral = Label(self.__NoFrame,text = 'Central: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelCoastal = Label(self.__NoFrame,text = 'Coastal: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelMontain = Label(self.__NoFrame,text = 'Montain: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelHoenn = Label(self.__NoFrame,text = 'Hoenn: ',bg = self.__background,font = ('Helvetica',12))
        ##Positioning inside NoFrame
        self.__labelNational.grid(row = 0,sticky = NSEW)
        self.__labelCentral.grid(row = 1,sticky = NSEW)
        self.__labelCoastal.grid(row = 2,sticky = NSEW)
        self.__labelMontain.grid(row = 3,sticky = NSEW)
        self.__labelHoenn.grid(row = 4,sticky = NSEW)
        ##Positioning NoFrame
        self.__NoFrame.grid(row = 0, column = 7, rowspan = 2)
        
        ##Make info
        self.__nationalNum = StringVar()
        self.__centralNum = StringVar()
        self.__coastalNum = StringVar()
        self.__mountainNum = StringVar()
        self.__hoennNum = StringVar()
        
        self.__labelNationalInfo = Label(self.__NoFrame,textvariable = self.__nationalNum,bg = self.__background,font = ('Helvetica',10))
        self.__labelCentralInfo = Label(self.__NoFrame,textvariable = self.__centralNum,bg = self.__background,font = ('Helvetica',10))
        self.__labelCoastalInfo = Label(self.__NoFrame,textvariable = self.__coastalNum,bg = self.__background,font = ('Helvetica',10))
        self.__labelMontainInfo = Label(self.__NoFrame,textvariable = self.__mountainNum,bg = self.__background,font = ('Helvetica',10))
        self.__labelHoennInfo = Label(self.__NoFrame,textvariable = self.__hoennNum,bg = self.__background,font = ('Helvetica',10))
        
        ##Positioning inside NoFrame
        self.__labelNationalInfo.grid(row = 0,column = 1,sticky = NSEW)
        self.__labelCentralInfo.grid(row = 1,column = 1,sticky = NSEW)
        self.__labelCoastalInfo.grid(row = 2,column = 1,sticky = NSEW)
        self.__labelMontainInfo.grid(row = 3,column = 1,sticky = NSEW)
        self.__labelHoennInfo.grid(row = 4,column = 1,sticky = NSEW)
        
        self.__nationalNum.set(self.__pokemon.getDexNum().getNational())
        self.__centralNum.set(self.__pokemon.getDexNum().getCentral())
        self.__coastalNum.set(self.__pokemon.getDexNum().getCoastal())
        self.__mountainNum.set(self.__pokemon.getDexNum().getMountain())
        self.__hoennNum.set(self.__pokemon.getDexNum().getHoenn())
        

    def __configDexText(self):
        
        ##DexText Frame
        self.__dexTextFrame = LabelFrame(self.__BasicInfo,text = 'Pokédex Text: ',background = self.__background)
        ##Label for each Dex text
        self.__LabelDexTextX = Label(self.__dexTextFrame,text = 'X: ',bg = self.__background,font = ('Helvetica',12))
        self.__LabelDexTextY = Label(self.__dexTextFrame,text = 'Y: ',bg = self.__background,font = ('Helvetica',12))
        self.__LabelDexTextOR = Label(self.__dexTextFrame,text = '\u03A9 Ruby: ',bg = self.__background,font = ('Helvetica',12))
        self.__LabelDexTextAS = Label(self.__dexTextFrame,text = '\u03B1 Shappire: ',bg = self.__background,font = ('Helvetica',12))
        
        ##Positioning inside dexTextFrame
        self.__LabelDexTextX.grid(row = 0,column = 0,sticky = NSEW)
        self.__LabelDexTextY.grid(row = 1,column = 0,sticky = NSEW) 
        self.__LabelDexTextOR.grid(row = 0,column = 2,sticky = NSEW)
        self.__LabelDexTextAS.grid(row = 1,column = 2,sticky = NSEW)
        
        ##Make info for each Dex text
        self.__dexTextX = StringVar()
        self.__dexTextY = StringVar()
        self.__dexTextOR = StringVar()
        self.__dexTextAS = StringVar()
        
        wl = 300
        
        self.__LabelDexTextXInfo = Label(self.__dexTextFrame,textvariable = self.__dexTextX, wraplength= wl ,bg = self.__background,font = ('Helvetica',9))
        self.__LabelDexTextYInfo = Label(self.__dexTextFrame,textvariable = self.__dexTextY, wraplength= wl,bg = self.__background,font = ('Helvetica',9))
        self.__LabelDexTextORInfo = Label(self.__dexTextFrame,textvariable = self.__dexTextOR, wraplength= wl,bg = self.__background,font = ('Helvetica',9))
        self.__LabelDexTextASInfo = Label(self.__dexTextFrame,textvariable = self.__dexTextAS, wraplength= wl,bg = self.__background,font = ('Helvetica',9))
        
        ##Positioning inside dexTextFrame
        self.__LabelDexTextXInfo.grid(row = 0,column = 1,sticky = NSEW)
        self.__LabelDexTextYInfo.grid(row = 1,column = 1,sticky = NSEW) 
        self.__LabelDexTextORInfo.grid(row = 0,column = 3,sticky = NSEW)
        self.__LabelDexTextASInfo.grid(row = 1,column = 3,sticky = NSEW)
        
        ##Positioning NoFrame
        self.__dexTextFrame.grid(row = 2, column = 0, columnspan = 8)
        
        self.__dexTextX.set(self.__pokemon.getDexText().getX())
        self.__dexTextY.set(self.__pokemon.getDexText().getY())
        self.__dexTextOR.set(self.__pokemon.getDexText().getOR())
        if(self.__pokemon.getDexText().getAS()):
            self.__dexTextAS.set(self.__pokemon.getDexText().getAS())
        else:
            self.__dexTextAS.set(self.__pokemon.getDexText().getOR())
            
            
    def __configBreedingInfo(self):
        self.__BreedingInfo = LabelFrame(self.__top,background = 'gray21')
        self.__BreedingInfo.grid(row = 3,column = 0,columnspan = 2, padx = 20,pady = 5, sticky = NSEW)
        self.__BreedingInfo.configure(highlightthickness = 2,highlightbackground = 'Black', text = 'Breeding Info')
        
        self.__configBaseEggSteps()
        self.__configEggGroups()
        
        
    def __configBaseEggSteps(self):
        ##Make label
        self.__labelBaseEggSteps = Label(self.__BreedingInfo,text = 'BaseEggSteps: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelBaseEggSteps.grid(row = 0, column =0,sticky=NSEW)
        ##Make info
        self.__baseEggSteps = StringVar()
        self.__labelBaseEggStepsInfo = Label(self.__BreedingInfo,textvariable = self.__baseEggSteps,bg = self.__background,font = ('Helvetica',10))
        self.__labelBaseEggStepsInfo.grid(row = 0, column = 1,sticky=NSEW)

        self.__baseEggSteps.set(self.__pokemon.getBaseEggSteps())
        
    def __configEggGroups(self):
        ##Make label
        self.__labelEggGroups = Label(self.__BreedingInfo,text = 'EggGroups: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelEggGroups.grid(row = 0, column =2,sticky=NSEW)
        ##Make info
        self.__eggGroups = StringVar()
        self.__labelEggGroupsInfo = Label(self.__BreedingInfo,textvariable = self.__eggGroups,bg = self.__background,font = ('Helvetica',10))
        self.__labelEggGroupsInfo.grid(row = 0, column = 3,sticky=NSEW)

        self.__eggGroups.set(self.__pokemon.getEggGroups())
        
    def __configTrainingInfo1(self):
        self.__TrainingInfo1 = LabelFrame(self.__top,background = 'gray21')
        self.__TrainingInfo1.grid(row = 4,column = 0,columnspan = 2, padx = 20,pady = 5,sticky = NSEW)
        self.__TrainingInfo1.configure(highlightthickness = 2,highlightbackground = 'Black', text = 'Training Info 1')
        
        self.__configEVWorth()
        self.__configCaptureRate()
        self.__configExpGrowth()
        self.__configBaseHappiness()
        
    def __configEVWorth(self):
        ##Make label
        self.__labelEVWorth = Label(self.__TrainingInfo1,text = 'EV Worth: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelEVWorth.grid(row = 0, column =0,sticky=NSEW)
        ##Make info
        self.__evWorth = StringVar()
        self.__labelEVWorthInfo = Label(self.__TrainingInfo1,textvariable = self.__evWorth,bg = self.__background,font = ('Helvetica',10))
        self.__labelEVWorthInfo.grid(row = 0, column = 1,sticky=NSEW)

        self.__evWorth.set(self.__pokemon.getEVWorth())
        
    def __configCaptureRate(self):
        ##Make label
        self.__labelCaptureRate = Label(self.__TrainingInfo1,text = 'Capture Rate: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelCaptureRate.grid(row = 0, column =2,sticky=NSEW)
        ##Make info
        self.__captureRate = StringVar()
        self.__labelCaptureRateInfo = Label(self.__TrainingInfo1,textvariable = self.__captureRate,bg = self.__background,font = ('Helvetica',10))
        self.__labelCaptureRateInfo.grid(row = 0, column = 3,sticky=NSEW)

        self.__captureRate.set(self.__pokemon.getCaptureRate())
        
    def __configExpGrowth(self):
        ##Make label
        self.__labelExpGrowth = Label(self.__TrainingInfo1,text = 'Exp: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelExpGrowth.grid(row = 1, column =0,sticky=NSEW)
        ##Make info
        self.__expGrowth = StringVar()
        self.__labelExpGrowthInfo = Label(self.__TrainingInfo1,textvariable = self.__expGrowth,bg = self.__background,font = ('Helvetica',10))
        self.__labelExpGrowthInfo.grid(row = 1, column = 1,sticky=NSEW)

        self.__expGrowth.set(self.__pokemon.getExpGrowth())
        
    def __configBaseHappiness(self):
        ##Make label
        self.__labelBaseHappiness = Label(self.__TrainingInfo1,text = 'Base Happiness: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelBaseHappiness.grid(row = 1, column =2,sticky=NSEW)
        ##Make info
        self.__baseHappiness = StringVar()
        self.__labelBaseHappinessInfo = Label(self.__TrainingInfo1,textvariable = self.__baseHappiness,bg = self.__background,font = ('Helvetica',10))
        self.__labelBaseHappinessInfo.grid(row = 1, column = 3,sticky=NSEW)

        self.__baseHappiness.set(self.__pokemon.getHappiness())
            
            
    def __configTrainingInfo2(self):
        self.__TrainingInfo2 = LabelFrame(self.__top,background = 'gray21')
        self.__TrainingInfo2.grid(row = 5,column = 0,columnspan = 6, padx = 20,pady = 5,sticky = NSEW)
        self.__TrainingInfo2.configure(highlightthickness = 2,highlightbackground = 'Black', text = 'Training Info 2')
        
        self.__configWildItems()
        self.__configLocation()
        self.__configEvoChain()
        
    def __configWildItems(self):
        ##Make label
        self.__labelWildItems = Label(self.__TrainingInfo2,text = 'Wild Items: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelWildItems.grid(row = 0, column =0,sticky=NSEW)
        ##Make info
        self.__wildItems = StringVar()
        self.__labelWildItemsInfo = Label(self.__TrainingInfo2,textvariable = self.__wildItems,bg = self.__background,font = ('Helvetica',10))
        self.__labelWildItemsInfo.grid(row = 0, column = 1,sticky=NSEW)

        self.__wildItems.set(self.__pokemon.getWildItems())
    
    def __configLocation(self):
        ##Location Frame
        self.__locationFrame = LabelFrame(self.__TrainingInfo2,text = 'Location: ',background = self.__background)
        ##Label for each Dex text
        self.__LabelLocationX = Label(self.__locationFrame,text = 'X: ',bg = self.__background,font = ('Helvetica',12))
        self.__LabelLocationY = Label(self.__locationFrame,text = 'Y: ',bg = self.__background,font = ('Helvetica',12))
        self.__LabelLocationOR = Label(self.__locationFrame,text = '\u03A9 Ruby: ',bg = self.__background,font = ('Helvetica',12))
        self.__LabelLocationAS = Label(self.__locationFrame,text = '\u03B1 Shappire: ',bg = self.__background,font = ('Helvetica',12))
        
        ##Positioning inside locationFrame
        self.__LabelLocationX.grid(row = 0,column = 0,sticky = NSEW)
        self.__LabelLocationY.grid(row = 1,column = 0,sticky = NSEW) 
        self.__LabelLocationOR.grid(row = 0,column = 2,sticky = NSEW)
        self.__LabelLocationAS.grid(row = 1,column = 2,sticky = NSEW)
        
        ##Make info for each Dex text
        self.__locationX = StringVar()
        self.__locationY = StringVar()
        self.__locationOR = StringVar()
        self.__locationAS = StringVar()
        
        wl = 300
        
        self.__LabelLocationXInfo = Label(self.__locationFrame,textvariable = self.__locationX, wraplength= wl ,bg = self.__background,font = ('Helvetica',9))
        self.__LabelLocationYInfo = Label(self.__locationFrame,textvariable = self.__locationY, wraplength= wl,bg = self.__background,font = ('Helvetica',9))
        self.__LabelLocationORInfo = Label(self.__locationFrame,textvariable = self.__locationOR, wraplength= wl,bg = self.__background,font = ('Helvetica',9))
        self.__LabelLocationASInfo = Label(self.__locationFrame,textvariable = self.__locationAS, wraplength= wl,bg = self.__background,font = ('Helvetica',9))
        
        ##Positioning inside locationFrame
        self.__LabelLocationXInfo.grid(row = 0,column = 1,sticky = NSEW)
        self.__LabelLocationYInfo.grid(row = 1,column = 1,sticky = NSEW) 
        self.__LabelLocationORInfo.grid(row = 0,column = 3,sticky = NSEW)
        self.__LabelLocationASInfo.grid(row = 1,column = 3,sticky = NSEW)
        
        ##Positioning NoFrame
        self.__locationFrame.grid(row = 0, column = 2,columnspan = 2,sticky = NSEW, padx = 10)
        
        self.__locationX.set(self.__pokemon.getLocation().getX())
        self.__locationY.set(self.__pokemon.getLocation().getY())
        self.__locationOR.set(self.__pokemon.getLocation().getOR())
        if(self.__pokemon.getLocation().getAS()):
            self.__locationAS.set(self.__pokemon.getLocation().getAS())
        else:
            self.__locationAS.set(self.__pokemon.getLocation().getOR())

    def __configEvoChain(self):
        ##Make label
        self.__labelEvoChain = Label(self.__TrainingInfo2,text = 'Evo Chain: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelEvoChain.grid(row = 0, column =4,sticky=NSEW)
        ##Make info
        self.__evoChain = StringVar()
        self.__labelEvoChainInfo = Label(self.__TrainingInfo2,textvariable = self.__evoChain,bg = self.__background,font = ('Helvetica',10))
        self.__labelEvoChainInfo.grid(row = 0, column = 5,sticky=NSEW)

        self.__evoChain.set(self.__pokemon.getEvoChain())

    def __configBattleInfo(self):
        self.__BattleInfo = LabelFrame(self.__top,background = 'gray21')
        self.__BattleInfo.grid(row = 6,column = 0,columnspan = 6, padx = 20,pady = 5,sticky = NSEW)
        self.__BattleInfo.configure(highlightthickness = 2,highlightbackground = 'Black', text = 'Battle Info')
        
        self.__configAbilities()
        self.__configAttacks()
        self.__configWeaknesses()
        self.__configStats()
        self.__skyBattle()
        
    def __configAbilities(self):
        ##Make info
        self.__abilities = StringVar()
        self.__frameAbilities = LabelFrame(self.__BattleInfo,text='Abilities')
        self.__scrollAbilities = Scrollbar(self.__frameAbilities)
        self.__scrollAbilities.pack(side=RIGHT,fill=Y)
        self.__labelAbilitiesInfo = Text(self.__frameAbilities,bg = self.__background,font = ('Helvetica',9),yscrollcommand=self.__scrollAbilities.set,width=40,height=5)
        self.__labelAbilitiesInfo.pack(side=LEFT,fill=BOTH)
        
        self.__abilities.set(self.__pokemon.getAbilities())
        self.__labelAbilitiesInfo.insert(INSERT,self.__abilities.get())
        
        self.__labelAbilitiesInfo.config(state = DISABLED)
        
        self.__scrollAbilities.config(command=self.__labelAbilitiesInfo.yview)
        self.__frameAbilities.grid(row = 0, column = 0,columnspan=8,sticky=NSEW)
        
    def __configAttacks(self):
        ##Make info
        self.__attack = StringVar()
        self.__frameAttacks = LabelFrame(self.__BattleInfo,text='Attacks')
        self.__scrollAttacks = Scrollbar(self.__frameAttacks)
        self.__scrollAttacks.pack(side=RIGHT,fill=Y)
        self.__labelAttacksInfo = Text(self.__frameAttacks,bg = self.__background,font = ('Helvetica',9),yscrollcommand=self.__scrollAttacks.set,width=40,height=5)
        self.__labelAttacksInfo.pack(side=LEFT,fill=BOTH)
        
        self.__attack.set(self.__pokemon.getAttacks())
        self.__labelAttacksInfo.insert(INSERT,self.__attack.get())
        
        self.__labelAttacksInfo.config(state = DISABLED)
        
        self.__scrollAttacks.config(command=self.__labelAttacksInfo.yview)
        self.__frameAttacks.grid(row = 0, column = 8,columnspan=8,sticky=NSEW)
        
    def __configWeaknesses(self):
        self.__frameWeaknesses = LabelFrame(self.__BattleInfo,text='weaknesses')
        self.__typeImg = []
        self.__typeCanvas = []
        self.__typeDmg = []
        self.__typeDmgInfo = []
        for i in range(1,17):
            type_ = Type(i)
            self.__typeImg.append(PhotoImage(file = type_.ImgV()))
            self.__typeDmg.append(StringVar())

            self.__typeDmgInfo.append(Label(self.__BattleInfo,textvariable = self.__typeDmg[i-1],bg = self.__background,font = ('Helvetica',12)))
            
            self.__typeDmg[i-1].set(self.__pokemon.getWeaknesses()[Type(i)])
            

            imgHeight = self.__typeImg[i-1].height()
            imgWidth = self.__typeImg[i-1].width()
            
            self.__typeCanvas.append(Canvas(self.__BattleInfo,bg='LightSteelBlue3',height=imgHeight,width=imgWidth))
            
            self.__typeCanvas[i-1].configure(highlightthickness=0)
            self.__typeCanvas[i-1].create_image(0,0,anchor = NW, image = self.__typeImg[i-1])
    
            self.__typeCanvas[i-1].grid(row = 1, column = i-1)
            self.__typeDmgInfo[i-1].grid(row = 2, column = i-1)
            
    def __configStats(self):
         ##Make info
        self.__attack = StringVar()
        self.__frameStats = LabelFrame(self.__BattleInfo,text='Stats',background=self.__background)
        self.__frameStats.grid(row = 0,column = 16,columnspan = 2,padx= 10,sticky = NSEW)
        
        self.__labelHp = Label(self.__frameStats,text = 'Hp:',bg = self.__background,font = ('Helvetica',12))
        self.__labelAttack = Label(self.__frameStats,text = 'Attack:',bg = self.__background,font = ('Helvetica',12))
        self.__labelDefense = Label(self.__frameStats,text = 'Defense:',bg = self.__background,font = ('Helvetica',12))
        self.__labelSpAttack = Label(self.__frameStats,text = 'Sp Attack:',bg = self.__background,font = ('Helvetica',12))
        self.__labelSpDefense = Label(self.__frameStats,text = 'Sp Defense:',bg = self.__background,font = ('Helvetica',12))
        self.__labelSpeed = Label(self.__frameStats,text = 'Speed:',bg = self.__background,font = ('Helvetica',12))
        self.__labelTotal = Label(self.__frameStats,text = 'Total:',bg = self.__background,font = ('Helvetica',12))
        
        self.__labelHp.grid(row = 0,column=0,sticky=NSEW) 
        self.__labelAttack.grid(row = 0,column=1,sticky=NSEW) 
        self.__labelDefense.grid(row = 0,column=2,sticky=NSEW)
        self.__labelSpAttack.grid(row = 0,column=3,sticky=NSEW)
        self.__labelSpDefense.grid(row = 0,column=4,sticky=NSEW)
        self.__labelSpeed.grid(row = 0,column=5,sticky=NSEW)
        self.__labelTotal.grid(row = 0,column=6,sticky=NSEW)
        
        self.__hp = StringVar()
        self.__attack = StringVar()
        self.__defense = StringVar()
        self.__spAttack = StringVar()
        self.__spDefense = StringVar()
        self.__speed = StringVar()
        self.__total = StringVar()
        
        self.__labelHpInfo = Label(self.__frameStats,textvariable = self.__hp,bg = self.__background,font = ('Helvetica',12))
        self.__labelAttackInfo = Label(self.__frameStats,textvariable = self.__attack,bg = self.__background,font = ('Helvetica',12))
        self.__labelDefenseInfo = Label(self.__frameStats,textvariable = self.__defense,bg = self.__background,font = ('Helvetica',12))
        self.__labelSpAttackInfo = Label(self.__frameStats,textvariable = self.__spAttack,bg = self.__background,font = ('Helvetica',12))
        self.__labelSpDefenseInfo = Label(self.__frameStats,textvariable = self.__spDefense,bg = self.__background,font = ('Helvetica',12))
        self.__labelSpeedInfo = Label(self.__frameStats,textvariable = self.__speed,bg = self.__background,font = ('Helvetica',12))
        self.__labelTotalInfo = Label(self.__frameStats,textvariable = self.__total,bg = self.__background,font = ('Helvetica',12))
        
        self.__labelHpInfo.grid(row = 1,column=0,sticky=NSEW) 
        self.__labelAttackInfo.grid(row = 1,column=1,sticky=NSEW) 
        self.__labelDefenseInfo.grid(row = 1,column=2,sticky=NSEW)
        self.__labelSpAttackInfo.grid(row = 1,column=3,sticky=NSEW)
        self.__labelSpDefenseInfo.grid(row = 1,column=4,sticky=NSEW)
        self.__labelSpeedInfo.grid(row = 1,column=5,sticky=NSEW)
        self.__labelTotalInfo.grid(row = 1,column=6,sticky=NSEW)
        
        self.__hp.set(self.__pokemon.getStats().getHp())
        self.__attack.set(self.__pokemon.getStats().getAttack())
        self.__defense.set(self.__pokemon.getStats().getDefense())
        self.__spAttack.set(self.__pokemon.getStats().getSpAttack())
        self.__spDefense.set(self.__pokemon.getStats().getSpDefense())
        self.__speed.set(self.__pokemon.getStats().getSpeed())
        self.__total.set(self.__pokemon.getStats().getTotal())
    
    def __skyBattle(self):
        ##Make label
        self.__labelSkyBattle = Label(self.__BattleInfo,text = 'Is Elegible to Sky Battle?: ',bg = self.__background,font = ('Helvetica',12))
        self.__labelSkyBattle.grid(row = 1, column =16,sticky=NSEW)
        ##Make info
        self.__skyBattle = StringVar()
        self.__labelSkyBattleInfo = Label(self.__BattleInfo,textvariable = self.__skyBattle,bg = self.__background,font = ('Helvetica',10))
        self.__labelSkyBattleInfo.grid(row = 1, column = 17,sticky=NSEW)

        self.__skyBattle.set(self.__pokemon.getSkyBattle())

if __name__ == '__main__':
    DexShow('Pikachu').run()
