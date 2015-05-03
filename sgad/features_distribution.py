"""

"""

import sqlalchemy

from numpy import random

from sgad import db_engine

from sgad.db import db_ob, my_table


class FeaturesDistribution(db_ob.Instantiable):

    natural_key = sqlalchemy.Index('natural', 'dist_name', 'dist_params', unique = True)

    other_cols = [sqlalchemy.Column('dist_name', sqlalchemy.VARCHAR(31), nullable = False),
                  sqlalchemy.Column('dist_params', sqlalchemy.VARCHAR(255), nullable = False),]

    table, primary_key_col = my_tab le.MyTableFactory.create_table(
        'features_distribution',
        other_cols = other_cols,
        indexes = [natural_key])

    def __init__(self, dist_name, dist_params):

        self.dist_name = dist_name

        self.dist = self.get_dist()

        self.dist_params = dist_params

        super(FeaturesDistribution, self).__init__()


    def get_dist(self):

        if self.dist_name in random.__dict__:

            return random.__dict__[self.dist_name]

        else:

            raise ValueError('no such distribution: {}'.format(self.dist_name))


    def get_feature(self):
        """

        """

        return self.dist(**self.dist_params)

