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
        pass

    def declare_action(self, valid_actions, tiles, round_state):
        err_msg = self.__build_err_msg("declare_action")
        raise NotImplementedError(err_msg)

    
    def receive_game_start_message(self, game_info):
        err_msg = self.__build_err_msg("receive_game_start_message")
        raise NotImplementedError(err_msg)

    def receive_round_start_message(self, round_count, action_info, seats):
        err_msg = self.__build_err_msg("receive_round_start_message")
        raise NotImplementedError(err_msg)


    def receive_game_update_message(self, round_count, action_info,  round_state):
        err_msg = self.__build_err_msg("receive_game_update_message")
        raise NotImplementedError(err_msg)

    def receive_round_result_message(self, round_count,  winners, action_info, round_state):
        err_msg = self.__build_err_msg("receive_round_result_message")
        raise NotImplementedError(err_msg)

    def set_uuid(self, uuid):
        self.uuid = uuid

    def respond_to_ask(self, message):
        """Called from Player when ask message received from RoundManager"""
        valid_actions, titles, round_state = self.__parse_ask_message(message)
        return self.declare_action(valid_actions, titles, round_state)

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
            round_count, action_info, round_state = self.__parse_game_update_message(message)
            self.receive_game_update_message(round_count, action_info, round_state)

        elif msg_type == "round_result_message":
            round_count, winners, action_info, round_state = self.__parse_round_result_message(message)
            self.receive_round_result_message(round_count, winners, action_info, round_state)


    def __build_err_msg(self, msg):
        return "Your client does not implement [ {0} ] method".format(msg)

    def __parse_ask_message(self, message):
        titls = message["titls"]
        valid_actions = message["valid_actions"]
        round_state = message["round_state"]
        return valid_actions, titls, round_state

    def __parse_game_start_message(self, message):
        game_info = message["game_information"]
        return game_info

    def __parse_round_start_message(self, message):
        round_count = message["round_count"]
        seats = message["seats"]
        action_info = message["action_info"]
        return round_count, action_info, seats


    def __parse_game_update_message(self, message):
        round_count = message["round_count"]
        action_info = message["action_info"]
        round_state = message["round_state"]
        return round_count, action_info, round_state

    def __parse_round_result_message(self, message):
        round_count = message["round_count"]
        winners = message["winners"]
        action_info = message["action_info"]
        round_state = message["round_state"]
        return round_count, winners, action_info, round_state

