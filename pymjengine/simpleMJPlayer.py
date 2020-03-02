
from pymjengine.engine.mj_constants import MJConstants
from pymjengine.baseMJPlayer import BaseMJPlayer
# Do not forget to make parent class as "BaseMJPlayer"


class SimpleMJPlayer(BaseMJPlayer):  

    def __init__(self, name, debug_info_level=0):
        self.debug_info_level = debug_info_level
        self.name = name
    #  we define the logic to make an action through this method.  
    #  this method would be the core of your AI

    def declare_action(self, valid_actions, hand_tiles, round_state, cur_action):
        # valid_actions 
        call_action_info = valid_actions
        if self.debug_info_level > 0:
            print("\npalyer: {}".format(self.name))
            print("==========>  AI declare actions")
            print("valid_actions:{} \nhand_tiles:{} \nround_state: {} \ncur_action:{}".format(\
                call_action_info, hand_tiles, round_state, cur_action))
        if cur_action == MJConstants.Action.TAKE:
            return cur_action
        return cur_action   # action returned here is sent to the mahjong engine

    #   game info
    '''
    game_info:{
    'rule': {'banker': 1, 'max_round': 2}, 
    'player_num': 4, 
    'seats': [
    {'uuid': 'tsuemzefiyxrxzqlhcnwpl', 'state': 'participating', 'name': 'p1'}, 
    {'uuid': 'sccsxzuuqcemvqdhgxbayy', 'state': 'participating', 'name': 'p2'}, 
    {'uuid': 'sfnsnwvmlobzjeecbhbcdo', 'state': 'participating', 'name': 'p3'}, 
    {'uuid': 'qmxaschksmbmdfxifarinm', 'state': 'participating', 'name': 'p4'}
    ]}
    '''
    def receive_game_start_message(self, game_info):
        if self.debug_info_level > 0:
            print("\npalyer: {}".format(self.name))
            print("==========>  AI receive_game_start_message")
            print("game_info:{}".format(game_info))
            print("banker:{}".format(game_info['rule']['banker']))
        return

    '''
    round_count:1,
    action_info:{'action': 'start', 'player_uuid': 'djuuvmrhgrrnapvisupqty'},
    seats:[
    {'state': 'participating', 'name': 'p1', 'uuid': 'djuuvmrhgrrnapvisupqty'}, 
    {'state': 'participating', 'name': 'p2', 'uuid': 'kzqdhnnfbvhscwhnlthpyd'}, 
    {'state': 'participating', 'name': 'p3', 'uuid': 'tkfrcdwejhokkqceelxxey'}, 
    {'state': 'participating', 'name': 'p4', 'uuid': 'wmjtfcbvfyiidyrwifqvta'}]
    '''
    def receive_round_start_message(self, round_count, action_info, seats):
        if self.debug_info_level > 0:
            print("\npalyer: {}".format(self.name))
            print("==========>  AI receive_round_start_message")
            print("round_count:{}, \naction_info:{},\nseats:{}".format(round_count, action_info, seats))
        return

    '''
    action_info:{'action': 'take', 'player_uuid': 'wmjtfcbvfyiidyrwifqvta'},
    round_state:{
    'river_tiles': [], 
    'seats': [
    {'state': 'participating', 'name': 'p1', 'uuid': 'djuuvmrhgrrnapvisupqty'}, 
    {'state': 'participating', 'name': 'p2', 'uuid': 'kzqdhnnfbvhscwhnlthpyd'}, 
    {'state': 'participating', 'name': 'p3', 'uuid': 'tkfrcdwejhokkqceelxxey'}, 
    {'state': 'participating', 'name': 'p4', 'uuid': 'wmjtfcbvfyiidyrwifqvta'}], 
    'round_count': 1, 
    'next_player': -1, 
    'action_histories': 0}
    '''
    def receive_game_update_message(self, action_info, round_state):
        if self.debug_info_level > 0:
            print("\npalyer: {}".format(self.name))
            print("==========>  AI receive_game_update_message")
            print("action_info:{}, \nround_state:{}".format(action_info, round_state))
        return

    def receive_round_result_message(self, winners, action_info, round_state):
        if self.debug_info_level > 0:
            print("\npalyer: ".format(self.name))
            print("==========>  AI receive_round_result_message")
            print("winners:{}, \naction_info:{}, \nround_state:{}".format(winners, action_info, round_state))
        return