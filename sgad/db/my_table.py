"""

"""

import copy

import sqlalchemy

from sgad.db import engine

db_engine = engine.Engine()

# class MyTable(sqlalchemy.Table):
class MyTableFactory(object):

    default_cols = [sqlalchemy.Column('row_toggle', sqlalchemy.BOOLEAN, nullable = False, default = 1),
                    sqlalchemy.Column('update_ts', sqlalchemy.TIMESTAMP, nullable = False, default = '0000-00-00 00:00:00'),
                    sqlalchemy.Column('insert_ts', sqlalchemy.TIMESTAMP, nullable = False, default = '0000-00-00 00:00:00')]

    @classmethod
    def create_table(cls, table_name, foreign_key_cols = [], other_cols = [], indexes = [], metadata = db_engine.metadata):
        """create a table object that conforms to our database standards

        Args:
            table_name: name of the table
            foreign_key_columns: columns which are foreign keys to other tables
            other_columns: any other columns which are not foreign keys
            indexes: additional indexes (besides primary key) to be defined

        Returns:
            an sqlalchemy.Table object

        Raises:

        """

## name table appropriately and add primary key column
        t = sqlalchemy.Table('{}_{}'.format(db_engine.table_prefix, table_name),
                             db_engine.metadata,
                             sqlalchemy.Column('{}_id'.format(table_name), sqlalchemy.INTEGER, primary_key = True, autoincrement = True, nullable = False),
                             keep_existing = True,
                             mysql_engine='MyISAM')



## add foriegn key columns after primary key column
        for col in foreign_key_cols:
            t.append_column(col)
        
## add default columns after foriegn key columns

        for col in cls.default_cols:
## give a copy or else single column assigned to multiple tables            
            t.append_column(copy.copy(col))

## add other columns at the end
        for col in other_cols:
            t.append_column(col)

## additional indexes (i.e. not primary key)
        for index in indexes:
            t.append_constraint(index)

        return t, t.primary_key.columns.values()[0]

class MediaTableFactory(MyTableFactory):

## should change ext_id to be VARCHAR(511) in case have to use name for ext_id
    default_cols = MyTableFactory.default_cols + \
                      [sqlalchemy.Column('ext_id', sqlalchemy.VARCHAR(255), nullable = False),
                       sqlalchemy.Column('name', sqlalchemy.VARCHAR(511))]#, nullable = False]


class PickledTableFactory(MyTableFactory):

##using sha256 has for checksum so this length is ok
    default_cols = MyTableFactory.default_cols + \
                      [sqlalchemy.Column('pickled_checksum', sqlalchemy.VARCHAR(127), nullable = False),
                       sqlalchemy.Column('pickled_object', sqlalchemy.PickleType, nullable = False)]


class UninstantiableTableFactory(MyTableFactory):

    default_cols = MyTableFactory.default_cols + \
                      [sqlalchemy.Column('class_name', sqlalchemy.VARCHAR(63), nullable = False),
                       sqlalchemy.Column('friendly_name', sqlalchemy.VARCHAR(63), nullable = False)]