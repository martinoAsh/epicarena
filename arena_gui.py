import tkinter as tk
import json
import random


GLOBAL_MaxDeckSize = 8
GLOBAL_MaxActiveUnits = 4
GLOBAL_LoserDrawAmount = 3
GLOBAL_WinnerDrawAmount = 1

GLOBAL_ButtonWitdh = 15
GLOBAL_Columnheight = 3
GLOBAL_UnitField = 50
GLOBAL_MiddleField = 20

# should be powers of 2 because units are always doubled when evolving
GLOBAL_MaxUnitsPerTier = {
    1: 128,
    2: 64,
    3: 32,
    4: 16,
    5: 8,
    6: 4,
    7: 1
    }

GLOBAL_MaxTier = 7
GLOBAL_RoundsUntilTierIncrease = 4

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
    def getStatsAsString(self):
    #------------------------------
        return self.unitName + " ("+ self.categoryName + ")"" - Amount: " + str(self.count) + " - Tier: " + str(self.tier)

#------------------------------------------------------------------------------
class Player:
#------------------------------------------------------------------------------
    def __init__(self, name):
        self.name = name
        self.deck=[]
        self.drawnUnits=[]
        self.score = 0
        self.maxDeckLen = GLOBAL_MaxDeckSize
        self.maxActiveUnits = GLOBAL_MaxActiveUnits
        self.unitList = []
        self.allowedDraws = 0
        self.lostRound = True
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


    #------------------------------
    def addUnit(self, newUnit):
    #------------------------------
        existingUnit = self.getUnitIfInDeck(newUnit.categoryNr, newUnit.unitNr)
        if existingUnit is not None:
            # Unit is already in deck: double it if allowed
            maxAllowedUnits = GLOBAL_MaxUnitsPerTier[existingUnit.tier]
            if existingUnit.count*2 > maxAllowedUnits:
                infoLabel["text"] = newUnit.unitName + " is already maxed out, SORRY!"
                return False
            else:
                existingUnit.count *= 2
                infoLabel["text"] = newUnit.unitName + " was doubled!"
                return True
        else:
            # unit is not already in deck: check if deck is full
            if len(self.deck) >= self.maxDeckLen:
                infoLabel["text"] = "Your deck is full, no unit was added!"
                return False
            else:
                newUnit.isActive = True
                if self.getActiveUnitCount() >= GLOBAL_MaxActiveUnits:
                    newUnit.isActive = False
                self.deck.append(newUnit)
                infoLabel["text"] = newUnit.unitName + " was added to deck!"
                return True

    #------------------------------
    def addDrawnUnitToDeck(self, drawnUnitIndex):
    #------------------------------
        if self.addUnit(self.drawnUnits[drawnUnitIndex]) == True:
            self.drawnUnits.pop(drawnUnitIndex)
            updateLabels()

    #------------------------------
    def isDrawnUnitInDeck(self, drawnUnitIndex):
    #------------------------------
        drawnUnit = self.drawnUnits[drawnUnitIndex]
        for currentUnit in self.deck:
            if currentUnit.categoryNr == drawnUnit.categoryNr and currentUnit.unitNr == drawnUnit.unitNr:
                return True
        return False

    #------------------------------
    def isUnitInDeckOrDrawn(self, categoryNr, unitNr):
    #------------------------------
        for currentUnit in self.deck:
            if currentUnit.categoryNr == categoryNr and currentUnit.unitNr == unitNr:
                return True
        for currentUnit in self.drawnUnits:
            if currentUnit.categoryNr == categoryNr and currentUnit.unitNr == unitNr:
                return True
        return False

    #------------------------------
    def getUnitIfInDeck(self, categoryNr, unitNr):
    #------------------------------
        for currentUnit in self.deck:
            if currentUnit.categoryNr == categoryNr and currentUnit.unitNr == unitNr:
                return currentUnit
        return None

    #------------------------------
    def drawUnit(self, otherPlayer):
    #------------------------------
        unitCount = 1 #TODO: calculate unitcount based on round and drawn tier

        while self.allowedDraws > 0:

            # Draw until an allowed unit is drawn
            redraw = True
            while redraw == True:
                categoryNr = random.randint(0,len(self.unitList)-1)
                unitNr = random.randint(0,self.unitList[categoryNr]-1)
                isActive = len(self.deck) < 4
                redraw = otherPlayer.isUnitInDeckOrDrawn(categoryNr, unitNr)
                drawnUnit = Unit(categoryNr, unitNr, unitCount, isActive)
                if drawnUnit.tier > currentMaxTier:
                    redraw = True

            drawnUnit = Unit(categoryNr, unitNr, unitCount, isActive)
            self.drawnUnits.append(drawnUnit)
            self.allowedDraws -= 1

    #------------------------------
    def enableDisableUnit(self, unitIndex):
    #------------------------------
        if self.deck[unitIndex].isActive == True:
            self.deck[unitIndex].isActive = False
            infoLabel["text"] = "Unit disabled!"
            updateLabels()
            return
        
        # count active units
        activeUnitsCount = self.getActiveUnitCount()

        if activeUnitsCount >= GLOBAL_MaxActiveUnits:
            infoLabel["text"] = "Your active units are already maxed out!"
            return

        self.deck[unitIndex].isActive = True
        infoLabel["text"] = "Unit enabled!"
        updateLabels()

    #------------------------------
    def removeUnit(self, unitIndex):
    #------------------------------
        self.deck.pop(unitIndex)
        infoLabel["text"] = "Unit was removed from deck!"
        updateLabels()

    #------------------------------
    def removeDrawnUnit(self, drawnUnitIndex):
    #------------------------------
        print("Player:"+ self.name +" is removing drawn unit, size of drawn units: " + str(len(self.drawnUnits)) + ", INDEX: " + str(drawnUnitIndex))
        self.drawnUnits.pop(drawnUnitIndex)
        updateLabels()

    #------------------------------
    def getActiveUnitCount(self):
    #------------------------------
        activeUnitsCount = 0
        for currentUnit in self.deck:
            if currentUnit.isActive == True:
                activeUnitsCount += 1

        return activeUnitsCount


