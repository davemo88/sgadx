"""Game

"""

from app import player



class AuctionGame(object):

    @classmethod
    def __call__(cls, user, advertisers):

        content_request = user.get_message()

        bids = {}

        for a in advertisers:

## TODO: advertisers record information about users over time to better calculate EV
            # a.opponent_features[user.id]['last_message'] = message

            bids[a.id] = a.get_action(user.id, content_request)

## what about ties?
        winning_advertiser_id = max(bids.iterkeys(), key = (lambda key: bids[key]))

        winning_bid = bids.pop(winning_advertiser_id)

        second_price = bids[max(bids.iterkeys(), key = (lambda key: bids[key]))]

        return {'user_id' : user.id,
                'winning_advertiser_id' : winning_advertiser_id,
                'winning_bid' : winning_bid,
                'second_price' : second_price}


class AdGame(object):

    @classmethod
    def __call__(cls, advertiser, user, auction_results):

        ad = advertiser.get_message()

        interaction = user.get_action(advertiser.id, ad)




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

