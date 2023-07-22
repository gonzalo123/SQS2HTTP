import json
import logging

import boto3
import requests

from settings import HTTP_ENDPOINT, AUTH_BEARER_TOKEN, SQS_QUEUE_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, \
    AWS_REGION, SQS_MAX_NUMBER_OF_MESSAGES, AWS_PROFILE

logger = logging.getLogger(__name__)


def get_sqs():
    if AWS_PROFILE:
        boto3.setup_default_session(profile_name=AWS_PROFILE)
        sqs_client = boto3.client(
            service_name='sqs',
            region_name=AWS_REGION
        )
    else:
        sqs_client = boto3.client(
            service_name='sqs',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
    return sqs_client


def remove_from_sqs(sqs, receipt_handle):
    sqs.delete_message(
        QueueUrl=SQS_QUEUE_URL,
        ReceiptHandle=receipt_handle
    )


def do_post(body):
    headers = {
        'Authorization': AUTH_BEARER_TOKEN,
        'Content-Type': 'application/json'
    }
    if AUTH_BEARER_TOKEN:
        headers[AUTH_BEARER_TOKEN] = AUTH_BEARER_TOKEN

    requests.post(
        url=HTTP_ENDPOINT,
        data=json.dumps(body),
        headers=headers)


def loop_step(sqs):
    response = sqs.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        MaxNumberOfMessages=SQS_MAX_NUMBER_OF_MESSAGES)

    if 'Messages' in response:
        for message in response.get('Messages', []):
            try:
                body = message.get('Body')
                logger.info(body)
                do_post(body)
                remove_from_sqs(sqs, message.get('ReceiptHandle'))

            except Exception as e:
                logger.exception(e)
