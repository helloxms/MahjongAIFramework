from pymjengine.engine.card import Card
from pymjengine.engine.seats import Seats
from pymjengine.engine.deck import Deck

class Table:

    def __init__(self, cheat_wall=None):
        self.seats = Seats()
        self.wall = cheat_wall if cheat_wall else Wall()
        self.river_tiles = []

    def get_river_tiles(self):
        return self._river_tiles[::]

    def add_river_tiles(self, tile):
        self._river_tiles.append(tile)

    def reset(self):
        self.wall.restore()
        self._river_tiles = []
        for player in self.seats.players:
            player.clear_handtiles()
            player.clear_action_histories()
            player.clear_pay_info()


    def next_active_player_pos(self, start_pos):
        return self.__find_entitled_player_pos(start_pos, lambda player: player.is_active())


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
        return self._player_not_found if match_player == -1 else players.index(match_player)

    _player_not_found = "not_found"

