from board import Board
from ships import *
import random

class Player:
    
    def __init__(self, board, name):
        self.board = board
        

        self.name = name
        self.ships = {"Carrier" : Carrier(), "Battleship" : Battleship(), "Cruiser" : Cruiser(),"Submarine" : Submarine(),"Destroyer" : Destroyer()}
        
    
    def placeShips(self):
        nonce = 1
        for name in self.ships.keys():
            ship = self.ships[name]
            fits = False
            while not fits:
                orientation = 'h'
                x = random.randint(0, self.board.gridSize)
                y = random.randint(0, self.board.gridSize - ship.size)
                if random.randint(0,1) == 1:
                    orientation = 'v'
                    b = x
                    x = y
                    y = b
                fits = ship.fits(x, y, orientation, self.board)
                if fits:
                    ship.place(x, y, orientation, self.board, nonce)
                    nonce += 1
                    
    def getShot(self, x, y):
        uid = self.board.getShot(x, y)
        killed = ""
        if uid != 0:
            for name in self.ships:
                ship = self.ships[name]
                if ship.uid != uid:
                    continue
                alive = ship.alive(self.board)
                if not alive:
                   killed = name
            return 1, killed
        return 0, killed
    
    
    def shoot(self, player, x, y):
        result, killed = player.getShot(x,y)
        self.board.processShot(x,y, result)
        #DEBUG
        if result == 0:
            print "MISS!"
        else:
            print "HIT!"
            