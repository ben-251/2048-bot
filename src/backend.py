from board import Board, BoardFullError, IllegalMoveError
from utils import GameState, Move
from customPlayer import customPlayer

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
			validMoves = self.getValidMoves()
			if not validMoves:
				self._status = GameState.LOST
				continue
			self.Move()
			self.board.display()
	
	def Move(self):
		move = self.player.makeMove()
		try:
			self.board.updateBoard(move)
			self.board.spawnTile()
		except IllegalMoveError as e:
			print(e)
			self.Move()

	def getValidMoves(self):
		simulation_board = Board()
		simulation_board.loadCustomBoard(self.board.cells)
		validMoves = []
		for move in Move:
			try:
				simulation_board.updateBoard(move)
				validMoves.append(move)
			except IllegalMoveError:
				pass
		return validMoves
		
	def loadBoard(self, gameState):
		self.board.loadCustomBoard(gameState)
			


