"""
=========================================================
EMIDAF Framework v1.0
MySQL Provider
=========================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .provider import DatabaseProvider


class MySQLProvider(DatabaseProvider):
    """
    Fournisseur MySQL.
    """

    def create_engine(self) -> Engine:

        return create_engine(

            self.url,

            future=True,

            pool_pre_ping=True,

            pool_recycle=3600,

            echo=False
        )