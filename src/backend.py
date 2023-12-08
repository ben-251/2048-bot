from board import Board, BoardFullError, IllegalMoveError
from utils import GameState, Move
from customPlayer import customPlayer
from typing import List
import time

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
			if self.isLost():
				self._status = GameState.LOST
				continue
			if self.hasWon():
				self._status = GameState.WON
				continue
			self.move()
			self.board.display()
		self.display_results()

	def display_results(self):
		match self._status:
			case GameState.WON:
				print("YOU WON!")
			case GameState.LOST:
				print("Game over.")
			case _:
				raise RuntimeError(f"Unexpected Gamestate: {self._status}")
	def move(self):
		move = self.player.makeMove(self.board)
		try:
			self.board.updateBoard(move)
			self.board.spawnTile()
		except IllegalMoveError as e:
			print(e)
			self.move()

	def getValidMoves(self) -> List[Move]:
		simulation_board = Board()
		validMoves = []
		for move in Move:
			simulation_board.loadCustomBoard(self.board.cells)
			try:
				simulation_board.updateBoard(move)
				validMoves.append(move)
			except IllegalMoveError:
				pass
			except ValueError:
				pass
		return validMoves

	def loadBoard(self, gameState):
		self.board.loadCustomBoard(gameState)
			

	def isLost(self):
		validMoves = self.getValidMoves()
		if not validMoves:
			return True
		return False

	def hasWon(self, targetNumber = None):
		if targetNumber is None:
			targetNumber = 2048
		for row in self.board.cells:
			for cell in row:
				if cell == targetNumber:
					return True
		return False