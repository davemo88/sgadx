from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
ad_game_result = Table('ad_game_result', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('consumer_id', Integer),
    Column('advertiser_id', Integer),
    Column('ad_id', Integer),
    Column('consumer_action', String(length=63)),
    Column('advertiser_utility', DECIMAL(precision=10, scale=6)),
    Column('consumer_utility', DECIMAL(precision=10, scale=6)),
)

auction_game_result = Table('auction_game_result', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('consumer_id', Integer),
    Column('advertiser_id', Integer),
    Column('winning_bid', DECIMAL(precision=10, scale=9)),
    Column('second_price', DECIMAL(precision=10, scale=9)),
)

sim = Table('sim', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('type', String(length=63)),
    Column('num_features', Integer),
    Column('num_consumers', Integer),
    Column('num_advertisers', Integer),
    Column('num_ads', Integer),
    Column('num_recommenders', Integer),
    Column('num_verifiers', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['ad_game_result'].create()
    post_meta.tables['auction_game_result'].create()
    post_meta.tables['sim'].columns['num_ads'].create()
    post_meta.tables['sim'].columns['num_advertisers'].create()
    post_meta.tables['sim'].columns['num_consumers'].create()
    post_meta.tables['sim'].columns['num_features'].create()
    post_meta.tables['sim'].columns['num_recommenders'].create()
    post_meta.tables['sim'].columns['num_verifiers'].create()
    post_meta.tables['sim'].columns['type'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['ad_game_result'].drop()
    post_meta.tables['auction_game_result'].drop()
    post_meta.tables['sim'].columns['num_ads'].drop()
    post_meta.tables['sim'].columns['num_advertisers'].drop()
    post_meta.tables['sim'].columns['num_consumers'].drop()
    post_meta.tables['sim'].columns['num_features'].drop()
    post_meta.tables['sim'].columns['num_recommenders'].drop()
    post_meta.tables['sim'].columns['num_verifiers'].drop()
    post_meta.tables['sim'].columns['type'].drop()
