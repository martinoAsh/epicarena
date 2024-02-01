import tkinter as tk
import json
import random


GLOBAL_MaxDeckSize = 8
GLOBAL_MaxActiveUnits = 4

#------------------------------------------------------------------------------
class Unit:
#------------------------------------------------------------------------------
    def __init__(self, categoryNr, unitNr, count, isActive):
        self.categoryNr = categoryNr
        self.unitNr = unitNr
        self.categoryName = ""
        self.unitName = ""
        self.tier = 0
        self.isActive = isActive
        self.lookUpAndSetNames()
        self.count = count

    #------------------------------
    def lookUpAndSetNames(self):
    #------------------------------
        file = open("unitList.json")
        unitData = json.load(file)
        self.categoryName = unitData['categories'][self.categoryNr]['name']
        self.unitName = unitData['categories'][self.categoryNr]['units'][self.unitNr]['name']
        self.tier = unitData['categories'][self.categoryNr]['units'][self.unitNr]['tier']

    #------------------------------
    def printStats(self):
    #------------------------------
        print(self.unitName + 
                " ("+ self.categoryName + ")"
                ", Count: " + str(self.count) + 
                ", Active: " + str(self.isActive) + ", Tier: " + str(self.tier))

#------------------------------------------------------------------------------
class Player:
#------------------------------------------------------------------------------
    def __init__(self, name):
        self.name = name
        self.deck=[]
        self.score = 0
        self.maxDeckLen = GLOBAL_MaxDeckSize
        self.maxActiveUnits = GLOBAL_MaxActiveUnits
        self.unitList = []
        self.canEvolve = False
        self.parseUnitList()

    #------------------------------
    # Parses all units of the json file and saves them in unitList
    #------------------------------
    def parseUnitList(self):
    #------------------------------
        file = open("unitList.json")
        unitData = json.load(file)
        for categoryIndex in range(len(unitData['categories'])):
            self.unitList.append((len(unitData['categories'][categoryIndex]['units'])))
        print(self.unitList)


    #------------------------------
    def addUnit(self, newUnit):
    #------------------------------

        if len(self.deck) >= self.maxDeckLen:
            # TODO: implement replacement of existing units
            print("Your deck is full! No unit will be added")

        else:
            self.deck.append(newUnit)
            print("Added new unit.")
            return
        
    #------------------------------
    def isUnitInDeck(self, categoryNr, unitNr):
    #------------------------------
        for currentUnit in self.deck:
            if currentUnit.categoryNr == categoryNr and currentUnit.unitNr == unitNr:
                return True
        return False

    #------------------------------
    def drawUnit(self, otherPlayer):
    #------------------------------
        redraw = True
        unitCount = 1 #TODO: calculate unitcount based on round and drawn tier

        # Draw until an allowed unit is drawn
        while redraw == True:
            categoryNr = random.randint(0,len(self.unitList)-1)
            unitNr = random.randint(0,self.unitList[categoryNr]-1)
            isActive = len(self.deck) < 4

            redraw = otherPlayer.isUnitInDeck(categoryNr, unitNr)

        drawnUnit = Unit(categoryNr, unitNr, unitCount, isActive)
        print(self.name + ", you drew: ", end='')
        drawnUnit.printStats()
        # TODO: check if already in deck
        # if self.evolveUnitIfInDeck(categoryNr, unitNr, drawnUnit.count):
        #     return

        self.addUnit(drawnUnit)

    #------------------------------
    def evolveUnit(self, unitIndex):
    #------------------------------
        # if self.canEvolve == False:
        #     infoLabel["text"] = "You can not evolve right now!"
        #     return
        # TODO: activate this check again

        print("evoling index: " +str(unitIndex))

        self.deck[unitIndex].count = self.deck[unitIndex].count*2
        self.canEvolve = False
        updateLabels()

    #------------------------------
    def enableDisableUnit(self, unitIndex):
    #------------------------------
        # TODO: check amount of enabled units

        self.deck[unitIndex].isActive = not self.deck[unitIndex].isActive
        updateLabels()



#------------------------------------------------------------------------------
def playerWonBtn(PlayerThatWon, OtherPlayer):
#------------------------------------------------------------------------------
    global roundsplayed
    roundsplayed += 1
    PlayerThatWon.score +=1
    OtherPlayer.canEvolve = True

    updateLabels()

#------------------------------------------------------------------------------
def drawUnitBtn(PlayerThatDraws, OtherPlayer):
#------------------------------------------------------------------------------
    PlayerThatDraws.drawUnit(OtherPlayer)
    updateLabels()

