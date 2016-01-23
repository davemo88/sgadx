"""Player

"""

from random import random

import sqlalchemy

from numpy import array, dot
from numpy.linalg import norm

from sgadx import db

## cumulative ad experience below threshold -> adblock (death event)
class Player(db.Model):
    __table_name__ = 'player'


    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(63))

    _features = db.relationship('PlayerFeature', order_by=sqlalchemy.asc('pos'))

    __mapper_args__ = {
    'polymorphic_identity' : 'Player',
    'polymorphic_on' : type
    }

    def __init__(self, features, **kwargs):

        super(Player, self).__init__()

        self.features = features
        self._features = [PlayerFeature(player_id=self.id, pos=i, val=self.features[i]) for i in range(len(self.features))]

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):

        self.features = array([f.val for f in self._features])

    def signal(self, **kwargs):
        """

        """
        return Signal()


    def action(self, signal, **kwargs):
        """perform an action

        """
        return Action()

class Move(db.Model):
    """

    """
    __table_name__ = 'move'
    id = db.Column(db.Integer, primary_key=True)
    player = db.relationship('Player', backref='moves')
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    val = db.Column(db.String(63), default='0')
    type = db.Column(db.String(63))
    _features = db.relationship('MoveFeature', order_by=sqlalchemy.asc('pos'))

## otherwise we get "features is an invalid keyword argument for Signal"
    features = None

    __mapper_args__ = {
    'polymorphic_identity' : 'Move',
    'polymorphic_on' : type
    }

    def __init__(self, player=None, val='0', features=[], **kwargs):

        super(Move, self).__init__(player=player, val=val, features=features, **kwargs)

        self._features = [MoveFeature(move_id=self.id, pos=i, val=features[i]) for i in range(len(features))]

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):

        self.features = array([f.val for f in self._features])

class Signal(Move):
    """

    """

    __mapper_args__ = {
    'polymorphic_identity' : 'Signal',
    }


class Action(Move):
    """

    """

    __mapper_args__ = {
    'polymorphic_identity' : 'Action',
    }


class Feature(db.Model):
    """ 

    """
    __table_name__ = 'feature'

    id = db.Column(db.Integer, primary_key=True)
    pos = db.Column(db.Integer)
    val = db.Column(db.Float)
    type = db.Column(db.String(63))

    __mapper_args__ = {
        'polymorphic_identity' : 'Feature',
        'polymorphic_on' : type,
    }


class PlayerFeature(Feature):
    __table_name__ = 'player_feature'
    id = db.Column(db.Integer, db.ForeignKey('feature.id'), primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

    __mapper_args__ = {
        'polymorphic_identity' : 'PlayerFeature',
    }


class MoveFeature(Feature):
    __table_name__ = 'page_feature'
    id = db.Column(db.Integer, db.ForeignKey('feature.id'), primary_key=True)
    move_id = db.Column(db.Integer, db.ForeignKey('move.id'))

    __mapper_args__ = {
        'polymorphic_identity' : 'MoveFeature',
    }