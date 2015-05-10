"""Game Result

"""



import sqlalchemy

from numpy import random

from sgadx import db_engine

from sgadx.db import db_ob, my_table




class GameResult(db_ob.Instantiable):

    natural_key = sqlalchemy.Index('natural', unique = True)

    foreign_key_cols = []

    other_cols = []

    # table, primary_key_col = my_table.MyTableFactory.create_table()

    def __init__(self):

        super(GameResult, self).__init__()

    