

from numpy import dot

from sgadx import db, sim, player
from sgadx import sg

class Adx(sim.Sim):
    """

    """
    __table_name__ = 'adx'

    __mapper_args__ = {
    'polymorphic_identity' : 'Adx'
    }

    def __init__(self, rounds, dimensionconsumers, advertisers, **kwargs):

        super(AdExchange, self).__init__(rounds, **kwargs)

        self.consumers = consumers
        self.advertisers = advertisers

    def run(self):
        """

        """

        for i in range(self.rounds):

            rr = AdxRoundRecord(sim_id=self.id,round=i)

            db.add(rr)

            for c in self.consumers:
                AuctionGame.play(c, self.advertisers)
                # c.convert()

## birth // death
            self.prune()
            self.spawn()

class AdxRoundRecord(sim.RoundRecord):
    """

    """
    # __table_name__ = 'adx_round_record'

    id = db.Column(db.Integer, db.ForeignKey('round_record.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'AdxRoundRecord'
    }

class AdxPlayer(player.Player):
    """

    """
    __table_name__ = 'adx_player'

class Consumer(AdxPlayer):
    """

    """

    __mapper_args__ = {
        'polymorphic_identity' : 'Consumer'
    }

class Advertiser(AdxPlayer):
    """

    """

    __mapper_args__ = {
        'polymorphic_identity' : 'Advertiser'
    }


class AuctionGame(sg.SignalingGame):

    sender_class = Consumer
    receiver_class = Advertiser

    @classmethod
    def play(cls, consumer, advertisers, round_record):

        signal = consumer.signal()
        
        actions = {}
        
        for a in self.advertisers:
        
            actions[a] = advertiser.action(signal)
        
        advertiser = max(actions.keys(), key=lambda x:float(actions[x].val))
        
        action = actions.pop(advertiser)      

        second_price = actions[max(actions.keys(), key=lambda x:float(actions[x].val))]

        return AuctionGameRecord(round_record = round_record,
                                 sender_id = consumer.id,
                                 receiver_id = advertiser.id,
                                 signal_id = signal.id,
                                 action_id = action.id,
                                 sender_utility = cls.get_sender_utility(consumer, signal),
                                 receiver_utility = cls.get_receiver_utility(second_price))


    __mapper_args__ = {
        'polymorphic_identity': 'AuctionGame'
    }

    @classmethod
    def get_sender_utility(cls, consumer, signal):

        return dot(consumer.features, signal)

    @classmethod
    def get_receiver_utility(cls, second_price):

        return -second_price

class AuctionGameRecord(sg.SignalingGameRecord):

    __mapper_args__ = {
        'polymorphic_identity': 'AuctionGameRecord'
    }


class AdGame(sg.SignalingGame):

    sender_class = Advertiser
    receiver_class = Consumer

    __mapper_args__ = {
        'polymorphic_identity': 'AdGame'
    }


class AdGameRecord(sg.SignalingGameRecord):

    __mapper_args__ = {
        'polymorphic_identity': 'AdGameRecord'
    }