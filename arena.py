import json
import random


def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

maxUnitCount = 128
Tier1MaxUnits = 128
Tier2MaxUnits = 64
Tier3MaxUnits = 32
Tier4MaxUnits = 16
Tier5MaxUnits = 8
Tier6MaxUnits = 4
Tier7MaxUnits = 1

newTierCounter = 3

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
        self.count = self.calculateCount(count)

    #------------------------------
    def printStats(self):
    #------------------------------
        if self.isActive:
            # TODO: make colors work in cmd
            prGreen(self.unitName + 
                  " ("+ self.categoryName + ")"
                  ", Count: " + str(self.count) + 
                  ", Active: " + str(self.isActive) + ", Tier: " + str(self.tier))
        else:
            prRed(self.unitName +
                  " ("+ self.categoryName + ")"
                  ", Count: " + str(self.count) + 
                  ", Active: " + str(self.isActive) + ", Tier: " + str(self.tier))

    #------------------------------
    def lookUpAndSetNames(self):
    #------------------------------
        file = open("unitList.json")
        unitData = json.load(file)
        self.categoryName = unitData['categories'][self.categoryNr]['name']
        self.unitName = unitData['categories'][self.categoryNr]['units'][self.unitNr]['name']
        self.tier = unitData['categories'][self.categoryNr]['units'][self.unitNr]['tier']

    #------------------------------
    def calculateCount(self, proposedCount):
    #------------------------------
        if self.tier == 1:
            return proposedCount
        elif self.tier == 2:
            return int(proposedCount/2)
        elif self.tier == 3:
            return int(proposedCount/4)
        elif self.tier == 4:
            return int(proposedCount/8)
        elif self.tier == 5:
            return int(proposedCount/16)
        elif self.tier == 6:
            return int(proposedCount/32)
        elif self.tier == 7:
            return 1
        else:
            return 1

    #------------------------------
    def evolveUnit(self):
    #------------------------------
        # TODO: improve this logic
 
        if self.tier == 1:
            if self.count*2 <= Tier1MaxUnits:
                self.count = self.count*2
                prYellow(self.unitName + " was evolved!")
                return True
            else:
                return False
        elif self.tier == 2:
            if self.count*2 <= Tier2MaxUnits:
                self.count = self.count*2
                prYellow(self.unitName + " was evolved!")
                return True
            else:
                return False
        elif self.tier == 3:
            if self.count*2 <= Tier3MaxUnits:
                self.count = self.count*2
                prYellow(self.unitName + " was evolved!")
                return True
            else:
                return False
        elif self.tier == 4:
            if self.count*2 <= Tier4MaxUnits:
                self.count = self.count*2
                prYellow(self.unitName + " was evolved!")
                return True
            else:
                return False
        elif self.tier == 5:
            if self.count+1 <= Tier5MaxUnits:
                self.count = self.count+1
                prYellow(self.unitName + " was evolved!")
                return True
            else:
                return False
        elif self.tier == 6:
            if self.count+1 <= Tier6MaxUnits:
                self.count = self.count+1
                prYellow(self.unitName + " was evolved!")
                return True
            else:
                return False
        elif self.tier == 7:
            if self.count+1 <= Tier7MaxUnits:
                self.count = self.count+1
                prYellow(self.unitName + " was evolved!")
                return True
            else:
                return False
        else:
            print("Unknown tier, nothing was evolved!")
            return False




