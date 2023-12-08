from enum import Enum, auto, Flag

class GameState(Enum):
	LOST = auto()
	WON = auto()
	IN_PLAY = auto()

class Move(Flag): #TODO: order in terms of which ones are most likely to get you tiles in bottom left
	DOWN = auto()
	LEFT = auto()
	RIGHT = auto()
	UP = auto()
	HORIZONTAL = LEFT | RIGHT
	VERTICAL = UP | DOWN
	NONE = auto()