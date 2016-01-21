"""Game

"""

from sgadx import db, player
from numpy import dot


class SignalingGame(object):

    sender_class = None
    receiver_class = None

    @classmethod
    def play(cls, sender, receiver, round_record_id, **kwargs):

        signal = sender.signal(**kwargs)
        action = receiver.action(signal, **kwargs)
        sender_utility = cls.get_sender_utility(**kwargs)
        receiver_utility = cls.get_receiver_utility(**kwargs)

        return SignalingGameRecord(round_record_id=round_record_id,
                                   sender_id=sender.id,
                                   receiver_id=receiver.id,
                                   signal_id=signal.id,
                                   action_id=action.id,
                                   sender_utility=sender_utility,
                                   receiver_utility=receiver_utility)

    @classmethod
    def get_sender_utility(cls,  **kwargs):

        pass

    @classmethod
    def get_receiver_utility(cls, **kwargs):

        pass

class SignalingGameRecord(db.Model):
    """

    """
    __table_name__ = 'signaling_game_record'

    id = db.Column(db.Integer, primary_key=True)
    round_record_id = db.Column(db.Integer, db.ForeignKey('round_record.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    signal_id = db.Column(db.Integer, db.ForeignKey('move.id'))
    action_id = db.Column(db.Integer, db.ForeignKey('move.id'))
    sender_utility = db.Column(db.Float())
    receiver_utility = db.Column(db.Float())
    type = db.Column(db.String(63))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'SignalingGameRecord'
    }