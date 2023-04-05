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

maxUnitCount = 256
Tier1MaxUnits = 256
Tier2MaxUnits = 128
Tier3MaxUnits = 100
Tier4MaxUnits = 10
Tier5MaxUnits = 5
Tier6MaxUnits = 1


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
                  ", Active: " + str(self.isActive))
        else:
            prRed(self.unitName +
                  " ("+ self.categoryName + ")"
                  ", Count: " + str(self.count) + 
                  ", Active: " + str(self.isActive))

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
            return proposedCount
        elif self.tier == 3:
            return proposedCount
        elif self.tier == 4:
            return 1
        elif self.tier == 5:
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
                prYellow(self.unitName + " was evolved! (Tier1)")
                return True
            else:
                return False
        elif self.tier == 2:
            if self.count*2 <= Tier2MaxUnits:
                self.count = self.count*2
                prYellow(self.unitName + " was evolved! (Tier2)")
                return True
            else:
                return False
        elif self.tier == 3:
            if self.count+10 <= Tier3MaxUnits:
                self.count = self.count+10
                prYellow(self.unitName + " was evolved! (Tier3)")
                return True
            else:
                return False
        elif self.tier == 4:
            if self.count+2 <= Tier4MaxUnits:
                self.count = self.count+2
                prYellow(self.unitName + " was evolved! (Tier4)")
                return True
            else:
                return False
        elif self.tier == 5:
            if self.count+1 <= Tier5MaxUnits:
                self.count = self.count+1
                prYellow(self.unitName + " was evolved! (Tier5)")
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
    def drawUnit(self, allowedTier, unitCount):
    #------------------------------
        file = open("unitList.json")
        unitData = json.load(file)
        drawnTier = 100

        # Draw until an allowed unit is drawn
        while drawnTier > allowedTier:
            categoryNr = random.randint(0,len(self.unitList)-1)
            unitNr = random.randint(0,self.unitList[categoryNr]-1)
            isActive = len(self.deck) < 4
            drawnTier = unitData['categories'][categoryNr]['units'][unitNr]['tier']
            # print("Drew Unit of tier: " + str(drawnTier) + ", allowed: "
            #       + str(allowedTier) + " , roundet unitcount: "
            #       + str(round(unitCount/drawnTier)))

        drawnUnit = Unit(categoryNr, unitNr, unitCount, isActive)
        print(self.name + ", you drew: ", end='')
        drawnUnit.printStats()
        # check if already in deck
        if self.evolveUnitIfInDeck(categoryNr, unitNr):
            return

        self.addUnit(drawnUnit)

    #------------------------------
    def evolveUnitIfInDeck(self, categoryNr, unitNr):
    #------------------------------
        for currentUnit in self.deck:
            if currentUnit.categoryNr == categoryNr and currentUnit.unitNr == unitNr:
                if currentUnit.evolveUnit():
                    print("Cool, you already had this unit. It was evolved!")
                else: 
                    print("Sorry, you have this unit but it is already maxed out")
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
    playerList = [Player("martin"), Player("mathias")]
    print("---------------------------------------------------------------")
    print("----------------NEW GAME---------------------------------------")
    print("---------------------------------------------------------------")
    print()

    #first draw for each player
    for currentPlayer in playerList:
        currentPlayer.drawUnit(1, 1)
        print("---------------------------------------------------------------")

    roundCount = 0
    allowedTier = 1
    newUnitCount = 1

    while 1:
        print("---------------------------------------------------------------")
        for currentPlayer in playerList:
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
            currentPlayer.drawUnit(allowedTier, newUnitCount)

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
        if roundCount %5 == 0:
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