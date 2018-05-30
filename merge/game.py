import numpy as np

from bdi_agent import BDIAgent
from board import Board
class Game:
    
    def __init__(self, gridSize):
        self.gridSize = gridSize
        self.p1Board = Board(self.gridSize)
        self.p2Board = Board(self.gridSize)
        
        self.player1 = BDIAgent(self.p1Board, "Alice")
        self.player2 = BDIAgent(self.p2Board, "Bob")
        
        
if __name__ == "__main__":
    game = Game(10)
    game.player1.shoot(game.player2, 2, 2)