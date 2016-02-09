
from random import choice, random

from numpy import dot, zeros
from numpy.linalg import norm

from sqlalchemy import inspect

from sgadx import db, sim, player
from sgadx import sg

import sys

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

            print '\nRound {}:'.format(i)

            adx_rr = AdxRoundRecord(sim=self,round=i)

            records[adx_rr] = []

            for consumer in self.consumers:

                print 'Auction Game:'

                auction_gr = AuctionGame.play(consumer, self.advertisers, adx_rr)
                records[adx_rr].append(auction_gr)

                print 'Consumer {} sends message'.format(auction_gr.sender.id)
                print auction_gr.signal.features

                if auction_gr.action.val == 0:
                    print 'No advertiser bids'
                    print 'Consumer receives payoff {}'.format(auction_gr.sender_utility)    
                else:
                    print 'Advertiser {} wins with bid {}, and pays second price {}.'\
                    .format(auction_gr.receiver.id, auction_gr.action.val, -auction_gr.receiver_utility)
                    print 'Consumer receives payoff {} and Advertiser receives payoff {}'\
                    .format(auction_gr.sender_utility, auction_gr.receiver_utility)


                    print 'Ad Game:'
                    ad_gr = AdGame.play(auction_gr.receiver, consumer, adx_rr, auction_gr.signal)
                    records[adx_rr].append(ad_gr)

                    print 'Advertiser {} sends message'.format(ad_gr.sender.id)
                    print 'Consumer interaction is {}'.format(ad_gr.action.val)
                    print 'Advertiser receives payoff 0 and Consumer receives payoff {}'\
                    .format(ad_gr.receiver_utility)

                    self.conversion_rate_data[consumer].append({
                        'round': adx_rr.round,
                        'ad_features': ad_gr.signal.features,
                        'action': ad_gr.action.val,
                    })

                records[adx_rr] += self.roll_conversions(consumer, self.advertisers, adx_rr)

## birth // death
            self.prune()
            self.spawn()

        return records

    # def

    def roll_conversions(self, consumer, advertisers, round_record):
        """

        """

        adx_vector = self.get_adx_vector(consumer, round_record)

        conversions = []

        for a in advertisers:

            cvr = dot(adx_vector, a.features) / float(100)

            if random() < cvr:

                conversions.append(ConversionGameRecord(round_record=round_record,
                                                        sender=a,
                                                        receiver=consumer,
                                                        sender_utility=100,
                                                        receiver_utility=100*norm(dot(a.features, consumer.features))))

        return conversions

    def get_adx_vector(self, consumer, round_record):
        """

        """

        adx_vector = zeros((len(consumer.features),))
        total_action = 0

        for cvr_data in self.conversion_rate_data[consumer]:
            # print adx_vector
            adx_vector += (cvr_data['ad_features'] * float(cvr_data['action'])) /\
                          (2**(round_record.round - cvr_data['round']))

            total_action += float(cvr_data['action'])

        # print adx_vector, norm(adx_vector)

        adx_vector = adx_vector / norm(adx_vector)

## rounds range from 0 so need to add one here or else divide by zero error
        contribution = total_action / (2 * (round_record.round+1))

        c_adx_vec = (1 - contribution) * consumer.features + contribution * adx_vector

        c_adx_vec = c_adx_vec / norm(c_adx_vec)

        return c_adx_vec


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
        self.moves = [player.Signal(player=self, features=self.features,desc='Honest')]


    def signal(self, **kwargs):
        """
            random by default
        """

        return choice(self.signals())


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

class Advertiser(AdxPlayer):
    """

    """

    __mapper_args__ = {
        'polymorphic_identity' : 'Advertiser'
    }

class Promoter(Advertiser):
    """
        Promoter will bid according to how good their ad matches the Consumer message,
        not how well their product does, and then show the closest matching ad.
    """

    __mapper_args__ = {
        'polymorphic_identity' : 'Promoter'
    }

    def signal(self, **kwargs):
        """

        """

        signals = self.signals()

        if 'auction_signal' in kwargs:

            return max(*signals, key=lambda x: dot(x.features, kwargs['auction_signal'].features))

        else:

            return choice(signals)


    def action(self, signal, **kwargs):
        """

        """

        return player.Action(player=self, val=max(0,max([dot(s.features, signal.features) for s in self.signals()])))

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

        # print action.val, second_price.val

        if action.val == 0:
            advertiser = None
        elif second_price.val == 0:
## if only one advertiser bids then pay their bid            
            second_price.val = action.val
##
## losing bets are being added to the session implicitly (related to players I guess)
## doesn't cause any problems except clutter
##
## the following will remove losing bets from the session
## see http://pythoncentral.io/understanding-python-sqlalchemy-session/
##
        for _ in actions.values():        
            ins = inspect(_)
            if not ins.transient:
                db.session.expunge(_)

        return AuctionGameRecord(round_record=round_record,
                                 sender=consumer,
                                 receiver=advertiser,
                                 signal=signal,
                                 action=action,
                                 sender_utility=cls.get_sender_utility(consumer, signal),
                                 receiver_utility=cls.get_receiver_utility(second_price))


    # __mapper_args__ = {
    #     'polymorphic_identity': 'AuctionGame'
    # }

    @classmethod
    def get_sender_utility(cls, consumer, signal):

        return float(dot(consumer.features, signal.features))

    @classmethod
    def get_receiver_utility(cls, second_price):

        return -float(second_price.val) if second_price != '0' else None

class AuctionGameRecord(sg.GameRecord):

    __mapper_args__ = {
        'polymorphic_identity': 'AuctionGameRecord'
    }


class AdGame(sg.SignalingGame):

    sender_class = Advertiser
    receiver_class = Consumer

    # __mapper_args__ = {
    #     'polymorphic_identity': 'AdGame'
    # }

    @classmethod
    def play(cls, advertiser, consumer, round_record, auction_signal, **kwargs):

        # assert isinstance(advertiser, Advertiser)
        # assert isinstance(contribution, Consumer)
        # assert isinstance(round_record, AdxRoundRecord)

        signal = advertiser.signal(auction_signal=auction_signal)
        action = consumer.action(signal)

        return AdGameRecord(round_record=round_record,
                            sender=advertiser,
                            receiver=consumer,
                            signal=signal,
                            action=action,
                            sender_utility=cls.get_sender_utility(),
                            receiver_utility=cls.get_receiver_utility(signal, action, auction_signal))

    @classmethod
    def get_sender_utility(cls):

        return 0

    @classmethod
    def get_receiver_utility(cls, signal, action, auction_signal):

        return ((1+float(action.val)) * dot(signal.features, auction_signal.features) - 1)# / 1000

class AdGameRecord(sg.GameRecord):

    __mapper_args__ = {
        'polymorphic_identity': 'AdGameRecord'
    }

class ConversionGameRecord(sg.GameRecord):
    """

    """

    __mapper_args__ = {
        'polymorphic_identity': 'ConversionGameRecord'
    }