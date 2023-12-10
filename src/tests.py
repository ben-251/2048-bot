import bentests as bt
import board
import customPlayer
import bot
import backend
from utils import *

class BoardTests(bt.testGroup):
	def __init__(self):
		super().__init__()

	def testBoardDimensions(self):
		new_board = board.Board()
		new_board_dimensions = [len(new_board.cells), len(new_board.cells[0])]
		bt.assertEquals(new_board_dimensions, [4,4])

	def testLoadCustomBoard(self):
		new_board = board.Board()
		new_board.loadCustomBoard(
			[[0,0,0,0],
			[2,4,8,16],
			[16,32,128,4],
			[2,0,0,4]
			]
		)
		bt.assertEquals(
			new_board.cells,
			[[0,0,0,0],
			[2,4,8,16],
			[16,32,128,4],
			[2,0,0,4]
			]
		)

class HorizontalMoves(bt.testGroup):
	def __init__(self):
		super().__init__()

	def testMerge(self):
		player = customPlayer.customPlayer()
		game_manager = backend.gameManager(player)
		game_manager.loadBoard(
			[
				[0,0,2,2],[0,0,0,0],[0,0,0,0], [0,0,0,0]
			]
		)
		game_manager.board.mergeTilesHorizontally(game_manager.board.cells[0],2,1)
		bt.assertEquals(
			game_manager.board.cells,
			[
				[0,0,0,4],[0,0,0,0],[0,0,0,0], [0,0,0,0]
			]			
		)
	
	def testSwap(self):
		new_board = board.Board()
		new_board.loadCustomBoard(
			[
				[0,0,2,2],[0,0,0,0],[0,0,0,0], [0,0,0,0]
			]
		)
		new_board.mergeTilesHorizontally(new_board.cells[0],2,1)
		bt.assertEquals(
			new_board.cells,
			[
				[0,0,0,4],[0,0,0,0],[0,0,0,0], [0,0,0,0]
			]			
		)
	
	def testInvalidRight(self):
		with bt.assertRaises(board.IllegalMoveError):
			player = customPlayer.customPlayer()
			new_board =  board.Board()
			new_board.loadCustomBoard(
				[
					[0,0,0,0],[0,0,0,2],[0,0,0,0],[4,2,4,2]
				]
			)
			move = player.makeMove("d")
			new_board.updateBoard(move)

	def test3_Consecutive(self):
		player = customPlayer.customPlayer()
		new_board = board.Board()
		new_board.loadCustomBoard(
			[[0,0,0,0],[0,4,4,4],[0,0,0,0], [0,0,0,0]]
		)
		move = player.makeMove("d")
		new_board.updateBoard(move)
		bt.assertEquals(
			new_board.cells,
			[[0,0,0,0], [0,0,4,8], [0,0,0,0], [0,0,0,0]]
		)


	def test4_Consecutive(self):
		player = customPlayer.customPlayer()
		game_manager = backend.gameManager(player)
		game_manager.loadBoard(
			[[0,0,0,0],[4,4,4,4],[0,0,0,0], [0,0,0,0]]
		)
		move = player.makeMove("d")
		game_manager.board.updateBoard(move)
		bt.assertEquals(
			game_manager.board.cells,
			[[0,0,0,0], [0,0,8,8], [0,0,0,0], [0,0,0,0]]
		)

	def test_two_pairs(self):
		player = customPlayer.customPlayer()
		game_manager = backend.gameManager(player)
		game_manager.loadBoard(
			[[0,0,0,0],[16,16,4,4],[0,0,0,0], [0,0,0,0]]
		)
		move = player.makeMove("d")
		game_manager.board.updateBoard(move)
		bt.assertEquals(
			game_manager.board.cells,
			[[0,0,0,0], [0,0,32,8], [0,0,0,0], [0,0,0,0]]
		)

	def testMoveThroughGap(self):
		with bt.assertNotRaises(board.IllegalMoveError):
			player = customPlayer.customPlayer()
			game_manager = backend.gameManager(player)
			game_manager.loadBoard(
				[
					[0,0,0,2], [0,0,0,4], [4,0,2,8], [0,0,4,64]
				]
			)
			move = player.makeMove("d")
			game_manager.board.updateBoard(move)

