"""
=========================================================
EMIDAF Framework
Logger
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
"""

from __future__ import annotations

import logging
from pathlib import Path


class Logger:
    """
    Logger unique du framework.
    """

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(
        self,
        name: str = "EMIDAF",
        level: int = logging.INFO,
        log_file: str | None = None,
    ) -> None:

        if hasattr(self, "_initialized"):

            return

        self._initialized = True

        self._logger = logging.getLogger(name)

        self._logger.setLevel(level)

        formatter = logging.Formatter(

            "[%(asctime)s] "

            "[%(levelname)s] "

            "%(message)s"

        )

        console = logging.StreamHandler()

        console.setFormatter(formatter)

        self._logger.addHandler(console)

        if log_file:

            Path(log_file).parent.mkdir(

                parents=True,

                exist_ok=True

            )

            file_handler = logging.FileHandler(log_file)

            file_handler.setFormatter(formatter)

            self._logger.addHandler(file_handler)

    @property
    def logger(self):

        return self._logger

    def debug(self, message: str):

        self._logger.debug(message)

    def info(self, message: str):

        self._logger.info(message)

    def warning(self, message: str):

        self._logger.warning(message)

    def error(self, message: str):

        self._logger.error(message)

    def critical(self, message: str):

        self._logger.critical(message)