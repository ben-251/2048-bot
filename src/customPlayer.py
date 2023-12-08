from player import Player
from utils import Move

class customPlayer(Player):
	def __init__(self):
		super().__init__()
	
	def makeMove(self, move):
		converted_move = self.convertToMove(move)
		return converted_move
	
