from pymjengine.simpleMJPlayer import SimpleMJPlayer
from pymjengine.gameConfig import setup_config, start_mahjong


# if debug_info_level > 0 will open the print log


def main():
    debug_level = 0
    game_round_statistic = []
    game_winner_statistic = []
    for i in range(0,100):
        config = setup_config(max_round=30)
        config.register_player(name="p0", algorithm=SimpleMJPlayer(name='p0', pos=0, debug_info_level=0))
        config.register_player(name="p1", algorithm=SimpleMJPlayer(name='p1', pos=1, debug_info_level=0))
        config.register_player(name="p2", algorithm=SimpleMJPlayer(name='p2', pos=2, debug_info_level=0))
        config.register_player(name="p3", algorithm=SimpleMJPlayer(name='p3', pos=3, debug_info_level=0))
        game_result = start_mahjong(config, debug_info_level=0)
        game_round_statistic.append(game_result["game_round"])
        game_winner_statistic.append(game_result["winner"])
        print(game_result)
        print(game_round_statistic)
        print(game_winner_statistic)

    iCount = 0
    for i in range(0, len(game_winner_statistic)):
        if game_winner_statistic[i] > 0:
            iCount += 1
    print("winner count :{}".format(iCount))



if __name__ == "__main__":
    main()
