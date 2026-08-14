"""
=========================================================
EMIDAF Framework v1.0
Provider Factory
---------------------------------------------------------
Fabrique des fournisseurs de bases de données.
=========================================================
"""

from __future__ import annotations

from typing import Any

from .provider import DatabaseProvider
from .sqlite_provider import SQLiteProvider
from .postgres_provider import PostgreSQLProvider
from .mysql_provider import MySQLProvider


class ProviderFactory:
    """
    Fabrique des fournisseurs de bases de données.
    """

    @staticmethod
    def create(configuration: dict[str, Any]) -> DatabaseProvider:
        """
        Crée le fournisseur de base de données.

        Parameters
        ----------
        configuration : dict
            Configuration chargée depuis config.yaml.

        Returns
        -------
        DatabaseProvider
            Fournisseur de base de données.
        """

        database = configuration["database"]

        provider = database["provider"].lower()

        if provider == "sqlite":
            return SQLiteProvider(database["sqlite"]["url"])

        if provider == "postgres":
            return PostgreSQLProvider(database["postgres"]["url"])

        if provider == "mysql":
            return MySQLProvider(database["mysql"]["url"])

        raise ValueError(
            f"Unsupported database provider '{provider}'."
        )