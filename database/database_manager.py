"""
=========================================================
EMIDAF Framework v1.0
Database Manager
---------------------------------------------------------
Gestionnaire central de la base de données.
Compatible SQLite / PostgreSQL / MySQL.
=========================================================
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from database.base import Base
from database.providers.provider import DatabaseProvider


class DatabaseManager:
    """
    Gestionnaire central de la base de données.

    Responsabilités
    ----------------
    - Créer une base SQLite
    - Initialiser SQLAlchemy
    - Gérer les sessions
    - Créer les tables
    - Supprimer les tables
    - Tester la connexion
    """

    def __init__(
        self,
        provider: DatabaseProvider
    ) -> None:

        self._provider = provider

        self._engine = None

        self._session_factory = None

        self.initialize()

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def initialize(self) -> None:
        """
        Initialise SQLAlchemy.
        """

        self._engine = create_engine(

            self._provider.connection_string,

            future=True,

            echo=False

        )

        self._session_factory = sessionmaker(

            bind=self._engine,

            autoflush=False,

            autocommit=False,

            expire_on_commit=False,

            future=True

        )

    # =====================================================
    # DATABASE CREATION
    # =====================================================

    def create_database(
        self,
        database_path: Optional[Path] = None
    ) -> None:
        """
        Crée une nouvelle base SQLite.
        """

        if database_path is not None:

            database_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            self._provider.set_database(
                database_path
            )

            self.initialize()

        Base.metadata.create_all(
            self._engine
        )

    # =====================================================
    # TABLES
    # =====================================================

    def create_tables(self) -> None:
        """
        Crée toutes les tables.
        """

        Base.metadata.create_all(
            self._engine
        )

    def drop_tables(self) -> None:
        """
        Supprime toutes les tables.
        """

        Base.metadata.drop_all(
            self._engine
        )

    def recreate_database(self) -> None:
        """
        Reconstruit complètement la base.
        """

        self.drop_tables()

        self.create_tables()

    # =====================================================
    # SESSIONS
    # =====================================================

    def get_session(self) -> Session:

        return self._session_factory()

    @contextmanager
    def session_scope(
        self
    ) -> Generator[Session, None, None]:

        session = self.get_session()

        try:

            yield session

            session.commit()

        except Exception:

            session.rollback()

            raise

        finally:

            session.close()

    # =====================================================
    # CONNECTION
    # =====================================================

    def test_connection(self) -> bool:
        """
        Teste la connexion.
        """

        try:

            with self._engine.connect():

                return True

        except Exception:

            return False

    # =====================================================
    # CHANGE DATABASE
    # =====================================================

    def change_database(
        self,
        provider: DatabaseProvider
    ) -> None:
        """
        Change complètement de base.
        """

        self.close()

        self._provider = provider

        self.initialize()

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self) -> None:
        """
        Ferme toutes les connexions.
        """

        if self._engine is not None:

            self._engine.dispose()

    # =====================================================
    # PROPERTIES
    # =====================================================

    @property
    def provider(self) -> DatabaseProvider:

        return self._provider

    @property
    def engine(self):

        return self._engine

    @property
    def session_factory(self):

        return self._session_factory