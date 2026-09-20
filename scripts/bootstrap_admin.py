from __future__ import annotations

import os
import sys

from emidaf_core.bootstrap.bootstrap import Bootstrap
from emidaf_core.repositories.user_repository import (
    UserRepository,
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
        if (
            existing.role != "super_admin"
            or not existing.is_active
            or not existing.is_verified
        ):
            raise RuntimeError(
                "Le compte administrateur existe déjà "
                "mais n'est pas un super-admin actif "
                "et vérifié. Bootstrap refusé."
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
