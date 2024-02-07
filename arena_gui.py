import tkinter as tk
import json
import random


GLOBAL_MaxDeckSize = 8
GLOBAL_MaxActiveUnits = 4
GLOBAL_LoserDrawAmount = 3
GLOBAL_WinnerDrawAmount = 1

GLOBAL_ButtonWitdh = 13
GLOBAL_Columnheight = 3
GLOBAL_UnitField = 20
GLOBAL_MiddleField = 15

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
        self.allowedDraws = 1
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
    middleLabel["text"] = "Rounds played:  " + str(roundsplayed) + " \n Max allowed Tier: " + str(currentMaxTier)

    for idx, CurrentPlayer in enumerate(GameManager):
        CurrentPlayerClass = CurrentPlayer["class"]

        # score
        CurrentPlayer["scoreLabel"]["text"] = CurrentPlayerClass.name + ": " + str(CurrentPlayerClass.score)

        # display deck
        for idx in range(GLOBAL_MaxDeckSize):
            if idx < len(CurrentPlayerClass.deck):
                # unit slot
                currentUnit = CurrentPlayerClass.deck[idx]
                labelText = getUnitStats(currentUnit)
                CurrentPlayer["deckLabels"][idx]["text"] = labelText
                CurrentPlayer["deckLabels"][idx]["background"] = "green" if currentUnit.isActive else "red"
                # enable buttons
                CurrentPlayer["deckButtons"][idx]["deleteButton"]["state"] = "normal"
                CurrentPlayer["deckButtons"][idx]["switchButton"]["state"] = "normal" if currentUnit.isActive or CurrentPlayerClass.getActiveUnitCount() < GLOBAL_MaxActiveUnits else "disabled"
                CurrentPlayer["deckButtons"][idx]["switchButton"]["fg"] = "red" if currentUnit.isActive else "#0ffa1b"
                CurrentPlayer["deckButtons"][idx]["switchButton"]["text"] = "DISABLE" if currentUnit.isActive else "ENABLE"
            else:
                # empty slot
                CurrentPlayer["deckLabels"][idx]["text"] = "<empty deck slot>"
                CurrentPlayer["deckLabels"][idx]["background"] = "white"
                CurrentPlayer["deckButtons"][idx]["deleteButton"]["state"] = "disabled"
                CurrentPlayer["deckButtons"][idx]["switchButton"]["state"] = "disabled"

        # display drawn units
        for idx in range(GLOBAL_LoserDrawAmount):
            if idx < len(CurrentPlayerClass.drawnUnits):
                # unit slot
                currentUnit = CurrentPlayerClass.drawnUnits[idx]
                labelText = getUnitStats(currentUnit)
                CurrentPlayer["drawnUnitLabels"][idx]["text"] = labelText
                # enable buttons
                CurrentPlayer["drawnUnitButtons"][idx]["discardButton"]["state"] = "normal"
                CurrentPlayer["drawnUnitButtons"][idx]["addButton"]["state"] = "normal"
                CurrentPlayer["drawnUnitButtons"][idx]["addButton"]["text"] = "EVOLVE" if CurrentPlayerClass.isDrawnUnitInDeck(idx) else "ADD"
                CurrentPlayer["drawnUnitButtons"][idx]["addButton"]["background"] = "green" if CurrentPlayerClass.isDrawnUnitInDeck(idx) else "purple"
            else:
                # empty slot
                CurrentPlayer["drawnUnitLabels"][idx]["text"] = "<drawn units>"
                CurrentPlayer["drawnUnitButtons"][idx]["discardButton"]["state"] = "disabled"
                CurrentPlayer["drawnUnitButtons"][idx]["addButton"]["state"] = "disabled"
                CurrentPlayer["drawnUnitButtons"][idx]["addButton"]["background"] = "purple"
                CurrentPlayer["drawnUnitButtons"][idx]["addButton"]["text"] = "ADD"

 #------------------------------------------------------------------------------
