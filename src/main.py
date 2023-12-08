import backend
from human import Human
from bot import Bot

def main():
	player = Bot()
	game_manager = backend.gameManager(player)
	game_manager.loadBoard(
		[
			[0,0,0,0],[4,2,4,4],[2,8,2,8],[32,32,4,2]
		]
	)
	game_manager.play()


if __name__ == "__main__":
	main()