from player import Player
import numpy as np
import cv2
import random

class BDIAgent(Player):
    
    def __init__(self, board, name):
        Player.__init__(self, board, name)
        self.placeShips()
        
        self.myShips = self.board.grid 
        self.hitGrid = self.board.hitGrid
        self.herShipsIKnow = np.zeros_like(self.myShips)
        
        self.potentialShipLocations = {}
        self.updatePotentialShipLocations()
    
    
    
    def updatePotentialShipLocations(self):
        for name in self.ships.keys():
            ship = self.ships[name]
            potMap = np.zeros_like(self.myShips)
            for mask in ship.masks:
                result = cv2.filter2D(self.hitGrid, -1, mask)
                potMap += result
            potMap[potMap != 0] = 1
            self.potentialShipLocations[name] = potMap
            
    def bestGuess(self):
        potMap = np.zeros_like(self.myShips)
        for name in self.ships.keys():
            potMap += self.potentialShipLocations[name]
        y = np.argmax(np.max(potMap, 1))
        x = np.argmax(potMap[y])
        return x, y
    
    def playRound(self, otherPlayer):
        x, y = self.bestGuess()
        if self.board.placesIShot[y, x] == 1:
            x = random.randint(0, self.board.gridSize - 1)
            y = random.randint(0, self.board.gridSize - 1)
        self.shoot(otherPlayer, x, y)
        