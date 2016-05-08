"""Player

"""

from random import choice

import sqlalchemy

from numpy import array, dot
from numpy.linalg import norm

from sgadx import db, sg, sim

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

class Move(db.Model):
    """

    """
    __table_name__ = 'move'
    id = db.Column(db.Integer, primary_key=True)
    player = db.relationship('Player', backref='moves')
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    val = db.Column(db.String(63), default='0')
    desc = db.Column(db.String(63))
    type = db.Column(db.String(63))

## otherwise we get "features is an invalid keyword argument for Signal"
    features = None

    __mapper_args__ = {
    'polymorphic_identity' : 'Move',
    'polymorphic_on' : type
    }

    def __init__(self, features, **kwargs):

        super(Move, self).__init__()

        self.features = features
        self._features = [MoveFeature(player_id=self.id, pos=i, val=self.features[i]) for i in range(len(self.features))]

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):

        self.features = array([f.val for f in self._features])
