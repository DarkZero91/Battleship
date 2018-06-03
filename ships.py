import numpy as np

class Ship(object):
	def __init__(self, size):
            self.hits = 0
            self.size = size
            self.masks = []
            self.generateMasks()
            self.uid = -1
            
        def generateMasks(self):
            self.masks.append(np.ones((1, 2 * self.size - 1)))
            self.masks.append(np.ones((2 * self.size - 1, 1)))
            
        def fits(self, x, y, orientation, board):
            return board.fits(x, y, self.size, orientation) and not board.collides(x, y, self.size, orientation)
        
        def place(self, x, y, orientation, board, uid):
            self.uid = uid
            self.x = x
            self.y = y
            self.orientation = orientation
            board.place(x, y, self.size, orientation, uid)
            
        def alive(self, board):
            return board.isPresent(self.uid)
            
        
                
class Carrier(Ship):
	def __init__(self):
		Ship.__init__(self, 5)

class Battleship(Ship):
	def __init__(self):
		Ship.__init__(self, 4)

class Cruiser(Ship):
	def __init__(self):
		Ship.__init__(self, 3)

class Submarine(Ship):
	def __init__(self):
		Ship.__init__(self, 3)

class Destroyer(Ship):
	def __init__(self):
		Ship.__init__(self, 2)
