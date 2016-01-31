from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
ad_feature = Table('ad_feature', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('ad_id', Integer),
)

player = Table('player', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('type', String(length=63)),
    Column('distribution_id', Integer),
    Column('sim_id', Integer),
)

feature = Table('feature', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('type', String(length=63)),
    Column('player_id', Integer),
    Column('value', DECIMAL(precision=10, scale=9)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['ad_feature'].create()
    post_meta.tables['player'].columns['sim_id'].create()
    post_meta.tables['feature'].columns['type'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['ad_feature'].drop()
    post_meta.tables['player'].columns['sim_id'].drop()
    post_meta.tables['feature'].columns['type'].drop()
