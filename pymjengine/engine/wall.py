from functools import reduce
import random
from pymjengine.engine.tile import Tile




class Wall:

    def __init__(self, wall_ids=None, cheat=False, cheat_tile_ids=[]):
        #print("init wall, wall ids:{}".format(wall_ids))
        self.cheat = cheat
        self.cheat_tile_ids = cheat_tile_ids
        self.wall = [Tile.from_id(tid) for tid in wall_ids] if wall_ids else self.__setup()

    
    def draw_tile(self):
        tile = self.wall.pop()
        return tile.to_id()

    def draw_tiles(self, num):
        tiles = reduce(lambda acc, _: acc + [self.draw_tile()], range(num), [])
        return tiles

    def size(self):
        return len(self.wall)

    def restore(self):
        self.wall = self.__setup()

    def shuffle(self):
        if not self.cheat:
            random.shuffle(self.wall)

# serialize format : [cheat_flg, cheat_tile_ids, wall_tile_ids]
    def serialize(self):
        return [self.cheat, self.cheat_tile_ids, [tile.to_id() for tile in self.wall]]

    @classmethod
    def deserialize(self, serial):
        cheat, cheat_tile_ids, wall_ids = serial
        return self(wall_ids=wall_ids, cheat=cheat, cheat_tile_ids=cheat_tile_ids)

    def __setup(self):
        if self.cheat:
            return self.__setup_cheat_wall()
        else:
            return self.__setup_136_tiles()

    def __setup_136_tiles(self):
        tiles = [Tile.from_136_id(tid) for tid in range(0,136)]
        random.shuffle(tiles)
        return tiles

    def __setup_cheat_wall(self):
        tiles = [Tile.from_id(tid) for tid in self.cheat_tile_ids]
        return tiles[::-1]

