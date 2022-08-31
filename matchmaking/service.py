import logging

import pika

import logic
import schemas.find_game

matcher = logic.Matcher()


def create_logger(corr_id: str) -> logging.Logger:
    logger = logging.getLogger(corr_id)
    formatter = logging.Formatter(
        fmt=
        '%(asctime)s.%(msecs)03d %(levelname)s %(module)s %(name)s: %(message)s',
        datefmt='%H:%M:%S',
    )
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('/logs/matchmaking.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def on_message(ch, method, properties, body):
    message = schemas.find_game.RequestMessage.from_json(body)
    logger = create_logger(message.corr_id)
    logger.debug(f'Matchmaker received message: {body}')
    matcher.find_game(logger=logger, request=message)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.URLParameters(url=schemas.find_game.QUEUE_URL))
    channel = connection.channel()
    channel.queue_declare(schemas.find_game.QUEUE_NAME)
    channel.basic_consume(queue=schemas.find_game.QUEUE_NAME, on_message_callback=on_message,
                          auto_ack=True)  # TODO: Ack on match submission
    channel.start_consuming()
