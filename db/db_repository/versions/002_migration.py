from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
ad_feature = Table('ad_feature', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('ad_id', Integer),
    Column('value', DECIMAL(precision=10, scale=9)),
)

feature = Table('feature', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('player_id', INTEGER),
    Column('value', DECIMAL(precision=10, scale=9)),
    Column('type', VARCHAR(length=63)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['ad_feature'].columns['value'].create()
    pre_meta.tables['feature'].columns['type'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['ad_feature'].columns['value'].drop()
    pre_meta.tables['feature'].columns['type'].create()
