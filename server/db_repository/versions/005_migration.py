from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
measurement = Table('measurement', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('tag', String(length=64)),
    Column('time_stamp', Integer),
    Column('gpio', Integer),
    Column('voltage', Integer),
    Column('power', Integer),
    Column('temperature', Integer),
    Column('timestamp', Integer),
    Column('device_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['measurement'].columns['timestamp'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['measurement'].columns['timestamp'].drop()
