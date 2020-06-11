import argparse
import logging.config
import yaml
import os

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker


logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()
class no_show(Base):
    """Create a data model for the database to captire features and response """
    __tablename__ = 'no_show'
    Id = Column(Integer, primary_key=True)
    Gender = Column(String(10), unique=False, nullable=False)
    Age = Column(Integer, unique=False, nullable=False)
    Scholarship = Column(Integer, unique=False, nullable=False)
    Hipertension = Column(Integer, unique=False, nullable=False)
    Diabetes = Column(Integer, unique=False, nullable=False)
    Alcoholism = Column(Integer, unique=False, nullable=False)
    Handcap = Column(Integer, unique=False, nullable=False)
    SMS_received = Column(Integer, unique=False, nullable=False)
    Interval = Column(Integer, unique=False, nullable=False)
    Show_No_show = Column(String(100), unique=False, nullable=True)

    def __repr__(self):
        return '<no_show %r>' % self.Show_No_show


def create_db(args):
    """Creates a database with the data model given by obj:`apps.models.Track`
    Args:
        args: Argparse args - should include args.title, args.artist, args.album
    Returns: None
    """

    engine = sqlalchemy.create_engine(args.engine_string)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    track = Tracks(artist=args.artist, album=args.album, title=args.title)
    session.add(track)
    session.commit()
    logger.info("Database created with song added: %s by %s from album, %s ", args.title, args.artist, args.album)
    session.close()


def add_track(args):
    """Seeds an existing database with additional songs.
    Args:
        args: Argparse args - should include args.title, args.artist, args.album
    Returns:None
    """

    engine = sqlalchemy.create_engine(args.engine_string)

    Session = sessionmaker(bind=engine)
    session = Session()

    track = Tracks(artist=args.artist, album=args.album, title=args.title)
    session.add(track)
    session.commit()
    logger.info("%s by %s from album, %s, added to database", args.title, args.artist, args.album)