"""

"""

from app import db

import sqlalchemy

from numpy import array, random
from numpy.linalg import norm

from ast import literal_eval


class Distribution(db.Model):
    """

    """
    __table_name__ = 'distribution'

    id = db.Column(db.Integer, primary_key=True)
    
    dist_name = db.Column(db.Text)
    dist_params = db.Column(db.Text, default = '{}')

    # natural_key = sqlalchemy.Index('natural', 'dist_name', 'dist_params', unique = True)
    sqlalchemy.Index('natural', 'dist_name', 'dist_params', unique = True)

    def __init__(self, dist_name, **dist_params):

        self.dist_name = unicode(dist_name)

        self.dist_params = unicode(repr(dist_params))

        super(Distribution, self).__init__()

    def __repr__(self):

        return '{} distribution with params {}'.format(self.dist_name, self.dist_params)

    def sample(self):
        """

        must return value between 0 and 1

        """

        return random.__dict__[self.dist_name](**literal_eval(self.dist_params))


    def draw_unit_vector(self, dim):
        """

        """

        v = array([self.sample for i in range(dim)])

        return v / norm(v)



