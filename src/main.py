import backend
from human import Human
from bot import Bot

def main():
	player = Bot()
	game_manager = backend.gameManager(player)
	game_manager.play()


if __name__ == "__main__":
	main()