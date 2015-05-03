"""

"""

from sgad import player

class SignalingGame(object):

    @classmethod
    def signal(self, sender, receivers):

        message = sender.get_message()

        actions = {r.id : r.get_action(message) for r in receivers}

        return message, actions

    def __init__(self, senders, receivers, recommenders = [], verifiers = []):

        self.senders = senders

        self.receivers = receivers


def auction_game(user_player, advertiser_players):

    message = user_player.get_message()
    
## could be a matrix multiplication which is probably faster
    bids = [advertiser_player.bid(user_player.features, message) for advertiser_player in advertiser_players]
    
    winner = bids.index(max(bids))
    
    bids.pop(winner)

    second_price = max(bids)
    
    payoffs = [-bid/1000.0 for bid in bids]

    payoffs.insert(winner, -second_price)

    return winner, payoffs

def impression_game(advertiser_player, user_player):

    message = advertiser_player.get_message()

    if user_player.purchase(message, advertiser_player.features):

        return [2, 2]

    else:

        return [0,0]

