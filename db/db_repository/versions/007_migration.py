from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
feature = Table('feature', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('index', INTEGER),
    Column('value', DECIMAL(precision=10, scale=9)),
    Column('type', VARCHAR(length=63)),
)

feature = Table('feature', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('position', Integer),
    Column('value', DECIMAL(precision=10, scale=9)),
    Column('type', String(length=63)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['feature'].columns['index'].drop()
    post_meta.tables['feature'].columns['position'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['feature'].columns['index'].create()
    post_meta.tables['feature'].columns['position'].drop()
