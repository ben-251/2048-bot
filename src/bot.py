import math
from typing import Optional, List, Tuple

from numpy import block
from backend import gameManager
from board import Board, IllegalMoveError
from player import Player
from customPlayer import customPlayer
from utils import Move

class Bot(Player):
	WEIGHT_MAP = [
		[-16.0, -16.0, -16.0, -16.0],
		[-5.4, -5.6, -5.8, -6.0], 
		[+1.0, +1.0, +2.0, +3.0], 
		[+50.0, +7.0, +6.0, +5.0]
	]

	def __init__(self):
		super().__init__()
		self.bestMove = Move.NONE #TODO: remove this montrosity
	
	def computeStaticEval(self, game_state: Board) -> float:
		evaluation = self.calculateWeightedEval(game_state)
		corner_penalty = self.getCornerPenalty(game_state)
		evaluation -= corner_penalty
		return evaluation

	def calculateWeightedEval(self, game_state):
		current_eval = 0
		for weight_row, board_row in zip(self.WEIGHT_MAP, game_state.cells):
			for weight, cell in zip(weight_row, board_row):
				current_eval += weight * cell
		return current_eval

	def getCornerPenalty(self, game_state):
		CORNER_WEIGHT = 15
		maxBlocks = self.getMaxBlocks(game_state)
		corner_penalty = min(map(self.getDistanceFromCorner, maxBlocks))
		return corner_penalty*CORNER_WEIGHT

	def getMaxBlocks(self, board: Board) -> List[List[int]]:
		max_block_value = 0
		max_blocks = []
		for row_number, row in enumerate(board.cells):
			for cell_number, cell in enumerate(row):
				current_position = [row_number, cell_number]
				if cell == max_block_value:
					max_blocks.append(current_position)
				elif cell > max_block_value:
					max_block_value = cell
					max_blocks = [current_position]
		return max_blocks
				
	def getDistanceFromCorner(self, block_position) -> float:
		delta_height = 3 -  block_position[0]
		delta_length = block_position[1] # - 0
		distance = (delta_height**2 + delta_length**2)**0.5
		return distance

	def minimax(self, board: Board, maxDepth: int, current_depth: Optional[int]=None, alpha: Optional[float]=None, beta: Optional[float] = None, isBotTurn: Optional[bool]=None, bestMove: Optional[Move]=None) -> Tuple[Move, float]:
		simulated_board = Board()
		simulated_board.loadCustomBoard(board.cells)
		if alpha is None:
			alpha = -math.inf
		if beta is None:
			beta = math.inf
		if isBotTurn is None:
			isBotTurn = True
		if current_depth is None:
			current_depth = maxDepth
		if bestMove is None:
			bestMove = Move.NONE

		if current_depth == 0:
			return bestMove, self.computeStaticEval(simulated_board)
		if simulated_board.isLost():
			return bestMove, -math.inf
		elif simulated_board.hasWon():
			return bestMove, math.inf

		if isBotTurn:
			best = -math.inf
			legalMoves = simulated_board.getValidMoves()
			for move in legalMoves:		
				simulated_board = Board()
				simulated_board.loadCustomBoard(board.cells)
				simulated_board.updateBoard(move)
				computer_best_move, evaluation = self.minimax(simulated_board, maxDepth, current_depth = current_depth-1, alpha=alpha, beta=beta, isBotTurn=False, bestMove = None)
				if evaluation > best:
					if current_depth == maxDepth:
						bestMove =  move # i know its disgusting i cant think of any oother wayy
					best = evaluation
				alpha = max(alpha, evaluation)
				if beta <= alpha:
					break
			# return bestmove, best eval
		else:
			best = math.inf
			possibleSpawns =self.getLegalSpawns(board)
			for spawn_position in possibleSpawns:
				simulated_board = self.simulateTileSpawn(board, spawn_position)
				human_best_move, evaluation = self.minimax(simulated_board, maxDepth, current_depth=current_depth-1, alpha=alpha, beta=beta, isBotTurn=True)
				best = min(evaluation, best)
				beta = min(beta, evaluation)
				if alpha >= beta:
					break
			# return bestmove, best eval

		        
		return bestMove, best

	def simulatePlayerMove(self): ...

	def simulateTileSpawn(self, board: Board, spawn_position: Tuple):
		simulated_board = Board()
		simulated_board.loadCustomBoard(board.cells)
		simulated_board.spawnTile(position=spawn_position[0],value=spawn_position[1])
		return simulated_board
	
	def getLegalSpawnPositions(self, board: Board) -> List[int]:
		legal_positions = []
		for row_num, row in enumerate(board.cells):
			for cell_num, cell in enumerate(row):
				if cell == 0:
					legal_positions.append([row_num, cell_num])
		return legal_positions

	def getLegalSpawns(self, board: Board):
		legal_positions = self.getLegalSpawnPositions(board)
		legal_spawns = self.generateLegalSpawns(legal_positions)
		return legal_spawns

	def generateLegalSpawns(self, legal_positions) -> List[Tuple[List[int], int]]:
		spawns = []
		for position in legal_positions:
			spawns.append((position, 2))
			spawns.append((position, 4))
		return spawns

	def makeMove(self, board):
		bestMove, evaluation = self.minimax(board, 4)
		return bestMove
