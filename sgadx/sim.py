"""

"""

from sgadx import db

import sqlalchemy

class Sim(db.Model):
    """

    """

    __table_name__ = 'sim'

    id = db.Column(db.Integer, primary_key=True)
    rounds = db.Column(db.Integer)
    # dimension = db.Column(db.Integer)
    type = db.Column(db.String(63))

    __mapper_args__ = {
    'polymorphic_identity' : 'Sim',
    'polymorphic_on' : type
    }

    def run(self):
        """

        """

        for i in range(self.rounds):

            rr = RoundRecord(sim_id=self.id,
                             round=i)

    def prune(self):
        """
        remove dead player at end of round
        """

        pass

    def spawn(self):
        """
        create new players at end of round
        """

        pass


class RoundRecord(db.Model):
    """

    """
    __table_name__ = 'round_record'

    id = db.Column(db.Integer, primary_key=True)
    sim = db.relationship('Sim')
    sim_id = db.Column(db.Integer, db.ForeignKey('sim.id'))
    round = db.Column(db.Integer)
    type = db.Column(db.String(63))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'RoundRecord'
    }

class RoundEvent(db.Model):
    """

    """
    __table_name__ = 'round_event'

    id = db.Column(db.Integer, primary_key=True)
    round_record = db.relationship('RoundRecord')
    round_record_id = db.Column(db.Integer, db.ForeignKey('round_record.id'))
    player = db.relationship('Player')
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    type = db.Column(db.String(63))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'RoundEvent'
    }

class Spawn(RoundEvent):
    """

    """

    __mapper_args__ = {
        'polymorphic_identity': 'Spawn'
    }


class Prune(RoundEvent):
    """

    """

    __mapper_args__ = {
        'polymorphic_identity': 'Prune'
    }

