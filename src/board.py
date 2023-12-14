import copy
import random
import colorama
from utils import GameState, Move
from typing import List, Optional

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
		ROW_COUNT, COLUMN_COUNT = 4, 4
		self.cells = [[0 for i in range(COLUMN_COUNT)] for j in range(ROW_COUNT)]
		
	def spawnTiles(self, tileCount:Optional[int]=None):
		'''
		Creates multiple random tiles. If tileCount is not provided, then behaviour matches `self.spawnTile()`.
		'''
		if tileCount is None:
			tileCount = 1
		for _ in range(tileCount):
			self.spawnTile()

	def spawnTile(self, position: Optional[List[int]]=None, value: Optional[int]=None):
		'''
		Adds a new random tile (2 or 4) to an empty space on the board. 
		'''
		if not position is None and not value is None:
			row_num = position[0]
			col_num = position[1]
			self.cells[row_num][col_num] = value
			return

		random_row_num = random.randint(0,3)
		random_col_num = random.randint(0,3)
		while self.cells[random_row_num][random_col_num] != 0:
			random_row_num = random.randint(0,3)
			random_col_num = random.randint(0,3)
		random_cell_value = random.choice([2,4])
		self.cells[random_row_num][random_col_num] = random_cell_value

	def getLegalSpawnPositions(self) -> List[int]:
		all_positions = []
		for x in range(4):
			all_positions.append([x,y] for y in range(4))
		legal_positions = list(filter(self.isCellEmpty, all_positions))
		return legal_positions

	def isCellEmpty(self, cell_position):
		return self.cells[cell_position[0]][cell_position[1]]

	def loadCustomBoard(self, gameState:List[List[int]]):
		self.cells = copy.deepcopy(gameState)

	def updateBoard(self,move:Move):
		if move in move.HORIZONTAL:
			self.slideTilesHorizontally(move)
		elif move in move.VERTICAL:
			self.slideTilesVertically(move)
		else:
			raise ValueError("invalid move type")

	def slideTilesHorizontally(self,move):
		haveTilesMoved:List[bool] = []
		for row in self.cells:
			direction = 1 if move is Move.RIGHT else -1
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
		for row_index in range(4):
			direction = 1 if move is Move.DOWN else -1
			current_tile_position = 2 if direction == 1 else 1
			while current_tile_position > -1 and current_tile_position < 4:
				if self.cells[current_tile_position][row_index] == 0:
					current_tile_position -= direction
					continue
				try:
					self.slideSingleTileVertically(row_index, current_tile_position, direction)
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

			next_tile = self.cells[current_row+direction][column]
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
		self.cells[row][column] = self.cells[row+direction][column]
		self.cells[row+direction][column] = buffer

	def mergeTilesHorizontally(self, row, column, direction):
		row[column + direction] = 2*row[column + direction]
		row[column] = 0

	def mergeTilesVertically(self, row: int, column: int, direction):
		'''
		If moving up, moves the bottom one into the top. 
		If moving down, moves the top one into the bottom.
		'''
		self.cells[row+direction][column] = 2*self.cells[row][column] 
		self.cells[row][column] = 0

	def isLost(self):
		validMoves = self.getValidMoves()
		return not validMoves

	def hasWon(self, targetNumber = None):
		if targetNumber is None:
			targetNumber = 2048
		return any(((targetNumber in row) for row in self.cells))

	def getValidMoves(self) -> List[Move]:
		validMoves = []
		for move in Move:
			simulation_board = Board()
			simulation_board.loadCustomBoard(self.cells)
			if move in [Move.HORIZONTAL, Move.VERTICAL, Move.NONE]:
				continue
			try:
				simulation_board.updateBoard(move)
				validMoves.append(move)
			except IllegalMoveError:
				pass

		return validMoves

	def display(self):
		print("\n")
		for row in self.cells:
			for cell in row:
				paddingSize = 4-len(str(cell))
				symbol = "○" if cell == 0 else cell
				print(f"{' '*paddingSize}{symbol}{''*paddingSize} ",end = "")
			print("")