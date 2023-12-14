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

	def testNoValidMoves(self):
		new_board = board.Board()
		new_board.loadCustomBoard([[2,4,2,4],[4,2,4,2],[2,4,2,4],[4,2,4,2]])
		valid_moves = new_board.getValidMoves()
		bt.assertEquals(valid_moves, [])

	def testVerticalValidOnly(self):
		new_board = board.Board()
		new_board.loadCustomBoard([[2,4,2,4],[2,16,64,16],[2,4,2,4],[4,2,4,2]])
		valid_moves = new_board.getValidMoves()
		bt.assertEquals(valid_moves, [Move.DOWN, Move.UP])
	
	def testRightAndUp(self):
		new_board = board.Board()
		new_board.loadCustomBoard([[0,0,0,0],[2,0,0,0],[8,0,0,0],[32,0,0,0]])
		valid_moves = new_board.getValidMoves()
		bt.assertEquals(valid_moves, [Move.RIGHT, Move.UP])		

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
		custom_board = board.Board()
		custom_board.loadCustomBoard(
			[
				[0,0,2,0],[0,0,2,0],[0,0,0,0], [0,0,0,0]
			]
		)
		custom_board.mergeTilesVertically(1,2,-1)
		bt.assertEquals(
			custom_board.cells,
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
		new_board = board.Board()
		new_board.loadCustomBoard([
			[2,4,8,16],
			[4,8,16,2],
			[8,16,2,4],
			[16,2,4,8]
		])
		validMoves = new_board.getValidMoves()
		bt.assertEquals(validMoves,[])

	def testHasLost(self):
		new_board = board.Board()
		new_board.loadCustomBoard([
			[2,4,8,16],
			[4,8,16,2],
			[8,16,2,4],
			[16,2,4,8]
		])
		isLost = new_board.isLost()
		bt.assertEquals(isLost,True)

	
	def testHasWon(self):
		new_board = board.Board()
		new_board.loadCustomBoard([
			[2,4,8,16],
			[4,8,2048,2],
			[8,16,2,4],
			[2,2,4,8]
		])
		hasWon = new_board.hasWon()
		bt.assertEquals(hasWon,True)
	
	def testHasNotWon(self):
		new_board = board.Board()
		new_board.loadCustomBoard([
			[2,4,8,16],
			[4,8,2,2],
			[8,16,2,4],
			[2,2,4,8]
		])
		hasWon = new_board.hasWon()
		bt.assertEquals(hasWon,False)

	def testHasNotLost(self):
		new_board = board.Board()
		new_board.loadCustomBoard([
			[2,4,8,16],
			[4,8,2,2],
			[8,16,2,4],
			[2,2,4,8]
		])
		hasLost = new_board.isLost()
		bt.assertEquals(hasLost,False)

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
		bt.assertEquals(max_blocks,[[1,1],[3,1]])

	def testVerticalDistanceFromCorner(self):
		simulated_bot = bot.Bot()
		verticalDistance = simulated_bot.getDistanceFromCorner([0,0])
		bt.assertEquals(verticalDistance,3)	

	def testHorizontalDistanceFromCorner(self):
		simulated_bot = bot.Bot()
		horizontalDistance = simulated_bot.getDistanceFromCorner([3,2])
		bt.assertEquals(horizontalDistance,2)	

	def testDiagonalDistance(self):
		simulated_bot = bot.Bot()
		distance = simulated_bot.getDistanceFromCorner([2,3])
		bt.assertAlmostEquals(distance,3.16227766)					

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
		bt.assertAlmostEquals(corner_penalty,565.685424949238)

	def testSimpleEvalComparison(self):
		simulated_bot = bot.Bot()
		new_board = board.Board()
		new_board.loadCustomBoard(
			[
				[0,0,0,0],
				[0,0,4,0],
				[0,2,0,0],
				[64, 4, 0, 0]
			]
		)
		better_position = simulated_bot.computeStaticEval(new_board)
		new_board.loadCustomBoard(
			[
				[64,2,4,0],
				[0,4,4,0],
				[0,0,0,0],
				[0, 0, 0, 0]
			]			
		)
		worse_position = simulated_bot.computeStaticEval(new_board)
		bt.assertAlmostEquals(better_position > worse_position,True)		

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
		bt.assertEquals(best_move, Move.LEFT) # at a depth of 1, left should be considered best. at any higher depth, it'll realise that all moves eventualy get to 2048 so will just use the first one

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
)
