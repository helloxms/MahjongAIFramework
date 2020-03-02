

import random
from collections import OrderedDict

from pymjengine.engine.mj_constants import MJConstants
from pymjengine.engine.table import Table
from pymjengine.engine.player import Player
from pymjengine.engine.round_manager import RoundManager
from pymjengine.engine.message_builder import MessageBuilder
from pymjengine.engine.message_handler import MessageHandler,MessageSummarizer

'''
server->client:
step0. start game,shffule table wall,check 4 seats are 4 active player.
step1. select the first player (banker)
step2. start from the first player,every one get 14 tiles
step3. start a round
step4. a player take a tile from wall
client->server:
step5. a player drop a tile to river
server->client:
step6.who will do "chow pong kong tin hu" action?
client->server:
step7. a player will do call request
server->client:
step8. check the  rule right,refuse some one, authorize some one
client->server:
step9. do the action requst
server->client:
step10. check the rule right,update every one's state
if the hu action is right,finish the game
step11. the next player recycle the same step 4-- step10
step12. if the next player is the first player,a new round begin.
if the round count is over max-round,game finished.

'''


class GameManager:

    def __init__(self):
        self.uuid_list = self.__generate_uuid_list()
        self.message_handler = MessageHandler()
        self.message_summarizer = MessageSummarizer(debug_info_level=0)
        self.table = Table()
        self.debug_info_level = 0
        self.table.banker = 0

    def register_player(self, player_name, algorithm):
        self.__config_check()
        uuid = self.__escort_player_to_table(player_name)
        algorithm.set_uuid(uuid)
        self.__register_algorithm_to_message_handler(uuid, algorithm)

    def set_debug_info_level(self, debug_info_level):
        self.message_summarizer.debug_info_level = debug_info_level
        self.debug_info_level = debug_info_level

    def start_game(self, max_round):
        print("*************************************************************************************************")
        print("******func* GameManager.start_game")
        table = self.table
        # step1. select the first player(banker)
        print("******func* step1. select the first player(banker)")
        self.table.banker = self.__get_banker_pos()
        # step2. start from the first player,every one get 14 tiles
        print("******func* step2. start from the first player,every one get 14 tiles")
        self.__draw_tiles()
        print("******func* GameManager.__notify_game_start")
        self.__notify_game_start(max_round)
        # step3. start a round
        print("******func* step3. start a round")
        for round_count in range(1, max_round+1):
            print("*************************************************************************************************")
            print("***************************************a new round***********************************************")
            print("round count:{}".format(round_count))
            if self.__is_game_finished(table): 
                print("game finished")
                break
            table = self.play_round(round_count)
        return self.__generate_game_result(max_round, table.seats)

    def play_round(self, round_count):
        state, msgs = RoundManager.start_new_round(round_count, self.table)
        self.__message_check(msgs)
        state["round_act_state"] = MJConstants.round_act_state.START
        check_action_result = self.__publish_messages(msgs)
        print("\n******func* GameManager.play_round check actions's answer is:{}".format(check_action_result))
        if check_action_result > 0:
            check_action = check_action_result
            check_player_pos = state["cur_player"]
            state, msgs = RoundManager.apply_action(state, check_player_pos, check_action)
            self.table = state["table"]
        if self.debug_info_level > 0:
            print("******func* GameManager.play_round apply_action state:{} msgs:{}".format(state, msgs))

        while True:
            self.__message_check(msgs)
            if state["round_act_state"] != MJConstants.round_act_state.FINISHED:  # continue the round
                check_action_result = self.__publish_messages(msgs)
                print("\n******func* GameManager.play_round check actions's answer is:{}".format(check_action_result))
                if check_action_result > 0:
                    state["cur_player"] = state["next_player"]
                    state["next_player"] = state["table"].get_next_player(state["cur_player"])
                    check_action = check_action_result
                    check_player_pos = state["cur_player"]
                    print("checked action is:{} cur_player:{} next_player:{}".format(check_action, state["cur_player"], state["next_player"]))
                    state, msgs = RoundManager.apply_action(state, check_player_pos, check_action)
                    self.table = state["table"]
                if state["next_player"] == self.table.banker:
                    state["round_act_state"] = MJConstants.round_act_state.FINISHED
            else:  
                print("******func* GameManager.play_round wall size:{}".format(self.table.wall.size()))
                print("******func* GameManager.play_round finish a round\n\n")
                break
            # self.__publish_messages(msgs)
        return state["table"]


    def __register_algorithm_to_message_handler(self, uuid, algorithm):
        self.message_handler.register_algorithm(uuid, algorithm)

    def __escort_player_to_table(self, player_name):
        uuid = self.__fetch_uuid()
        player = Player(uuid, player_name)
        self.table.seats.sitdown(player)
        return uuid

    def __notify_game_start(self, max_round):
    	#config is the play rule
        config = self.__gen_config(max_round, self.table.banker)
        start_msg = MessageBuilder.build_game_start_message(config, self.table.seats)
        self.message_handler.process_message(-1, start_msg)
        self.message_summarizer.summarize(start_msg)

    def __is_game_finished(self, table):
        bFinish = False
        for player in table.seats.players:
            print("check game end: {}".format(player.is_hu))
            if player.is_hu :
                bFinish = True
        return bFinish

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
        config = self.__gen_config(max_round, self.table.banker)
        result_message = MessageBuilder.build_game_result_message(config, seats)
        self.message_summarizer.summarize(result_message)
        return result_message

    def __gen_config(self, max_round, banker):
        return {
            "max_round": max_round,
            "banker": banker
        }

    def __draw_tiles(self):
        for player in self.table.seats.players:
            tiles = self.table.wall.draw_tiles(14)
            print("draw tiles: {}".format([tid.to_id() for tid in tiles] ))
            player.add_hand_tiles( tiles )
    		

    #return 0,1,2,3 as index position
    def __get_banker_pos(self):
    	a = [1,2,3,4]
    	random.shuffle(a)
    	return a[0]-1

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

