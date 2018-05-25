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

    def place_ship(self, ship, x, y, orientation):
        self.placedships.append(self.board.place_ship(ship, x, y, orientation))

    def make_guess(self, player, x, y):
        ship = player.board.ship_at_location(x, y)
        if ship != 0:
            sunk = self.board.hit_ship(ship)
            if sunk != 0:
                self.sunkenships.append(sunk)
                self._update_ship_lists(player)

    def print_status(self, enemy):
        self._update_ship_lists(enemy)
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

    def check_won(self):
        if (self.finish):
            print("Gewonnen!")
            return True

    def _update_ship_lists(self, enemy):
        self.remainships = list(set(enemy.placedships) - set(self.sunkenships))
        if self.remainships == []:
            self.finish = True
            self.check_won()
