"""
Written By - Manish Kumar
This python script reads the clean data from s3 and uses it to train a xgboost model
The final model is saved to s3 again in pickle format
"""


import boto3
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import pickle
import yaml
import logging.config
import logging
import os
import pandas as pd
import sys

logging.basicConfig(filename='config/logging/msia423_copys3.log', level=logging.DEBUG)
logger = logging.getLogger('msia423')

cred_list = {}
# Reading the config file
with open(r'config/parameter.yaml') as file:
    cred_list = yaml.load(file, Loader=yaml.FullLoader)

s3 = boto3.client('s3',aws_access_key_id = os.environ['aws_access_key_id'],aws_secret_access_key = os.environ['aws_secret_access_key'])
obj = s3.get_object(Bucket = cred_list['bucket_name'], Key = cred_list['cleaned_file'])
df = pd.read_csv(obj['Body'])
# Converting texts to Integers
df.loc[df["No-show"] == 'No',"No-show"] = 1
df.loc[df["No-show"] == 'Yes',"No-show"] = 0
df.loc[df["Gender"] == 'M',"Gender"] = 1
df.loc[df["Gender"] == 'F',"Gender"] = 0
df = df.drop('Unnamed: 0',axis = 1)
X = df.drop('No-show',axis = 1)
Y = df['No-show']
seed = 7
test_size = 0.33
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

clf = XGBClassifier(
    n_estimators=300,
    reg_lambda=1,
    gamma=1,
    max_depth=15
)

clf.fit(X_train, y_train)
# Loading the pickled model to s3
logger.info("Model training on the data complete")

pickle_byte_obj = pickle.dumps(clf)
try :
    s3_resource = boto3.resource('s3',aws_access_key_id = os.environ['aws_access_key_id'],aws_secret_access_key = os.environ['aws_secret_access_key'])
    s3_resource.Object(cred_list['bucket_name'], cred_list['model']).put(Body=pickle_byte_obj)
    logger.info("Model saved to s3")

except Exception as e:
    logger.error(e)
    sys.exit(1)