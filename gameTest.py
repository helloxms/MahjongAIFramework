

from pymjengine.simpleMJPlayer import SimpleMJPlayer
from pymjengine.gameConfig import setup_config, start_mahjong

# if debug_info_level > 0 will open the print log


def main():
	debug_level = 1
	config = setup_config(max_round=10)
	config.register_player(name="p1", algorithm=SimpleMJPlayer(name='p1', debug_info_level=debug_level))
	config.register_player(name="p2", algorithm=SimpleMJPlayer(name='p2', debug_info_level=debug_level))
	config.register_player(name="p3", algorithm=SimpleMJPlayer(name='p3', debug_info_level=debug_level))
	config.register_player(name="p4", algorithm=SimpleMJPlayer(name='p4', debug_info_level=debug_level))
	game_result = start_mahjong(config, debug_info_level=1)


if __name__ == "__main__":
	main()
