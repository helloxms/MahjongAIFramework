class BaseMJPlayer(object):
    
    """
    Base MJ client implementation

    To create mahjong client, you need to override this class and
    implement following 6 methods.

    - declare_action
    - receive_game_start_message
    - receive_round_start_message
    - receive_game_update_message
    - receive_round_result_message
    """
    def __init__(self):
        self.debug_info_level = 0

    def declare_action(self, valid_actions, hand_tiles, round_state, cur_action):
        err_msg = self.__build_err_msg("declare_action")
        raise NotImplementedError(err_msg)

    
    def receive_game_start_message(self, game_info):
        err_msg = self.__build_err_msg("receive_game_start_message")
        raise NotImplementedError(err_msg)

    def receive_round_start_message(self, round_count, action_info, seats):
        err_msg = self.__build_err_msg("receive_round_start_message")
        raise NotImplementedError(err_msg)


    def receive_game_update_message(self, action_info,  round_state):
        err_msg = self.__build_err_msg("receive_game_update_message")
        raise NotImplementedError(err_msg)

    def receive_round_result_message(self, winners, action_info, round_state):
        err_msg = self.__build_err_msg("receive_round_result_message")
        raise NotImplementedError(err_msg)

    def set_uuid(self, uuid):
        self.uuid = uuid

    def respond_to_ask(self, message):
        """Called from Player when ask message received from RoundManager"""
        valid_actions, hand_tiles, round_state, cur_action, last_drop_tile_136 = self.__parse_ask_message(message)
        return self.declare_action(valid_actions, hand_tiles, round_state, cur_action, last_drop_tile_136)

    def receive_notification(self, message):
        """Called from Player when notification received from RoundManager"""
        msg_type = message["message_type"]
        if msg_type == "game_start_message":
            info = self.__parse_game_start_message(message)
            self.receive_game_start_message(info)

        elif msg_type == "round_start_message":
            round_count, action_info, seats = self.__parse_round_start_message(message)
            self.receive_round_start_message(round_count, action_info, seats)

        elif msg_type == "game_update_message":
            action_info, round_state = self.__parse_game_update_message(message)
            self.receive_game_update_message(action_info, round_state)

        elif msg_type == "round_result_message":
            winners, action_info, round_state = self.__parse_round_result_message(message)
            self.receive_round_result_message(winners, action_info, round_state)


    def __build_err_msg(self, msg):
        return "Your client does not implement [ {0} ] method".format(msg)

    def __parse_ask_message(self, message):
        if self.debug_info_level > 0:
            # print("\n******func* baseMJPlayer.__parse_ask_message: {}".format(message))
            pass
        hand_tiles = message["hand_tiles"]
        round_state = message["round_state"]
        valid_actions = message["valid_actions"]
        cur_action = message["cur_action"]
        last_drop_tile_136 = message["last_drop_tile_136"]
        return valid_actions, hand_tiles, round_state, cur_action, last_drop_tile_136

    def __parse_game_start_message(self, message):
        game_info = message["game_information"]
        return game_info

    def __parse_round_start_message(self, message):
        round_count = message["round_count"]
        seats = message["seats"]
        action_info = message["action_info"]
        return round_count, action_info, seats


    def __parse_game_update_message(self, message):
        action_info = message["action_info"]
        round_state = message["round_state"]
        return  action_info, round_state

    def __parse_round_result_message(self, message):
        winners = message["winners"]
        action_info = message["action_info"]
        round_state = message["round_state"]
        return  winners, action_info, round_state

