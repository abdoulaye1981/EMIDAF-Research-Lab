import logging
from pathlib import Path


class LoggerManager:

    def __init__(self):

        Path("logs").mkdir(exist_ok=True)

        logging.basicConfig(

            filename="logs/application.log",

            level=logging.INFO,

            format="%(asctime)s - %(levelname)s - %(message)s"

        )

        self.logger = logging.getLogger("EMIDAF")

    def info(self, message):

        self.logger.info(message)

    def warning(self, message):

        self.logger.warning(message)

    def error(self, message):

        self.logger.error(message)