from player import Player
from board import Board
import numpy as np
import cv2
import random
import copy

#TODO: (add missing/required functions from BDIAgent class) xor (inheret from BDIAgent + add overloads) (first is probably nicest)
class MinmaxAgent(Player):
    
    def __init__(self, board, name, depth = 0, maxdepth):
        Player.__init__(self, board, name)
        self.depth = depth
        self.maxdepth = maxdepth
        self.placeShips()
        self.killedShips = []
        self.myShips = self.board.grid 
        self.hitGrid = self.board.hitGrid
        self.herShipsIKnow = np.zeros_like(self.myShips)
        
        self.potentialShipLocations = {}
        self.updatePotentialShipLocations()
        
        self.killLocations = {}
        self.potentialKillLocations = {}
        self.initKillLocations()
        
        
        
    def preference(self):
        #TODO: fix preference function
        boardPref = self.board.evaluate()
        #intelPref = np.sum(np.sum(placesTheOpponent knows I have a shippart there, 1))
        
        return boardPref #+ intelPref
    
    
    
    def exploreActions(self, opponent):
        size = self.board.gridSize
        bestPref = -100
        bestX = 0
        bestY = 0
        
        for y in xrange(size):
            for x in xrange(size):
                #TODO: add check here whether this place is already shot at, or can be skipped for some other reason.
                #if skippable:
                #   continue
                pref = self.exploreAction(opponent, x, y)
                if pref > bestPref:
                    bestPref = pref
                    bestX = x
                    bestY = y
        return bestPref, bestX, bestY
    
    def constructOpponentsBoard(self):
        #TODO construct opponents board given the intel I know
    
    
    def exploreAction(self, opponent, x, y):

        futureSelf = copy.deepcopy(self)
        futureSelf.depth += 1
        
        futureOpponent = copy.deepcopy(opponent)
        #TODO: give oppenent a board according to the intell I know
        #futureOpponent.board = self.constructOpponentsBoard()
        futureOpponent.depth += 1
        
        result, kill = futureSelf.shoot(futureOpponent, x, y)
        if result == 1 and kill != "":
            futureSelf.processKill(kill, x, y)
            
        if self.depth == self.maxdepth:
            return self.preference()
        elif self.depth < self.maxdepth:
            otherpref, x, y = futureOpponent.exploreActions(futureSelf)
            return -1 * otherpref
        else:
            except "Searchdepth above maxdepth: Fix your code dumbass!"
            
            
            
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
            potMap = np.zeros_like(self.myShips)
            for mask in ship.masks:
                result = cv2.filter2D(self.hitGrid, -1, mask)
                potMap += result
            potMap[potMap != 0] = 1
            potMap[self.board.placesIShot == 1] = 0
            self.potentialShipLocations[name] = potMap
            
    def bestGuess(self):
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
        if self.name == "Bob":
            potmap = self.potentialKillLocations["Battleship"].copy()
            potmap[potmap == 0] = 0
            potmap[potmap == -1] = 0
            potmap[potmap == 1] = 255
            h, w = potmap.shape
            potmap = np.reshape(potmap, (h,w,1))
            potmap = potmap.astype(np.uint8)
            toshow = cv2.resize(self.myShips, (100,100), cv2.INTER_NEAREST)
            cv2.imshow("bob potKillMap", potmap)
            cv2.waitKey(1000)
    
    def playRound(self, otherPlayer):
        self.updatePotentialShipLocations()
        self.updatePotentialKillMap()
        x, y = self.bestGuess()
        if self.board.placesIShot[y, x] == 1:
            print self.name, "fires at random location"
            x = random.randint(0, self.board.gridSize - 1)
            y = random.randint(0, self.board.gridSize - 1)
        result, killed = self.shoot(otherPlayer, x, y)
        if result == 1 and killed != "":
            self.processKill(killed, x, y)
        self.visualize()