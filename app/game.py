"""Game

"""

from app import db

class GameResult(db.Model):
    """

    """
    __table_name__ = 'game_result'

    id = db.Column(db.Integer, primary_key=True)
    run = db.relationship('Run')
    run_id = db.Column(db.Integer, db.ForeignKey('run.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('player.id'))

class AuctionGameResult(GameResult):
    """

    """
    __table_name__ = 'auction_game_result'

    id = db.Column(db.Integer, db.ForeignKey('game_result.id'), primary_key=True)
    # consumer = db.relationship('Consumer')
    # consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id'))
    # winning_advertiser = db.relationship('Advertiser')
    # advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    winning_bid = db.Column(db.DECIMAL(10,9))
    second_price = db.Column(db.DECIMAL(10,9))


class AdGameResult(GameResult):
    """

    """
    __table_name__ = 'ad_game_result'

    id = db.Column(db.Integer, db.ForeignKey('game_result.id'), primary_key=True)
    # consumer = db.relationship('Consumer')
    # consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id'))
    # advertiser = db.relationship('Advertiser')
    # advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    # ad = db.relationship('Ad')
    ad_id = db.Column(db.Integer, db.ForeignKey('ad.id'))
    consumer_action = db.Column(db.String(63))
    advertiser_utility = db.Column(db.DECIMAL(10,6))
    consumer_utility = db.Column(db.DECIMAL(10,6))


def auction_game(run, consumer, advertisers):

        content_request = consumer.get_message()

        bids = {}
        for a_id in advertisers:
## TODO: advertisers record information about users over time to better calculate EV
            # a.opponent_features[user.id]['last_message'] = message
            if consumer.id not in advertisers[a_id].consumer_history:

                advertisers[a_id].consumer_history[consumer.id] = {'last_content_request' : None,
                                                                   'converted' : False}

            advertisers[a_id].consumer_history[consumer.id]['last_content_request'] = content_request

            if not advertisers[a_id].consumer_history[consumer.id]['converted']:

                bids[a_id] = advertisers[a_id].get_action(consumer, content_request)

            else:
##  don't bid if the advertiser has already converted the users
                bids[a_id] = 0

## what about ties?
        winning_advertiser_id = max(bids.iterkeys(), key = (lambda key: bids[key]))
        winning_bid = bids.pop(winning_advertiser_id)
        second_price = bids[max(bids.iterkeys(), key = (lambda key: bids[key]))]


        return AuctionGameResult(run = run,
                                 sender_id = consumer.id,
                                 receiver_id = winning_advertiser_id,
                                 winning_bid = winning_bid,
                                 second_price = second_price)


def ad_game(run, advertiser, consumer):

        ad = advertiser.get_message(consumer = consumer)
        action = consumer.get_action(advertiser.id, ad.ad_features)
        advertiser_utility = advertiser.get_sender_utility(consumer, action)
        consumer_utility = consumer.get_receiver_utility(advertiser, action)

        if action == 'conversion':

            advertiser.consumer_history[consumer.id]['converted'] = True

        return AdGameResult(run = run,
                            sender_id = advertiser.id,
                            receiver_id = consumer.id,
                            ad_id = ad.id,
                            consumer_action = action,
                            advertiser_utility = advertiser_utility,
                            consumer_utility = consumer_utility)