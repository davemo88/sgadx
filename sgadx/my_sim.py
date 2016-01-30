
from random import choice

from numpy import dot, zeros
from numpy.linalg import norm

from sqlalchemy import inspect

from sgadx import db, sim, player
from sgadx import sg

class Adx(sim.Sim):
    """

    """
    __table_name__ = 'adx'

    __mapper_args__ = {
    'polymorphic_identity' : 'Adx'
    }

    def __init__(self, rounds, consumers, advertisers, **kwargs):

        super(Adx, self).__init__(rounds=rounds)

        self.consumers = consumers
        self.advertisers = advertisers

## for computing conversion probalities
## each round will create a key-value pair like
## {round : 1, round_record_id: 2, ad_features: array([...]), action: 0.5}
        self.conversion_rate_data = {_ : [] for _ in self.consumers}

    def run(self):
        """

        """

        records = {}

        for i in range(self.rounds):

            adx_rr = AdxRoundRecord(sim=self,round=i)

            records[adx_rr] = []

            for consumer in self.consumers:
                auction_gr = AuctionGame.play(consumer, self.advertisers, adx_rr)
                ad_gr = AdGame.play(auction_gr.receiver, consumer, adx_rr)

                self.conversion_rate_data[consumer].append({
                    'round': adx_rr.round,
                    'ad_features': ad_gr.signal.features,
                    'action': ad_gr.action.val,
                })
## should we have another game record for this? would be a little abusive
## need to find a better way to record this                
                self.roll_conversions(consumer, self.advertisers, i)

                records[adx_rr].append(auction_gr)
                records[adx_rr].append(ad_gr)

## birth // death
            self.prune()
            self.spawn()

        return records

    # def

    def roll_conversions(self, consumer, advertisers, round):

        adx_vector = numpy.zeros((len(consumer.features),))
        cvr_data = self.conversion_rate_data[consumer]
        total_action = 0

        for i in range(len(cvr_data)):
            adx_vector += (float(cvr_data[i]['ad_features']) * float(cvr_data[i]['action'])) /\
                          (2**(round - cvr_data[i]['round']))

            total_action += float(cvr_data[i]['action'])

        adx_vector = adx_vector / norm(adx_vector)
        contribution = total_action / (2 * round)
        c_adx_vec = (1 - contribution) * consumer.features + contribution * adx_vector
        c_adx_vec = c_adx_vec / norm(c_adx_vec)

        for a in advertisers:

            cvr = dot(c_adx_vec, a.features) / float(100)


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


    def __init__(self, features, **kwargs):

        super(AdxPlayer, self).__init__(features, **kwargs)

## give each adxplayer the honest signal by default
        self.moves = [player.Signal(player=self, features=self.features)]


    def signal(self):
        """
            random by default
        """

        return choice(filter(lambda x: x.__class__ == player.Signal, self.moves))


    def action(self, signal, **kwargs):
        """
            honest by default
        """

        return player.Action(player=self, val=max(0,dot(self.features, signal.features)))


class Consumer(AdxPlayer):
    """

    """

    __mapper_args__ = {
        'polymorphic_identity' : 'Consumer'
    }

    def __init__(self, features, **):

        super(Consumer, self).__init__(features, **kwargs)      

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
        for _ in advertisers:
            actions[_] = _.action(signal)

        advertiser = max(actions.keys(), key=lambda x:float(actions[x].val))        
        action = actions.pop(advertiser)
        second_price = actions[max(actions.keys(), key=lambda x:float(actions[x].val))]

##
## losing bets are being added to the session implicitly (related to players I guess)
## doesn't cause any problems except clutter
##
## the following will remove losing bets from the session
## see http://pythoncentral.io/understanding-python-sqlalchemy-session/
##
        # for _ in actions.values():        
        #     ins = inspect(_)
        #     if not ins.transient:
        #         db.session.expunge(_)
        #     else:
        #         print ins.transient, ins.pending

        return AuctionGameRecord(round_record=round_record,
                                 sender=consumer,
                                 receiver=advertiser,
                                 signal=signal,
                                 action=action,
                                 sender_utility=cls.get_sender_utility(consumer, signal),
                                 receiver_utility=cls.get_receiver_utility(second_price))


    __mapper_args__ = {
        'polymorphic_identity': 'AuctionGame'
    }

    @classmethod
    def get_sender_utility(cls, consumer, signal):

        return dot(consumer.features, signal.features)

    @classmethod
    def get_receiver_utility(cls, second_price):

        return -float(second_price.val)

class AuctionGameRecord(sg.GameRecord):

    __mapper_args__ = {
        'polymorphic_identity': 'AuctionGameRecord'
    }


class AdGame(sg.SignalingGame):

    sender_class = Advertiser
    receiver_class = Consumer

    __mapper_args__ = {
        'polymorphic_identity': 'AdGame'
    }

class AdGameRecord(sg.GameRecord):

    __mapper_args__ = {
        'polymorphic_identity': 'AdGameRecord'
    }