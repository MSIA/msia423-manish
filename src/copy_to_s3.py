"""
Written By - Manish Kumar
This python scripts copies file to s3 location.
The file location, bucket name and object name are in config/parameter.yaml
"""



import os
import boto3
from botocore.exceptions import ClientError
import yaml
import logging.config
import logging

logging.basicConfig(filename='config/logging/msia423_copys3.log', level=logging.DEBUG)
logger = logging.getLogger('msia423')

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket 
       :param file_name: File to upload
       :param bucket: Bucket to upload to
       :param object_name: S3 object name. If not specified then file_name is used
       :return: True if file was uploaded, else False"""
		       

    	# If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name
		  
		        
							            
    s3_client = boto3.client('s3',aws_access_key_id = os.environ['aws_access_key_id'],aws_secret_access_key = os.environ['aws_secret_access_key'])
    
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)

        logger.info("File upladed to S3 ")
    except ClientError as e:
        logger.info("File upload failed")
        logging.error(e)
        return False
    return True


cred_list = {}


with open(r'config/parameter.yaml') as file:
    cred_list = yaml.load(file, Loader=yaml.FullLoader)


upload_file(cred_list['file_to_upload'],cred_list['bucket_name'],cred_list['object_name'])
