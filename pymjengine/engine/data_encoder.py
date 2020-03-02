from functools import reduce

from pymjengine.engine.mj_constants import MJConstants



class DataEncoder:

    ACTIVE_STR = "active"

    @classmethod
    def encode_player(self, player, hand_tiles=False):
        hash_ = {
            "name": player.name,
            "uuid": player.uuid,
            "state": self.__active_str()
        }
        if hand_tiles:
            tile_hash = {"hand_tiles": [str(tile) for tile in player.hand_tiles]}
            hash_.update(tile_hash)
        return hash_

    @classmethod
    def encode_seats(self, seats):
        return {
            "seats": [self.encode_player(player) for player in seats.players]
        }

    @classmethod
    def encode_game_information(self, config, seats):
        hsh = {
            "player_num" : len(seats.players),
            "rule": {
              "max_round": config["max_round"],
              "banker": config["banker"]
            }
        }
        hsh.update(self.encode_seats(seats))
        return hsh

    @classmethod
    def encode_valid_actions(self):
        return {
            "valid_actions": [
              {"action1": "chow",
              "action2": "pong",
              "action3":"kong",
              "action4":"take",
              "action5":"play",
              "action6":"tin",
              "action7":"hu"
               },
            ]
        }

    @classmethod
    def encode_action(self, player, action):
        return {
            "player_uuid": player.uuid,
            "action": action
            }

    @classmethod
    def encode_action_histories(self, table):
        return { "action_histories": 0 }

    @classmethod
    def encode_winners(self, winners):
        return { "winners": self.__encode_players(winners) }

    @classmethod
    def encode_round_state(self, state):
        hsh = {
            "river_tiles": [str(tile) for tile in state["table"].get_river_tiles()],
            "next_player": state["next_player"],
            "round_count": state["round_count"]
        }
        hsh.update(self.encode_seats(state["table"].seats))
        hsh.update(self.encode_action_histories(state["table"]))
        return hsh


    @classmethod
    def __active_str(self):
        return self.ACTIVE_STR

    @classmethod
    def __encode_players(self, players):
        return [self.encode_player(player) for player in players]


    @classmethod
    def __unify_length(self, max_len, lst):
        for _ in range(max_len-len(lst)):
            lst.append(None)
        return lst
        