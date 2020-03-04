
class Tile:
    
    TILE_ID_STR_MAP={
      0  :  'M1',      1  :  'M2',      2  :  'M3',      3  :  'M4',      4  :  'M5',
      5  :  'M6',      6  :  'M7',      7  :  'M8',      8  :  'M9',
      9  :  'S1',      10  :  'S2',      11  :  'S3',      12  :  'S4',      13  :  'S5',
      14  :  'S6',      15  :  'S7',      16  :  'S8',      17  :  'S9',
      18  :  'P1',      19  :  'P2',      20  :  'P3',      21  :  'P4',      22  :  'P5',
      23  :  'P6',      24  :  'P7',      25  :  'P8',      26  :  'P9',      
      27  :  'E',      28  :  'S',      29  :  'W',      30  :  'N',       31  :  'C', 
      32  :  'F',       33  :  'P'
  }
      
    TILE_STR_ID_MAP ={
      'M1' : 0,      'M2' : 1,      'M3' : 2,      'M4' : 3,      'M5' : 4,
      'M6' : 5,      'M7' : 6,      'M8' : 7,      'M9' : 8,
      'S1' : 9,      'S2' : 10,      'S3' : 11,      'S4' : 12,      'S5' : 13,      'S6' : 14,
      'S7' : 15,      'S8' : 16,      'S9' : 17,
      'P1' : 18,      'P2' : 19,      'P3' : 20,      'P4' : 21,      'P5' : 22,
      'P6' : 23,      'P7' : 24,      'P8' : 25,      'P9' : 26,
      'E' : 27,      'S' : 28,      'W' : 29,      'N' : 30,      'C' : 31,
      'F' : 32,      'P' : 33
      }
      
    #default is int type
    def __init__(self, iType):
        self.iType = iType
        self.strType = self.TILE_ID_STR_MAP[int(iType/4)]

    def __eq__(self, other):
        return self.iType == other.iType

    def __str__(self):
        return self.strType
    
#tid in [1 - 136]
    @classmethod
    def from_136_id(cls, tid):
        iType = int(tid)
        return cls(iType)

    @classmethod
    def from_id(cls, tid):
        iType = int(tid)
        return cls(iType)
    
    def to_id(self):
        return self.iType
