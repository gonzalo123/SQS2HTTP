# SQS2HTTP

Simple service that listen to a sqs queue and bypass the payload to a http server, sending a POST request with the 
SQS's payload and a Bearer Token


The main script read a .env file with the aws credentials and http endpoint

```dotenv
# AWS CREDENTIALS
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_REGION=eu-west-1
#AWS_PROFILE=xxx
# SQS
SQS_QUEUE_URL=https://sqs.eu-west-1.amazonaws.com/xxx/name
# REST ENDPOINT
HTTP_ENDPOINT=http://localhost:5555
AUTH_BEARER_TOKEN=xxx
```

```python
import logging

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

from lib.sqs2http import loop_step, get_sqs

for library in ['botocore', 'boto3']:
    logging.getLogger(library).setLevel(logging.WARNING)

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level='INFO',
    datefmt='%d/%m/%Y %X'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("sqs2http start")
    sqs = get_sqs()
    while True:
        loop_step(sqs)
```

The main loop is like this:

```python
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
```

With this simple script you can set up a web server that process all incoming SQS messages.