import logging
from pathlib import Path


class LoggerManager:

    def __init__(self):

        self.logs_directory = Path("logs")

        self.logs_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self._loggers = {}

        self._initialize_loggers()

    # =======================================================
    # Initialisation
    # =======================================================

    def _initialize_loggers(self):

        loggers = [

            "application",

            "project",

            "import",

            "inspection",

            "error"

        ]

        for logger_name in loggers:

            self._create_logger(logger_name)

    # =======================================================
    # Création d'un logger
    # =======================================================

    def _create_logger(self, name):

        logger = logging.getLogger(name)

        logger.setLevel(logging.INFO)

        logger.propagate = False

        if logger.handlers:

            logger.handlers.clear()

        file_handler = logging.FileHandler(

            self.logs_directory / f"{name}.log",

            encoding="utf-8"

        )

        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(message)s"

        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        self._loggers[name] = logger

    # =======================================================
    # Accès
    # =======================================================

    def get_logger(self, name):

        return self._loggers.get(name)

    def exists(self, name):

        return name in self._loggers

    def list(self):

        return list(self._loggers.keys())

    # =======================================================
    # Logger principal
    # =======================================================

    def info(self, message):

        self.application.info(message)

    def warning(self, message):

        self.application.warning(message)

    def error_message(self, message):

        self.application.error(message)

    def critical(self, message):

        self.application.critical(message)

    # =======================================================
    # Propriétés
    # =======================================================

    @property
    def application(self):

        return self.get_logger("application")

    @property
    def project(self):

        return self.get_logger("project")

    @property
    def importer(self):

        return self.get_logger("import")

    @property
    def inspection(self):

        return self.get_logger("inspection")

    @property
    def error(self):

        return self.get_logger("error")