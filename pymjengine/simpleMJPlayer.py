

from pymjengine.players import BaseMJPlayer

# Do not forget to make parent class as "BaseMJPlayer"
class SimpleMJPlayer(BaseMJPlayer):  

    #  we define the logic to make an action through this method.  
    #  this method would be the core of your AI
    def declare_action(self, valid_actions, hand_tiles, round_state):
        # valid_actions 
        call_action_info = valid_actions
        
        print("==========>  AI declare actions here:{} hand_tiles:{}".format(call_action_info, hand_tiles))
        return call_action_info   # action returned here is sent to the mahjong engine

    def receive_game_start_message(self, game_info):
        print("==========>  AI receive_game_start_message，game_info{}".format(game_info))
        return

    def receive_round_start_message(self, round_count, action_info, seats):
        print("==========>  AI receive_round_start_message, round_count:{}, action_info:{},seats:{}".format(round_count, action_info, seats))
        return

    def receive_game_update_message(self, action_info, round_state):
        print("==========>  AI receive_game_update_message, action_info:{}, round_state{}".format(action_info, round_state))
        return

    def receive_round_result_message(self, winners, action_info, round_state):
        print("==========>  AI receive_round_result_message, winners:{}, action_info:{}, round_state:{}".format(winners, action_info, round_state))
        return