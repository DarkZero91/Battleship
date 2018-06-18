from player import Player
import numpy as np
import cv2
import random
import copy
from board import Board


class MinmaxAgent(Player):
    def __init__(self, board, name, depth = 0, maxdepth = 3, placeShips=True):
        Player.__init__(self, board, name)
        self.depth = depth
        self.maxdepth = maxdepth
        if placeShips:
            self.placeShips()
        self.killedShips = []
        self.myShips = self.board.grid 
        self.hitGrid = self.board.hitGrid  ##places I hit the opponent
        self.herShipsIKnow = np.zeros_like(self.myShips)
        self.myShipSheKnows = np.zeros_like(self.myShips)
        self.potentialShipLocations = {}
        self.updatePotentialShipLocations()
        
        self.killLocations = {}
        self.potentialKillLocations = {}
        self.initKillLocations()

    def preference(self):
        boardPref = self.board.evaluate()
        intelPref = np.sum(np.sum(self.myShipSheKnows, 1))
        return boardPref - intelPref + random.uniform(-0.1, 0.1)

    def exploreActions(self, opponent):
        size = self.board.gridSize
        madeChoice = False
        bestPref = -1000
        bestX = 0
        bestY = 0
        for y in xrange(size):
            for x in xrange(size):
                if self.board.placesIShot[y,x] == 1 or (self.summedPotentialShipLocations()[y,x] == 0):
                    continue
                #print "explore", x, y, "@depth ", self.depth
                pref = self.exploreAction(opponent, x, y)
                if pref > bestPref:
                    madeChoice = True
                    bestPref = pref
                    bestX = x
                    bestY = y
        if not madeChoice:
            bestPref = random.uniform(-0.1, 0.1)
        self.myShipSheKnows = opponent.herShipsIKnow
        return bestPref, bestX, bestY
    
    def constructOpponentsBoard(self):
        mat = np.zeros_like(self.hitGrid)
        mat[self.board.grid == -1] = 1
        
        grid = np.zeros_like(self.board.grid)
        potmap = self.summedPotentialShipLocations() #HACK
        grid[potmap != 0] = 1
        
        board = Board(self.board.gridSize)
        board.grid = grid #self.herShipsIKnow.copy()
        board.hitGrid = mat
        board.placesIShot = np.zeros_like(board.grid)
        board.placesIShot[self.board.grid < 0] = 1
        
        return board
    
    def exploreAction(self, opponent, x, y):
        #print "depth = ", self.depth, "max = ", self.maxdepth

        if self.depth == self.maxdepth:
            return self.preference()
        futureSelf = copy.deepcopy(self)
        futureSelf.depth += 1
        futureSelf.name = "future_" + self.name
        
        futureOpponent = MinmaxAgent(
                self.constructOpponentsBoard(),  
                "future_" + opponent.name,
                depth=opponent.depth + 1,
                maxdepth = self.maxdepth,
                placeShips=False
            )
        futureOpponent.ships = opponent.ships.copy()#self.herShipsIKnow
        futureOpponent.herShipsIKnow = opponent.herShipsIKnow.copy()
        futureOpponent.killLocations = opponent.killLocations.copy()
        futureOpponent.updatePotentialShipLocations()
        result, kill = futureSelf.shoot(futureOpponent, x, y)
        if result == 1 and kill != "":
            futureSelf.processKill(kill, x, y)
            
        if self.depth < self.maxdepth:
            otherpref, x, y = futureOpponent.exploreActions(futureSelf)
            #print "deeper"
            return -1 * otherpref
        else:
            raise "Searchdepth above maxdepth: Fix your code dumbass!"
            
    def initKillLocations(self):
        for name in self.ships.keys():
            self.killLocations[name] = np.ones_like(self.hitGrid, dtype = np.int16) * -1
            self.potentialKillLocations[name] = np.ones_like(self.hitGrid, dtype = np.int16) * -1
            
    def processKill(self, shipname, x, y):
        self.killLocations[shipname][x,y] = 1
        self.killedShips.append(shipname)
        
    def updatePotentialKillMap(self):

        for name in self.ships.keys():
            if not name in self.killedShips:
                potmap = np.zeros_like(self.hitGrid)
                ship = self.ships[name]
                for mask in ship.masks:
                    kills = np.zeros_like(self.myShips)
                    kills[self.killLocations[name] == 1] = 1
                    result = cv2.filter2D(kills, -1 , mask)
                    potmap += result
                potkill = (potmap != 0) & (self.hitGrid == 1)
                self.potentialKillLocations[name][potkill] = 1
            else:
                self.potentialKillLocations[name] = np.zeros_like(self.hitGrid)
            
    def updatePotentialShipLocations(self):
        for name in self.ships.keys():
            ship = self.ships[name]
            if ship in self.killedShips:
                continue
            potMap = np.zeros_like(self.myShips)
            for mask in ship.masks:
                result = cv2.filter2D(self.hitGrid, -1, mask)
                potMap += result
            potMap[potMap != 0] = 1
            potMap[self.board.placesIShot == 1] = 0
            self.potentialShipLocations[name] = potMap
            
    def summedPotentialShipLocations(self):
        potMap = np.zeros_like(self.myShips)
        for name in self.ships.keys():
            potMap += self.potentialShipLocations[name]
        return potMap
     
    def bestGuess(self, opp):
        pref, x, y = self.exploreActions(opp)
        if self.depth == 0:
            print self.name + " fires at", x, y, "with pref", pref
        return x, y
        potMap = np.zeros_like(self.myShips)
        for name in self.ships.keys():
            potMap += self.potentialShipLocations[name]
        if self.name == "Bob":
            toshow = potMap.copy()
            toshow = toshow.astype(np.float)
            if np.max(np.max(potMap,1)) != 0:
                toshow /= np.max(np.max(potMap,1))
                toshow *= 255
                toshow = toshow.astype(np.uint8)
                cv2.imshow("potmap", toshow)
                cv2.waitKey(20)
            
        y = np.argmax(np.max(potMap, 1))
        x = np.argmax(potMap[y])
        return x, y
    
    def visualize(self):
        if self.name == "Bob" or self.name == "Alice":
            potmap = self.board.grid.copy()
            potmap[potmap > 0 ] = 255
            potmap[potmap == 0 ] = 125
            potmap[potmap == -1] = 80
            potmap[potmap == -2] = 0
            
            
            h, w = potmap.shape
            potmap = np.reshape(potmap, (h,w,1))
            potmap = potmap.astype(np.uint8)
            toshow = cv2.resize(self.myShips, (200,200), cv2.INTER_NEAREST)
            cv2.imshow(self.name + "'s grid", potmap)
            cv2.waitKey(10)
    
    def playRound(self, otherPlayer):
        self.updatePotentialShipLocations()
        self.updatePotentialKillMap()
        x, y = self.bestGuess(otherPlayer)
        if self.board.placesIShot[y, x] == 1:
            print self.name, "fires at random location"
            x = random.randint(0, self.board.gridSize - 1)
            y = random.randint(0, self.board.gridSize - 1)
        result, killed = self.shoot(otherPlayer, x, y)
        if result == 1 and killed != "":
            self.processKill(killed, x, y)
        self.visualize()