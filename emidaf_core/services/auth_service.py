"""
=========================================================
EMIDAF Framework v1.0
Authentication Service
=========================================================
"""

from __future__ import annotations

from datetime import datetime
import re

from database.models.user_model import UserModel
from emidaf_core.repositories.user_repository import (
    UserRepository,
)
from emidaf_core.security.password import (
    hash_password,
)
from emidaf_core.security.password import (
    verify_password,
)


VALID_ROLES = {
    "user",
    "admin",
    "super_admin",
}

EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)


class AuthService:
    """
    Authentification et création des comptes EMIDAF.
    """

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self._users = user_repository

    @staticmethod
    def normalize_email(
        email: str,
    ) -> str:
        return email.strip().lower()

    @staticmethod
    def validate_email(
        email: str,
    ) -> None:
        if not EMAIL_PATTERN.fullmatch(email):
            raise ValueError(
                "Adresse e-mail invalide."
            )

    def register(
        self,
        *,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        institution: str | None = None,
        country: str | None = None,
        role: str = "user",
        is_verified: bool = False,
    ) -> UserModel:
        first_name = first_name.strip()
        last_name = last_name.strip()
        email = self.normalize_email(email)

        if not first_name:
            raise ValueError(
                "Le prénom est obligatoire."
            )

        if not last_name:
            raise ValueError(
                "Le nom est obligatoire."
            )

        self.validate_email(email)

        if role not in VALID_ROLES:
            raise ValueError(
                f"Rôle utilisateur invalide : {role}"
            )

        if self._users.email_exists(email):
            raise ValueError(
                "Un compte utilisant cette adresse "
                "e-mail existe déjà."
            )

        user = UserModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=hash_password(
                password
            ),
            role=role,
            is_active=True,
            is_verified=is_verified,
            institution=(
                institution.strip()
                if institution
                else None
            ),
            country=(
                country.strip()
                if country
                else None
            ),
        )

        return self._users.add(user)

    def authenticate(
        self,
        email: str,
        password: str,
    ) -> UserModel | None:
        email = self.normalize_email(email)

        user = self._users.get_by_email(email)

        if user is None:
            return None

        if not user.is_active:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        user.last_login_at = datetime.utcnow()

        return self._users.update(user)

    def get_current_user(
        self,
        user_id: int | None,
    ) -> UserModel | None:
        if user_id is None:
            return None

        user = self._users.get_by_id(
            int(user_id)
        )

        if (
            user is None
            or not user.is_active
        ):
            return None

        return user

    @staticmethod
    def is_admin(
        user: UserModel | None,
    ) -> bool:
        return bool(
            user
            and user.is_active
            and user.role in {
                "admin",
                "super_admin",
            }
        )

    @staticmethod
    def is_super_admin(
        user: UserModel | None,
    ) -> bool:
        return bool(
            user
            and user.is_active
            and user.role == "super_admin"
        )
