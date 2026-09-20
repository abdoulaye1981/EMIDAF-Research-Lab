"""
=========================================================
EMIDAF Framework v1.0
User Service
=========================================================
"""

from __future__ import annotations

from database.models.user_model import UserModel
from emidaf_core.repositories.user_repository import (
    UserRepository,
)
from emidaf_core.services.auth_service import VALID_ROLES

from emidaf_core.security.password import (
    hash_password,
    verify_password,
)


class UserService:
    """
    Administration des comptes utilisateurs.
    """

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self._users = user_repository

    def get(
        self,
        user_id: int,
    ) -> UserModel | None:
        return self._users.get_by_id(
            user_id
        )

    def get_all(
        self,
    ) -> list[UserModel]:
        return self._users.get_all()

    def count(self) -> int:
        return self._users.count()

    def set_active(
        self,
        user_id: int,
        is_active: bool,
    ) -> UserModel:
        user = self._require_user(
            user_id
        )

        user.is_active = bool(
            is_active
        )

        return self._users.update(user)

    def set_verified(
        self,
        user_id: int,
        is_verified: bool,
    ) -> UserModel:
        user = self._require_user(
            user_id
        )

        user.is_verified = bool(
            is_verified
        )

        return self._users.update(user)

    def set_role(
        self,
        user_id: int,
        role: str,
    ) -> UserModel:
        if role not in VALID_ROLES:
            raise ValueError(
                f"Rôle invalide : {role}"
            )

        user = self._require_user(
            user_id
        )

        user.role = role

        return self._users.update(user)

    def update_profile(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        email: str,
        institution: str | None = None,
        country: str | None = None,
    ) -> UserModel:
        """
        Met à jour les informations personnelles
        d'un utilisateur.

        Le rôle et les droits ne sont pas modifiables
        par cette opération.
        """
        user = self._require_user(user_id)

        first_name = (
            first_name or ""
        ).strip()

        last_name = (
            last_name or ""
        ).strip()

        email = (
            email or ""
        ).strip().lower()

        institution = (
            institution.strip()
            if institution
            else None
        )

        country = (
            country.strip()
            if country
            else None
        )

        if not first_name:
            raise ValueError(
                "Le prénom est obligatoire."
            )

        if not last_name:
            raise ValueError(
                "Le nom est obligatoire."
            )

        if not email or "@" not in email:
            raise ValueError(
                "Adresse e-mail invalide."
            )

        existing = (
            self._users.get_by_email(email)
        )

        if (
            existing is not None
            and int(existing.id) != int(user_id)
        ):
            raise ValueError(
                "Cette adresse e-mail est déjà utilisée."
            )

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.institution = institution
        user.country = country

        return self._users.update(user)

    def change_password(
        self,
        user_id: int,
        current_password: str,
        new_password: str,
    ) -> UserModel:
        """
        Change le mot de passe après vérification
        du mot de passe actuel.
        """
        user = self._require_user(user_id)

        if not verify_password(
            current_password,
            user.password_hash,
        ):
            raise ValueError(
                "Le mot de passe actuel est incorrect."
            )

        if current_password == new_password:
            raise ValueError(
                "Le nouveau mot de passe doit être "
                "différent de l'ancien."
            )

        user.password_hash = hash_password(
            new_password
        )

        return self._users.update(user)

    def _require_user(
        self,
        user_id: int,
    ) -> UserModel:
        user = self._users.get_by_id(
            user_id
        )

        if user is None:
            raise ValueError(
                "Utilisateur introuvable."
            )

        return user
