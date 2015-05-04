"""Utility Function

"""

import sqlalchemy

from numpy import random

from sgadx import db_engine

from sgadx.db import db_ob, my_table


class UtilityFunction(db_ob.Instantiable):
    """ must return value between -1 and 1

    """

    natural_key = sqlalchemy.Index('natural', 'func_name', 'func_params', unique = True)

    other_cols = [sqlalchemy.Column('func_name', sqlalchemy.VARCHAR(31), nullable = False),
                  sqlalchemy.Column('func_params', sqlalchemy.VARCHAR(255), nullable = False),]

    table, primary_key_col = my_table.MyTableFactory.create_table(
        'utility_function',
        other_cols = other_cols,
        indexes = [natural_key])

    def __init__(self, func_name, **kwargs):

        self.func_name = func_name

        self.func_params = repr(**kwargs)

        self.func = self.get_func()

        self.kwargs = kwargs

    def get_func(self):

        pass

    def __call__(self, 

