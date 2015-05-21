"""

"""

from app import db

import sqlalchemy

from numpy import array, random
from numpy.linalg import norm

from ast import literal_eval
import decimal

class Distribution(db.Model):
    """

    """
    __table_name__ = 'distribution'

    id = db.Column(db.Integer, primary_key=True)
    
    dist_name = db.Column(db.String)
    dist_params = db.Column(db.String, default = '{}')

    __table_args__ = (sqlalchemy.Index('natural', 'dist_name', 'dist_params', unique = True), )

    def __init__(self, dist_name, **dist_params):

        self.dist_name = unicode(dist_name)

        self.dist_params = unicode(repr(dist_params))

        super(Distribution, self).__init__()

        self.dist = random.__dict__[self.dist_name]

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):

        self.dist = random.__dict__[self.dist_name]

    def __repr__(self):

        return '{} distribution with params {}'.format(self.dist_name, self.dist_params)

    def sample(self):
        """

        """

        return decimal.Decimal(self.dist(**literal_eval(self.dist_params)))


    def draw_unit_vector(self, dim):
        """

        """

        v = array([self.sample() for i in range(dim)])

        return v / norm(v)

