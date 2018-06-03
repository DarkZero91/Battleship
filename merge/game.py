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
        
    
    def playRound(self):
        done = False
        self.player1.playRound(self.player2)
        if self.player2.alive():
            self.player2.playRound(self.player1)
            if not self.player1.alive():
                print self.player1.name + " lost.."
                done = True
        else:
            print self.player2.name + " lost.."
            done = True
        return done
        
if __name__ == "__main__":
    game = Game(10)
    rounds = 0
    done = False
    while not done:
        rounds += 1
        done = game.playRound()
        
    print "game done in ", rounds, " rounds"
        