from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
social_profile = Table('social_profile', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('social_id', String(length=64)),
    Column('nickname', String(length=64)),
    Column('access_token', String(length=256)),
    Column('expires_at', Integer),
    Column('expires_in', Integer),
    Column('avatar', LargeBinary),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['social_profile'].columns['avatar'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['social_profile'].columns['avatar'].drop()
