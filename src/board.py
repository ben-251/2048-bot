import copy
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
		if not any([cell != 0 for cell in [row for row in self.cells]]):
			raise BoardFullError("")
		while self.cells[random_row_num][random_col_num] != 0:
			random_row_num = random.randint(0,3)
			random_col_num = random.randint(0,3)
		random_cell_value = random.choice([2,4])
		self.cells[random_row_num][random_col_num] = random_cell_value

	def loadCustomBoard(self, gameState:List[List[int]]):
		self.cells = copy.deepcopy(gameState)

	
	def updateBoard(self,move:Move):
		if move is move.HORIZONTAL or move is move.VERTICAL:
			raise ValueError

		if move in move.HORIZONTAL:
			self.slideTilesHorizontally(move)
		elif move in move.VERTICAL:
			self.slideTilesVertically(move)
		elif move is move.NONE:
			raise BoardFullError("Game over")
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
		if not validMoves:
			return True
		return False

	def hasWon(self, targetNumber = None):
		if targetNumber is None:
			targetNumber = 2048
		for row in self.cells:
			for cell in row:
				if cell == targetNumber:
					return True
		return False

	def getValidMoves(self) -> List[Move]:
		simulation_board = Board()
		validMoves = []
		for move in Move:
			simulation_board.loadCustomBoard(self.cells)
			try:
				simulation_board.updateBoard(move)
				validMoves.append(move)
			except IllegalMoveError:
				pass
			except BoardFullError:
				pass
			except ValueError:
				pass
		return validMoves

	def display(self):
		print("\n")
		for row in self.cells:
			for cell in row:
				paddingSize = 4-len(str(cell))
				if cell == 0:
					symbol = "○"
				else:
					symbol = cell
				print(f"{' '*paddingSize}{symbol}{''*paddingSize} ",end = "")
			print("")