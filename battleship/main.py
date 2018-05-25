from battleship.player import *

p1 = Player()
p2 = Player()

p2.place_ship(Cruiser(), 0, 0, 0) # place_ship(type, x, y, orientation)
p2.place_ship(Cruiser(), 1, 2, 0)

# p2.visualize_board()
p2.print_board()

p1.make_guess(p2, 0, 0)
p1.make_guess(p2, 0, 1)
p1.make_guess(p2, 1, 2)

p1.print_enemyhitgrid(p2)
p1.print_status(p2)
