import numpy as np
import cv2
import random

class Player:

    def __init__(self, name):
        self.name = name
        self.gridSize = 10
        self.grid = np.zeros((self.gridSize,self.gridSize), dtype = np.uint8)
        self.shot = np.zeros((self.gridSize,self.gridSize), dtype = np.uint8)

        self.hitGrid = np.zeros((self.gridSize,self.gridSize), dtype = np.uint8)
        self.shipSizes = [5,4,3,3,2]
        self.potentialShipMaps = np.zeros((len(self.shipSizes), self.gridSize, self.gridSize), dtype = np.uint8)
        self.shipMasks = []
        self.generateShipMasks()
        self.placeShips()
    
    def placeShips(self):
        for ship in self.shipSizes:
            fits = False
            while not fits:
                orientation = 'h'
                x = random.randint(0, self.gridSize)
                y = random.randint(0, self.gridSize - ship)
                if random.randint(0,1) == 1:
                    orientation = 'v'
                    b = x
                    x = y
                    y = b
                fits = self.fits(x, y, ship, orientation) and not self.collides(x, y, ship, orientation)
                if fits:
                    self.place(x, y, ship, orientation)
                
    def generateShipMasks(self):
        for size in self.shipSizes:
            masks = []
            masks.append(np.ones((size * 2 - 1, 1))) #vertical mask
            masks.append(np.ones((1, size * 2 - 1))) #horizontal mask
            self.shipMasks.append(masks)
            
    def fits(self, x, y, size, orientation):
        if orientation == 'h':
            return not (x + size >= self.gridSize)
        elif orientation == 'v':
            return not (y + size >= self.gridSize)
        else:
            raise "Invalid orientation @ fit check"
        
    def collides(self, x, y, size, orientation):
        if orientation == 'h':
            return np.dot(self.grid[y, x : x + size], np.ones_like(self.grid[y, x : x + size])) != 0
        elif orientation == 'v':
            return np.dot(self.grid[y : y + size,x], np.ones_like(self.grid[y : y + size, x])) != 0
        else:
            raise "Invalid orientation @ collsision check"
        
            
        
    def place(self, x, y, size, orientation):
        if orientation == 'h':
            ship = np.ones((1,size), dtype = np.uint8)
            self.grid[y, x : x + size] += np.ones_like(self.grid[y, x : x + size])
        elif orientation == 'v':
            ship = np.ones((size, 1), dtype = np.uint8)
            self.grid[y : y + size, x] += np.ones_like(self.grid[y : y + size, x])
        else:
            raise "Invalid orientation @ ship placement"
        
    
        
    def updatePotentialShipMaps(self):
        for sIdx in xrange(len(self.shipSizes)):
            for mask in self.shipMasks[sIdx]:
                result = np.zeros_like(self.potentialShipMaps[sIdx])
                result = cv2.filter2D(self.hitGrid, -1, mask)
                shipmap = self.potentialShipMaps[sIdx]
                shipmap += result
                shipmap[shipmap != 0] = 1
                shipmap[self.shot == 1] = 0
                
    def best_guess(self):
        potention = np.zeros_like(self.grid, dtype = np.uint8)
        for sIdx in xrange(len(self.shipSizes)):
            potention += self.potentialShipMaps[sIdx]
        
        print np.max(potention,1)
        
        y = np.argmax(np.max(potention, 1))
        x = np.argmax(potention[y])
        max = np.max(np.max(potention))
        cv2.imshow("heatmap" + self.name, cv2.resize(potention, (100,100), interpolation = cv2.INTER_NEAREST) * (255. / max))
        print "best guess", x, y
        return x, y
                
    
    def shoot(self,other):
        x, y = self.best_guess()
        if self.shot[y,x] == 1:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
        print "shooting ", x, y
        hit = other.get_shot(x, y)
        self.shot[y,x] = 1
        if hit:
            print "hit!"
            self.hitGrid[y, x] = 1
        else:
            print "miss.."
    
    def get_shot(self, x, y):
        hit = self.grid[y, x] == 1

        self.grid[y, x] = 0
        return hit
    
    def lost(self):
        return np.sum(np.sum(self.grid)) == 0
    
    def render(self):
        h, w = self.grid.shape
        cv2.imshow(self.name + 'grid', cv2.resize(self.grid, (100,100),interpolation =  cv2.INTER_NEAREST) * 255)
        cv2.imshow(self.name + 'hitgrid', cv2.resize(self.hitGrid,(100,100),interpolation = cv2.INTER_NEAREST) * 255)
        cv2.imshow(self.name + "potentatial_destroyers", cv2.resize(self.potentialShipMaps[4],(100,100),interpolation = cv2.INTER_NEAREST) * 255)
        cv2.waitKey(200)
    
if __name__ == "__main__":
    p1 = Player("p1")
    p2 = Player("p2")
    for idx in xrange(1000):

        p1.shoot(p2)
        p1.updatePotentialShipMaps()
        p1.render()
        p2.render()
        if p2.lost():
            print "p2 lost"
            break

        p2.shoot(p1)
        p2.updatePotentialShipMaps()
        p2.render()
        p1.render()
        if p1.lost():
            print "p1 lost"
            break
    raw_input("press enter to quit..")