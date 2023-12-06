import random
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
					row = self.slideSingleTile(row, current_tile_position, direction)
					haveTilesMoved.append(True)
				except NotMoved:
					haveTilesMoved.append(False)
				current_tile_position -= direction
		if not any(haveTilesMoved):
			raise IllegalMoveError("no tiles can move that way")

	def slideSingleTile(self, row, current_tile_position, direction):
		hasMoved = False
		hasMerged = False
		while True:
			current_tile = row[current_tile_position]
			if current_tile_position + direction == -1 or current_tile_position + direction == 4:
				break
			next_tile = row[current_tile_position + direction]
			if next_tile == 0:
				self.swap(row, current_tile_position, direction)
				hasMoved = True
			elif next_tile == current_tile:
				self.mergeTiles(row, current_tile_position, direction)
				hasMerged = True
				break
			else:
				break
			current_tile_position += direction

		if not hasMoved and not hasMerged:
			raise NotMoved() #TODO: refactor out (side effect ish)
		return row

	def swap(self,row, starting_cell_position, direction):
		buffer = row[starting_cell_position]
		row[starting_cell_position] = row[starting_cell_position + direction]
		row[starting_cell_position + direction] = buffer

	def mergeTiles(self, row, current_tile_position, direction):
		row[current_tile_position + direction] = 2*row[current_tile_position + direction]
		row[current_tile_position] = 0

	def slideTilesVertically(self, move):
		...
			