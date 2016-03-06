from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
device = Table('device', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('uuid', String(length=64), nullable=False),
    Column('user_id', Integer),
    Column('ip_addr', String(length=40)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['device'].columns['ip_addr'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['device'].columns['ip_addr'].drop()
