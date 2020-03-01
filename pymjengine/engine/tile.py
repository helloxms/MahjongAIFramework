
class Tile:
    
    TILE_ID_STR_MAP={
      1  :  'M1',      2  :  'M2',      3  :  'M3',      4  :  'M4',      5  :  'M5',
      6  :  'M6',      7  :  'M7',      8  :  'M8',      9  :  'M9',
      10  :  'S1',      11  :  'S2',            12  :  'S3',      13  :  'S4',      14  :  'S5',
      15  :  'S6',      16  :  'S7',      17  :  'S8',      18  :  'S9',
      19  :  'P1',      20  :  'P2',      21  :  'P3',      22  :  'P4',      23  :  'P5',
      24  :  'P6',      25  :  'P7',      26  :  'P8',      27  :  'P9',      
      28  :  'E',      29  :  'S',      30  :  'W',      31  :  'N',       32  :  'C', 
      33  :  'F',       34  :  'P'
  }
      
    TILE_STR_ID_MAP ={
      'M1' : 1,      'M2' : 2,      'M3' : 3,      'M4' : 4,      'M5' : 5,
      'M6' : 6,      'M7' : 7,      'M8' : 8,      'M9' : 9,
      'S1' : 10,      'S2' : 11,      'S3' : 12,      'S4' : 13,      'S5' : 14,      'S6' : 15,
      'S7' : 16,      'S8' : 17,      'S9' : 18,
      'P1' : 19,      'P2' : 20,      'P3' : 21,      'P4' : 22,      'P5' : 23,
      'P6' : 24,      'P7' : 25,      'P8' : 26,      'P9' : 27,
      'E' : 28,      'S' : 29,      'W' : 30,      'N' : 31,      'C' : 32,
      'F' : 33,      'P' : 34
      }
      
    #default is int type
    def __init__(self, iType):
        self.iType = iType
        self.strType = self.TILE_ID_STR_MAP[iType]

    def __eq__(self, other):
        return self.iType == other.iType

    def __str__(self):
        return self.strType
    
#tid in [1 - 136]
    @classmethod
    def from_136_id(cls, tid):
        iType = int(tid/4)+1
        return cls(iType)

    @classmethod
    def from_id(cls, tid):
        iType = int(tid)
        return cls(iType)
    
    def to_id(self):
        return self.iType
