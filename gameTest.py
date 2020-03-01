

from pymjengine.simpleMJPlayer import SimpleMJPlayer
from pymjengine.gameConfig import setup_config, start_mahjong


def main(argv=None):
	config = setup_config(max_round=3)
	config.register_player(name="p1", algorithm=SimpleMJPlayer(name='p1', debug_info_level = 1))
	config.register_player(name="p2", algorithm=SimpleMJPlayer(name='p2', debug_info_level = 1))
	config.register_player(name="p3", algorithm=SimpleMJPlayer(name='p3', debug_info_level = 1))
	config.register_player(name="p4", algorithm=SimpleMJPlayer(name='p4', debug_info_level = 1))
	game_result = start_mahjong(config, debug_info_level=0)


if __name__ == "__main__":
    main()