from random import random

import numpy as np
from PIL import Image

class Board(object):
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.color = [random()*255, random()*255, random()*255]
        self.reset_board()

    def ship_at_location(self, x, y):
        return self.grid[y][x] != 0

    # orientation may be one of:
    # 0 -> up to down,
    # 90 -> right to left,
    # 180-> down to up,
    # 270 -> left to right
    def place_ship(self, ship, x, y, orientation):
        locations = self._calculate_locations(ship, x, y, orientation)
        i = 0

        for location in locations:
            if self._valid_location(location[0], location[1]):
                i += 1
                self.grid[location[1]][location[0]] = ship
            else:
                # Backtrack
                for j in range(0, i):
                    self.grid[locations[j][1]][locations[j][0]] = 0
                print("FAULTY PLACEMENT")
                return False

        self.print_board()
        self.visualize_board()
        return True

    def reset_board(self):
        self.grid = [[0] * self.width for x in range(self.height)]
        self.hit_grid = [[0] * self.width for x in range(self.height)]

    def print_board(self):
        for row in self.grid:
            print('{:4}'.format(str(row)))

    def visualize_board(self):

        w, h = self.width, self.height
        data = np.zeros((h, w, 3), dtype=np.uint8)
        for i in range(self.height):
            for j in range(self.width):
                if type(self.grid[i][j]) is not int:
                    data[i][j] = self.color
        img = Image.fromarray(data, 'RGB')
        img = img.resize(size=(1000, 1000))
        img.show()

    def _valid_location(self, x, y):
        valid = True
        # Check if location exists on the grid
        valid = valid and (x >= 0 and y >= 0 and x < self.width and y < self.height)
        # Check if location is occupied
        valid = valid and (self.grid[y][x] == 0)

        return valid

    def _calculate_locations(self, ship, x, y, orientation):
        locations = []
        for i in range(0, ship.size):
            if orientation == 0:
                xx = x
                yy = y + i
            elif orientation == 90:
                xx = x - i
                yy = y
            elif orientation == 180:
                xx = x
                yy = y - i
            elif orientation == 270:
                xx = x + i
                yy = y

            locations.append((xx, yy))
        return locations
