import math
from typing import Optional, List, Tuple
from backend import gameManager
from board import Board, IllegalMoveError
from player import Player
from customPlayer import customPlayer
from utils import Move

class Bot(Player):
	WEIGHT_MAP = [
		[-7.6, -7.8, -8.0, -8.0], #-125.6
		[-1.4, -1.6, -1.8, -2.0], # -27.2
		[-1.0, -0.8, -0.4, -0.2], # -10
		[+1.0, +0.8, +0.6, +0.4]
	]

	def __init__(self):
		super().__init__()
	
	def computeStaticEval(self, game_state: Board) -> float:
		current_eval = 0
		for weight_row, board_row in zip(self.WEIGHT_MAP, game_state.cells):
			for weight, cell in zip(weight_row, board_row):
				current_eval += weight * cell
		#TODO: return -inf if lost and +inf if won.
		return current_eval

	def minimax(self, board: Board, depth: int, alpha: Optional[float]=None, beta: Optional[float] = None, isBotTurn: Optional[float]=None) -> float:
		simulated_player = customPlayer()
		simulated_game_manager = gameManager(simulated_player)
		simulated_game_manager.loadBoard(board.cells)
		if alpha is None:
			alpha = -math.inf
		if beta is None:
			beta = math.inf
		if isBotTurn is None:
			isBotTurn = True	
		if depth == 0:
			return self.computeStaticEval(simulated_game_manager.board)
		if simulated_game_manager.isLost():
			return -math.inf
		elif simulated_game_manager.hasWon():
			return math.inf


		if isBotTurn:
			best = -math.inf
			legalMoves = simulated_game_manager.getValidMoves()
			legalMoves
			for move in legalMoves:
				letter_for_move = simulated_player.convertToLetter(move)
				simulated_game_manager.loadBoard(board.cells) # or maybe redefine simulated manager and player just to be sure there are no side effects
				simulated_player.makeMove(letter_for_move)
				evaluation = self.minimax(simulated_game_manager.board, depth-1, alpha, beta, isBotTurn=False)
				if evaluation > best:
					self.bestMove =  move # i know its disgusting i cant think of any oother wayy
					best = evaluation
				alpha = max(alpha, evaluation)
				if beta <= alpha:
					break
		else:
			best = math.inf
			legalSpawnPositions = self.getLegalSpawnPositions(board)
			possibleSpawns = self.getLegalSpawns(legalSpawnPositions)
			for spawn_position in possibleSpawns:
				simulated_game_manager.board.spawnTile(position=spawn_position[0],value=spawn_position[1]) # or maybe redefine simulated manager and player just to be sure there are no side effects
				evaluation = self.minimax(simulated_game_manager.board, depth-1, alpha, beta, isBotTurn=True)
				best = min(evaluation, best)
				beta = min(beta, evaluation)
				if alpha >= beta:
					break
		return best
	
	def getLegalSpawnPositions(self, board: Board) -> List[int]:
		legal_positions = []
		for row_num, row in enumerate(board.cells):
			for cell_num, cell in enumerate(row):
				if cell == 0:
					legal_positions.append([row_num, cell_num])
		return legal_positions

	def getLegalSpawns(self, legal_positions) -> List[Tuple[List[int], int]]:
		spawns = []
		for position in legal_positions:
			spawns.append((position, 2))
			spawns.append((position, 4))
		return spawns

	def makeMove(self, board):
		self.minimax(board, 2)
		return self.bestMove
