

from collections import OrderedDict
from pymjengine.engine.message_builder import MessageBuilder

class MessageHandler:

    def __init__(self):
        self.algo_owner_map = {}

    def register_algorithm(self, uuid, algorithm):
        self.algo_owner_map[uuid] = algorithm

    def process_message(self, address, msg):
        receivers = self.__fetch_receivers(address)
        for receiver in receivers:
            if msg["type"] == 'ask':
                return receiver.respond_to_ask(msg["message"])
            elif msg["type"] == 'notification':
                receiver.receive_notification(msg["message"])
            else:
                raise ValueError("Received unexpected message which type is [%s]" % msg["type"])


    def __fetch_receivers(self, address):
        if address == -1:
            return self.algo_owner_map.values()
        else:
            if address not in self.algo_owner_map:
                raise ValueError("Received message its address [%s] is unknown" % address)
            return [self.algo_owner_map[address]]

        
class MessageSummarizer(object):

    def __init__(self, verbose):
        self.verbose = verbose

    def print_message(self, message):
        print(message)

    def summarize_messages(self, raw_messages):
        if self.verbose == 0: return

        summaries = [self.summarize(raw_message[1]) for raw_message in raw_messages]
        summaries = [summary for summary in summaries if summary is not None]
        summaries = list(OrderedDict.fromkeys(summaries))
        for summary in summaries: self.print_message(summary)

    def summarize(self, message):
        if self.verbose == 0: return None

        content = message["message"]
        message_type = content["message_type"]
        if MessageBuilder.GAME_START_MESSAGE == message_type:
            return self.summarize_game_start(content)
        if MessageBuilder.ROUND_START_MESSAGE == message_type:
            return self.summarize_round_start(content)
        if MessageBuilder.GAME_UPDATE_MESSAGE == message_type:
            return self.summarize_player_action(content)
        if MessageBuilder.ROUND_RESULT_MESSAGE == message_type:
            return self.summarize_round_result(content)
        if MessageBuilder.GAME_RESULT_MESSAGE == message_type:
            return self.summarize_game_result(content)

    def summarize_game_start(self, message):
        base = "Started the game with player %s for %d round."
        names = [player["name"] for player in message["game_information"]["seats"]]
        rule = message["game_information"]["rule"]
        return base % (names, rule["max_round"])

    def summarize_round_start(self, message):
        base = "Started the round %d"
        return base % message["round_count"]


    def summarize_player_action(self, message):
        print("summarize player action {}".format(message))
        base = '"%s" declared "%s"'
        players = message["round_state"]["seats"]
        action = message["action_info"]
        player_name = [player["name"] for player in players if player["uuid"] == action["player_uuid"]][0]
        return base % (player_name, action["action"])

    def summarize_round_result(self, message):
        base = '"%s" won the round %d (stack = %s)'
        winners = [player["name"] for player in message["winners"]]
        stack = { player["name"] for player in message["round_state"]["seats"] }
        return base % (winners, message["round_count"], stack)

    def summarize_game_result(self, message):
        print("summarize game result: {}".format(message))
        base = 'Game finished. (stack = %s)'
        stack = { player["name"] for player in message["game_information"]["seats"] }
        return base % stack