#------------------------------------------------------------------------------
def playerWonBtn(PlayerThatWon, OtherPlayer):
#------------------------------------------------------------------------------
    global roundsplayed
    global currentMaxTier
    roundsplayed += 1
    PlayerThatWon.score +=1

    if roundsplayed % GLOBAL_RoundsUntilTierIncrease == 0 and currentMaxTier < GLOBAL_MaxTier:
        infoLabel["text"] =" Allowed Tier increased!"
        currentMaxTier +=1


    # empty drawn units of both players
    PlayerThatWon.drawnUnits = []
    OtherPlayer.drawnUnits = []
    PlayerThatWon.allowedDraws = GLOBAL_WinnerDrawAmount
    OtherPlayer.allowedDraws = GLOBAL_LoserDrawAmount

    # Other player draws first
    OtherPlayer.drawUnit(PlayerThatWon)
    PlayerThatWon.drawUnit(OtherPlayer)

    infoLabel["text"] = PlayerThatWon.name + " won the round. "
    updateLabels()

#------------------------------------------------------------------------------
def getUnitStats(Unit):
#------------------------------------------------------------------------------
    return Unit.unitName + " (" + Unit.categoryName + ", Tier: "+ str(Unit.tier) +") --- COUNT: " + str(Unit.count)

#------------------------------------------------------------------------------
def updateLabels():
#------------------------------------------------------------------------------
    player1Label["text"] = Player1.name + ": " + str(Player1.score)
    player2Label["text"] = Player2.name + ": " + str(Player2.score)
    middleLabel["text"] = "Rounds played:  " + str(roundsplayed) + " \n Max allowed Tier: " + str(currentMaxTier)

    # put labels for units
    for idx in range(GLOBAL_MaxDeckSize):
        tk.Label(
            text="<empty deck slot>",
            foreground = "black",
            background = "white",
            font='Helvetica 10 bold',
            width=GLOBAL_UnitField + GLOBAL_ButtonWitdh + GLOBAL_ButtonWitdh,
            height=GLOBAL_Columnheight
        ).grid(row=idx+1, column=0, columnspan=3)
        tk.Label(
            text="<empty deck slot>",
            foreground = "black",
            background = "white",
            font='Helvetica 10 bold',
            width=GLOBAL_UnitField + GLOBAL_ButtonWitdh*2,
            height=GLOBAL_Columnheight
        ).grid(row=idx+1, column=4, columnspan=3)

    # put labels for drawnUnits
    for idx in range(GLOBAL_LoserDrawAmount):
        tk.Label(
            text="<drawn units>",
            foreground = "yellow",
            background = "gray",
            font='Helvetica 10 bold',
            width=GLOBAL_UnitField + GLOBAL_ButtonWitdh + GLOBAL_ButtonWitdh,
            height=GLOBAL_Columnheight
        ).grid(row=idx+GLOBAL_MaxDeckSize+1, column=0, columnspan=3)
        tk.Label(
            text="<drawn units>",
            foreground = "yellow",
            background = "gray",
            font='Helvetica 10 bold',
            width=GLOBAL_UnitField + GLOBAL_ButtonWitdh*2,
            height=GLOBAL_Columnheight
        ).grid(row=idx+GLOBAL_MaxDeckSize+1, column=4, columnspan=3)

    # Units in deck player 1:
    for unitindex in range(len(Player1.deck)):
        currentUnit = Player1.deck[unitindex]
        labelText = getUnitStats(currentUnit)
        tk.Label(
            text=labelText,
            foreground = "black",
            background = "green" if currentUnit.isActive else "red",
            width=GLOBAL_UnitField,
            height=GLOBAL_Columnheight,
            font='Helvetica 10 bold'
        ).grid(row=unitindex+1, column= 2)
        tk.Button(
            text="DELETE",
            width=GLOBAL_ButtonWitdh,
            height=GLOBAL_Columnheight-1,
            bg="red",
            fg="black",
            command= lambda idx = unitindex: Player1.removeUnit(idx)).grid(row=unitindex+1, column=0)
        tk.Button(
            text="ENABLE/DISABLE",
            width=GLOBAL_ButtonWitdh,
            height=GLOBAL_Columnheight-1,
            bg="grey",
            fg="yellow",
            state= "normal" if Player1.deck[unitindex].isActive == True or Player1.getActiveUnitCount() < GLOBAL_MaxActiveUnits else "disabled",
            command= lambda idx = unitindex: Player1.enableDisableUnit(idx)).grid(row=unitindex+1, column= 1)
    # Drawn units player1:
    for unitindex in range(len(Player1.drawnUnits)):
        currentUnit = Player1.drawnUnits[unitindex]
        labelText = getUnitStats(currentUnit)
        tk.Label(
            text=labelText,
            foreground = "black",
            background = "yellow",
            width=GLOBAL_UnitField,
            height=GLOBAL_Columnheight,
            font='Helvetica 10 bold'
        ).grid(row=unitindex+GLOBAL_MaxDeckSize+1, column=2)
        tk.Button(
            text="EVOLVE" if Player1.isDrawnUnitInDeck(unitindex) else "ADD",
            width=GLOBAL_ButtonWitdh,
            height=GLOBAL_Columnheight-1,
            bg="purple",
            fg="yellow",
            command= lambda idx = unitindex: Player1.addDrawnUnitToDeck(idx)).grid(row=GLOBAL_MaxDeckSize+unitindex+1, column= 1)
        tk.Button(
            text="DISCARD",
            width=GLOBAL_ButtonWitdh,
            height=GLOBAL_Columnheight-1,
            bg="grey",
            fg="yellow",
            command= lambda idx = unitindex: Player1.removeDrawnUnit(idx)).grid(row=GLOBAL_MaxDeckSize+unitindex+1, column= 0)


    # Units in deck player 2:
    for unitindex in range(len(Player2.deck)):
        currentUnit = Player2.deck[unitindex]
        labelText = getUnitStats(currentUnit)
        tk.Label(
            text=labelText,
            foreground = "black",
            background = "green" if currentUnit.isActive else "red",
            width=GLOBAL_UnitField,
            height=GLOBAL_Columnheight,
            font='Helvetica 10 bold'
        ).grid(row=unitindex+1, column= 4)
        tk.Button(
            text="DELETE",
            width=GLOBAL_ButtonWitdh,
            height=GLOBAL_Columnheight-1,
            bg="red",
            fg="black",
            command= lambda idx = unitindex: Player2.removeUnit(idx)).grid(row=unitindex+1, column=6)
        tk.Button(
            text="ENABLE/DISABLE",
            width=GLOBAL_ButtonWitdh,
            height=GLOBAL_Columnheight-1,
            bg="grey",
            fg="yellow",
            state= "normal" if Player2.deck[unitindex].isActive == True or Player2.getActiveUnitCount() < GLOBAL_MaxActiveUnits else "disabled",
            command= lambda idx = unitindex: Player2.enableDisableUnit(idx)).grid(row=unitindex+1, column= 5)
    # Drawn units player2:
    for unitindex in range(len(Player2.drawnUnits)):
        currentUnit = Player2.drawnUnits[unitindex]
        labelText = getUnitStats(currentUnit)
        tk.Label(
            text=labelText,
            foreground = "black",
            background = "yellow",
            width=GLOBAL_UnitField,
            height=GLOBAL_Columnheight,
            font='Helvetica 10 bold'
        ).grid(row=unitindex+GLOBAL_MaxDeckSize+1, column=4)
        tk.Button(
            text="EVOLVE" if Player2.isDrawnUnitInDeck(unitindex) else "ADD",
            width=GLOBAL_ButtonWitdh,
            height=GLOBAL_Columnheight-1,
            bg="purple",
            fg="yellow",
            command= lambda idx = unitindex: Player2.addDrawnUnitToDeck(idx)).grid(row=GLOBAL_MaxDeckSize+unitindex+1, column= 5)
        tk.Button(
            text="DISCARD",
            width=GLOBAL_ButtonWitdh,
            height=GLOBAL_Columnheight-1,
            bg="grey",
            fg="yellow",
            command= lambda idx = unitindex: Player2.removeDrawnUnit(idx)).grid(row=GLOBAL_MaxDeckSize+unitindex+1, column= 6)

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
currentMaxTier = 1

