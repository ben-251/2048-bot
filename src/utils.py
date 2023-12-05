from enum import Enum, auto

class GameState(Enum):
	LOST = auto()
	WON = auto()
	IN_PLAY = auto()

class Move(Enum):
	UP = "w"
	LEFT = "a"
	DOWN = "s"
	RIGHT = "d"
