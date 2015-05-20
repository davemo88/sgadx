"""

"""

from app import db




class Sim(db.Model):
    __table_name__ = 'sim'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(63))
    num_features = db.Column(db.Integer)

    __mapper_args__ = {
    'polymorphic_identity' : 'Sim',
    'polymorphic_on' : type
    }

class AdExchange(Sim):
    __table_name__ = 'adx'

    num_consumers = db.Column(db.Integer)
    num_advertisers = db.Column(db.Integer)
    num_ads = db.Column(db.Integer)
    consumers = db.relationship('Consumer')
    advertisers = db.relationship('Advertiser')