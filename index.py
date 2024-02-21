import boto3
import json
import uuid
import datetime
import os
import botocore
import requests
import time
from botocore.exceptions import ClientError
from aws_lambda_powertools.utilities import parameters
from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway

session = boto3.session.Session()
pushgateway_host = os.environ.get('PUSHGATEWAY_HOST')
application = os.environ.get('APPLICATION', 'shield')
environment = os.environ.get('ENVIRONMENT', 'staging')
region = os.environ.get('REGION', 'us-east-1')

if os.environ.get('SECRET_NAME'):
    token = parameters.get_secret(
        os.environ.get('SECRET_NAME'), max_age=os.environ.get('SECRET_CACHE_AGE', default=300))
else:
    token = os.environ.get('TOKEN')

def lambda_handler(event, context):
    start_time = time.time()

    url = os.environ.get('URL')
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    data = json.dumps({"job_class_name": event})
    resp = requests.post(url, data=data, headers=headers)
    print (resp.status_code, resp.reason)
    end_time = time.time()

    # metrics
    if (pushgateway_host is not None and pushgateway_host != ''):
        full_env = f'{application}-{environment}-{region}'
        registry = CollectorRegistry()
        metric_request_total = Counter('queue_scheduled_lambda_requests_total', 'Total requests of the lambda', ['environment', 'event', 'status'], registry=registry)
        metric_request_total.labels(environment=full_env, event=str(event), status=resp.status_code).inc()
        metric_runtime = Gauge('queue_scheduled_lambda_runtime_milliseconds', 'Total runtime of the lambda in milliseconds', ['environment', 'event'], registry=registry)
        metric_runtime.labels(environment=full_env, event=str(event)).set(round((end_time - start_time)*1000))
        push_to_gateway(pushgateway_host, job='lambda', registry=registry)
    