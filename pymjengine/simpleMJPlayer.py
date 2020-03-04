
from pymjengine.engine.mj_constants import MJConstants
from pymjengine.engine.tile import Tile
from pymjengine.baseMJPlayer import BaseMJPlayer
import random

# Do not forget to make parent class as "BaseMJPlayer"


class SimpleMJPlayer(BaseMJPlayer):  

    def __init__(self, name, debug_info_level=0):
        self.debug_info_level = debug_info_level
        self.name = name
        self.hand_tiles = []






        
    #  we define the logic to make an action through this method.  
    #  this method would be the core of your AI
    '''
    valid_actions:{'valid_actions': [{'action1': 'chow', 'action2': 'pong', 'action3': 'kong', 'action4': 'take', 'action5': 'play', 'action6': 'tin', 'action7': 'hu'}]}
    hand_tiles:['P9', 'M2', 'P1', 'M9', 'M1', 'M7', 'M8', 'M1', 'P8', 'P9', 'S6', 'C', 'P', 'M4']
    round_state: {'river_tiles': [], 'next_player': 3, 'round_count': 1, 
    'seats': [
    {'name': 'p1', 'uuid': 'cnbedzresnnaxflbpktlmk', 'state': 'active'}, 
    {'name': 'p2', 'uuid': 'rxmwobjzuhffloobebyoim', 'state': 'active'}, 
    {'name': 'p3', 'uuid': 'zoijvyspgzrctacppasqyu', 'state': 'active'}, 
    {'name': 'p4', 'uuid': 'kpownyaxvovpyxibceraqf', 'state': 'active'}], 
    'action_histories': 0}
    cur_action:1
    '''
    def declare_action(self, valid_actions, hand_tiles, round_state, cur_action):
        # valid_actions 
        call_action_info = valid_actions
        respons = cur_action

        if self.debug_info_level > 0:
            print("==========> player:{}  (BaseMJPlayer)AI receive check actions".format(self.name))
            # print("valid_actions:{} \nhand_tiles:{} \nround_state: {} \ncur_action:{}".format(
            #    call_action_info, hand_tiles, round_state, cur_action))
            print("player:{} :{}".format(self.name, MJConstants.ACT_ID_STR_MAP[cur_action]))

        str_act = MJConstants.ACT_ID_STR_MAP[cur_action]
        if cur_action == 2:
            print("<========== response take, I will drop this xx tile~~~~")
        if cur_action in [3,4,6]:
            a = [3,4,5,9,9,9,9,9,9,9,9,9,9,9]
            random.shuffle(a)
            respons = a[0]
            str_drop = ""
            if respons == 3 or respons == 4:
                str_drop = "and drop xx tile"
            print("<========== response act:{}, my choise is:{} {}~~~~~~~~~~\n".format( str_act, respons, str_drop))  
            if respons == 3:
                print("")              
        self.hand_tiles = [Tile.TILE_STR_ID_MAP[tile] for tile in hand_tiles] 
        return respons   # action returned here is sent to the mahjong engine

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
        if self.debug_info_level > 1:
            print("==========> player:{}  (BaseMJPlayer)AI receive_game_start_message".format(self.name))
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
        if self.debug_info_level > 1:
            print("==========> player:{}   (BaseMJPlayer)AI receive_round_start_message".format(self.name))
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
        if self.debug_info_level > 1:
            print("==========> player:{}   (BaseMJPlayer)AI receive_game_update_message".format(self.name))
            print("action_info:{}, \nround_state:{}".format(action_info, round_state))
        return

    def receive_round_result_message(self, winners, action_info, round_state):
        if self.debug_info_level > 1:
            print("==========> player:{}   (BaseMJPlayer)AI receive_round_result_message".format(self.name))
            print("winners:{}, \naction_info:{}, \nround_state:{}".format(winners, action_info, round_state))
        return