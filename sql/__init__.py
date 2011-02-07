from sqlalchemy import *
from sqlalchemy.types import *
from sqlalchemy.orm import sessionmaker

db = create_engine("sqlite:///procrastinate.db")

metadata = MetaData()
Session = sessionmaker(bind=db)
session = Session()

users_table = Table("users", metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50)),
    Column('password', String(50)))

stories_table = Table("stories", metadata,
    Column('id', Integer, primary_key=True),
    Column('source_site', Integer),
    Column('content', UnicodeText),
    Column('hash', String(128), index=True),
    Column('date', DateTime),
    Column('crawled_date', DateTime))

read_stories_table = Table("read_stories", metadata,
    Column('user_id', Integer, index=True),
    Column('story_id', Integer))
