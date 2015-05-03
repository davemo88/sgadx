
"""
This file contains classes to handle basic interaction with the database.
"""

from datetime import datetime

import sqlalchemy

import config

class Engine(object):

    def __init__(self, server=config.mysql_info['server'], port=config.mysql_info['port'], database=config.mysql_info['database'], \
     user=config.mysql_info['user'], password=config.mysql_info['password'], table_prefix=config.mysql_info['table_prefix']):

        self.server = server

        self.port = port

        self.database = database

        # self.user = user

        # self.password = password

        self.table_prefix = table_prefix

        self.engine = self.get_engine(user, password)

        self.metadata = self.get_metadata()

    def get_engine(self, user, password):

        engine = sqlalchemy.create_engine("mysql://{}:{}@{}:{}/{}".format(user,
                                                                          password,
                                                                          self.server,
                                                                          self.port,
                                                                          self.database))

        return engine

    def get_metadata(self):

        m = sqlalchemy.MetaData(self.engine)

        m.reflect()

        return m


    def get_table(self, table_name):

        if self.table_prefix != None and table_name.split('_')[0] != self.table_prefix:

            table_name = "{}_{}".format(self.table_prefix, table_name)

        return self.metadata.tables[table_name]

## use decorators here?
    def insert(self, table, values=None, inline=False, bind=None, prefixes=None, returning=None, return_defaults=False, **dialect_kw):

        values = QueryHelper.set_insert_ts(values)

        query = sqlalchemy.insert(table, values, inline, bind, prefixes, returning, return_defaults, **dialect_kw)

        return query


    def select(self, columns=None, whereclause=None, from_obj=None, distinct=False, having=None, correlate=True, prefixes=None, **kwargs):

        query = sqlalchemy.select(columns, whereclause, from_obj, distinct, having, correlate, prefixes, **kwargs)

        query = QueryHelper.enforce_row_toggle_conditions(query)

        return query


    def update(self, table, whereclause=None, values=None, inline=False, bind=None, prefixes=None, returning=None, return_defaults=False, **dialect_kw):

        query = sqlalchemy.update(table, whereclause, values, inline, bind, prefixes, returning, return_defaults, **dialect_kw)

        query = QueryHelper.enforce_row_toggle_conditions(query)

        return query


    def delete(self, table, whereclause=None, bind=None, returning=None, prefixes=None, **dialect_kw):

        query = sqlalchemy.delete(table, whereclause, bind, returning, prefixes, **dialect_kw)

        query = QueryHelper.enforce_row_toggle_conditions(query)

        return query

class QueryHelper(object):

    @classmethod
    def set_insert_ts(cls, insert_values):

        insert_ts = datetime.now()

        if type(insert_values) == list:

            for values in insert_values:

                values['insert_ts'] = insert_ts

        else:
# type(insert_values) == dict
            insert_values['insert_ts'] = insert_ts

        return insert_values

    @classmethod
    def enforce_row_toggle_conditions(cls, query):
        """Ensure that all queries include "where row_toggle = 1"
        for all tables involved unless explicitly contradicted
        in the query's where clause

        Args:
            query: the query to be inspected and modified if necessary

        """

        def get_where_clause_columns(query):
            """Get all columns in there where clause
            that 

            Args:
                query: the query to be inspected

            Returns:


            Raises:
                none

            """

            pass

        def get_from_clause_tables(query):
            """Get all tables in the from clause

            Args:
                query: the query to be inspected

            Returns:
                a list of table objects

            Raises:
                none

            """

            pass

        return query

