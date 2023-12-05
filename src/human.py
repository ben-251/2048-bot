from player import Player
from utils import Move

class Human(Player):
	def __init__(self):
		super().__init__()

	def makeMove(self):
		move = input("enter move").lower()
		try:
			converted_move = Move(move)
		except KeyError:
			print("Enter w, a, s, or d.")
			return self.makeMove()
		return converted_move