#------------------------------------------------------------------------------
class Player:
#------------------------------------------------------------------------------
    def __init__(self, name):
        self.name = name
        self.deck=[]
        self.score = 0
        self.maxDeckLen = 8
        self.maxActiveUnits = 4
        self.unitList = []
        self.parseUnitList()

    #------------------------------
    def addUnit(self, newUnit):
    #------------------------------
        userInput = ""

        if len(self.deck) >= self.maxDeckLen:
            inputCorrect = False
            while inputCorrect == False:
                userInput = input("Your Deck is full. Which unit should be replaced? (n for none) ")
                if userInput == 'n':
                    print("No unit will be added.")
                    break
                inputCorrect = checkIfInputIsInRange(userInput, 0, len(self.deck)-1)

            if userInput != 'n':
                print("Replacing unit.")
                self.deck[int(userInput)] = newUnit

        else:
            self.deck.append(newUnit)
            print("Added new unit.")
            return
        
    def isUnitInDeck(self, categoryNr, unitNr):
        for currentUnit in self.deck:
            if currentUnit.categoryNr == categoryNr and currentUnit.unitNr == unitNr:
                return True
        return False


    #------------------------------
    def printUnits(self):
    #------------------------------
        if len(self.deck) == 0:
            print(self.name + " has no Units yet")
            return
        print("")
        # print(self.name + " has following Units: ")
        print("- Units of " + self.name + ": - - - - - - - - - - - - - - - - - -")
        for unitIndex in range(len(self.deck)):
            print(str(unitIndex) + ": ", end='')
            self.deck[unitIndex].printStats()
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")

    #------------------------------
    def evolveUnitAfterRound(self):
    #------------------------------
        if len(self.deck) == 0:
            print(self.name + " has no Units to evolve yet")
            return
        userInput = ""
        inputCorrect = False
        while inputCorrect == False:
            userInput = input("Which unit do you want to evolve? ")
            inputCorrect = checkIfInputIsInRange(userInput, 0, len(self.deck)-1)
        
        while self.deck[int(userInput)].evolveUnit() != True:
            inputCorrect = False
            while inputCorrect == False:
                userInput = input("Unit is maxed out. Choose other unit: ")
                inputCorrect = checkIfInputIsInRange(userInput, 0, len(self.deck)-1)


    #------------------------------
    def drawUnit(self, allowedTier, unitCount, otherPlayer):
    #------------------------------
        file = open("unitList.json")
        unitData = json.load(file)
        drawnTier = 10000
        otherPlayerHasUnit = True

        # Draw until an allowed unit is drawn
        while drawnTier > allowedTier or otherPlayerHasUnit == True:
            categoryNr = random.randint(0,len(self.unitList)-1)
            unitNr = random.randint(0,self.unitList[categoryNr]-1)
            isActive = len(self.deck) < 4
            drawnTier = unitData['categories'][categoryNr]['units'][unitNr]['tier']
            otherPlayerHasUnit = otherPlayer.isUnitInDeck(categoryNr, unitNr)
            # print("Drew Unit of tier: " + str(drawnTier) + ", allowed: "
            #       + str(allowedTier) + " , roundet unitcount: "
            #       + str(round(unitCount/drawnTier)))

        drawnUnit = Unit(categoryNr, unitNr, unitCount, isActive)
        print(self.name + ", you drew: ", end='')
        drawnUnit.printStats()
        # check if already in deck
        if self.evolveUnitIfInDeck(categoryNr, unitNr, drawnUnit.count):
            return

        self.addUnit(drawnUnit)

    #------------------------------
    def evolveUnitIfInDeck(self, categoryNr, unitNr, newCount):
    #------------------------------
        for currentUnit in self.deck:
            if currentUnit.categoryNr == categoryNr and currentUnit.unitNr == unitNr:
                userInput = input("NICE! You already have this Unit. You wanna evolve or replace it? (e/r) ")
                if userInput == 'e':
                    if currentUnit.evolveUnit():
                        print("Cool, Unit was evolved!")
                    else: 
                        print("Sorry, Unit is already maxed out")
                else:
                    currentUnit.count = newCount
                    print("Unit was replaced!")
                return True
        return False

    #------------------------------
    def swapUnits(self):
    #------------------------------
        userInput = ""

        inputCorrect = False

        while inputCorrect == False:
            userInput = input("Which unit gets deactivated? ")
            inputCorrect = checkIfInputIsInRange(userInput, 0, len(self.deck)-1)
        self.deck[int(userInput)].isActive = False

        inputCorrect = False

        while inputCorrect == False:
            userInput = input("Which unit gets activated? ")
            inputCorrect = checkIfInputIsInRange(userInput, 0, len(self.deck)-1)
        self.deck[int(userInput)].isActive = True

    #------------------------------
    def parseUnitList(self):
    #------------------------------
        file = open("unitList.json")
        unitData = json.load(file)
        for categoryIndex in range(len(unitData['categories'])):
            self.unitList.append((len(unitData['categories'][categoryIndex]['units'])))
        # print(self.unitList)

    #------------------------------
    def alterUnitCount(self):
    #------------------------------
        if len(self.deck) == 0:
            print(self.name + " has no Units to alter yet")
            return
        userInput = ""
        userInputCount = ""
        inputCorrect = False
        while inputCorrect == False:
            userInput = input("Which unit's count do you want to alter? ")
            inputCorrect = checkIfInputIsInRange(userInput, 0, len(self.deck)-1)

        inputCorrect = False
        while inputCorrect == False:
            userInputCount = input("What is the new unit count? ")
            inputCorrect = checkIfInputIsInRange(userInputCount, 0, 512)

        self.deck[int(userInput)].count = int(userInputCount)
        print("Changed unit count to: " + userInputCount)

