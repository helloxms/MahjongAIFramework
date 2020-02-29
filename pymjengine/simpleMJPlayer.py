

from pymjengine.players import BaseMJPlayer

# Do not forget to make parent class as "BaseMJPlayer"
class SimpleMJPlayer(BaseMJPlayer):  

    #  we define the logic to make an action through this method.  
    #  this method would be the core of your AI
    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions 
        call_action_info = valid_actions
        
        print("==========>  AI declare actions here:{}".format(call_action_info))
        return call_action_info   # action returned here is sent to the mahjong engine

    def receive_game_start_message(self, game_info):
        print("==========>  AI receive_game_start_message")
        return

    def receive_round_start_message(self, round_count, hole_card, seats):
        print("==========>  AI receive_round_start_message")
        return

    def receive_game_update_message(self, action, round_state):
        print("==========>  AI receive_game_update_message")
        return

    def receive_round_result_message(self, winners, hand_info, round_state):
        print("==========>  AI receive_round_result_message")
        return