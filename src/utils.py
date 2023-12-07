from enum import Enum, auto, Flag

class GameState(Enum):
	LOST = auto()
	WON = auto()
	IN_PLAY = auto()

class Move(Flag):
	UP = auto()
	LEFT = auto()
	DOWN = auto()
	RIGHT = auto()
	HORIZONTAL = LEFT | RIGHT
	VERTICAL = UP | DOWN