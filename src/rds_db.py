import os
import logging.config
import sqlalchemy as sql
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
import logging.config
import logging
import yaml

conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
database = os.environ.get("DATABASE_NAME")
engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)

Base = declarative_base()  

logging.basicConfig(filename='config/logging/msia423.log', level=logging.DEBUG)
logger = logging.getLogger('msia423-demo')


class no_show(Base):
    """Create a data model for the database to captire features and response """
    __tablename__ = 'no_show'
    PaientId = Column(Integer, primary_key=True)
    Gender = Column(String(1), unique=False, nullable=False)
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
        pred = "<no_show(PatientId='%d', Gender='%s', Age='%d', Scholarship='%d',Hipertension='%d',Diabetes='%d',Alcoholism='%d',Handcap='%d', SMS_received ='%d', Interva'%d', Show_No_show='%s',)>"
        return pred % (self.PaientId, self.Gender, self.Age, self.Scholarship, self.Hipertension, self,Diabetes, self.Alcoholism, self.Handcap, self.SMS_received, self.Interval, self.Show_No_show)


# set up mysql connection
cred_list = {}
# Upload the file
with open(r'config/parameter.yaml') as file:
    cred_list = yaml.load(file, Loader=yaml.FullLoader)

if (cred_list['loc_database'] == 'AWS') :
    engine = sql.create_engine(engine_string)

    # create the no_show table
    Base.metadata.create_all(engine)
    # set up looging config
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__file__)
    # create a db session
    Session = sessionmaker(bind=engine)  
    session = Session()
    session.commit()   
    session.close()
   
else:
    
    try:
        print ("creating table locally")
        engine_string = 'sqlite:///data/msia423.db'
        engine = sql.create_engine(engine_string)
        Base.metadata.create_all(engine)
        logger.info("Database: msia423.db created successfully")
        logger.info("Table: no_show created in database successfully")
        print ("DB created locally in the data folder")
    except Exception as e:
        logger.error(e)
        sys.exit(1)

