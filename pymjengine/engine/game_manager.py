

import random
from collections import OrderedDict

from pymjengine.engine.mj_constants import MJConstants
from pymjengine.engine.table import Table
from pymjengine.engine.player import Player
from pymjengine.engine.round_manager import RoundManager
from pymjengine.engine.message_builder import MessageBuilder


class GameManager:

    def __init__(self):
        self.uuid_list = self.__generate_uuid_list()
        self.message_handler = MessageHandler()
        self.message_summarizer = MessageSummarizer(verbose=0)
        self.table = Table()

    def register_player(self, player_name, algorithm):
        self.__config_check()
        uuid = self.__escort_player_to_table(player_name)
        algorithm.set_uuid(uuid)
        self.__register_algorithm_to_message_handler(uuid, algorithm)

    def set_verbose(self, verbose):
        self.message_summarizer.verbose = verbose

    def start_game(self, max_round):
        table = self.table
        self.__notify_game_start(max_round)
        for round_count in range(1, max_round+1):
            if self.__is_game_finished(table): break
            table = self.play_round(round_count)
        return self.__generate_game_result(max_round, table.seats)

    def play_round(self, round_count):
        state, msgs = RoundManager.start_new_round(round_count, self.table)
        while True:
            self.__message_check(msgs)
            if state["round_act_state"] != MJConstants.round_act_state.FINISHED :  # continue the round
                print("continue round apply action")
                self.__publish_messages(msgs)
                state, msgs = RoundManager.apply_action(state,"take")
                print("here finish a round")
                state["round_act_state"] = MJConstants.round_act_state.FINISHED
            else:  # finish the round after publish round result
                print("finish round")
                self.__publish_messages(msgs)
                break
        return state["table"]


    def __register_algorithm_to_message_handler(self, uuid, algorithm):
        self.message_handler.register_algorithm(uuid, algorithm)

    def __escort_player_to_table(self, player_name):
        uuid = self.__fetch_uuid()
        player = Player(uuid, player_name)
        self.table.seats.sitdown(player)
        return uuid

    def __notify_game_start(self, max_round):
        config = self.__gen_config(max_round)
        start_msg = MessageBuilder.build_game_start_message(config, self.table.seats)
        self.message_handler.process_message(-1, start_msg)
        self.message_summarizer.summarize(start_msg)

    def __is_game_finished(self, table):
        for player in table.seats.players:
            print("player is active: {}".format(player.is_active()))
        return len([player for player in  table.seats.players if player.is_active()]) == 1

    def __message_check(self, msgs):
        address, msg = msgs[-1]
        invalid = msg["type"] != 'ask'
        if invalid:
            raise Exception("Last message is not ask type. : %s" % msgs)

    def __publish_messages(self, msgs):
        for address, msg in msgs[:-1]:
            self.message_handler.process_message(address, msg)
        self.message_summarizer.summarize_messages(msgs)
        return self.message_handler.process_message(*msgs[-1])


    def __generate_game_result(self, max_round, seats):
        config = self.__gen_config(max_round)
        result_message = MessageBuilder.build_game_result_message(config, seats)
        self.message_summarizer.summarize(result_message)
        return result_message

    def __gen_config(self, max_round):
        return {
            "max_round": max_round
        }


    def __config_check(self):
        return

    def __fetch_uuid(self):
        return self.uuid_list.pop()

    def __generate_uuid_list(self):
        return [self.__generate_uuid() for _ in range(100)]

    def __generate_uuid(self):
        uuid_size = 22
        chars = [chr(code) for code in range(97,123)]
        return "".join([random.choice(chars) for _ in range(uuid_size)])

