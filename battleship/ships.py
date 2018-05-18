class Ship(object):
	def __init__(self):
		self.hits = 0

class Carrier(Ship):
	def __init__(self):
		super(Carrier, self).__init__()
		self.name = "Carrier"
		self.size = 5

class Battleship(Ship):
	def __init__(self):
		super(Battleship, self).__init__()
		self.name = "Battleship"
		self.size = 4

class Cruiser(Ship):
	def __init__(self):
		super(Cruiser, self).__init__()
		self.name = "Cruiser"
		self.size = 3

class Submarine(Ship):
	def __init__(self):
		super(Submarine, self).__init__()
		self.name = "Submarine"
		self.size = 3

class Destroyer(Ship):
	def __init__(self):
		super(Destroyer, self).__init__()
		self.name = "Destroyer"
		self.size = 2
