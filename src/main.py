import backend
from human import Human
from bot import Bot

def main():
	player = Bot()
	game_manager = backend.gameManager(player)
	game_manager.loadBoard(
		[
			[4,0,0,0],
			[0,0,2,4],
			[0,0,8,16],
			[64,2,16,8]
		]
	)
	game_manager.play()


if __name__ == "__main__":
	main()