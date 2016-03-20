from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
o_auth_profile = Table('o_auth_profile', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('social_id', VARCHAR(length=64)),
    Column('nickname', VARCHAR(length=64)),
    Column('user_id', INTEGER),
)

social_profile = Table('social_profile', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('social_id', String(length=64)),
    Column('nickname', String(length=64)),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['o_auth_profile'].drop()
    post_meta.tables['social_profile'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['o_auth_profile'].create()
    post_meta.tables['social_profile'].drop()
