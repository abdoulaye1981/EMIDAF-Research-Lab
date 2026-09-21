from __future__ import annotations

import os
import sys

from emidaf_core.bootstrap.bootstrap import Bootstrap
from emidaf_core.repositories.user_repository import (
    UserRepository,
)
from emidaf_core.security.password import (
    hash_password,
)
from emidaf_core.services.auth_service import (
    AuthService,
)


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()

    if not value:
        raise RuntimeError(
            f"{name} est obligatoire."
        )

    return value


def _env_flag(name: str) -> bool:
    return (
        os.environ.get(name, "0")
        .strip()
        .lower()
        in {
            "1",
            "true",
            "yes",
            "on",
        }
    )


def main() -> int:
    email = _required_env(
        "EMIDAF_ADMIN_EMAIL"
    ).lower()

    password = _required_env(
        "EMIDAF_ADMIN_PASSWORD"
    )

    first_name = _required_env(
        "EMIDAF_ADMIN_FIRST_NAME"
    )

    last_name = _required_env(
        "EMIDAF_ADMIN_LAST_NAME"
    )

    institution = (
        os.environ.get(
            "EMIDAF_ADMIN_INSTITUTION",
            "",
        ).strip()
        or None
    )

    country = (
        os.environ.get(
            "EMIDAF_ADMIN_COUNTRY",
            "",
        ).strip()
        or None
    )

    reset_password = _env_flag(
        "EMIDAF_ADMIN_RESET_PASSWORD"
    )

    bootstrap = Bootstrap()
    bootstrap.initialize()

    repository = UserRepository(
        bootstrap.database_manager
    )

    auth_service = AuthService(
        repository
    )

    normalized_email = (
        auth_service.normalize_email(email)
    )

    existing = repository.get_by_email(
        normalized_email
    )

    if existing is not None:

        if existing.role != "super_admin":
            raise RuntimeError(
                "Le compte existe déjà mais "
                "n'est pas super-admin."
            )

        if reset_password:
            existing.password_hash = (
                hash_password(password)
            )

            existing.is_active = True
            existing.is_verified = True

            repository.update(existing)

            print(
                "SUPER ADMIN : "
                "mot de passe réinitialisé"
            )

            return 0

        if (
            not existing.is_active
            or not existing.is_verified
        ):
            raise RuntimeError(
                "Le super-admin existe mais "
                "n'est pas actif et vérifié."
            )

        print(
            "SUPER ADMIN : déjà présent"
        )

        return 0

    user = auth_service.register(
        first_name=first_name,
        last_name=last_name,
        email=normalized_email,
        password=password,
        institution=institution,
        country=country,
        role="super_admin",
        is_verified=True,
    )

    print(
        "SUPER ADMIN : créé "
        f"(id={user.id}, email={user.email})"
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())

    except Exception as exc:
        print(
            f"BOOTSTRAP ADMIN ERROR : {exc}",
            file=sys.stderr,
        )

        raise SystemExit(1)
