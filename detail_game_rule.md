# detail game flow


server->client:
0. start game,shffule table wall,check 4 seats are 4 active player.
1. select the first player (banker)
2. start from the first player,every one get 14 tiles
3. start a round
4. a player take a tile from wall
client->server:
5. a player drop a tile to river
server->client:
6.who will do "chow pong kong tin hu" action?
client->server:
7. a player will do call request
server->client:
8. check the  rule right,refuse some one, authorize some one
client->server:
9. do the action requst
server->client:
10. check the rule right,update every one's state
if the hu action is right,finish the game
11. the next player recycle the same step 3-- step10
12. 
13. if the next player is the first player,a new round begin.
if the round count is over max-round,game finished.


