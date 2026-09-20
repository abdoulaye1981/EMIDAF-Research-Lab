"""
EMIDAF Framework v1.0
Database Manager
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator
from typing import Optional
from pathlib import Path

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from database.base import Base
from database.models.dataset_model import DatasetModel
from database.models.analysis_result_model import AnalysisResultModel
from database.models.project_model import ProjectModel
from database.models.workspace_model import WorkspaceModel
from database.models.user_model import UserModel
from database.providers.provider import DatabaseProvider


class DatabaseManager:
    """
    Gestionnaire central de la base de données.
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

        self._engine = self._provider.create_engine()

        self._session_factory = sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    # =====================================================
    # DATABASE CREATION
    # =====================================================

    def create_database(
        self,
        database_path: Optional[Path] = None
    ) -> None:

        if database_path is not None:

            database_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            self._provider.set_url(
                f"sqlite:///{database_path}"
            )

            self.initialize()

        Base.metadata.create_all(
            self._engine
        )

    # =====================================================
    # TABLES
    # =====================================================

    def create_tables(self) -> None:

        Base.metadata.create_all(
            self._engine
        )

    def drop_tables(self) -> None:

        Base.metadata.drop_all(
            self._engine
        )

    def recreate_database(self) -> None:

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

        self.close()

        self._provider = provider

        self.initialize()

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self) -> None:

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
