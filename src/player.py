from utils import Move

class InvalidLetterError(Exception): ...

class Player:
	def __init__(self):
		self.score = 0
	
	def makeMove(self):
		return ""
	
	def convertToMove(self, move):
		match move:
			case "w":
				return Move.UP
			case "a":
				return Move.LEFT
			case "s":
				return Move.DOWN
			case "d":
				return Move.RIGHT
			case _:
				raise InvalidLetterError