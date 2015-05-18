"""Player

"""


import sqlalchemy

from numpy import array, dot
from numpy.linalg import norm

from config import NUM_FEATURES

from sgadx import db_engine

from sgadx.db import db_ob, my_table




class Player(db_ob.Instantiable):

    foreign_key_cols = [sqlalchemy.Column('feature_distribution_id', sqlalchemy.INTEGER, nullable = False),
                        sqlalchemy.Column('utility_function_id', sqlalchemy.INTEGER, nullable = False)]

    other_cols = [sqlalchemy.Column('class_name', sqlalchemy.VARCHAR(63), nullable = False),
                  sqlalchemy.Column('features', sqlalchemy.VARCHAR(255), nullable = False)]

    table, primary_key_col = my_table.MyTableFactory.create_table(
        'player',
        foreign_key_cols = foreign_key_cols,
        other_cols = other_cols)

    player_type_id = None


    def __init__(self, feature_distribution, utility_function, **kwargs):
        """

        """

        self.features_distribution = features_distribution
        
        if 'features' in kwargs:
            self.features = kwargs['features']
        else:
            self.features = self.get_features(features)

        self.utility_function = utility_function

        self.kwargs = kwargs

        self.state = [...]

        super(Player, self).__init__()


    def get_features(self, **kwargs):
        """use the given distribution to draw the features

        """
        
        features = array([self.features_distribution.get_feature() for i in range(NUM_FEATURES)])
        
        features = features / norm(features)

        return features


    def compare_features(self, opponent_features, **kwargs):
        """compare features to another player's

        """
    
        return dot(self.features, opponent_features)


    def get_message(self, **kwargs):
        """generate a message as a perturbed features vector

        """
    
        perturbation = self.get_features()

        perturbed_features = (self.features + perturbation) / norm(self.features + perturbation)

        return perturbed_features


    def get_action(self, sender_id, message, **kwargs):
        """perform an action

        """

        average = (sender.features + message) / norm(sender.features + message)

        comparison = self.compare_features(average)

        return max(comparison, 0)


    def get_insert_values(self, **kwargs):
        """

        """

        return {'class_name' : self.__class__.__name__,
                'features_distribution_id' : self.features_distribution.id,
                'features' : self.features,
                'utility_function_id' : self.utility_function.id}


class User(Player):
    """

    TODO: should add click / convert probability. when a user clicks / converts
    the advertiser can infer that the user's type is probably similar to the ad
    or advertiser's type 

    TODO: DMP frustration parameter. how much information does this user give to each DMP (this is per DMP)

    """

    def get_action(self, sender_id, message, **kwargs):

        average = (sender.features + message) / norm(sender.features + message)

        comparison = self.compare_features(average)


class Advertiser(Player):
    """

    """

    pass


class Recommender(Player):
    """

    """

    pass


class Verifier(Player):
    """

    """

    pass
