"""Game

"""

from app import db, game_result, player
from numpy import dot


class SignalingGame(object):

    @classmethod
    def play(cls, **kwargs):

        pass

    @classmethod
    def get_sender_utility(cls,  **kwargs):

        pass

    @classmethod
    def get_receiver_utility(cls, **kwargs):

        pass


class AuctionGame(SignalingGame):

    @classmethod
    def play(cls, sim, consumer, advertisers):

        content_request = consumer.get_message()

        bids = {}
        for advertiser in advertisers:
## TODO: advertisers record information about users over time to better calculate EV
            # a.opponent_features[user.id]['last_message'] = message
            if consumer.id not in advertiser.consumer_history:

                advertiser.consumer_history[consumer.id] = {'last_content_request' : None,
                                                            'last_action' : None}

            advertiser.consumer_history[consumer.id]['last_content_request'] = content_request

            if advertiser.consumer_history[consumer.id]['last_action'] != 'conversion':

                bids[advertiser] = advertiser.get_action(consumer, content_request)

            else:
##  don't bid if the advertiser has already converted the users
                bids[advertiser] = 0

## what about ties?
        winning_advertiser = max(bids.iterkeys(), key = (lambda key: bids[key]))
        winning_bid = bids.pop(winning_advertiser)
        second_price = bids[max(bids.iterkeys(), key = (lambda key: bids[key]))]

        return game_result.AuctionGameResult(sim = sim,
                                             sender_id = consumer.id,
                                             receiver_id = winning_advertiser.id,
                                             consumer = consumer,
                                             advertiser = winning_advertiser,                                 
                                             winning_bid = winning_bid,
                                             second_price = second_price,
                                             receiver_utility = -second_price)



class AdGame(SignalingGame):

    @classmethod
    def play(cls, sim, advertiser, consumer):

        ad = advertiser.get_message(consumer = consumer)
        action = consumer.get_action(advertiser.id, ad.ad_features)
        advertiser_utility = cls.get_sender_utility(consumer, advertiser, ad, action)
        consumer_utility = cls.get_receiver_utility(consumer, advertiser, ad, action)

        advertiser.consumer_history[consumer.id]['last_action'] = action

        return game_result.AdGameResult(sim = sim,
                                        sender_id = advertiser.id,
                                        receiver_id = consumer.id,
                                        ad = ad,
                                        advertiser = advertiser,                                        
                                        consumer = consumer,
                                        consumer_action = action,
                                        sender_utility = advertiser_utility,
                                        receiver_utility = consumer_utility)


    @classmethod
    def get_sender_utility(cls, consumer, advertiser, ad, action, **kwargs):

        if action != 'conversion':

            return 0

        else:

            return 1 # advetiser.product_price

    @classmethod
    def get_receiver_utility(cls, consumer, advertiser, ad, action, **kwargs):

        if action == 'conversion':

            ad_integrity = dot(advertiser.features, ad.ad_features)

            product_fit = dot(advertiser.features, consumer.features)

            return ad_integrity * product_fit # * advertiser.product_price

        else:

            return -1
