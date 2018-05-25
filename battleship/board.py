import numpy as np
from PIL import Image

class Board(object):
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.reset_board()

    def ship_at_location(self, x, y):
        ship = self.grid[y][x]
        if ship != 0:
            self.hit_grid[y][x] = True
        else:
            self.hit_grid[y][x] = False
        return ship

    def hit_ship(self, ship):
        ship.hits += 1
        if ship.hits == ship.size:
            return ship
        else:
            return 0

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

        return ship

    def reset_board(self):
        self.grid = [[0] * self.width for x in range(self.height)]
        self.hit_grid = [[0] * self.width for x in range(self.height)]

    def visualize_board(self, color):
        w, h = self.width, self.height
        data = np.zeros((h, w, 3), dtype=np.uint8)
        for i in range(self.height):
            for j in range(self.width):
                if type(self.grid[i][j]) is not int:
                    data[i][j] = color
        img = Image.fromarray(data, 'RGB')
        img = img.resize(size=(1000, 1000))
        img.show()

    def print_hitgrid(self):
        print("\nHitgrid:")
        for row in self.hit_grid:
            print('{:4}'.format(str(row)))

    def print_board(self):
        print("\nBord:")
        for row in self.grid:
            print('{:4}'.format(str(row)))

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
