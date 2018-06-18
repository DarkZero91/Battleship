import numpy as np


class Board:
    def __init__(self, gridsize):
        self.gridSize = gridsize
        self.grid = np.zeros((self.gridSize,self.gridSize), dtype = np.int16)
        self.hitGrid = np.zeros((self.gridSize,self.gridSize), dtype = np.int16)
        self.placesIShot = np.zeros_like(self.grid)
        
    def fits(self, x, y, size, orientation):
        if orientation == 'h':
            return not (x + size >= self.gridSize)
        elif orientation == 'v':
            return not (y + size >= self.gridSize)
        else:
            raise "Invalid orientation @ fit check"
        
    def evaluate(self):
        partsLeft = np.zeros_like(self.grid)
        partsLeft[self.grid > 0] = 1
        return np.sum(np.sum(self.hitGrid, 1)) + np.sum(np.sum(partsLeft, 1))  ## nr of hits + nr of shipparts left
        
    def processShot(self, x, y, hit):
        self.placesIShot[y, x] = 1
        self.hitGrid[y, x] = hit
        
    def isPresent(self, uid):
        presence = np.zeros_like(self.grid)
        presence[self.grid == uid] = 1
        cnt = np.sum(np.sum(presence, 1))
        return cnt != 0
        
    def getShot(self, x, y):
        val = self.grid[y, x]
        if val == 0:
            self.grid[y, x] = -2 ## I got shot here, but there was nothing there
        else:
            self.grid[y, x] = -1 ## I got shot here, and some shippart was here
        return val
        
    def collides(self, x, y, size, orientation):
        if orientation == 'h':
            return np.dot(self.grid[y, x : x + size], np.ones_like(self.grid[y, x : x + size])) != 0
        elif orientation == 'v':
            return np.dot(self.grid[y : y + size,x], np.ones_like(self.grid[y : y + size, x])) != 0
        else:
            raise "Invalid orientation @ collsision check"
    
    def place(self, x, y, size, orientation, uid):
        if orientation == 'h':
            ship = np.ones((1,size), dtype = np.uint8)
            self.grid[y, x : x + size] += np.ones_like(self.grid[y, x : x + size]) * uid
        elif orientation == 'v':
            ship = np.ones((size, 1), dtype = np.uint8)
            self.grid[y : y + size, x] += np.ones_like(self.grid[y : y + size, x]) * uid
        else:
            raise "Invalid orientation @ ship placement"