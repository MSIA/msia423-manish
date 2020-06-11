""" 
Written By - Manish Kumar

This python script creates a database either locally or on AWS RDS depending on the loc_database value in the parameter.yaml file

"""
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
import pandas as pd

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
    PatientId = Column(Integer, primary_key=True)
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

# set up mysql connection
cred_list = {}
# Upload the file
with open(r'config/parameter.yaml') as file:
    cred_list = yaml.load(file, Loader=yaml.FullLoader)

if (cred_list['loc_database'] == 'AWS') :
 #   try:
        engine = sql.create_engine(engine_string)

        # create the no_show table
        Base.metadata.create_all(engine)
        # set up looging config
        logger.info("Database: msia423.db created successfully on AWS RDS")
        logger.info("Table: no_show created in database successfully")

        # create a db session
        Session = sessionmaker(bind=engine)  
        session = Session()
	##############################Add code for putting data

        if (cred_list["populate"] == True):

            df =  pd.read_csv(cred_list['load_file_address'])
                      
            df["interval"] = df["interval"].astype('int')
             
            for index, row in df.iterrows():
                
                df_row = no_show(Gender = row["Gender"], Age = row["Age"], Scholarship = row["Scholarship"], Hipertension = row["Hipertension"], Diabetes = row["Diabetes"], Alcoholism = ["Alcoholism"], Handcap = row["Handcap"], SMS_received = row["SMS_received"], Interval = row["interval"], Show_No_show = row["No-show"])
                session.add(df_row)
                session.commit()
                             
            session.close()
#    except Exception as e:
#        logger.error(e)
#        sys.exit(1)
   
else:
    
    try:
        engine_string = 'sqlite:///data/msia423.db'
        engine = sql.create_engine(engine_string)
        Base.metadata.create_all(engine)
        logger.info("Database: msia423.db created successfully")
        logger.info("Table: no_show created in database successfully")
        Session = sessionmaker(bind=engine)
        session = Session()
        ##############################Add code for putting data

        if (cred_list["populate"] == True):
            df = pd.read_csv(cred_list['load_file_address'])

            df["interval"] = df["interval"].astype('int')

            for index, row in df.iterrows():
                df_row = no_show(Gender=row["Gender"], Age=row["Age"], Scholarship=row["Scholarship"],
                                 Hipertension=row["Hipertension"], Diabetes=row["Diabetes"], Alcoholism=["Alcoholism"],
                                 Handcap=row["Handcap"], SMS_received=row["SMS_received"], Interval=row["interval"],
                                 Show_No_show=row["No-show"])
                session.add(df_row)
                session.commit()

            session.close()
    except Exception as e:
        logger.error(e)
        sys.exit(1)
