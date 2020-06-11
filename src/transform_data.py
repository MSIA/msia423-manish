"""
Written By - Manish Kumar

This puthon script
"""


import pandas as pd
from io import StringIO
import boto3
import os
import yaml
import logging.config
import logging
import sys
from featurise import build_feature_interval

logging.basicConfig(filename='config/logging/msia423_copys3.log', level=logging.DEBUG)
logger = logging.getLogger('msia423')


"""Table Schema
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

"""

# Reading csv file from S3

cred_list = {}

with open(r'config/parameter.yaml') as file:
    cred_list = yaml.load(file, Loader=yaml.FullLoader)

s3 = boto3.client('s3',aws_access_key_id = os.environ['aws_access_key_id'],aws_secret_access_key = os.environ['aws_secret_access_key'])
obj = s3.get_object(Bucket = cred_list['bucket_name'], Key = cred_list['object_name'])
df = pd.read_csv(obj['Body'])

no_show_df = df

no_show_df['ScheduledDay'] = pd.to_datetime(no_show_df['ScheduledDay'])
no_show_df['ScheduledDay'] = no_show_df['ScheduledDay'].dt.date

no_show_df['AppointmentDay'] = pd.to_datetime(no_show_df['AppointmentDay'])
no_show_df['AppointmentDay'] = no_show_df['AppointmentDay'].dt.date
clean_df = no_show_df[no_show_df['AppointmentDay'] >= no_show_df['ScheduledDay']]

try:
    no_show_df = build_feature_interval(clean_df)

    logger.info("Transformed data")
    df_to_train = no_show_df[
        ['Gender', 'Age', 'Scholarship', 'Hipertension', 'Diabetes', 'Alcoholism', 'Handcap', 'SMS_received', 'No-show',
         'interval']]

except Exception as e:
    logger.error(e)
    sys.exit(1)

try :
    csv_buffer = StringIO()
    df_to_train.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3',aws_access_key_id = os.environ['aws_access_key_id'],aws_secret_access_key = os.environ['aws_secret_access_key'])
    s3_resource.Object(cred_list['bucket_name'], cred_list['cleaned_file']).put(Body=csv_buffer.getvalue())
    logger.info("Cleaned file uploaded to s3")
except Exception as e:
    logger.error(e)
    sys.exit(1)