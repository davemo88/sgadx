"""Game

"""

from numpy import dot

from sgadx import db

class SignalingGame(object):

    sender_class = None
    receiver_class = None

    @classmethod
    def play(cls, sender, receiver, round_record, **kwargs):

        signal = sender.signal(**kwargs)
        action = receiver.action(signal, **kwargs)
        sender_utility = cls.get_sender_utility(**kwargs)
        receiver_utility = cls.get_receiver_utility(**kwargs)

        return GameRecord(round_record=round_record,
                          sender=sender,
                          receiver=receiver,
                          signal=signal,
                          action=action,
                          sender_utility=sender_utility,
                          receiver_utility=receiver_utility)

    @classmethod
    def get_sender_utility(cls,  **kwargs):

        pass

    @classmethod
    def get_receiver_utility(cls, **kwargs):

        pass

class GameRecord(db.Model):
    """

    """
    __table_name__ = 'game_record'

    id = db.Column(db.Integer, primary_key=True)
    round_record_id = db.Column(db.Integer, db.ForeignKey('round_record.id'))
    round_record = db.relationship('RoundRecord')
    sender_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    sender = db.relationship('Player', foreign_keys=[sender_id])
    receiver_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    receiver = db.relationship('Player', foreign_keys=[receiver_id])
    signal_id = db.Column(db.Integer, db.ForeignKey('move.id'))
    signal = db.relationship('Move', foreign_keys=[signal_id])
    action_id = db.Column(db.Integer, db.ForeignKey('move.id'))
    action = db.relationship('Move', foreign_keys=[action_id])
    sender_utility = db.Column(db.Float())
    receiver_utility = db.Column(db.Float())
    type = db.Column(db.String(63))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'GameRecord'
    }