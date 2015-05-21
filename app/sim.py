"""

"""

from app import db, player, distribution, game

import sqlalchemy

from random import choice

class Sim(db.Model):
    """

    """
    __table_name__ = 'sim'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(63))
    num_features = db.Column(db.Integer)

    __mapper_args__ = {
    'polymorphic_identity' : 'Sim',
    'polymorphic_on' : type
    }

    def run(self):
        """

        """
        pass

# class SimPlayer(db.Model):
#     """

#     """
#     __table_name__ = 'sim_player'


#     sim = db.relationship('Sim')
#     sim_id = db.Column(db.Integer, db.ForeignKey('sim.id'))
#     player = db.relationship('Player')
#     player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

class AdExchange(Sim):
    """

    """
    __table_name__ = 'adx'
 
    # sim_players = db.relationship('SimPlayer')

    __mapper_args__ = {
    'polymorphic_identity' : 'AdExchange'
    }


    def __init__(self, consumers, advertisers, recommenders = [], verifiers = [], **kwargs):

        super(AdExchange, self).__init__(**kwargs)

        self.consumers = consumers
        self.advertisers = advertisers
        self.recommenders = recommenders
        self.verifiers = verifiers

    def run(self, num_iterations):
        """

        """

## initialize consumer state machines
        for consumer in self.consumers:
            for advertiser in self.advertisers:

                consumer.advertiser_state_machines[advertiser.id] = consumer.get_state_machine()
                consumer.advertiser_state_machines[advertiser.id].init()

        for i in range(num_iterations):

## pick a random consumer
            consumer = choice(self.consumers)

            auction_result = game.auction_game(self,
                                               consumer,
                                               self.advertisers)

            db.session.add(auction_result)

            print 'iteration {}, advertiser {} wins auction. consumer {} in state {}.'\
                .format(i,
                        auction_result.receiver_id,
                        consumer.id,
                        self.consumers[consumer.id].advertiser_state_machines[auction_result.receiver_id].current)

## don't show an ad if nobody bids above 0
            if auction_result.winning_bid != 0:

                ad_result = game.ad_game(self,
                                         self.advertisers[auction_result.receiver_id],
                                         self.consumers[consumer.id])

                print 'advertiser {} shows ad {}. consumer {} takes action "{}"'\
                    .format(auction_result.receiver_id,
                            ad_result.ad_id,
                            consumer.id,
                            ad_result.consumer_action)

                db.session.add(ad_result)

            db.session.commit()