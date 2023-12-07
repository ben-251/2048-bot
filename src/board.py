import random

from bentests import colorama
from utils import GameState, Move
from typing import List, Optional

class BoardFullError(Exception): ...
class IllegalMoveError(Exception): ...
class NotMoved(Exception): ...

class Board():
	'''
	The board for the game. 
	Cell values are stored as `int`s.
	0 represents empty cells.
	'''
	def __init__(self):
		self.initCells()
		self.spawnTiles(2)
		
	def initCells(self):
		self.cells = []
		ROW_COUNT = 4
		COLUMN_COUNT = 4
		for y in range(ROW_COUNT):
			row = []
			for x in range(COLUMN_COUNT):
				row.append(0)
			self.cells.append(row)
		
	def spawnTiles(self, tileCount:Optional[int]=None):
		'''
		Creates multiple random tiles. If tileCount is not provided, then behaviour matches `self.spawnTile()`.
		'''
		if tileCount is None:
			tileCount = 1
		for _ in range(tileCount):
			self.spawnTile()

	def spawnTile(self):
		'''
		Adds a new random tile (2 or 4) to an empty space on the board. 
		'''
		random_row_num = random.randint(0,3)
		random_col_num = random.randint(0,3)
		if not any([cell != 0 for cell in [row for row in self.cells]]):
			raise BoardFullError("")
		while self.cells[random_row_num][random_col_num] != 0:
			random_row_num = random.randint(0,3)
			random_col_num = random.randint(0,3)
		random_cell_value = random.choice([2,4])
		self.cells[random_row_num][random_col_num] = random_cell_value

	def loadCustomBoard(self, gameState:List[List[int]]):
		self.cells = gameState

	def display(self):
		for row in self.cells:
			for cell in row:
				if cell == 0:
					symbol = "○"
				else:
					symbol = cell
				print(f" {symbol} ",end = "")
			print("")
	
	def updateBoard(self,move):
		# will probably need to implement the up downs seperate from left rights.
		isHorizontal = move == Move.LEFT or move == Move.RIGHT
		if isHorizontal:
			self.slideTilesHorizontally(move)
		else:
			self.slideTilesVertically(move)

	def slideTilesHorizontally(self,move):
		haveTilesMoved:List[bool] = []
		for row in self.cells:
			direction = 1 if move == Move.RIGHT else -1
			current_tile_position = 2 if direction == 1 else 1
			while current_tile_position > -1 and current_tile_position < 4:
				if row[current_tile_position] == 0:
					current_tile_position -= direction
					continue
				try:
					row = self.slideSingleTileHorizontally(row, current_tile_position, direction)
					haveTilesMoved.append(True)
				except NotMoved:
					haveTilesMoved.append(False)
				current_tile_position -= direction
		if not any(haveTilesMoved):
			raise IllegalMoveError("no tiles can move that way")

	def slideSingleTileHorizontally(self, row, current_tile_position, direction):
		hasMoved = False
		hasMerged = False
		while True:
			current_tile = row[current_tile_position]
			if current_tile_position + direction == -1 or current_tile_position + direction == 4:
				break
			next_tile = row[current_tile_position + direction]
			if next_tile == 0:
				self.swapHorizontally(row, current_tile_position, direction)
				hasMoved = True
			elif next_tile == current_tile:
				self.mergeTilesHorizontally(row, current_tile_position, direction)
				hasMerged = True
				break
			else:
				break
			current_tile_position += direction

		if not hasMoved and not hasMerged:
			raise NotMoved() #TODO: refactor out (side effect ish)
		return row

	def slideTilesVertically(self, move):
		haveTilesMoved:List[bool] = []

		for column_index in range(4):
			column_values = [row[column_index] for row in self.cells]
			for row_index, cell_value in enumerate(column_values):
				direction = 1 if move == Move.RIGHT else -1
				current_tile_position = 2 if direction == 1 else 1
				while current_tile_position > -1 and current_tile_position < 4:
					if cell_value == 0:
						current_tile_position -= direction
						continue
					try:
						self.slideSingleTileVertically(row_index, column_index, direction)
						haveTilesMoved.append(True)
					except NotMoved:
						haveTilesMoved.append(False)
					current_tile_position -= direction
		if not any(haveTilesMoved):
			raise IllegalMoveError("no tiles can move that way")

			
	def slideSingleTileVertically(self, column: int, current_row: int, direction: int):
		hasMoved = False
		hasMerged = False
		while True:
			current_tile = self.cells[current_row][column]
			if current_row + direction == -1 or current_row + direction == 4:
				break
			next_tile = self.cells[current_row][column]
			if next_tile == 0:
				self.swapVertically(current_row, column, direction)
				hasMoved = True
			elif next_tile == current_tile:
				self.mergeTilesVertically(current_row, column, direction)
				hasMerged = True
				break
			else:
				break
			current_row += direction

		if not hasMoved and not hasMerged:
			raise NotMoved() #TODO: refactor out (side effect ish)
		return 

	def swapHorizontally(self,row, column, direction):
		buffer = row[column]
		row[column] = row[column + direction]
		row[column + direction] = buffer
	
	def swapVertically(self, row, column, direction):
		buffer = self.cells[row][column]
		self.cells[row][column] = self.cells[row][column+direction]
		self.cells[row][column + direction] = buffer

	def mergeTilesHorizontally(self, row, column, direction):
		row[column + direction] = 2*row[column + direction]
		row[column] = 0

	def mergeTilesVertically(self, row: int, column: int, direction):
		self.cells[row][column + direction] = 2*self.cells[row][column + direction]
		self.cells[row][column] = 0