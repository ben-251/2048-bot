from player import Player

class InvalidLetterError(Exception): ...

class Human(Player):
	def __init__(self):
		super().__init__()

	def makeMove(self):
		move = input("Enter move: ").lower()
		try:
			converted_move = self.convertToMove(move)
		except InvalidLetterError:
			print("Enter w, a, s, or d.")
			return self.makeMove()
		return converted_move
	

