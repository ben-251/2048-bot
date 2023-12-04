import random
from typing import List, Optional

class BoardFullError(Exception): ...

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