def checkIfInputIsInRange(value, min, max):
    try:
        # try converting it into integer
        val = int(value)
        return ((val >=min) and (val <=max))
    except ValueError:
        return False

#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
    player1 = input("Who is Player 1: ")
    player2 = input("Who is Player 2: ")

    playerList = [Player(player1), Player(player2)]


    print("---------------------------------------------------------------")
    print("----------------NEW GAME---------------------------------------")
    print("---------------------------------------------------------------")
    print()

    #first draw for each player
    for playerIndex in range(len(playerList)):
        playerList[playerIndex].drawUnit(1, 1, playerList[abs(playerIndex-1)])
        print("---------------------------------------------------------------")


    roundCount = 0
    allowedTier = 1
    newUnitCount = 1

    while 1:
        print("---------------------------------------------------------------")
        for playerIndex in range(len(playerList)):
            currentPlayer = playerList[playerIndex]
            print("")
            playerInput = print(currentPlayer.name + "s TURN: ")
            print("")
            currentPlayer.printUnits()
            playerInput = input(currentPlayer.name + ", did you win? (y/n) ")
            print("-----------------------------")
            if playerInput == 'n':
                # player gets to evolve a unit
                currentPlayer.evolveUnitAfterRound()
            else:
                currentPlayer.score += 1

            #draw a new unit
            currentPlayer.drawUnit(allowedTier, newUnitCount, playerList[abs(playerIndex-1)])

            print("")
            currentPlayer.printUnits()

            while 1:
                print("")
                print("1: Swap units")
                print("2: Show current deck")
                print("3: Alter unit count (ADMIN ONLY)")
                print("4: Conclude round")
                playerInput = input(currentPlayer.name + ", what do you want to do? ")

                if playerInput == '1':
                    currentPlayer.swapUnits()
                elif playerInput == '2':
                    currentPlayer.printUnits()
                elif playerInput == '3':
                    currentPlayer.alterUnitCount()
                elif playerInput == '4':
                    break

            print("---------------------------------------------------------------")
            print("---------------------------------------------------------------")
        roundCount += 1
        if roundCount %newTierCounter == 0:
            allowedTier += 1
            print("RAISING TIER TO: " + str(allowedTier))
            if newUnitCount*2 <= maxUnitCount:
                newUnitCount *= 2
        prPurple("Current round: " + str(roundCount+1) +
              " || " + playerList[0].name + " " + str(playerList[0].score) +
              " : "+ str(playerList[1].score) + " " + playerList[1].name
              )
            

if __name__ == "__main__":
    main()