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
