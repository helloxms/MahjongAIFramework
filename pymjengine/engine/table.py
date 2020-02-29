from pymjengine.engine.card import Card
from pymjengine.engine.seats import Seats
from pymjengine.engine.wall import Wall



class Table:

    def __init__(self, cheat_wall=None):
        self.seats = Seats()
        self.wall = cheat_wall if cheat_wall else Wall()
        self._river_tiles = []
        self.cur_player_pos = 1

    def get_river_tiles(self):
        return self._river_tiles[::]

    def add_river_tiles(self, tile):
        self._river_tiles.append(tile)

    def reset(self):
        self.wall.restore()
        self._river_tiles = []
        self.cur_player_pos = 1
        for player in self.seats.players:
            player.clear_handtiles()
            player.clear_action_histories()
            player.clear_pay_info()


    def next_active_player_pos(self, start_pos):
        return self.__find_entitled_player_pos(start_pos, lambda player: player.is_active())

    def next_ask_act_player_pos(self, start_pos):
        return self.__find_entitled_player_pos(start_pos, lambda player: player.get_ask_act()>0)
    
    def get_player_act(self, pos):
        print("get {} player act".format(pos))
        return self.seats.players[pos].get_ask_act()

    def serialize(self):
        river_tiles = [tile.to_id() for tile in self._river_tiles]
        return [
            Seats.serialize(self.seats),
            Wall.serialize(self.wall), river_tiles
        ]

    @classmethod
    def deserialize(self, serial):
        wall = Wall.deserialize(serial[1])
        river_tiles = [Tile.from_id(tid) for tid in serial[2]]
        table = self(cheat_wall=wall)
        table.seats = Seats.deserialize(serial[0])
        table._river_tiles = river_tiles
        return table

    def __find_entitled_player_pos(self, start_pos, check_method):
        players = self.seats.players
        search_targets = players + players
        search_targets = search_targets[start_pos+1:start_pos+len(players)+1]
        assert(len(search_targets) == len(players))
        match_player = next((player for player in search_targets if check_method(player)), -1)
        if match_player>0:
            return players.index(match_player)
        else:
            return -1
