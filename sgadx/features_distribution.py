"""

"""

import sqlalchemy

from numpy import random

from sgadx import db_engine

from sgadx.db import db_ob, my_table


class FeaturesDistribution(db_ob.Instantiable):
    """

    """

    natural_key = sqlalchemy.Index('natural', 'dist_name', 'dist_params', unique = True)

    other_cols = [sqlalchemy.Column('dist_name', sqlalchemy.VARCHAR(31), nullable = False),
                  sqlalchemy.Column('dist_params', sqlalchemy.VARCHAR(255), nullable = False),]

    table, primary_key_col = my_table.MyTableFactory.create_table(
        'features_distribution',
        other_cols = other_cols,
        indexes = [natural_key])

    def __init__(self, dist_name, **kwargs):

        self.dist_name = dist_name

        self.dist_params = repr(kwargs)

        self.dist = self.get_dist()

        self.kwargs = kwargs

        super(FeaturesDistribution, self).__init__()


    def get_dist(self):

        if self.dist_name in random.__dict__:

            return random.__dict__[self.dist_name]

        else:

            raise ValueError('no such distribution: {}'.format(self.dist_name))


    def get_feature(self):
        """

        """

        return self.dist(**self.kwargs)

