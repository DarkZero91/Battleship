from random import random
from battleship.board import Board
from battleship.ships import *

class Player(object):
    def __init__(self):
        self.color = [random() * 255, random() * 255, random() * 255]
        self.board = Board()
        self.finish = False
        self.remainships = []
        self.placedships = []
        self.sunkenships = []

#------------------------------------------------

    def place_carrier(self, x, y, orientation):
        ship = Carrier()
        self.placedships.append(self.board.place_ship(ship, x, y, orientation))

    def place_battleship(self, x, y, orientation):
        ship = Battleship()
        self.placedships.append(self.board.place_ship(ship, x, y, orientation))

    def place_cruiser(self, x, y, orientation):
        ship = Cruiser()
        self.placedships.append(self.board.place_ship(ship, x, y, orientation))

    def place_submarine(self, x, y, orientation):
        ship = Submarine()
        self.placedships.append(self.board.place_ship(ship, x, y, orientation))

    def place_destroyer(self, x, y, orientation):
        ship = Destroyer()
        self.placedships.append(self.board.place_ship(ship, x, y, orientation))

#--------------------------------------------------

    def make_guess(self, player, x, y):
        ship = player.board.ship_at_location(x, y)
        if ship != 0:
            sunk = self.board.hit_ship(ship)
            if sunk != 0:
                self.sunkenship.append(sunk)
    #     ship = self.
    #
    # for i in range(len(self.ships)):
    #     if self.ships[i] == ship:
    #         self.ships.pop(i)
    #         if self.ships == []:
    #             self.finish = True
    #         break

    def update_ship_lists(self):
        self.remainships = list(set(self.placedships)-set(self.sunkenships))
        if self.remainships == []:
            self.finish = True

    def check_won(self):
        if (self.finish):
            print "Gewonnen!"
            return True

    def print_status(self):
        self.update_ship_lists()
        print("\nStatus:\nShips:")
        print(self.remainships)
        print("Hits:")
        for ship in self.remainships:
            print(ship.name, ship.hits)

    def print_board(self):
        self.board.print_board()

    def visualize_board(self):
        self.board.visualize_board(self.color)

    def print_enemyhitgrid(self, player):
        player.board.print_hitgrid()