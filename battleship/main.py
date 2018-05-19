from battleship.board import *
from battleship.ships import *

b = Board()
s = Cruiser()
b.place_ship(s, 0, 0, 0)

b2 = Board()
s2 = Cruiser()
b2.place_ship(s2, 1, 2, 0)


for i in range(b.height):
    for j in range(b.width):
        b2.hit_grid[j][i] = b2.ship_at_location(b, i, j)

b2.print_hitgrid()
