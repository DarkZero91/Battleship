from battleship.player import *

p1 = Player()
p1.place_cruiser(0, 0, 0)

p2 = Player()
p2.place_cruiser(1, 2, 0)

# p1.visualize_board()
p2.print_board()

p1.make_guess(p2, 0, 0)
p1.make_guess(p2, 0, 1)
p1.make_guess(p2, 1, 2)

# TO TEST THE WHOLE BOARD
# for i in range(b.width):
#     for j in range(b.height):
#         b2.hit_grid[j][i] = b2.ship_at_location(b, i, j)

if not p1.check_won():
    p2.print_hitgrid()
    p1.print_status()
