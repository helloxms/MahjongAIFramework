from pymjengine.engine.data_encoder import DataEncoder
from pymjengine.engine.mj_constants import MJConstants


class MessageBuilder:
    GAME_START_MESSAGE = "game_start_message"
    ROUND_START_MESSAGE = "round_start_message"
    ASK_MESSAGE = "ask_message"
    GAME_UPDATE_MESSAGE = "game_update_message"
    ROUND_RESULT_MESSAGE = "round_result_message"
    GAME_RESULT_MESSAGE = "game_result_message"

    @classmethod
    def build_game_start_message(cls, config, seats):
        message = {
            "message_type": cls.GAME_START_MESSAGE,
            "game_information": DataEncoder.encode_game_information(config, seats)
        }
        return cls.__build_notification_message(message)

    @classmethod
    def build_round_start_message(cls, round_count, player_pos, seats, action):
        player = seats.players[player_pos]
        hand_tiles = DataEncoder.encode_player(player, hand_tiles=True)["hand_tiles"]
        message = {
            "message_type": cls.ROUND_START_MESSAGE,
            "round_count": round_count,
            "hand_tiles": hand_tiles,
            "action_info": DataEncoder.encode_action(player, action),
        }
        message.update(DataEncoder.encode_seats(seats))
        return cls.__build_notification_message(message)

    # update message: publish a player's action info
    @classmethod
    def build_game_update_message(cls, state, player_pos, action):
        player = state["table"].seats.players[player_pos]
        message = {
            "message_type": cls.GAME_UPDATE_MESSAGE,
            "action_info": DataEncoder.encode_action(player, action),
            "round_state": DataEncoder.encode_round_state(state),
            "action_histories": DataEncoder.encode_action_histories(state["table"])
        }
        return cls.__build_notification_message(message)

    @classmethod
    def build_round_result_message(cls, round_count, winners, hand_info, state):
        message = {
            "message_type": cls.ROUND_RESULT_MESSAGE,
            "round_count": round_count,
            "hand_info": hand_info,
            "round_state": DataEncoder.encode_round_state(state)
        }
        message.update(DataEncoder.encode_winners(winners))
        return cls.__build_notification_message(message)

    @classmethod
    def build_game_result_message(cls, config, seats):
        message = {
            "message_type": cls.GAME_RESULT_MESSAGE,
            "game_information": DataEncoder.encode_game_information(config, seats)
        }
        return cls.__build_notification_message(message)

    @classmethod
    def build_ask_message(cls, player_pos, state):
        players = state["table"].seats.players
        player = players[player_pos]
        river_tiles = DataEncoder.encode_river(state["table"])
        hand_tiles = DataEncoder.encode_player(player, hand_tiles=True)["hand_tiles"]
        message = {
            "message_type": cls.ASK_MESSAGE,
            "hand_tiles": hand_tiles,
            "round_state": DataEncoder.encode_round_state(state),
            "valid_actions": DataEncoder.encode_valid_actions(),
            "cur_action": state["cur_act"],
            "last_drop_tile_136": state["last_drop_tile_136"],
            "action_histories": DataEncoder.encode_action_histories(state["table"])
        }

        if state["cur_act"] == MJConstants.Action.READY:
            print("==========> server: player{}, are you ready???????????????????".format(player_pos))
        elif state["cur_act"] == MJConstants.Action.TAKE:
            print("==========> server: player{}, is it your take and drop turn????????????".format(player_pos))
        elif state["cur_act"] == MJConstants.Action.PLAY:
            print(
                "==========> server: player{}, after PLAY drop a tile, choose one: pass_9,chow_3,pong_4,kong_5 ???".format(
                    player_pos))
        elif state["cur_act"] == MJConstants.Action.CHOW:
            print(
                "==========> server: player{}, after CHOW drop a tile, choose one: pass_9,chow_3,pong_4,kong_5 ???".format(
                    player_pos))
        elif state["cur_act"] == MJConstants.Action.PONG:
            print(
                "==========> server: player{}, after PONG drop a tile, choose one: pass_9,chow_3,pong_4,kong_5 ???".format(
                    player_pos))
        else:
            print("==========> server: player{}, who am I?".format(player_pos))
        return cls.__build_ask_message(message)

    @classmethod
    def __build_ask_message(cls, message):
        return {
            "type": "ask",
            "message": message
        }

    @classmethod
    def __build_notification_message(cls, message):
        return {
            "type": "notification",
            "message": message
        }
