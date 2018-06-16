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
        
    def preference(self):
        #TODO: fix preference function
        return 1 #tmp
    
    
    
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