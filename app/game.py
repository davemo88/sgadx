"""Game

"""

from app import db, game_result, player


def auction_game(sim, consumer, advertisers):

        content_request = consumer.get_message()

        bids = {}
        for advertiser in advertisers:
## TODO: advertisers record information about users over time to better calculate EV
            # a.opponent_features[user.id]['last_message'] = message
            if consumer.id not in advertiser.consumer_history:

                advertiser.consumer_history[consumer.id] = {'last_content_request' : None,
                                                            'converted' : False}

            advertiser.consumer_history[consumer.id]['last_content_request'] = content_request

            if not advertiser.consumer_history[consumer.id]['converted']:

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
                                             second_price = second_price)


def ad_game(sim, advertiser, consumer):

        ad = advertiser.get_message(consumer = consumer)
        action = consumer.get_action(advertiser.id, ad.ad_features)
        advertiser_utility = advertiser.get_sender_utility(consumer, action)
        consumer_utility = consumer.get_receiver_utility(advertiser, action)

        if action == 'conversion':

            advertiser.consumer_history[consumer.id]['converted'] = True

        return game_result.AdGameResult(sim = sim,
                                        sender_id = advertiser.id,
                                        receiver_id = consumer.id,
                                        ad = ad,
                                        advertiser = advertiser,                                        
                                        consumer = consumer,
                                        consumer_action = action,
                                        advertiser_utility = advertiser_utility,
                                        consumer_utility = consumer_utility)