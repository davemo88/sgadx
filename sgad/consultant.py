"""Consultant

"""


import sqlalchemy

from numpy import array, dot
from numpy.linalg import norm

from config import NUM_FEATURES

from sgad import db_engine

from sgad.db import db_ob, my_table



class Consultant(db_ob.Instantiable):

	def __init__(self):

		pass


class Recommender(Consultant):

	def __init__(self):

		pass


class Verifier(Consultant):

	def __init__(self):

		pass