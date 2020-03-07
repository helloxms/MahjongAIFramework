


from pymjengine.engine.game_manager import GameManager
from pymjengine.baseMJPlayer import BaseMJPlayer

def setup_config(max_round):
    return Config(max_round)

#debug_info_level
def start_mahjong(config, debug_info_level=0):
    config.validation()
    gm = GameManager()
    gm.set_debug_info_level(debug_info_level)
    for info in config.players_info:
        gm.register_player(info["name"], info["algorithm"])
    result_message = gm.start_game(config.max_round)
    return _format_result(result_message)

def _format_result(result_message):
    return {
            "rule": result_message["message"]["game_information"]["rule"],
            "game_round": result_message["message"]["game_round"],
            "winner": result_message["message"]["winner"]
            # "players": result_message["message"]["game_information"]["seats"]
            }

class Config(object):

    def __init__(self, max_round):
        self.players_info = []
        self.max_round = max_round


    def register_player(self, name, algorithm):
        if not isinstance(algorithm, BaseMJPlayer):
            base_msg = 'Mahjong player must be child class of "BaseMJPlayer". But its parent was "%s"'
            raise TypeError(base_msg % algorithm.__class__.__bases__)
        info = { "name" : name, "algorithm" : algorithm }
        self.players_info.append(info)


    def validation(self):
        player_num = len(self.players_info)
        if player_num < 2:
            detail_msg = "no player is registered yet" if player_num==0 else "you registered only 1 player"
            base_msg = "At least 2 players are needed to start the game"
            raise Exception("%s (but %s.)" % (base_msg, detail_msg))