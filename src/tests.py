import bentests as bt
import board

class BoardTests(bt.testGroup):
	def __init__(self):
		super().__init__()

	# no way to directly test a random board
	def testBoardDimensions(self):
		new_board = board.Board()
		new_board_dimensions = [len(new_board.cells), len(new_board.cells[0])]
		bt.assertEquals(new_board_dimensions, [4,4])

bt.test_all(
	BoardTests
)
