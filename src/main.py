import backend
from human import Human

def main():
	player = Human()
	game_manager = backend.gameManager(player)
	game_manager.loadBoard(
		[
			[0,0,0,0],[2,0,0,2],[0,4,4,0],[16,16,16,16]
		]
	)
	game_manager.play()


if __name__ == "__main__":
	main()