def initPlayerLabelsAndButtons():
#------------------------------------------------------------------------------
    # Player specific lables and buttons
    for idx, CurrentPlayer in enumerate(GameManager):
        CurrentPlayerClass = CurrentPlayer["class"]
        OtherPlayerClass = GameManager[1 - idx]["class"]
        # score label
        CurrentPlayer["scoreLabel"] = tk.Label(
            text=CurrentPlayerClass.name + ": " + str(CurrentPlayerClass.score),
            foreground = "white",
            background = "black",
            width=GLOBAL_UnitField,
            height=GLOBAL_Columnheight,
            font='Helvetica 10 bold')

        # Round won button
        CurrentPlayer["wonButton"] = tk.Button(
        text="WON ROUND",
        width=GLOBAL_ButtonWitdh,
        height=GLOBAL_Columnheight,
        bg="black",
        fg="white",
        command= lambda x=CurrentPlayerClass, y=OtherPlayerClass: playerWonBtn(x, y))

        # Deck labels and buttons
        for idx in range(GLOBAL_MaxDeckSize):
            # labels
            CurrentPlayer["deckLabels"].append(tk.Label(
                text="<empty deck slot>",
                foreground = "black",
                background = "white",
                font='Helvetica 10 bold',
                borderwidth = 1,
                relief="solid",
                width=GLOBAL_UnitField + GLOBAL_ButtonWitdh + GLOBAL_ButtonWitdh,
                height=GLOBAL_Columnheight))
            # generate delete button
            currentDeleteButton = tk.Button(
            text="DELETE",
            width=GLOBAL_ButtonWitdh-1,
            height=GLOBAL_Columnheight-1,
            bg="red",
            fg="black",
            state= "disabled",
            font='Helvetica 10 bold',
            borderwidth = 1,
            relief="solid",
            command= lambda index = idx, player = CurrentPlayerClass : player.removeUnit(index))
            # generate switch button
            currentSwitchButton = tk.Button(
            text="",
            width=GLOBAL_ButtonWitdh-1,
            height=GLOBAL_Columnheight-1,
            bg="blue",
            fg="black",
            state= "disabled",
            font='Helvetica 10 bold',
            borderwidth = 1,
            relief="solid",
            command= lambda index = idx, player = CurrentPlayerClass: player.enableDisableUnit(index))
            # append buttons
            CurrentPlayer["deckButtons"].append({"deleteButton": currentDeleteButton, "switchButton": currentSwitchButton})

        # DrawnUnits labels and buttons
        # labels
        for idx in range(GLOBAL_LoserDrawAmount):
            CurrentPlayer["drawnUnitLabels"].append(tk.Label(
                text="<drawn units>",
                foreground = "yellow",
                background = "gray",
                font='Helvetica 10 bold',
                borderwidth = 1,
                relief="solid",
                width=GLOBAL_UnitField + GLOBAL_ButtonWitdh + GLOBAL_ButtonWitdh,
                height=GLOBAL_Columnheight))
            #generate add button
            addButton = tk.Button(
                text="ADD",
                width=GLOBAL_ButtonWitdh-1,
                height=GLOBAL_Columnheight-1,
                bg="purple",
                fg="yellow",
                state= "disabled",
                font='Helvetica 10 bold',
                borderwidth = 1,
                relief="solid",
                command= lambda index = idx, player = CurrentPlayerClass: player.addDrawnUnitToDeck(index))
            # generate discard button
            discardButton = tk.Button(
                text="DISCARD",
                width=GLOBAL_ButtonWitdh-1,
                height=GLOBAL_Columnheight-1,
                bg="red",
                fg="black",
                state= "disabled",
                font='Helvetica 10 bold',
                borderwidth = 1,
                relief="solid",
                command= lambda index = idx, player = CurrentPlayerClass: player.removeDrawnUnit(index))
            # append buttons
            CurrentPlayer["drawnUnitButtons"].append({"addButton": addButton, "discardButton": discardButton})

