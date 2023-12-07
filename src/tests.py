import bentests as bt
import board
import customPlayer
import backend

class BoardTests(bt.testGroup):
	def __init__(self):
		super().__init__()

	# no way to directly test a random board
	def testBoardDimensions(self):
		new_board = board.Board()
		new_board_dimensions = [len(new_board.cells), len(new_board.cells[0])]
		bt.assertEquals(new_board_dimensions, [4,4])

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
		...
	
	def testInvalidRight(self):
		with bt.assertRaises(board.IllegalMoveError):
			player = customPlayer.customPlayer()
			game_manager = backend.gameManager(player)
			game_manager.loadBoard(
				[
					[0,0,0,0],[0,0,0,2],[0,0,0,0],[4,2,4,2]
				]
			)
			move = player.makeMove("d")
			game_manager.board.updateBoard(move)

	def test3_Consecutive(self):
		player = customPlayer.customPlayer()
		game_manager = backend.gameManager(player)
		game_manager.loadBoard(
			[[0,0,0,0],[0,4,4,4],[0,0,0,0], [0,0,0,0]]
		)
		move = player.makeMove("d")
		game_manager.board.updateBoard(move)
		bt.assertEquals(
			game_manager.board.cells,
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

bt.test_all(
	BoardTests,
	HorizontalMoves,
	VerticalMoves
)
