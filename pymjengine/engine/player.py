
from pymjengine.engine.tile import Tile
from pymjengine.engine.mj_constants import MJConstants
import random

import sys

sys.path.append("..")
sys.path.append("../../")
from mahjong.tile import TilesConverter


class Player:

    ACTION_TAKE_STR = "TAKE"
    ACTION_CHOW_STR = "CHOW"
    ACTION_PONG_STR = "PONG"
    ACTION_KONG_STR = "KONG"
    ACTION_PLAY_STR = "PLAY"
    ACTION_TIN_STR = "TIN"
    ACTION_HU_STR = "HU" 
    ACTION_NONE_STR = "NONE" 

    def __init__(self, uuid, name="No Name"):
        self.name = name
        self.uuid = uuid
        self.ask_act = MJConstants.Action.START
        self.is_hu = False
        self.active_info = False
        self.hand_tiles = []
        self.action_histories = []
        self.last_drop_tile_136 = -1

    def drop_hand_tile_34(self, tile_34):
        tile_ids = [tile.to_id() for tile in self.hand_tiles]
        tile_136 = TilesConverter.find_34_tile_in_136_array(tile_34, tile_ids)
        if tile_136:
            self.drop_hand_tile_136(self, tile_136)

    def drop_hand_tile_136(self, tile_136):
        for tile in self.hand_tiles:
            if tile_136 == tile.iType:
                self.hand_tiles.remove(tile)
                self.last_drop_tile_136 = tile_136
                print("player:{} drop a handtile_136: {}".format(self.name, tile_136))
                break
        return tile_136

    def add_hand_tile_136(self, tile_136):
        self.hand_tiles.append(Tile(tile_136))

    def add_hand_tiles_136(self, tiles):
        for i in range(0, len(tiles)):
            self.hand_tiles.append( Tile.from_136_id(tiles[i]) )

    def clear_hand_tiles(self):
        self.hand_tiles = []

    def is_hu(self):
        return self.is_hu

    def set_hu(self, bHu):
        self.is_hu = bHu

    def is_active(self):
        return self.active_info

    def set_active(self, bActive):
        self.active_info = bActive
    
    def set_ask_act(self, act):
        self.ask_act = act
        
    def get_ask_act(self):
        # print("get_ask_act:{}".format(self.ask_act))
        return self.ask_act

    def add_action_history(self, kind ):
        history = None
        history = self.__get_history_node(kind)
        history = self.__add_uuid_on_history(history)
        self.action_histories.append(history)

    def clear_action_histories(self):
        self.action_histories = []

    def clear_active_info(self):
        self.active_info = False

    def get_handtile_size(self):
        return len(self.hand_tiles)

    def get_handtile_ids(self):
        tile_ids = [tile.to_id() for tile in self.hand_tiles]
        return [tile_ids]

    def serialize(self):
        tile_ids = [tile.to_id() for tile in self.hand_tiles]
        return [
            self.name, self.uuid, self.hand_tiles, tile_ids,\
            self.action_histories[::],self.active_info
        ]

    @classmethod
    def deserialize(self, serial):
        tiles = [tid for tid in serial[3]]
        player = self(serial[1], serial[0])
        if len(tiles) != 0:
            player.add_hand_tiles_136(tiles)
        player.action_histories = serial[4]
        player.active_info = serial[5]
        return player


    def __get_history_node(self, kind):
        if kind == MJConstants.Action.TAKE:
            return { "action" : self.ACTION_TAKE_STR }
        elif kind == MJConstants.Action.CHOW:
            return { "action" : self.ACTION_CHOW_STR }
        elif kind == MJConstants.Action.PONG:
            return { "action" : self.ACTION_PONG_STR }
        elif kind == MJConstants.Action.KONG:
            return { "action" : self.ACTION_KONG_STR }
        elif kind == MJConstants.Action.PLAY:
            return { "action" : self.ACTION_PLAY_STR }
        elif kind == MJConstants.Action.TIN:
            return { "action" : self.ACTION_TIN_STR }
        elif kind == MJConstants.Action.HU:
            return { "action" : self.ACTION_HU_STR }
        else:
            return { "action" : self.ACTION_NONE_STR }
 

    def __add_uuid_on_history(self, history):
        history["uuid"] = self.uuid
        return history
