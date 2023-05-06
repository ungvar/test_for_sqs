import boto3
import logging
from botocore.exceptions import ClientError
import json


# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

queue_url_standard = 'https://sqs.eu-central-1.amazonaws.com/065103934905/immo-video-queue-standard'
queue_arn_standard = 'arn:aws:sqs:eu-central-1:065103934905:immo-video-queue-standard'
queue_url_fifo = 'https://sqs.eu-central-1.amazonaws.com/065103934905/immo-video-queue.fifo'
queue_arn_fifo = 'arn:aws:sqs:eu-central-1:065103934905:immo-video-queue.fifo'

class test_for_sqs:
    def __init__(self):
        self.sqs = boto3.client('sqs', region_name='eu-central-1')


# Receive messages from a queue
    def read_from_sqs_queue(self):
        response = self.sqs.receive_message(
            QueueUrl=queue_url_standard,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        print(f"Number of messages received: {len(response.get('Messages', []))}")

        for message in response.get('Messages', []):
            message_body = message['Body']
            print(f"Message body: {json.loads(message_body)} \n")
            receipt_handle = message['ReceiptHandle']
            print(f"Receipt Handle: {message['ReceiptHandle']} \n")
        return receipt_handle

# Delete a message from a queue
    def delete_from_sqs_queue(self, receipt_handle):
        response = self.sqs.delete_message(
            QueueUrl=queue_url_standard,
            ReceiptHandle=receipt_handle,
        )
        print(f"Deleted message: {response}\n")

# Send a message to a queue
    def send_message_to_sqs_queue(self):
        message = {'key': 'value'}
        response = self.sqs.send_message(
            QueueUrl=queue_url_standard,
            MessageBody=json.dumps(message)
        )
        print(f"Sent message: {response}\n")


my_test = test_for_sqs()
#my_test.send_message_to_sqs_queue()
receipt_handle = my_test.read_from_sqs_queue()
my_test.delete_from_sqs_queue(receipt_handle)
my_test.read_from_sqs_queue()