class VerticalMoves(bt.testGroup):
	def __init__(self):
		super().__init__()

	def testMerge(self):
		player = customPlayer.customPlayer()
		game_manager = backend.gameManager(player)
		game_manager.loadBoard(
			[
				[0,0,2,0],[0,0,2,0],[0,0,0,0], [0,0,0,0]
			]
		)
		game_manager.board.mergeTilesVertically(1,2,-1)
		bt.assertEquals(
			game_manager.board.cells,
			[
				[0,0,4,0],[0,0,0,0],[0,0,0,0], [0,0,0,0]
			]			
		)
	
	def testInvalidUp(self):
		with bt.assertRaises(board.IllegalMoveError):
			player = customPlayer.customPlayer()
			game_manager = backend.gameManager(player)
			game_manager.loadBoard(
				[
					[0,16,0,4],
					[0,32,0,2],
					[0,2,0,4],
					[0,4,0,2]
				]
			)
			move = player.makeMove("w")
			game_manager.board.updateBoard(move)

	def test3_Consecutive(self):
		player = customPlayer.customPlayer()
		game_manager = backend.gameManager(player)
		game_manager.loadBoard(
			[
				[0,0,0,0],
				[0,4,0,0],
				[0,4,0,0],
				[0,4,0,0]
			]
		)
		move = player.makeMove("s")
		game_manager.board.updateBoard(move)
		bt.assertEquals(
			game_manager.board.cells,
			[
				[0,0,0,0],
				[0,0,0,0],
				[0,4,0,0],
				[0,8,0,0]
			]
		)

	def test4_Consecutive(self):
		player = customPlayer.customPlayer()
		game_manager = backend.gameManager(player)
		game_manager.loadBoard(
			[[16,0,0,0],
			[16,0,0,0],
			[16,0,0,0],
			[16,0,0,0]]
		)
		move = player.makeMove("s")
		game_manager.board.updateBoard(move)
		bt.assertEquals(
			game_manager.board.cells,
			[[0,0,0,0],
			 [0,0,0,0],
			 [32,0,0,0],
			 [32,0,0,0]]
		)

	def test_two_pairs(self):
		player = customPlayer.customPlayer()
		game_manager = backend.gameManager(player)
		game_manager.loadBoard(
			[[16,0,0,0],[16,0,0,0],[4,0,0,0], [4,0,0,0]]
		)
		move = player.makeMove("w")
		game_manager.board.updateBoard(move)
		bt.assertEquals(
			game_manager.board.cells,
			[[32,0,0,0], [8,0,0,0], [0,0,0,0], [0,0,0,0]]
		)

	def testMoveThroughGap(self):
		player = customPlayer.customPlayer()
		game_manager = backend.gameManager(player)
		game_manager.loadBoard(
			[
				[0,0,4,0],
				[0,0,0,0], 
				[0,0,2,4], 
				[2,4,8,64] 
			]
		)
		move = player.makeMove("w")
		game_manager.board.updateBoard(move)
		bt.assertEquals(
			game_manager.board.cells,
			[
				[2,4,4,4],
				[0,0,2,64], 
				[0,0,8,0], 
				[0,0,0,0] 
			]			
		)

class GamePlay(bt.testGroup):
	def __init__(self):
		super().__init__()
	
	def testGameOver(self):
		player = customPlayer.customPlayer()
		game_manager = backend.gameManager(player)
		game_manager.loadBoard([
			[2,4,8,16],
			[4,8,16,2],
			[8,16,2,4],
			[16,2,4,8]
		])
		validMoves = game_manager.board.getValidMoves()
		bt.assertEquals(validMoves,[])

