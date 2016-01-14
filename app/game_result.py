"""

"""


from app import db

class GameResult(db.Model):
    """

    """
    __table_name__ = 'game_result'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(63))
    sim = db.relationship('Sim')
    sim_id = db.Column(db.Integer, db.ForeignKey('sim.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    sender_utility = db.Column(db.DECIMAL(10,6), default = 0)
    receiver_utility = db.Column(db.DECIMAL(10,6), default = 0)

    __mapper_args__ = {
        'polymorphic_on' : type,
        'polymorphic_identity' : 'GameResult'
    }

class AuctionGameResult(GameResult):
    """

    """
    __table_name__ = 'auction_game_result'

    id = db.Column(db.Integer, db.ForeignKey('game_result.id'), primary_key=True)
    consumer = db.relationship('Consumer')
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id'))
    advertiser = db.relationship('Advertiser')
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    winning_bid = db.Column(db.DECIMAL(10,9))
    second_price = db.Column(db.DECIMAL(10,9))

    __mapper_args__ = {
        'polymorphic_identity' : 'AuctionGameResult'
    }

class AdGameResult(GameResult):
    """

    """
    __table_name__ = 'ad_game_result'

    id = db.Column(db.Integer, db.ForeignKey('game_result.id'), primary_key=True)
    consumer = db.relationship('Consumer')
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id'))
    advertiser = db.relationship('Advertiser')
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    ad = db.relationship('Ad')
    ad_id = db.Column(db.Integer, db.ForeignKey('ad.id'))
    consumer_action = db.Column(db.String(63))

    __mapper_args__ = {
        'polymorphic_identity' : 'AdGameResult'
    }
