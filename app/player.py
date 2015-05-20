"""Player

"""


import sqlalchemy
import fysom

from numpy import array, dot
from numpy.linalg import norm

from app import db


NUM_FEATURES = 10

class Player(db.Model):
    __table_name__ = 'player'

    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(63))


    distribution = db.relationship('Distribution')
    distribution_id = db.Column(db.Integer, db.ForeignKey('distribution.id'))
    _features = db.relationship('Feature')

    __mapper_args__ = {
    'polymorphic_identity' : 'Player',
    'polymorphic_on' : type
    }

    def __init__(self, distribution):

        self.distribution = distribution

        self.features = self.distribution.draw_unit_vector()

        super(Player, self).__init__()


    @sqlalchemy.orm.reconstructor
    def init_on_load(self):




    def get_features(self, **kwargs):
        """use the given distribution to draw the features

        """

        
        
        features = array([self.distribution.sample() for i in range(NUM_FEATURES)])
        
        features = features / norm(features)



        return features


    def compare_features(self, opponent_features, **kwargs):
        """compare features to another player's

        """
    
        return dot(self.features, opponent_features)


    def get_message(self, **kwargs):
        """generate a message as a perturbed features vector

        """

        perturbation = array([self.distribution.sample() for i in range(len(self.features))])
        
        perturbation = perturbation / norm(perturbation)

        perturbed_features = (self.features + perturbation) / norm(self.features + perturbation)

        return perturbed_features


    def get_action(self, sender, message, **kwargs):
        """perform an action

        """

        average = (sender.features + message) / norm(sender.features + message)

        comparison = self.compare_features(average)

        return max(comparison, 0)


    def get_sender_utility(self, opponent, action):

        pass

    def get_receiver_utility(self, opponent, action):

        pass


class Consumer(Player):
    """

    TODO: should add click / convert probability. when a user clicks / converts
    the advertiser can infer that the user's type is probably similar to the ad
    or advertiser's type 

    TODO: DMP frustration parameter. how much information does this user give to each DMP (this is per DMP)

    """

    __table_name__ = 'consumer'

    id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key = True)
    click_threshold = db.Column(db.DECIMAL(10,9))
    conversion_threshold = db.Column(db.DECIMAL(10,9))

    __mapper_args__ = {
        'polymorphic_identity' : 'consumer'
    }

    state_machine = fysom.Fysom({
            'events' : [('init', '*', 'awareness'),
                        ('click', 'awareness', 'consideration'),
                        ('conversion', 'awareness', 'purchase'),
                        ('conversion', 'consideration', 'purchase')]})

    state_threshold_multipliers = {
        'awareness' : 1,
        'consideration' : 10,
## once a user has purchased, they will no longer respond to ads     
        'purchase' : 0}

    def __init__(feature_distribution, click_threshold, conversion_threshold, **kwargs):

        self.feature_distribution = feature_distribution
        self.click_threshold = click_threshold
        self.conversion_threshold = conversion_threshold

        self.state_machine = fysom.Fysom({
            'events' : [('init', '*', 'awareness'),
                        ('click', 'awareness', 'consideration'),
                        ('click', 'consideration', 'consideration'),
                        ('conversion', 'awareness', 'purchase'),
                        ('conversion', 'consideration', 'purchase')]})

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.state_machine = fysom.Fysom({
            'events' : [('init', '*', 'awareness'),
                        ('click', 'awareness', 'consideration'),
                        ('conversion', 'awareness', 'purchase'),
                        ('conversion', 'consideration', 'purchase')]})

    def get_action(self, sender_id, message, **kwargs):

        average = (sender.features + message) / norm(sender.features + message)

        comparison = self.compare_features(average) * state_threshold_multipliers[self.state_machine.current]

        if comparison > self.conversion_threshold:

            self.state_machine.conversion()

            return 'conversion'

        elif comparison > self.click_threshold:

            self.state_machine.click()

            return 'click'

        else:

            return 'impression'



class Advertiser(Player):
    """

    """

    __table_name__ = 'advertiser'

    id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key = True)

    __mapper_args__ = {
        'polymorphic_identity' : 'Advertiser'
    }


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

