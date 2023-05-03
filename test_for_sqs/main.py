import boto3
import logging
from botocore.exceptions import ClientError


# создаем клиент для работы с SQS
logger = logging.getLogger(__name__)
sqs = boto3.client('sqs')


class test_for_sqs:
    def __init__(self):
        self.sqs = boto3.client('sqs')

    def delete(self, queue_url, receipt_handle):
        try:
            self.sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        except ClientError as error:
            logger.exception("Couldn't delete message with ReceiptHandle=%s from queue at URL=%s.", receipt_handle, queue_url)
            raise error
        else:
            logger.info("Deleted message with ReceiptHandle=%s from queue at URL=%s.", receipt_handle, queue_url)


# Receive messages from a queue
    def receive_messages(queue, max_number, wait_time):
        """
        Receive a batch of messages in a single request from an SQS queue.

        :param queue: The queue from which to receive messages.
        :param max_number: The maximum number of messages to receive. The actual number
                           of messages received might be less.
        :param wait_time: The maximum time to wait (in seconds) before returning. When
                          this number is greater than zero, long polling is used. This
                          can result in reduced costs and fewer false empty responses.
        :return: The list of Message objects received. These each contain the body
                 of the message and metadata and custom attributes.
        """
        try:
            messages = queue.receive_messages(
                MessageAttributeNames=['All'],
                MaxNumberOfMessages=max_number,
                WaitTimeSeconds=wait_time
            )
            for msg in messages:
                logger.info("Received message: %s: %s", msg.message_id, msg.body)
        except ClientError as error:
            logger.exception("Couldn't receive messages from queue: %s", queue)
            raise error
        else:
            return messages

# Delete a message from a queue
    def delete_message(message):
        """
        Delete a message from a queue. Clients must delete messages after they
        are received and processed to remove them from the queue.

        :param message: The message to delete. The message's queue URL is contained in
                        the message's metadata.
        :return: None
        """
        try:
            message.delete()
            logger.info("Deleted message: %s", message.message_id)
        except ClientError as error:
            logger.exception("Couldn't delete message: %s", message.message_id)
            raise error

# Send a message to a queue
    def send_message(queue, message_body, message_attributes=None):
        """
        Send a message to an Amazon SQS queue.

        :param queue: The queue that receives the message.
        :param message_body: The body text of the message.
        :param message_attributes: Custom attributes of the message. These are key-value
                                   pairs that can be whatever you want.
        :return: The response from SQS that contains the assigned message ID.
        """
        if not message_attributes:
            message_attributes = {}

        try:
            response = queue.send_message(
                MessageBody=message_body,
                MessageAttributes=message_attributes
            )
        except ClientError as error:
            logger.exception("Send message failed: %s", message_body)
            raise error
        else:
            return response

