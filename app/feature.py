"""

"""

from app import db

class Feature(db.Model):
    """ 

    """
    __table_name__ = 'feature'

    id = db.Column(db.Integer, primary_key = True)
    index = db.Column(db.Integer)
    value = db.Column(db.DECIMAL(10,9))
    type = db.Column(db.String(63))

    __mapper_args__ = {
        'polymorphic_identity' : 'Feature',
        'polymorphic_on' : type,
    }


class PlayerFeature(Feature):
    __table_name__ = 'player_feature'
    id = db.Column(db.Integer, db.ForeignKey('feature.id'), primary_key = True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

    __mapper_args__ = {
        'polymorphic_identity' : 'PlayerFeature',
    }

class AdFeature(Feature):
    __table_name__ = 'ad_feature'

    id = db.Column(db.Integer, db.ForeignKey('feature.id'), primary_key = True)
    ad_id = db.Column(db.Integer, db.ForeignKey('ad.id'))

    __mapper_args__ = {
        'polymorphic_identity' : 'AdFeature',
    }