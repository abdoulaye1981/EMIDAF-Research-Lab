"""
=========================================================
EMIDAF Framework v1.0
SQLite Provider
=========================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .provider import DatabaseProvider


class SQLiteProvider(DatabaseProvider):
    """
    Fournisseur SQLite.
    """

    def create_engine(self) -> Engine:

        return create_engine(

            self.url,

            future=True,

            echo=False
        )