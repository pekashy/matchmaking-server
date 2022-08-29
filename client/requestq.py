import schemas
import logging


class MQ:
    def __init__(self):
        pass

    def send(self, logger: logging.Logger, message: schemas.common.Message):
        logger.info("Sending message: %s", message.corr_id)
