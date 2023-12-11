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
			# if self.board.isLost():
			# 	self._status = GameState.LOST
			# 	continue
			if self.board.hasWon():
				self._status = GameState.WON
				continue
			try:
				self.move()
			except BoardFullError as e:
				print(e)
				self._status = GameState.LOST
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

	def loadBoard(self, gameState):
		self.board.loadCustomBoard(gameState)
			

