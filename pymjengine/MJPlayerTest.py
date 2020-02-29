


from pymjengine.game import setup_config, start_mahjong


def main(argv=None):
	opts,args = getopt.getopt(argv[1:],"h",["help"])
	config = setup_config(max_round=10)
	config.register_player(name="p1", algorithm=SimpleMJPlayer())
	config.register_player(name="p2", algorithm=SimpleMJPlayer())
	config.register_player(name="p3", algorithm=SimpleMJPlayer())
	config.register_player(name="p4", algorithm=SimpleMJPlayer())
	game_result = start_mahjong(config, verbose=1)


if __name__ == "__main__":
    main()
    