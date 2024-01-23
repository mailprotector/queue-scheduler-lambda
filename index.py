import boto3
import json
import uuid
import datetime
import os
import botocore
import requests
from botocore.exceptions import ClientError
from aws_lambda_powertools.utilities import parameters

session = boto3.session.Session()

if os.environ.get('SECRET_NAME'):
    token = parameters.get_secret(
        os.environ.get('SECRET_NAME'), max_age=os.environ.get('SECRET_CACHE_AGE', default=300))
else:
    token = os.environ.get('TOKEN')

def lambda_handler(event, context):

    url = os.environ.get('URL')
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    data = json.dump({"job_class_name": event})
    resp = requests.post(url, data=data, headers=headers)
    print (resp.status_code, resp.reason)

# if __name__ == "__main__":
#     event = "Scheduled::QueueMessageLockJob"
#     lambda_handler(event, None)