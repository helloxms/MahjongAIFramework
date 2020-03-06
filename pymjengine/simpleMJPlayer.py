from pymjengine.engine.mj_constants import MJConstants
from pymjengine.engine.tile import Tile
from pymjengine.baseMJPlayer import BaseMJPlayer
import random
import sys

sys.path.append("..")
sys.path.append("../../")
from mahjong.tile import TilesConverter
from mahjong.divider import HandDivider
from mahjong.shanten import Shanten

# Do not forget to make parent class as "BaseMJPlayer"


class SimpleMJPlayer(BaseMJPlayer):

    def __init__(self, name, pos, debug_info_level=0):
        self.debug_info_level = debug_info_level
        self.name = name
        self.pos = pos
        self.hand_tiles = []
        self.kong_tiles = []
        self.pong_tiles = []
        self.chow_tiles = []
        self.cur_player = -1

    def is_chow_able(self, cur_pos, pos):
        if cur_pos == 3 and pos == 0:
            return True
        if cur_pos == pos-1:
            return True
        return False

    def drop_tile(self, tiles, tile_136):
        if tile_136 in tiles:
            tiles.remove(tile_136)
        return tiles

    def calc_kong_tile(self, hand_tiles, tile):
        tile_34 = int(tile/4)
        result = TilesConverter.to_34_array(hand_tiles)
        for i in range(0, len(result)):
            if result[i] == 3 and i == tile_34:
                return tile
        return -1

    def calc_pong_tile(self, hand_tiles, tile):
        tile_34 = int(tile/4)
        result = TilesConverter.to_34_array(hand_tiles)
        for i in range(0, len(result)):
            if result[i] == 2 and i == tile_34:
                return tile
        return -1

    '''
    0-6 left chow
    1-7 mid chow
    2-8 right chow
    
    tile_9 : is 0-8
    '''
    def __calc_chow(self, tiles, tile_9, offset):
        meld = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
        a = tile_9-2
        b = tile_9-1
        c = tile_9
        d = tile_9+1
        e = tile_9+2
        if 0 <= c <= 6 and d in tiles and e in tiles:
            meld[6] = c + offset
            meld[7] = d + offset
            meld[8] = e + offset
        if 1 <= c <= 7 and b in tiles and d in tiles:
            meld[3] = b + offset
            meld[4] = c + offset
            meld[5] = d + offset
        if 2 <= c <= 8 and a in tiles and b in tiles:
            meld[0] = a + offset
            meld[1] = b + offset
            meld[2] = c + offset
        return meld

    def calc_chow_tile(self, hand_tiles, tile_136):
        if tile_136 >= 108:
            return [], 0
        tiles = [int(tile/4) for tile in hand_tiles]
        tiles.sort()
        tile_34 = int(tile_136/4)
        meld_man = []
        meld_pin = []
        meld_sou = []
        melds = []
        meld_type = 0
        man = [t for t in tiles if t < 9]
        pin = [t for t in tiles if 9 <= t < 18]
        pin = [t - 9 for t in pin]
        sou = [t for t in tiles if 18 <= t < 27]
        sou = [t - 18 for t in sou]
        if tile_34 < 9 and len(man) >= 2:
            tile = tile_34
            offset = 0
            meld_man = self.__calc_chow(man, tile, offset)
            if sum(meld_man) > -6:
                meld_type = 1
                melds = meld_man
        elif 9 <= tile_34 < 18 and len(pin) >= 2:
            tile = tile_34 - 9
            offset = 9
            meld_pin = self.__calc_chow(pin, tile, offset)
            if sum(meld_pin) > -6:
                meld_type = 2
                melds = meld_pin
        elif 18 <= tile_34 < 27 and len(sou) >= 2:
            tile = tile_34 - 18
            offset = 18
            meld_sou = self.__calc_chow(sou, tile, offset)
            if sum(meld_sou) > -6:
                meld_type = 3
                melds = meld_sou
        return melds, meld_type

    '''
    melds = [a,b,c,b,c,d,c,d,e]
    melds[2] melds[4] melds[6] is the chow target tile.
    [a,b,c] is left chow
    [b,c,d] is mid chow
    [c,d,e] is right chow
    '''
    def calc_chow_tile_with_melds(self, hand_tiles, target_tile_136, melds):
        hand = HandDivider()
        shanten = Shanten()
        hand_tiles.sort()
        tiles_34_array = TilesConverter.to_34_array(hand_tiles)
        target_tile_34 = int(target_tile_136/4)
        min_shanten = 9
        min_shanten_pos = -1
        meld_array = []
        if melds[2] >= 0:
            meld_array.append([melds[0], melds[1], melds[2]])
        if melds[4] >= 0:
            meld_array.append([melds[3], melds[4], melds[5]])
        if melds[6] >= 0:
            meld_array.append([melds[6], melds[7], melds[8]])
        origin_shanten = shanten.calculate_shanten(tiles_34_array)
        tiles_34_array.append(target_tile_34)
        for i in range(0, len(tiles_34_array)):
            if tiles_34_array[i] > 0 and tiles_34_array[i] not in melds:
                tiles_34_array[i] -= 1
                count = shanten.calculate_shanten(tiles_34_array, meld_array)
                # print("cur shanten count:{}".format(count))
                if min_shanten > count:
                    min_shanten = count
                    min_shanten_pos = i
                tiles_34_array[i] += 1
        if min_shanten <= origin_shanten:
            drop_tile_136 = TilesConverter.find_34_tile_in_136_array(min_shanten_pos, hand_tiles)
            print("calc_chow_tile:  chow action drop id is:{} tile:{} ".format(drop_tile_136, Tile.TILE_ID_STR_MAP[min_shanten_pos]))
            print("calc_chow_tile:  find a chow action")
            tiles_34_array[min_shanten_pos] -= 1

            return True, drop_tile_136
        return False, -1

    def calc_drop_tile(self, hand_tiles):
        hand = HandDivider()
        shanten = Shanten()

        tiles_34_array = TilesConverter.to_34_array(hand_tiles)
        min_shanten = 9
        min_shanten_pos = -1
        for i in range(0, len(tiles_34_array)):
            if tiles_34_array[i] > 0:
                tiles_34_array[i] -= 1
                count = shanten.calculate_shanten(tiles_34_array)
                if min_shanten > count:
                    min_shanten = count
                    min_shanten_pos = i
                tiles_34_array[i] += 1

        if min_shanten_pos >= 0:
            print("calc_drop_tile: drop id_34:{} tile:{}".format(min_shanten_pos, Tile.TILE_ID_STR_MAP[min_shanten_pos]))
            tiles_34_array[min_shanten_pos] -= 1

        tile_136 = TilesConverter.find_34_tile_in_136_array(min_shanten_pos, hand_tiles)
        print("drop tile_136 id:{}".format(tile_136))
        if tile_136 is None:
            print("ERROR!ERROR!ERROR!ERROR!ERROR!ERROR!ERROR!ERROR!ERROR!ERROR!")

        count = shanten.calculate_shanten(tiles_34_array)
        if count == -1:
            result1 = hand.divide_hand(tiles_34_array)
            if len(result1) > 0:
                print(result1)
        return tile_136, count

    #  we define the logic to make an action through this method.
    #  this method would be the core of your AI
    '''
    valid_actions:{'valid_actions': [{'action1': 'chow', 'action2': 'pong', 'action3': 'kong', 
    'action4': 'take', 'action5': 'play', 'action6': 'tin', 'action7': 'hu'}]}
    hand_tiles:[55, 97, 105, 82, 41, 119, 52, 124, 69, 51, 89, 11, 61, 75]
    round_state: {'next_player': 3, 'round_count': 1, 
    'seats': [{'name': 'p0', 'uuid': 'ttqwmgnwjgzpglhqzsdtbj', 'state': 'active'}, 
    {'name': 'p1', 'uuid': 'ibhzxlybuaepfaznkrdvsv', 'state': 'active'}, 
    {'name': 'p2', 'uuid': 'uwcxxlimbsuqxuzajqkzie', 'state': 'active'}, 
    {'name': 'p3', 'uuid': 'urdyefdlxauzzuvudklyvb', 'state': 'active'}], 'action_histories': 0}
    cur_action:0
    cur_drop_tile_136:
    player:p2 :take
    '''
    def declare_action(self, valid_actions, hand_tiles, round_state, cur_action, last_drop_tile_136):
        # valid_actions 
        call_action_info = valid_actions
        response = [-1, -1, -1]
        response[0] = cur_action
        hand_tiles.sort()
        str_tiles = [ Tile.TILE_ID_STR_MAP[int(tile/4)] for tile in hand_tiles]

        self.hand_tiles = hand_tiles
        self.cur_player = round_state["cur_player"]
        if self.debug_info_level > 0:
            print("==========> client:player:{}  (BaseMJPlayer)AI receive check actions".format(self.name))
            # print("valid_actions:{} \nhand_tiles:{} \nround_state: {} \ncur_action:{}\nlast_drop_tile_136:{}".format(
            #   call_action_info, hand_tiles, round_state, cur_action, last_drop_tile_136))
            # print("cur_player:{}".format(round_state["cur_player"]))
            print("player:{} :{}".format(self.name, MJConstants.ACT_ID_STR_MAP[cur_action]))
        print("player:{}, hand tiles:{}".format(self.name, str_tiles))

        str_act = MJConstants.ACT_ID_STR_MAP[cur_action]
        if cur_action == 2:

            tile_136, count  = self.calc_drop_tile(hand_tiles)
            if tile_136 >= 0:
                self.hand_tiles.remove(tile_136)
                print("<========== client:player {}, response take, I will drop this {} id: {} tile~~~~~~~~~~~~".format(self.name, Tile.TILE_ID_STR_MAP[int(tile_136/4)], tile_136))
            if count == -1:
                print("\n\n*********************** response take, I will call HU!! ***********************")
                print("*********************** response take, I will call HU!! ***********************")
                print("*********************** response take, I will call HU!! ***********************\n\n")
            response = [2, tile_136, count]

        if cur_action in [3, 4, 6]:

            response[0] = 9
            if self.is_chow_able(self.cur_player, self.pos):
                print("now is chow check: tile:{}".format(last_drop_tile_136))
                melds, meld_type = self.calc_chow_tile(hand_tiles, last_drop_tile_136)
                if meld_type > 0:
                    print("find meld type:{} melds:{}".format(meld_type, melds))
                    result, drop_tile_136 = self.calc_chow_tile_with_melds(hand_tiles, last_drop_tile_136, melds)
                    if result:
                        response = [3, drop_tile_136, -1]
                    else:
                        print("{} is not proper tile to chow".format(last_drop_tile_136))

            print("<========== client:player {}, response act:{}, my choise is act:{} id:{}~~~~~~~~~~\n".format(self.name, str_act,
                                                        MJConstants.ACT_ID_STR_MAP[response[0]], response[1]))

        return response  # action returned here is sent to the mahjong engine

    #   game info
    '''
    game_info:{
    'rule': {'banker': 1, 'max_round': 2}, 
    'player_num': 4, 
    'seats': [
    {'uuid': 'tsuemzefiyxrxzqlhcnwpl', 'state': 'participating', 'name': 'p0'}, 
    {'uuid': 'sccsxzuuqcemvqdhgxbayy', 'state': 'participating', 'name': 'p1'}, 
    {'uuid': 'sfnsnwvmlobzjeecbhbcdo', 'state': 'participating', 'name': 'p2'}, 
    {'uuid': 'qmxaschksmbmdfxifarinm', 'state': 'participating', 'name': 'p3'}
    ]}
    '''
    def receive_game_start_message(self, game_info):
        if self.debug_info_level > 1:
            print("==========> client:player:{}  (BaseMJPlayer)AI receive_game_start_message".format(self.name))
            print("game_info:{}".format(game_info))
            print("banker:{}".format(game_info['rule']['banker']))
        return

    '''
    round_count:1,
    action_info:{'action': 'start', 'player_uuid': 'djuuvmrhgrrnapvisupqty'},
    seats:[
    {'state': 'participating', 'name': 'p0', 'uuid': 'djuuvmrhgrrnapvisupqty'}, 
    {'state': 'participating', 'name': 'p1', 'uuid': 'kzqdhnnfbvhscwhnlthpyd'}, 
    {'state': 'participating', 'name': 'p2', 'uuid': 'tkfrcdwejhokkqceelxxey'}, 
    {'state': 'participating', 'name': 'p3', 'uuid': 'wmjtfcbvfyiidyrwifqvta'}]
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
    {'state': 'participating', 'name': 'p0', 'uuid': 'djuuvmrhgrrnapvisupqty'}, 
    {'state': 'participating', 'name': 'p1', 'uuid': 'kzqdhnnfbvhscwhnlthpyd'}, 
    {'state': 'participating', 'name': 'p2', 'uuid': 'tkfrcdwejhokkqceelxxey'}, 
    {'state': 'participating', 'name': 'p3', 'uuid': 'wmjtfcbvfyiidyrwifqvta'}], 
    'round_count': 1, 
    'next_player': -1, 
    'action_histories': 0}
    '''
    def receive_game_update_message(self, action_info, round_state):
        self.cur_player = round_state["cur_player"]
        if self.debug_info_level > 1:
            print("==========> player:{}   (BaseMJPlayer)AI receive_game_update_message".format(self.name))
            print("action_info:{}, \nround_state:{}".format(action_info, round_state))
        return

    def receive_round_result_message(self, winners, action_info, round_state):
        self.cur_player = round_state["cur_player"]
        if self.debug_info_level > 1:
            print("==========> player:{}   (BaseMJPlayer)AI receive_round_result_message".format(self.name))
            print("winners:{}, \naction_info:{}, \nround_state:{}".format(winners, action_info, round_state))
        return
