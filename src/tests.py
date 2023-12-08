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
		validMoves = game_manager.getValidMoves()
		bt.assertEquals(validMoves,[])

class StaticEval(bt.testGroup):
	def __init__(self):
		super().__init__()
	
	def testBottomRowOnly(self):
		simulated_bot = bot.Bot()
		new_board = board.Board()
		new_board.loadCustomBoard(
			[
				[0,0,0,0], [0,0,0,0], [0,0,0,0], [128, 64, 4, 2]
			]
		)
		evaluation = simulated_bot.computeStaticEval(new_board)
		bt.assertEquals(evaluation,182.4)

	def testBadRowsOnly(self):
		simulated_bot = bot.Bot()
		new_board = board.Board()
		new_board.loadCustomBoard(
			[
				[2,8,2,4], [2,8,2,4], [2,8,2,4], [0, 0, 0, 0]
			]
		)
		evaluation = simulated_bot.computeStaticEval(new_board)
		bt.assertAlmostEquals(evaluation,-162.8)

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
			best_move, Move.UP # cuz it checks moves in w, a, s, d order
		)

	def testWinningHorizontalMove(self):
		simulated_bot = bot.Bot()
		simulated_board = board.Board()

		simulated_board.loadCustomBoard(
			[[0,0,0,0],[0,0,0,0],[1024,1024,0,0],[0, 0,0,0]])
		best_move = simulated_bot.makeMove(simulated_board)
		bt.assertEquals(best_move, Move.LEFT) # cuz it checks moves in w, a, s, d order

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
			best_move, Move.DOWN # cuz it checks moves in w, a, s, d order
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
			best_move, Move.DOWN # cuz it checks moves in w, a, s, d order
		)
	
bt.test_all(
	BoardTests,
	Bot,
	HorizontalMoves,
	VerticalMoves,
	GamePlay,
	StaticEval,
	stats_amount="low"
)