#------------------------------------------------------------------------------
def updateLabels():
#------------------------------------------------------------------------------
    player1Label["text"] = Player1.name + ": " + str(Player1.score)
    player2Label["text"] = Player2.name + ": " + str(Player2.score)
    middleLabel["text"] = "Rounds played:  " + str(roundsplayed)

    # Units player1:
    for unitIndexA in range(len(Player1.deck)):
        currentUnit = Player1.deck[unitIndexA]
        labelText = str(currentUnit.count) + ": " + currentUnit.unitName + "(" + currentUnit.categoryName + ") INDEX: "+ str(unitIndexA)
        tk.Label(
            text=labelText,
            foreground = "black",
            background = "green" if currentUnit.isActive else "red",
            width=50,
            height=5
        ).grid(row=unitIndexA+1, column=2)
        tk.Button(
            text="EVOLVE",
            width=25,
            height=5,
            bg="purple",
            fg="yellow",
            command= lambda idx = unitIndexA: Player1.evolveUnit(idx)).grid(row=unitIndexA+1, column=1)
        tk.Button(
            text="ENABLE/DISABLE",
            width=25,
            height=5,
            bg="white",
            fg="black",
            command= lambda idx = unitIndexA: Player1.enableDisableUnit(idx)).grid(row=unitIndexA+1, column=0)

    # Units player2:
    for unitIndexB in range(len(Player2.deck)):
        currentUnit = Player2.deck[unitIndexB]
        labelText = str(currentUnit.count) + ": " + currentUnit.unitName + "(" + currentUnit.categoryName + ")  INDEX: "+ str(unitIndexB)
        tk.Label(
            text=labelText,
            foreground = "black",
            background = "green" if currentUnit.isActive else "red",
            width=50,
            height=5
        ).grid(row=unitIndexB+1, column=4)
        tk.Button(
            text="EVOLVE",
            width=25,
            height=5,
            bg="purple",
            fg="yellow",
            command= lambda idx = unitIndexB: Player2.evolveUnit(idx)).grid(row=unitIndexB+1, column=5)
        tk.Button(
            text="ENABLE/DISABLE",
            width=25,
            height=5,
            bg="white",
            fg="black",
            command= lambda idx = unitIndexB: Player2.enableDisableUnit(idx)).grid(row=unitIndexB+1, column=6)


#------------------------------------------------------------------------------
# -------MAIN CODE:
#------------------------------------------------------------------------------
# player1 = input("Who is Player 1: ")
# player2 = input("Who is Player 2: ")
# TODO: use input for player names
player1name = "MARTINO"
player2name = "MATTI"


window = tk.Tk()

Player1 = Player(player1name)
Player2 = Player(player2name)

roundsplayed = 0

# Labels
player1Label = tk.Label(
        text=Player1.name + ": " + str(Player1.score),
        foreground = "white",
        background = "black",
        width=50,
        height=5
    )
player2Label = tk.Label(
        text=Player2.name + ": " + str(Player2.score),
        foreground = "white",
        background = "black",
        width=50,
        height=5
    )
middleLabel = tk.Label(
        text="Rounds played:  " + str(roundsplayed),
        foreground = "purple",
        background = "grey",
        width=20,
        height=5
    )
infoLabel = tk.Label(
        text="",
        foreground = "black",
        background = "white",
        width=100,
        height=5
    )


# Buttons
player1WonButton = tk.Button(
    text="WON ROUND",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command= lambda: playerWonBtn(Player1, Player2)
)
player2WonButton = tk.Button(
    text="WON ROUND",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command= lambda: playerWonBtn(Player2, Player1)
)

player1DrawUnitButton = tk.Button(
    text="Draw unit",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command= lambda: drawUnitBtn(Player1, Player2)
)
player2DrawUnitButton = tk.Button(
    text="Draw unit",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command= lambda: drawUnitBtn(Player2, Player1)
)

# window.rowconfigure([0,1,2,3,4,5,6,7,8,9,10], minsize=1)
# window.columnconfigure([0, 1, 2], minsize=50)

# add lables to grid
player1Label.grid(row=0, column=2, sticky="nsew")
middleLabel.grid(row = 0, rowspan=GLOBAL_MaxDeckSize+1, column=3, sticky="nsew")
player2Label.grid(row=0, column=4, sticky="nsew")
infoLabel.grid(row=GLOBAL_MaxDeckSize+2, columnspan=7, sticky="nsew")


# add buttons to grid
player1WonButton.grid(row=0, column=1)
player2WonButton.grid(row=0, column=5)
player1DrawUnitButton.grid(row=GLOBAL_MaxDeckSize+1, column=2)
player2DrawUnitButton.grid(row=GLOBAL_MaxDeckSize+1, column=4)

updateLabels()

window.mainloop()
