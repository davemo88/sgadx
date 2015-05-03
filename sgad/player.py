"""Player

"""


import sqlalchemy

from numpy import array, dot
from numpy.linalg import norm

from config import NUM_FEATURES

from sgad import db_engine

from sgad.db import db_ob, my_table




class Player(db_ob.Instantiable):

    foriegn_key_cols = [sqlalchemy.Column('feature_distribution_id', sqlalchemy.INTEGER, nullable = False),
                        sqlalchemy.Column('utility_function_id', sqlalchemy.INTEGER, nullable = False)]

    other_cols = [sqlalchemy.Column('class_name', sqlalchemy.VARCHAR(63), nullable = False),
                  sqlalchemy.Column('features', sqlalchemy.VARCHAR(255), nullable = False)]

    table, primary_key_col = my_table.MyTableFactory.create_table(
        'player',
        foriegn_key_cols = foriegn_key_cols,
        other_cols = other_cols)

    player_type_id = None


    def __init__(self, feature_distribution, utility_function, features = None, opponents_features = {}):
        """

        """

## probability distribution to draw features from
        self.features_distribution = features_distribution
        
## features vector
        if features != None:
            self.features = features
        else:
            self.features = self.get_features(features)

## function to compute utility based on 
        self.utility_function = utility_function

        super(Player, self).__init__()


    def get_features(self):
        """use the given distribution to draw the features

        """
        
        features = array([self.features_distribution.get_feature() for i in range(NUM_FEATURES)])
        
        features = features / norm(features)

        return features


    def compare_features(self, opponent_features):
        """compare features to another player's

        """
    
        return dot(self.features, opponent_features)


    def get_message(self):
        """generate a message as a perturbed features vector

        """
    
        perturbation = self.get_features()

        perturbed_features = (self.features + perturbation) / norm(self.features + perturbation)

        return perturbed_features


    def get_action(self, message, sender):
        """perform an action

        """

        average = (sender_features + message) / norm(sender_features + message)

        comparison = self.compare_features(average)

        return max(comparison, 0)


    def get_insert_values(self):
        """

        """

        return {'class_name' : self.__class__.__name__,
                'features_distribution_id' : self.features_distribution.id,
                'features' : self.features,
                'utility_function_id' : self.utility_function.id}


class User(Player):
    """

    """

    pass


class Advertiser(Player):
    """

    """

    pass