#------------------------------------------------------------------------------
def addLabelsAndButtonsToGrid():
#------------------------------------------------------------------------------
    # add static lables to grid
    GameManager[0]["scoreLabel"].grid(row=0, column=2, sticky="nsew")
    GameManager[1]["scoreLabel"].grid(row=0, column=4, sticky="nsew")
    middleLabel.grid(row = 0, rowspan=GLOBAL_MaxDeckSize+GLOBAL_LoserDrawAmount+1, column=3, sticky="nsew")
    infoLabel.grid(row=GLOBAL_MaxDeckSize+GLOBAL_LoserDrawAmount+1, column=0, columnspan=7, sticky="nsew")

    # add static buttons to grid
    GameManager[0]["wonButton"].grid(row=0, column=1)
    GameManager[1]["wonButton"].grid(row=0, column=5)

    #add deck labels and buttons for both players
    for idx in range(GLOBAL_MaxDeckSize):
        GameManager[0]["deckLabels"][idx].grid(row=idx+1, column=2)
        GameManager[0]["deckButtons"][idx]["deleteButton"].grid(row=idx+1, column=0)
        GameManager[0]["deckButtons"][idx]["switchButton"].grid(row=idx+1, column=1)

        GameManager[1]["deckLabels"][idx].grid(row=idx+1, column=4)
        GameManager[1]["deckButtons"][idx]["deleteButton"].grid(row=idx+1, column=6)
        GameManager[1]["deckButtons"][idx]["switchButton"].grid(row=idx+1, column=5)

    #add drawnUnit labels and buttons for both players
    for idx in range(GLOBAL_LoserDrawAmount):
        GameManager[0]["drawnUnitLabels"][idx].grid(row=idx+GLOBAL_MaxDeckSize+1, column=2)
        GameManager[0]["drawnUnitButtons"][idx]["discardButton"].grid(row=idx+GLOBAL_MaxDeckSize+1, column=0)
        GameManager[0]["drawnUnitButtons"][idx]["addButton"].grid(row=idx+GLOBAL_MaxDeckSize+1, column=1)

        GameManager[1]["drawnUnitLabels"][idx].grid(row=idx+GLOBAL_MaxDeckSize+1, column=4)
        GameManager[1]["drawnUnitButtons"][idx]["discardButton"].grid(row=idx+GLOBAL_MaxDeckSize+1, column=6)
        GameManager[1]["drawnUnitButtons"][idx]["addButton"].grid(row=idx+GLOBAL_MaxDeckSize+1, column=5)


#------------------------------------------------------------------------------
# -------MAIN CODE:
#------------------------------------------------------------------------------
# player1 = input("Who is Player 1: ")
# player2 = input("Who is Player 2: ")
# TODO: use input for player names
player1name = "MARTINO"
player2name = "MATTI"

roundsplayed = 0
currentMaxTier = 1

window = tk.Tk()


Player1 = Player(player1name)
Player2 = Player(player2name)


player1Data = {"class": Player1, "scoreLabel": tk.Label(), "wonButton": tk.Button(),
            "deckLabels": [], "drawnUnitLabels" : [], "deckButtons": [], "drawnUnitButtons": []}

player2Data = {"class": Player2, "scoreLabel": tk.Label(), "wonButton": tk.Button(),
            "deckLabels": [], "drawnUnitLabels" : [], "deckButtons": [], "drawnUnitButtons": []}


GameManager = [player1Data, player2Data]

middleLabel = tk.Label(
        text="Rounds played:  " + str(roundsplayed),
        foreground = "purple",
        background = "grey",
        borderwidth = 1,
        relief="solid",
        width=GLOBAL_MiddleField,
        height=GLOBAL_Columnheight)
infoLabel = tk.Label(
        text="",
        foreground = "black",
        background = "white",
        borderwidth = 1,
        relief="solid",
        width= GLOBAL_ButtonWitdh*4 + GLOBAL_MiddleField + GLOBAL_UnitField*2,
        height=GLOBAL_Columnheight)


initPlayerLabelsAndButtons()

addLabelsAndButtonsToGrid()

Player1.drawUnit(Player2)
Player2.drawUnit(Player1)

updateLabels()

window.mainloop()