# Labels
player1Label = tk.Label(
        text=Player1.name + ": " + str(Player1.score),
        foreground = "white",
        background = "black",
        width=GLOBAL_UnitField,
        height=GLOBAL_Columnheight,
        font='Helvetica 10 bold'
    )
player2Label = tk.Label(
        text=Player2.name + ": " + str(Player2.score),
        foreground = "white",
        background = "black",
        width=GLOBAL_UnitField,
        height=GLOBAL_Columnheight,
        font='Helvetica 10 bold'
    )
middleLabel = tk.Label(
        text="Rounds played:  " + str(roundsplayed),
        foreground = "purple",
        background = "grey",
        width=GLOBAL_MiddleField,
        height=GLOBAL_Columnheight
    )
infoLabel = tk.Label(
        text="",
        foreground = "black",
        background = "white",
        width= GLOBAL_ButtonWitdh*4 + GLOBAL_MiddleField + GLOBAL_UnitField*2,
        height=GLOBAL_Columnheight
    )


# Buttons
player1WonButton = tk.Button(
    text="WON ROUND",
    width=GLOBAL_ButtonWitdh,
    height=GLOBAL_Columnheight,
    bg="blue",
    fg="yellow",
    command= lambda: playerWonBtn(Player1, Player2)
)
player2WonButton = tk.Button(
    text="WON ROUND",
    width=GLOBAL_ButtonWitdh,
    height=GLOBAL_Columnheight,
    bg="blue",
    fg="yellow",
    command= lambda: playerWonBtn(Player2, Player1)
)

window.rowconfigure(0 ,minsize=7)
window.columnconfigure(0, minsize=GLOBAL_MaxDeckSize+2)

# add lables to grid
player1Label.grid(row=0, column=2, sticky="nsew")
middleLabel.grid(row = 0, rowspan=GLOBAL_MaxDeckSize+GLOBAL_LoserDrawAmount+1, column=3, sticky="nsew")
player2Label.grid(row=0, column=4, sticky="nsew")
infoLabel.grid(row=GLOBAL_MaxDeckSize+GLOBAL_LoserDrawAmount+1, column=0, columnspan=7, sticky="nsew")


# add buttons to grid
player1WonButton.grid(row=0, column=1)
player2WonButton.grid(row=0, column=5)
# player1DrawUnitButton.grid(row=GLOBAL_MaxDeckSize+GLOBAL_LoserDrawAmount+1, column=2)
# player2DrawUnitButton.grid(row=GLOBAL_MaxDeckSize+GLOBAL_LoserDrawAmount+1, column=4)

updateLabels()

window.mainloop()
