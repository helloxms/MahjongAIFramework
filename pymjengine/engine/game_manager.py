
import random
from collections import OrderedDict

from pymjengine.engine.mj_constants import MJConstants
from pymjengine.engine.table import Table
from pymjengine.engine.player import Player
from pymjengine.engine.round_manager import RoundManager
from pymjengine.engine.message_builder import MessageBuilder
from pymjengine.engine.message_handler import MessageHandler ,MessageSummarizer

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
        for round_count in range(1, max_round + 1):
            print("*************************************************************************************************")
            print("***********************************   a new round   *********************************************")
            print("round count:{}".format(round_count))
            if self.__is_game_finished(table): 
                print("game finished")
                break
            table = self.play_round(round_count)
        return self.__generate_game_result(max_round, table.seats)

    def play_round(self, round_count):
        state, msgs = RoundManager.start_new_round(round_count, self.table)
        self.__message_check(msgs)
        # player give a ready info
        check_action_result = self.__publish_and_callbak_msg(msgs)
        state["round_act_state"] = MJConstants.round_act_state.START
        state["cur_act"] = MJConstants.Action.TAKE
        state["cur_winner"] = -1

        while True:
            # self.__message_check(msgs)
            if state["round_act_state"] != MJConstants.round_act_state.FINISHED:
                # take and play query (no choice)
                # step4. a player take a tile from wall
                check_player_pos = state["cur_player"]
                check_action = state["cur_act"] 
                client_drop_tiles = []

                if state["cur_act"] == MJConstants.Action.TAKE:
                    state, msgs = RoundManager.apply_action_with_askmsg(state, check_player_pos, check_action, -1)
                    # player give a take info in check_action_result!
                    # here result should be a tile info!
                    check_action_result = self.__publish_and_callbak_msg(msgs)
                    state["cur_drop"] = check_action_result[1]
                    if check_action_result[2] == -1:
                        state["cur_winner"] = check_player_pos
                    
                    if check_action_result[0] == MJConstants.Action.TAKE:
                        print("==========> server: player{}, ok, i will drop this tile:{}".format(check_player_pos, check_action_result
                                                                                                      [1]))
                    state["cur_act"] = MJConstants.Action.PLAY

                if state["cur_act"] == MJConstants.Action.PLAY and state["cur_drop"] >= 0:
                    # step5. a player drop a tile to river
                    check_action = state["cur_act"]
                    state, msgs = RoundManager.apply_action_no_askmsg(state, check_player_pos, check_action ) 
                    self.__publish_and_no_return(msgs)
                    check_action = state["cur_act"]

                # pass chow pong kong query
                # step6. who will do "pass chow pong kong tin hu" action?
                # step7. a player will do call request or pass
                # step8. check the  rule right,refuse some one, authorize some one
                # step9. do the action requst
                if check_action == MJConstants.Action.PLAY or check_action == MJConstants.Action.CHOW or check_action == MJConstants.Action.PONG :
                    choosed_player, choosed_action, choosed_tile = self.__get_choosed_player(state, check_player_pos, check_action, False)
                    state["cur_act"] = choosed_action
                    state["cur_player"] = choosed_player
                    state["next_player"] = state["table"].get_next_player(state["cur_player"])
                    if choosed_action == MJConstants.Action.KONG or choosed_action == MJConstants.Action.PONG or choosed_action == MJConstants.Action.CHOW:
                        choosed_player = state["cur_player"]
                        print("__get_choosed_player: checked cur_player:{} action:{} ".format(state["cur_player"], choosed_action))
                        if choosed_action == MJConstants.Action.KONG:                        
                            state, msgs = RoundManager.apply_action_no_askmsg(state, choosed_player, choosed_action)
                            state["cur_player"] = state["next_player"]
                            state["next_player"] = state["table"].get_next_player(state["cur_player"])
                            choosed_player = state["cur_player"]
                            choosed_action = MJConstants.Action.TAKE
                            state["cur_act"] = MJConstants.Action.TAKE
                        else:
                            state, msgs = RoundManager.apply_action_with_askmsg(state, choosed_player, choosed_action, choosed_tile)

                print("round count:{} cur_player:{} cur_act:{} banker:{}".format(round_count, state['cur_player'], state['cur_act'], self.table.banker))

                #
                # step11. the next player recycle the same step 4-- step10
                # step12. if the next player is the first player,a new round begin.
                if state["next_player"] == self.table.banker and state["cur_act"] == MJConstants.Action.TAKE:
                    state["round_act_state"] = MJConstants.round_act_state.FINISHED
                if state["cur_winner"] >= 0:
                    state["table"].seats.players[state["cur_winner"]].set_hu(True)
                    state["round_act_state"] = MJConstants.round_act_state.FINISHED
                self.table = state["table"]
            else:  
                print("\n\n******func* GameManager.play_round finish a round\n\n")
                break

        return state["table"]

    # 2020-03-02
    # need add more game rule logic here
    def __get_choosed_player(self, state, player_pos, action, bInclude = False):
        table = state["table"]
        result_map = {}
        result_map[0] = [9, -1, -1]
        result_map[1] = [9, -1, -1]
        result_map[2] = [9, -1, -1]
        result_map[3] = [9, -1, -1]
        result_map[player_pos] = [0, -1, -1]
        # print("******func* __get_choosed_player player size:{}".format(len(table.seats.players)))
        for i in range(0, len(table.seats.players)):
            if not bInclude and (i == player_pos):
                print("skip player{}".format(player_pos))
            else:
                player = table.seats.players[i]
                ask_message = MessageBuilder.build_ask_message(i, state)
                check_action_result = self.__callback_msg(player.uuid, ask_message)
                print("******func* game_manager.__get_choosed_player check_action_result:{}".format(check_action_result))
                result_map[i] = check_action_result

        print("player choose result:{}".format(result_map))
        choosed_player = state["table"].get_next_player(player_pos)
        choosed_action = MJConstants.Action.TAKE
        choosed_tile = -1

        for i in range(0, 4):
            if result_map[i][0] == MJConstants.Action.KONG:
                choosed_player = i
                choosed_action = MJConstants.Action.KONG
                break
            elif result_map[i][0] == MJConstants.Action.PONG:
                choosed_player = i
                choosed_action = MJConstants.Action.PONG    
                break
            elif result_map[i][0] == MJConstants.Action.CHOW and result_map[i][1] >= 0 and table.is_chow_pos(player_pos, i):
                choosed_player = i
                choosed_action = MJConstants.Action.CHOW
                choosed_tile = result_map[i][1]
                break
        if choosed_action == MJConstants.Action.TAKE:
            print("all player pass, the next player{} take tile".format(choosed_player))
        return choosed_player, choosed_action, choosed_tile


    def __register_algorithm_to_message_handler(self, uuid, algorithm):
        self.message_handler.register_algorithm(uuid, algorithm)

    def __escort_player_to_table(self, player_name):
        uuid = self.__fetch_uuid()
        player = Player(uuid, player_name)
        self.table.seats.sitdown(player)
        return uuid

    def __notify_game_start(self, max_round):
    	# config is the play rule
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

    # 2020-03-03
    # In this function:
    # there are a state update message + a callback message (combined in msgs)
    # update message is boadcast to all player
    # callback message is  specified one by one 
    # we should get all other player's answer, then check the right one, then apply the action!
    def __publish_and_callbak_msg(self, msgs):
        for address, msg in msgs[:-1]:
            self.message_handler.process_message(address, msg)
        self.message_summarizer.summarize_messages(msgs)
        return self.message_handler.process_message(*msgs[-1])

    def __publish_and_no_return(self, msgs):
        for address, msg in msgs:
            self.message_handler.process_message(address, msg)
        self.message_summarizer.summarize_messages(msgs)
        return


    def __callback_msg(self, address, msg):
        return self.message_handler.process_message(address, msg)

    def __generate_game_result(self, max_round, seats):
        print("\n******func* GameManager.__generate_game_result")
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
            print("draw tiles: {}".format(tiles))
            player.add_hand_tiles_136(tiles)

    # return 0,1,2,3 as index position
    def __get_banker_pos(self):
    	a = [1 ,2 ,3 ,4]
    	random.shuffle(a)
    	return a[0 ] -1

    def __config_check(self):
        return

    def __fetch_uuid(self):
        return self.uuid_list.pop()

    def __generate_uuid_list(self):
        return [self.__generate_uuid() for _ in range(100)]

    def __generate_uuid(self):
        uuid_size = 22
        chars = [chr(code) for code in range(97 ,123)]
        return "".join([random.choice(chars) for _ in range(uuid_size)])

