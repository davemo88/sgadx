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


class Run(db.Model):
    """

    """
    __table_name__ = 'run'

    id = db.Column(db.Integer, primary_key=True)
    sim = db.relationship('Sim')
    sim_id = db.Column(db.Integer, db.ForeignKey('sim.id'))


class AdExchange(Sim):
    """

    """
    __table_name__ = 'adx'

    num_consumers = db.Column(db.Integer)
    num_advertisers = db.Column(db.Integer)
    num_ads = db.Column(db.Integer)

## not required
    num_recommenders = db.Column(db.Integer)
    num_verifiers = db.Column(db.Integer)
## number of ads available to each advertiser    
    _consumers = db.relationship('Consumer')
    _advertisers = db.relationship('Advertiser')
    _recommenders = db.relationship('Recommender')
    _verifiers = db.relationship('Verifier')

    # consumers = {}
    # advertisers = {}
    # recommenders = {}
    # verifiers = {}

    __mapper_args__ = {
    'polymorphic_identity' : 'AdExchange'
    }


    def __init__(self, num_features, num_consumers, num_advertisers, num_ads, num_recommenders = 0, num_verifiers = 0):

        super(AdExchange, self).__init__(num_features=num_features)

        self.num_consumers = num_consumers
        self.num_advertisers = num_advertisers
        self.num_ads = num_ads
        self.num_recommenders = num_recommenders
        self.num_verifiers = num_verifiers

        self._consumers = self.generate_players(num_consumers, player.Consumer, click_threshold=0.5, conversion_threshold=0.999999)
        self._advertisers = self.generate_players(num_advertisers, player.Advertiser)
        self._recommenders = self.generate_players(num_recommenders, player.Recommender)
        self._verifiers = self.generate_players(num_verifiers, player.Verifier)

## this seems like bad style
        db.session.add(self)
        db.session.commit()

        self.consumers = {c.id : c for c in self._consumers}
        self.advertisers = {a.id : a for a in self._advertisers}
        self.recommenders = {r.id : r for r in self._recommenders}
        self.verifiers = {v.id : v for v in self._verifiers}

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):

        self.consumers = {c.id : c for c in self._consumers}
        self.advertisers = {a.id : a for a in self._advertisers}
        self.recommenders = {r.id : r for r in self._recommenders}
        self.verifiers = {v.id : v for v in self._verifiers}

    def run(self, num_iterations):
        """

        """

        r = Run(sim = self)
        db.session.add(r)
        db.session.commit()

## initialize consumer state machines
        for consumer in self.consumers.values():
            for advertiser_id in self.advertisers:

                consumer.advertiser_state_machines[advertiser_id] = consumer.get_state_machine()
                consumer.advertiser_state_machines[advertiser_id].init()

                # print consumer.id, advertiser_id, id(consumer.advertiser_state_machines[advertiser_id])
                # print 'init state for advertiser {}: '.format(advertiser_id), consumer.advertiser_state_machines[advertiser_id].current

        for i in range(num_iterations):

## pick a random consumer
            consumer_id = choice(self.consumers.keys())

            auction_result = game.auction_game(r,
                                               self.consumers[consumer_id],
                                               self.advertisers)

            db.session.add(auction_result)

            print 'iteration {}, advertiser {} wins auction. consumer {} in state {}.'\
                .format(i,
                        auction_result.receiver_id,
                        consumer_id,
                        self.consumers[consumer_id].advertiser_state_machines[auction_result.receiver_id].current)

## don't show an ad if nobody bids above 0
            if auction_result.winning_bid != 0:

                ad_result = game.ad_game(r,
                                         self.advertisers[auction_result.receiver_id],
                                         self.consumers[consumer_id])

                print 'advertiser {} shows ad {}. consumer {} takes action "{}"'\
                    .format(auction_result.receiver_id,
                            ad_result.ad_id,
                            consumer_id,
                            ad_result.consumer_action)

                db.session.add(ad_result)

            db.session.commit()            


    def generate_players(self, num_players, player_class=player.Player, **kwargs):
        """

        """

        try:

            d = distribution.Distribution.query.filter(distribution.Distribution.dist_name == 'uniform',
                                                       distribution.Distribution.dist_params == '{}').one()

        except sqlalchemy.orm.exc.NoResultFound:

            d = distribution.Distribution('uniform')
            db.session.add(d)
            db.session.commit()

        return [player_class(sim=self, distribution=d, **kwargs) for i in range(num_players)]

