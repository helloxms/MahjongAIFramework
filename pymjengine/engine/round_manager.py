from functools import reduce

from pymjengine.engine.table import Table
from pymjengine.engine.player import Player
from pymjengine.engine.pay_info import PayInfo
from pymjengine.engine.mj_constants import MJConstants
from pymjengine.engine.message_builder import MessageBuilder

class RoundManager:

    @classmethod
    def start_new_round(self, round_count, table):
        print("start new round")
        _state = self.__gen_initial_state(round_count, table)
        
        state = self.__deep_copy_state(_state)
        table = state["table"]
        table.cur_player_pos = 1

        table.wall.shuffle()
        self.__deal_handtiles(table.wall, table.seats.players)
        start_msg = self.__round_start_message(round_count, table)
        state, takeround_msgs = self.__start_act_round(state)
        return state, start_msg + takeround_msgs

    @classmethod
    def apply_action(self, original_state, action):
        print("apply_action: origin state:{}".format(original_state))
        print("apply_action: action:{}".format(action))
        state = self.__deep_copy_state(original_state)
        print("apply_action: cur state:{}".format(state))
        state = self.__update_state_by_action(state, action)
        
        update_msg = self.__update_message(state, action)
        state["next_player"] = state["table"].next_ask_act_player_pos(state["next_player"])
        state["valid_actions"] =['chow','pong','kong']
        next_player_pos = state["next_player"]
        next_player = state["table"].seats.players[next_player_pos]
        ask_message = (next_player.uuid, MessageBuilder.build_ask_message(next_player_pos, state))
        return state, [update_msg, ask_message]

    @classmethod
    def __update_message(self, state, action):
        return (-1, MessageBuilder.build_game_update_message(
          state["next_player"], action,state))
        
    @classmethod
    def __update_state_by_action(self, state, action):
        table = state["table"]
        return self.__accept_action(state, action)

    @classmethod
    def __accept_action(self, state, action):
        print("accept action:{}".format(action))
        player = state["table"].seats.players[state["next_player"]]

        player.add_action_history(MJConstants.Action.TAKE)
        return state

    @classmethod
    def __deal_handtiles(self, wall, players):
        for player in players:
            player.add_hand_tiles(wall.draw_tiles(14))

        
        
    @classmethod
    def __start_act_round(self, state):
        print("__start_act_round")
         
        next_player_pos = state["table"].next_ask_act_player_pos(state["table"].cur_player_pos)
        if(next_player_pos > 0):
            state["table"].cur_player_pos = next_player_pos
            state["next_player"] = next_player_pos
            state["cur_act"] = state["table"].get_player_act(next_player_pos)
        else:
            state["next_player"] = -1           
            
        round_act = state["cur_act"] 
        if round_act == MJConstants.Action.TAKE:
            return self.__act_take(state)
        elif round_act == MJConstants.Action.CHOW:
            return self.__act_chow(state)
        elif round_act == MJConstants.Action.PONG:
            return self.__act_pong(state)
        elif round_act == MJConstants.Action.KONG:
            return self.__act_kong(state)
        elif round_act == MJConstants.Action.PLAY:
            return self.__act_play(state)
        else:
            raise ValueError("round is already finished [round act = %d]" % round_act)

    @classmethod
    def __act_take(self, state):
        print("act take")
        return self.__forward_act(state)
            
    @classmethod
    def __act_chow(self, state):
        print("act chow")
        return self.__forward_act(state)

    @classmethod
    def __act_pong(self, state):
        print("act pong")
        return self.__forward_act(state)

    @classmethod
    def __act_kong(self, state):
        print("act kong")
        return self.__forward_act(state)

    @classmethod
    def __act_play(self, state):
        print("act play")
        return self.__forward_act(state)

    @classmethod
    def __showResult(self, state):
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
    def __forward_act(self, state):
        table = state["table"]
        next_player_pos = state["next_player"]
        print("forward_act, next player pos:{}".format(next_player_pos)) 
        next_player = table.seats.players[next_player_pos]
        print("forward_act, next player uuid:{}".format(next_player.uuid))
        ask_message = [(next_player.uuid, MessageBuilder.build_ask_message(next_player_pos, state))]
        return state, ask_message

    #be carefull,for this init will miss some param,if we don't add them
    @classmethod
    def __gen_initial_state(self, round_count, table):
        return {
        "round_count": round_count,
        "table": table,
        "cur_act" : MJConstants.Action.TAKE,
        "next_player" : -1 ,
        "round_act_state" : MJConstants.round_act_state.START
        }

    #be carefull,for this deep copy will miss some param,if we don't add them
    @classmethod
    def __deep_copy_state(self, state):
        table_deepcopy = Table.deserialize(state["table"].serialize())
        return {
        "round_count": state["round_count"],
        "round_act_state": state["round_act_state"],
        "cur_act": state["cur_act"],
        "next_player": state["next_player"]  , 
        "table": table_deepcopy
        }