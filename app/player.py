"""Player

"""


import sqlalchemy
import fysom

from numpy import array, dot
from numpy.linalg import norm

from app import db, feature, ad, distribution


class Player(db.Model):
    __table_name__ = 'player'

    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(63))

    distribution = db.relationship('Distribution')
    distribution_id = db.Column(db.Integer, db.ForeignKey('distribution.id'))
    sims = db.relationship('SimPlayer')
    _features = db.relationship('PlayerFeature', order_by=sqlalchemy.asc('position'))

    __mapper_args__ = {
    'polymorphic_identity' : 'Player',
    'polymorphic_on' : type
    }

    def __init__(self, distribution, num_features, **kwargs):

        super(Player, self).__init__()

        self.distribution = distribution

        self.num_features = num_features

        self.features = self.distribution.draw_unit_vector(self.num_features)

        self._features = [feature.PlayerFeature(player_id=self.id, position = i, value=self.features[i]) for i in range(len(self.features))]

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):

        self.features = array([f.value for f in self._features])

    def compare_features(self, opponent_features, **kwargs):
        """compare features to another player's

        """
    
        return dot(self.features, opponent_features)


    def get_perturbed_features(self, **kwargs):
        """generate a message as a perturbed features vector

        """

        perturbation = self.distribution.draw_unit_vector(self.num_features)

        perturbed_features = (self.features + perturbation) / norm(self.features + perturbation)

        return perturbed_features


    def get_message(self, **kwargs):
        """

        """

        return self.get_perturbed_features(**kwargs)


    def get_action(self, sender, message, **kwargs):
        """perform an action

        """

        average = (sender.features + message) / norm(sender.features + message)

        comparison = self.compare_features(average)

        return max(comparison, 0)


class Consumer(Player):
    """

    TODO: DMP frustration parameter. how much information does this user give to each DMP (this is per DMP)

    """

    __table_name__ = 'consumer'

    id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key = True)
    click_threshold = db.Column(db.DECIMAL(10,9))
    conversion_threshold = db.Column(db.DECIMAL(10,9))

    __mapper_args__ = {
        'polymorphic_identity' : 'Consumer'
    }

    state_multipliers = {
        'awareness' : 1,
        'consideration' : 10,
## once a user has purchased, they will no longer respond to ads  
        'purchase' : 0}


    def __init__(self, distribution, num_features, click_threshold, conversion_threshold):

        super(Consumer, self).__init__(distribution, num_features)

        self.click_threshold = click_threshold

        self.conversion_threshold = conversion_threshold

        self.advertiser_state_machines = {}

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):

        self.features = array([f.value for f in self._features])
        
        self.advertiser_state_machines = {}

    def get_action(self, advertiser_id, ad, **kwargs):
        """

        """

        # average = (sender.features + message) / norm(sender.features + message)

        comparison = self.compare_features(ad) * self.state_multipliers[self.advertiser_state_machines[advertiser_id].current]

        if comparison > self.conversion_threshold:

            self.advertiser_state_machines[advertiser_id].conversion()

            return 'conversion'

        elif comparison > self.click_threshold:

            self.advertiser_state_machines[advertiser_id].click()

            return 'click'

        else:

            return 'impression'


    def get_state_machine(self):

        return fysom.Fysom({
            'events' : [('init', '*', 'awareness'),
                        ('click', 'awareness', 'consideration'),
                        ('click', 'consideration', 'consideration'),
                        ('conversion', 'awareness', 'purchase'),
                        ('conversion', 'consideration', 'purchase')]})


class Advertiser(Player):
    """

    """

    __table_name__ = 'advertiser'

    id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key = True)
    ads = db.relationship('Ad')

    __mapper_args__ = {
        'polymorphic_identity' : 'Advertiser'
    }

    def __init__(self, distribution, num_features, num_ads, **kwargs):

        super(Advertiser, self).__init__(distribution, num_features)

        self.ads = [ad.Ad(self) for i in range(num_ads)]

## should know at least last message and if the user has converted
        self.consumer_history = {}

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):

        self.features = array([f.value for f in self._features])

## should know at least last message and if the user has converted
        self.consumer_history = {}        


    def get_message(self, consumer, **kwargs):
        """

        """

        best_fit = 0
        best_fit_index = None

        for i in range(len(self.ads)):

            fit = dot(self.consumer_history[consumer.id]['last_content_request'], self.ads[i].ad_features)

            if fit > best_fit:

                best_fit = fit

                best_fit_index = i

        return self.ads[best_fit_index]


class Recommender(Player):
    """

    """
    __table_name__ = 'recommender'

    id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key = True)

    __mapper_args__ = {
        'polymorphic_identity' : 'Recommender'
    }


class Verifier(Player):
    """

    """
    __table_name__ = 'verifier'

    id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key = True)

    __mapper_args__ = {
        'polymorphic_identity' : 'Verifier'
    }
