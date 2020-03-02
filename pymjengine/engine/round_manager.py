from functools import reduce

from pymjengine.engine.table import Table
from pymjengine.engine.player import Player
from pymjengine.engine.mj_constants import MJConstants
from pymjengine.engine.message_builder import MessageBuilder

class RoundManager:

    @classmethod
    def start_new_round(self, round_count, table):
        print("*********************************************")
        print("******func* RoundManager.start_new_round")
        # step3. start a round        
        _state = self.__gen_initial_state(round_count, table)
        state = self.__deep_copy_state(_state)
        table = state["table"]
        update_msg = self.__round_start_message(round_count, table)
        state, ask_message = self.__start_ready_check(state)
        return state, update_msg + ask_message

    @classmethod
    def apply_action(self, original_state, player_pos, action):
        # apply current action
        state = self.__deep_copy_state(original_state)
        state = self.__update_state_by_action(state, player_pos, action)
        update_msg = self.__update_message(state, player_pos, action)
        # then we ask for player's call
        state["next_player"] = state["table"].get_next_player(player_pos)
        state["valid_actions"] = []
        target_player_pos = player_pos
        ask_message = ()
        if action == MJConstants.Action.TAKE:
            state["valid_actions"] = ['play']
        if action == MJConstants.Action.PLAY:
            state["valid_actions"] = ['chow', 'pong', 'kong']

        if target_player_pos >= 0:
            target_player = state["table"].seats.players[target_player_pos]
            ask_message = (target_player.uuid, MessageBuilder.build_ask_message(target_player_pos, state))
        return state, [update_msg, ask_message]
        

    @classmethod
    def query_action(self, state, player_pos, action):
 
        target_player_pos = player_pos
        ask_message = ()
        state["valid_actions"] = []
        if action == MJConstants.Action.TAKE:
            state["valid_actions"] = ['play']
        if action == MJConstants.Action.PLAY:
            state["valid_actions"] = ['chow', 'pong', 'kong']

        if target_player_pos >= 0:
            target_player = state["table"].seats.players[target_player_pos]
            ask_message = (target_player.uuid, MessageBuilder.build_ask_message(target_player_pos, state))
        return message_handler.process_message(ask_message)



    @classmethod
    def __update_message(cls, state, player_pos, action):
        return (-1, MessageBuilder.build_game_update_message(state, player_pos, action))
        
    @classmethod
    def __update_state_by_action(cls, state, player_pos, action):
        table = state["table"]
        return cls.__accept_action(state, player_pos, action)

    # step4. a player take a tile from wall
    @classmethod
    def __accept_action(cls, state, player_pos, action):
        print("******func* RoundManager.__accept_action palyer_pos:{} action:{}".format(player_pos, action))
        player = state["table"].seats.players[player_pos]
        table = state["table"]
        if action == MJConstants.Action.TAKE:
            tile = table.wall.draw_tile()
            player.add_hand_tile(tile)
            player.add_action_history(action)
            print("wall size:{} player handtiles:{} size: {}".format(table.wall.size(), player.get_handtile_ids(), player.get_handtile_size()))
            state["table"].wall = table.wall
        return state

    @classmethod
    def __deal_handtiles(self, wall, players):
        for player in players:
            player.add_hand_tiles(wall.draw_tiles(14))


    @classmethod
    def __start_ready_check(self, state):
        print("******func* RoundManager.__start_ready_check")
        
        first_player = state["table"].banker
        if(first_player >= 0):
            state["table"].cur_player = first_player
            state["cur_player"] = first_player
            state["next_player"] = state["table"].get_next_player(first_player)
            state["cur_act"] = MJConstants.Action.START
        else:
            state["next_player"] = -1           
        return self.__get_ask_msg(state)
        
    # round start action: ask for take a tile
    # here get the banker player pos , and return a ask_msg
    @classmethod
    def __start_take_act_check(self, state):
        print("******func* RoundManager.__start_round_act")
        
        first_player = state["table"].banker
        if(first_player >= 0):
            state["table"].cur_player = first_player
            state["cur_player"] = first_player
            state["next_player"] = state["table"].get_next_player(first_player)
            state["cur_act"] = MJConstants.Action.TAKE
        else:
            state["next_player"] = -1           
        return self.__get_ask_msg(state)



    @classmethod
    def __showResult(self, state):
        print("******func* RoundManager.__showResult")
        winners = 1
        hand_info = "handinfo123456789"
        prize_map = {1:100,2:200,3:300,4:400}
        self.__prize_to_winners(state["table"].seats.players, prize_map)
        result_message = MessageBuilder.build_round_result_message(state["round_count"], winners, hand_info, state)
        state["table"].reset()
        state["takeround"] += 1
        return state, [(-1, result_message)]

    @classmethod
    def __prize_to_winners(self, players, prize_map):
        for idx, prize in prize_map.items():
            players[idx].append_chip(prize)

    @classmethod
    def __round_start_message(self, round_count, table):
        players = table.seats.players
        gen_msg = lambda idx: (players[idx].uuid, MessageBuilder.build_round_start_message(round_count, idx, table.seats, "start"))
        return reduce(lambda acc, idx: acc + [gen_msg(idx)], range(len(players)), [])

    @classmethod
    def __get_ask_msg(self, state):
        table = state["table"]
        cur_player_pos = state["cur_player"]
        print("forward_act, wait player pos:{}".format(cur_player_pos)) 
        cur_player = table.seats.players[cur_player_pos]
        print("forward_act, wait player uuid:{}".format(cur_player.uuid))
        ask_message = [(cur_player.uuid, MessageBuilder.build_ask_message(cur_player_pos, state))]
        return state, ask_message

    # be carefull,for this init will miss some param,if we don't add them
    @classmethod
    def __gen_initial_state(cls, round_count, table):
        return {
        "round_count": round_count,
        "table": table,
        "cur_act" : MJConstants.Action.TAKE,
        "cur_player" : -1,
        "next_player" : -1,
        "round_act_state" : MJConstants.round_act_state.START
        }

    # be carefull,for this deep copy will miss some param,if we don't add them
    @classmethod
    def __deep_copy_state(cls, state):
        table_deepcopy = Table.deserialize(state["table"].serialize())
        return {
        "round_count": state["round_count"],
        "round_act_state": state["round_act_state"],
        "cur_act": state["cur_act"],
        "cur_player": state["cur_player"],
        "next_player": state["next_player"],
        "table": table_deepcopy
        }