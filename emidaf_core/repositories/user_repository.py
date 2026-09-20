"""
=========================================================
EMIDAF Framework v1.0
User Repository
=========================================================
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import func
from sqlalchemy import select

from database.database_manager import DatabaseManager
from database.models.user_model import UserModel


class UserRepository:
    """
    Persistance des utilisateurs EMIDAF.
    """

    def __init__(
        self,
        database_manager: DatabaseManager,
    ) -> None:
        self._database = database_manager

    def add(
        self,
        user: UserModel,
    ) -> UserModel:
        with self._database.session_scope() as session:
            session.add(user)
            session.flush()
            session.refresh(user)
            session.expunge(user)
            return user

    def get_by_id(
        self,
        user_id: int,
    ) -> Optional[UserModel]:
        with self._database.session_scope() as session:
            user = session.get(
                UserModel,
                user_id,
            )

            if user is not None:
                session.expunge(user)

            return user

    def get_by_email(
        self,
        email: str,
    ) -> Optional[UserModel]:
        normalized_email = email.strip().lower()

        with self._database.session_scope() as session:
            statement = select(UserModel).where(
                func.lower(UserModel.email)
                == normalized_email
            )

            user = session.scalar(statement)

            if user is not None:
                session.expunge(user)

            return user

    def email_exists(
        self,
        email: str,
    ) -> bool:
        return self.get_by_email(email) is not None

    def get_all(self) -> list[UserModel]:
        with self._database.session_scope() as session:
            statement = (
                select(UserModel)
                .order_by(UserModel.created_at.desc())
            )

            users = list(
                session.scalars(statement).all()
            )

            for user in users:
                session.expunge(user)

            return users

    def count(self) -> int:
        with self._database.session_scope() as session:
            statement = select(
                func.count(UserModel.id)
            )

            return int(
                session.scalar(statement) or 0
            )

    def update(
        self,
        user: UserModel,
    ) -> UserModel:
        with self._database.session_scope() as session:
            user = session.merge(user)
            session.flush()
            session.refresh(user)
            session.expunge(user)
            return user
