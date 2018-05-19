from battleship.board import *
from battleship.ships import *

b = Board()
bs = Cruiser()
bs2 = Cruiser()
b.place_ship(bs, 0, 0, 0)
# b.place_ship(bs2, 1, 4, 0)

b2 = Board()
b2s = Cruiser()
b2.place_ship(b2s, 1, 2, 0)

# FORMAT: playerBoard.hit_grid[y][x] = ship_at_location(opponentBoard, x, y)
b2.ship_at_location(b, 0, 0)
b2.ship_at_location(b, 0, 1)
b2.ship_at_location(b, 1, 4)
b2.ship_at_location(b, 0, 2)

# TO TEST THE WHOLE BOARD
# for i in range(b.width):
#     for j in range(b.height):
#         b2.hit_grid[j][i] = b2.ship_at_location(b, i, j)

if not b2.check_won():
    b2.print_hitgrid()
    b2.print_status(b)