class StaticEval(bt.testGroup):
	def __init__(self):
		super().__init__()

	def testMaxBlock(self):
		simulated_bot = bot.Bot()
		new_board = board.Board()
		new_board.loadCustomBoard(
			[
				[0,0,0,0], [0,0,0,0], [0,0,0,0], [128, 64, 4, 2]
			]
		)
		max_block = simulated_bot.getMaxBlocks(new_board)[0]
		bt.assertEquals(max_block,[3,0])

	def testMaxBlocks(self):
		simulated_bot = bot.Bot()
		new_board = board.Board()
		new_board.loadCustomBoard(
			[
				[0,0,0,0], [0,64,0,0], [0,0,0,0], [2, 64, 4, 2]
			]
		)
		max_blocks = simulated_bot.getMaxBlocks(new_board)
		bt.assertEquals(max_blocks,[[1,1],[3,0]])

	def testVerticalDistanceFromCorner(self):
		simulated_bot = bot.Bot()
		verticalDistance = simulated_bot.getDistanceFromCorner([0,0])
		bt.assertEquals(verticalDistance,3)	

	def testHorizontalDistanceFromCorner(self):
		simulated_bot = bot.Bot()
		horizontalDistance = simulated_bot.getDistanceFromCorner([0,2])
		bt.assertEquals(horizontalDistance,2)	

	def testDiagonalDistance(self):
		simulated_bot = bot.Bot()
		distance = simulated_bot.getDistanceFromCorner([2,3])
		bt.assertAlmostEquals(distance,3.605551275)						

	def testFullCornerPenalty(self):
		simulated_bot = bot.Bot()
		new_board = board.Board()
		new_board.loadCustomBoard(
			[
				[0,0,0,0],
				[0,64,0,0],
				[0,64,0,0],
				[2, 2, 4, 2]
			]
		)
		corner_penalty = simulated_bot.getCornerPenalty(new_board)
		bt.assertAlmostEquals(corner_penalty,1.4142135)

class Bot(bt.testGroup):
	def __init__(self):
		super().__init__()
	
	def testWinningVerticalMove(self):
		simulated_bot = bot.Bot()
		simulated_board = board.Board()

		simulated_board.loadCustomBoard(
			[[0,0,0,0],
			[0,0,0,0],
			[1024,0,0,0],
			[1024, 0,0,0]
			]
		)
		best_move = simulated_bot.makeMove(simulated_board)
		
		bt.assertEquals(
			best_move, Move.DOWN
		)

	def testWinningHorizontalMove(self):
		simulated_bot = bot.Bot()
		simulated_board = board.Board()

		simulated_board.loadCustomBoard(
			[[0,0,0,0],[0,0,0,0],[1024,1024,0,0],[0, 0,0,0]])
		best_move = simulated_bot.makeMove(simulated_board)
		bt.assertEquals(best_move, Move.DOWN) # any move will be evaluated as good since they're all "forced mate"

	def testWinInTwo(self):
		simulated_bot = bot.Bot()
		simulated_board = board.Board()

		simulated_board.loadCustomBoard(
			[[0,0,0,0],
			[0,0,0,0],
			[512,0,0,0],
			[512, 1024,0,0]
			]
		)
		best_move = simulated_bot.makeMove(simulated_board)
		
		bt.assertEquals(
			best_move, Move.DOWN
		)
	def testObviousBestMove(self):
		simulated_bot = bot.Bot()
		simulated_board = board.Board()

		simulated_board.loadCustomBoard(
			[[0,0,0,0],
			[0,0,0,0],
			[8,0,0,0],
			[8, 16,0,0]
			]
		)
		best_move = simulated_bot.makeMove(simulated_board)
		
		bt.assertEquals(
			best_move, Move.DOWN
		)
	
	def testComplexPosition(self):
		simulated_bot = bot.Bot()
		simulated_board = board.Board()

		simulated_board.loadCustomBoard(
			[[4,2,4,2],
			[16,4,2,4],
			[0,2,32,2],
			[64,32,2,4]
			]
		)
		best_move = simulated_bot.makeMove(simulated_board)
		
		bt.assertEquals(
			best_move, Move.LEFT
		)		

	def testMoreComplexPosition(self):
		simulated_bot = bot.Bot()
		simulated_board = board.Board()

		simulated_board.loadCustomBoard( #TODO: come up with a nice puzzle
			[[4,2,4,2],
			[16,4,2,4],
			[0,2,32,2],
			[64,32,2,4]
			]
		)
		best_move = simulated_bot.makeMove(simulated_board)
		
		bt.assertEquals(
			best_move, Move.LEFT
		)		


bt.test_all(
	BoardTests,
	StaticEval,
	Bot,
	HorizontalMoves,
	VerticalMoves,
	GamePlay,
	stats_amount="low"
)
