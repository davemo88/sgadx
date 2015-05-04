"""DataBase OBjects


"""
import inspect
import cPickle
import os
from datetime import datetime

import sqlalchemy

from sgadx.db import engine
from sgadx.util import util


db_engine = engine.Engine()


class DbObBase(object):
    """Database Object Base Class

    """

    foreign_key_cols = []

    other_cols = []

    table, primary_key_col = None, None


class Instantiable(DbObBase):
    """Instantiable objects

    Rows in the class' table correspond to instances
    if the class subclasses this class.

    """

    natural_key = sqlalchemy.Index('natural')

    @classmethod
    def get_saved_instance(cls, instance_id):
        """retrieve a saved instance of the class from the database

        Args:
            instance_id: primary key value and id attribute of resulting instance

        Returns:
            an instance of cls with cls.id = instance_id

        Raises:
            ???                                                                                               

        """

        ignore_cols = ['insert_ts', 'update_ts', 'row_toggle', cls.primary_key_col.name]

        cols = [col for col in cls.table.columns if col.name not in ignore_cols]

        query = db_engine.select(cols,
                                 cls.primary_key_col == instance_id).execute()

        if query.rowcount:

            row = query.fetchone()

            args_spec = inspect.getargspec(cls.__init__)

            args = []

            for arg in args_spec.args[1:]:

                    args.append(row[arg])

            return cls(*args)

        else:

## should i warn here?
            pass


    def __init__(self):

        self.id = self.get_id()


    def get_id(self):
        """get the id of the object from the database.

        if there isn't one, insert the object and return that id

        Args:

        Returns:

        Raises:


        """

        if hasattr(self, 'id') and self.id != None:

            return unicode(self.id)

        query = self.add_natural_key_where(db_engine.select([self.primary_key_col]))

        query_result = query.execute()

        if query_result.rowcount:

            return unicode(query_result.fetchone()[self.primary_key_col.name])

        else:

## should i warn here?
            return unicode(self.insert())


    def add_natural_key_where(self, query):
        """add a where clause to a query that
        matches the instances' natural key value

        obviously doesn't work with insert queries

        Args:
            query: the query to be modified

        Returns: an sqlalchemy query

        Raises:
            TypeError if you pass an insert query

        """

        for col_name in self.natural_key.columns.keys():

            query = query.where(self.table.c.get(col_name) == getattr(self, col_name))

        return query


    def insert(self):
        """insert the mob into its corresponding table

        Args:

        Returns: integer id of the inserted row

        Raises:

        """

        insert_values = self.get_insert_values()

        try:

            query = db_engine.insert(self.table,
                                     insert_values).execute()

            return query.lastrowid  

## don't insert duplicates
        except sqlalchemy.exc.IntegrityError:

## should i warn here
            pass


    def get_insert_values(self):
        """get the values to be inserted in the class' table

        Args:

        Returns: dictionary like {column_name : value}

        Raises:
        """

        ignore_cols = ['insert_ts', 'update_ts', 'row_toggle', self.primary_key_col.name]

        insert_values = {col_name : getattr(self, col_name) for col_name in self.table.columns.keys() if col_name not in ignore_cols}

        return insert_values


class Uninstantiable(DbObBase):
    """Uninstantiable objects

    Rows in the class' table correspond to classes or subclasses (not instances)
    if the class subclasses this class.

    """


    friendly_name = ''

    @classmethod
    def get_id(cls):


        query = db_engine.select([cls.primary_key_col],
                                 cls.table.c.get('class_name') == cls.__name__).execute()

        if query.rowcount:

            return query.fetchone()[cls.primary_key_col.name]

        else:

## should i warn here?
            pass


class UninstantiableHelper(object):
    """

    """

    @classmethod
    def maintain_table(cls, base_class):
        """

        """

        query = db_engine.select([base_class.table]).execute()

        existing_classes = {row['class_name'] for row in query}

        classes = {c.__name__ : c for c in util.Util.all_subclasses(base_class)}

        classes[base_class.__name__] = base_class

        for c in classes:

            if c in existing_classes:

                db_engine.update(base_class.table,
                                 base_class.table.c.get('class_name') == c,
                                 {'friendly_name' : classes[c].friendly_name}).execute()

            else:

                db_engine.insert(base_class.table,
                                 {'friendly_name' : classes[c].friendly_name,
                                  'class_name' : c}).execute()




    @classmethod
    def get_class(cls, base_class, class_id):
        """

        """

        query = db_engine.select([base_class.table.c.get('class_name')],
                                 base_class.primary_key_col == class_id).execute()

        if query.rowcount:

            subclasses = {c.__name__ : c for c in util.Util.all_subclasses(base_class)}

            return subclasses[query.fetchone()['class_name']]

        else:

## should i warn here?
            pass


class MediaBase(Instantiable):
    """Media Object Base Class

    """


    @classmethod
    def get_existing(cls):
        """Get all existing instances from the database. 

        Returns: a dictionary with natural keys mapped to primary keys




        """

        columns = [cls.primary_key_col] + cls.natural_key.columns.values()

        query = db_engine.select(columns).execute()

        return {tuple(row[col_name] for col_name in cls.natural_key.columns.keys()) : row[cls.primary_key_col.name] for row in query}


    def __init__(self, ext_id, name):

        self.ext_id = ext_id

        self.name = name

        super(MediaBase, self).__init__()