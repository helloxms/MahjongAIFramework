# SAMPLE OF CALLBACK ARGUMENTS
`BaseMJPlayer` class requires you to implement following 6 methods.
- `declare_action(self, valid_actions, tiles, round_state)`
- `receive_game_start_message(self, game_info)`
- `receive_round_start_message(self, round_count, action_info, seats)`
- `receive_game_update_message(self, round_count, action_info, round_state)`
- `receive_round_result_message(self, round_count, winner, action_info, round_state)`

In this document, we show actual argument of each callback method sampled from real game.

#### `declare_action(self, valid_actions, tiles, round_state)`
- valid_actions
```
[
  {'action': 'take', 'amount': 1},
  {'action': 'chow', 'amount': 1},
  {'action': 'pong', 'amount': 1},
  {'action': 'kong', 'amount': 1},
  {'action': 'play', 'amount': 1},
  {'action': 'joke', 'amount': 1},
  {'action': 'tin', 'amount': 1},
  {'action': 'hu', 'amount': 1},
  
]
```
- tiles
```
[
'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9',
'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9',
'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9',
'E','S','W','N','C','F','P'
]
```
- round_state
```
{
  'round_count': 2,
  'next_player': 0,
  'river_tiles': [''],
  'seats': [
    {'hand': '', 'state': 'participating', 'name': 'p1', 'uuid': 'ftwdqkystzsqwjrzvludgi'},
    {'hand': '', 'state': 'participating', 'name': 'p2', 'uuid': 'bbiuvgalrglojvmgggydyt'},
    {'hand': '', 'state': 'participating', 'name': 'p3', 'uuid': 'zkbpehnazembrxrihzxnmt'}
    {'hand': '', 'state': 'tin', 'name': 'p4', 'uuid': 'zkbpehnazembrxrihzxnmt'}
  ]
}
```

#### `receive_game_start_message(self, game_info)`
- game_info
```
{
  'player_num': 4,
  'rule': {
    'joke': 5,
    '': '',
    'max_round': 100,
    'max_tiles': 100,

  },
  'seats': [
    {'wall': 100, 'state': 'participating', 'name': 'p1', 'uuid': 'ftwdqkystzsqwjrzvludgi'},
    {'wall': 100, 'state': 'participating', 'name': 'p2', 'uuid': 'bbiuvgalrglojvmgggydyt'},
    {'wall': 100, 'state': 'participating', 'name': 'p3', 'uuid': 'zkbpehnazembrxrihzxnmt'}
    {'wall': 100, 'state': 'tin', 'name': 'p4', 'uuid': 'zkbpehnazembrxrihzxnmt'}
  ]
}
```

#### `receive_round_start_message(self, round_count, action_info, seats):`
- round_count
```
2
```
- action_info
```
['take':'M1']
```
- seats
```
[
    {'wall': 100, 'state': 'participating', 'name': 'p1', 'uuid': 'ftwdqkystzsqwjrzvludgi'},
    {'wall': 100, 'state': 'participating', 'name': 'p2', 'uuid': 'bbiuvgalrglojvmgggydyt'},
    {'wall': 100, 'state': 'participating', 'name': 'p3', 'uuid': 'zkbpehnazembrxrihzxnmt'}
    {'wall': 100, 'state': 'tin', 'name': 'p4', 'uuid': 'zkbpehnazembrxrihzxnmt'}
]
```


#### `receive_game_update_message(self, round_count, action_info, round_state)`
- round_count
```
2
```
- action_info
```
['take':'M1']
```
- round_state
```
{
  'round_count': 2,
  'next_player': 0,
  'river_tiles': [''],
  'seats': [
    {'hand': '', 'state': 'participating', 'name': 'p1', 'uuid': 'ftwdqkystzsqwjrzvludgi'},
    {'hand': '', 'state': 'participating', 'name': 'p2', 'uuid': 'bbiuvgalrglojvmgggydyt'},
    {'hand': '', 'state': 'participating', 'name': 'p3', 'uuid': 'zkbpehnazembrxrihzxnmt'}
    {'hand': '', 'state': 'tin', 'name': 'p4', 'uuid': 'zkbpehnazembrxrihzxnmt'}
  ]
}
```

#### `receive_round_result_message(self, round_count, winners, action_info, round_state)`
- round_count
```
2
```
- winners
```
[
  {'stack': 300, 'state': 'participating', 'name': 'p1', 'uuid': 'ftwdqkystzsqwjrzvludgi'}
]
```
- action_info
```
['take':'M1']
```
- round_state
```
{
  'round_count': 2,
  'next_player': 0,
  'river_tiles': [''],
  'seats': [
    {'hand': '', 'state': 'participating', 'name': 'p1', 'uuid': 'ftwdqkystzsqwjrzvludgi'},
    {'hand': '', 'state': 'participating', 'name': 'p2', 'uuid': 'bbiuvgalrglojvmgggydyt'},
    {'hand': '', 'state': 'participating', 'name': 'p3', 'uuid': 'zkbpehnazembrxrihzxnmt'}
    {'hand': '', 'state': 'tin', 'name': 'p4', 'uuid': 'zkbpehnazembrxrihzxnmt'}
  ]
}
```

