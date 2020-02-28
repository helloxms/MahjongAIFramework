# PyMJEngine


Mahjong engine for AI development in Python

# Tutorial
This tutorial leads you to start point of Mahjong Game AI development!!
#### Outline of Tutorial
1. Create simple AI which always returns same action.
2. Play AI vs AI Mahjong game and see its result.

#### Installation
Before start AI development, we need to install *PyMJEngine*.  
You can use pip like this.
```
pip install PyMJEngine
```
This library supports Python3 (>3.6).

## Create first AI
In this section, we create simple AI which always declares *CALL* action.  
To create Mahjong AI, what we do is following

1. Create MJPlayer class which is subclass of [`PyMJEngine.players.BaseMJPlayer`]
2. Implement abstract methods which inherit from `BaseMJPlayer` class.


Here is the code of our first AI. (We assume you saved this file at `~/dev/mj_player.py`)  

```python
from pymjengine.players import BaseMJPlayer

class MJPlayer(BaseMJPlayer):  # Do not forget to make parent class as "BaseMJPlayer"

    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hand_tile, round_state):
        # valid_actions format => [hand_action_info, take_action_info, play_action_info]
        call_action_info = valid_actions[1]
        action, amount = call_action_info["action"], call_action_info["amount"]
        return action, amount   # action returned here is sent to the mahjong engine

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, action_info, seats):
        pass

    def receive_game_update_message(self, action_info, round_state):
        pass

    def receive_round_result_message(self, round_count, action_info, round_state):
        pass


```
If you are interested in what each callback method receives, See [AI_CALLBACK_FORMAT.md]

## Play AI vs AI mahjong game
Ok, let's play the Mahjong game by using our created `MJPlayer`.  
To start the game, what we need to do is following

1. Define game rule through `Config` object (ex. start stack, rule)
2. Register your AI with `Config` object.
3. Start the game and get game result

Here is the code to play mahjong for 15 round with our created `MJPlayer`.
```python
from pymjengine.api.game import setup_config, start_mj

config = setup_config(max_round=100, initial_stack=144, rule=1)
config.register_player(name="p1", algorithm=MJPlayer())
config.register_player(name="p2", algorithm=MJPlayer())
config.register_player(name="p3", algorithm=MJPlayer())
config.register_player(name="p4", algorithm=MJPlayer())
game_result = start_mj(config, verbose=1)
```
We set `verbose=1`, so simple game logs are output after `start_mj` call.
```
Started the round 1

"p1" played "take:M1, play:M1 "
"p2" played "take:S2, play:M2 "
"p1" played "take:S1, play:S1 "
"p2" played "take:P2, play:S2 "

Started the round 2
...
"['p1']" won the round 15 (stack = {'M1M2M3M5M5M5S5S6S7S9S9S9P2P2'})
```
Finally, let's check the game result !!
```python
>>> print game_result
{
  'rule': {'1'},
  'players': [
    {'hand': {'M1M2M3M5M5M5S5S6S7S9S9S9P2P2'}, 'state': 'participating', 'name': 'p1', 'uuid': 'ijaukuognlkplasfspehcp'},
    {'hand': {'M1M2M3M5M5M5S5S6S7S9S9S9P2P2'}, 'state': 'participating', 'name': 'p2', 'uuid': 'uadjzyetdwsaxzflrdsysj'},
    {'hand': {'M1M2M3M5M5M5S5S6S7S9S9S9P2P2'}, 'state': 'participating', 'name': 'p3', 'uuid': 'tmnkoazoqitkzcreihrhao'}
    {'hand': {'M1M2M3M5M5M5S5S6S7S9S9S9P2P2'}, 'state': 'participating', 'name': 'p3', 'uuid': 'tmnkoazoqitkzcreihrhao'}
  ]
}
```

# Documentation
For mode detail, please checkout [doc site](https://helloxms.github.io/PyMJEngine/)

