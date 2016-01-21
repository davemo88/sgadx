"""

"""

from sgadx import db

import sqlalchemy

from numpy import array, random
from numpy.linalg import norm

from ast import literal_eval
# import decimal

class Distribution(db.Model):
    """

    """
    __table_name__ = 'distribution'

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(length=63))
    params = db.Column(db.String(length=63), default = '{}')

    __table_args__ = (sqlalchemy.Index('natural', 'name', 'params', unique = True), )

    def __init__(self, name, **kwargs):

        self.name = unicode(name)

        self.kwargs = unicode(repr(kwargs))

        super(Distribution, self).__init__()

        self.dist = random.__dict__[self.name]

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):

        self.dist = random.__dict__[self.name]

    def __repr__(self):

        return '{} distribution with params {}'.format(self.name, self.kwargs)

    def sample(self):
        """

        """

        return float(self.dist(**literal_eval(self.kwargs)))


    def draw_unit_vector(self, dim):
        """

        """

        v = array([self.sample() for i in range(dim)])

        return v / norm(v)