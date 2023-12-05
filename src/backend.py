from board import Board, BoardFullError, IllegalMoveError
from utils import GameState, Move

class gameManager():
	def __init__(self,player):
		# clear_terminal()
		self.board = Board()
		self._status = GameState.IN_PLAY
		self.player = player

	def play(self):
		print("Use WASD to move")
		self.board.display()
		while self._status == GameState.IN_PLAY:
			try:
				self.Move()
				self.board.display()
			except BoardFullError:
				self._status = GameState.LOST
	
	def Move(self):
		move = self.player.makeMove()
		try:
			self.board.updateBoard(move)
		except IllegalMoveError as e:
			print(e)
			self.Move()


	def loadBoard(self, gameState):
		self.board.loadCustomBoard(gameState)
			


