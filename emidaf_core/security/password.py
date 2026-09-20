"""
=========================================================
EMIDAF Framework v1.0
Password Security
=========================================================
"""

from __future__ import annotations

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


def hash_password(password: str) -> str:
    """
    Hash sécurisé d'un mot de passe.

    Le mot de passe en clair n'est jamais persisté.
    """

    if not isinstance(password, str):
        raise TypeError(
            "Le mot de passe doit être une chaîne."
        )

    if len(password) < 10:
        raise ValueError(
            "Le mot de passe doit contenir au moins "
            "10 caractères."
        )

    return generate_password_hash(
        password,
        method="scrypt",
    )


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    """
    Vérifie un mot de passe contre son hash.
    """

    if not password or not password_hash:
        return False

    try:
        return check_password_hash(
            password_hash,
            password,
        )
    except (ValueError, TypeError):
        return False
