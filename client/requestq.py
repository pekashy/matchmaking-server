import logging

import pika

import schemas.common
import schemas.find_game


class MQ:
    def __init__(self):
        self.connection: pika.BlockingConnection = pika.BlockingConnection(
            pika.URLParameters(url=schemas.find_game.QUEUE_URL))
        self.connection.channel().queue_declare(queue=schemas.find_game.QUEUE_NAME)

    def send(self, logger: logging.Logger, message: schemas.common.Message):
        channel = self.connection.channel()
        logger.info("Sending message: %s", message.corr_id)
        channel.basic_publish(exchange="",
                              routing_key=schemas.find_game.QUEUE_NAME,
                              body=message.to_json())

    def shutdown(self):
        self.connection.close()
