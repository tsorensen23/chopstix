from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
ticket = Table('ticket', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('game', String(length=80)),
    Column('section', String(length=10)),
    Column('row', String(length=10)),
    Column('seat_no', String(length=10)),
    Column('created_on', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['ticket'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['ticket'].drop()
