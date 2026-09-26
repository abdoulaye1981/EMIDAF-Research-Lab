"""
=========================================================
EMIDAF Framework v1.0
EQAE - Thematic Analysis
=========================================================
"""

from __future__ import annotations

from .theme import QualitativeTheme
from ..coding import Codebook


class ThematicAnalysis:
    """
    Gestion des thèmes qualitatifs et de leur liaison
    avec les codes du codebook.
    """

    def __init__(
        self,
        codebook: Codebook,
    ) -> None:

        if not isinstance(
            codebook,
            Codebook,
        ):
            raise TypeError(
                "codebook doit être une instance de Codebook."
            )

        self.codebook = codebook

        self._themes: dict[
            str,
            QualitativeTheme,
        ] = {}

        self._theme_codes: dict[
            str,
            set[str],
        ] = {}

    @property
    def themes(
        self,
    ) -> list[QualitativeTheme]:

        return list(
            self._themes.values()
        )

    def add_theme(
        self,
        name: str,
        *,
        description: str = "",
        parent_theme_id: str | None = None,
        theme_id: str | None = None,
    ) -> QualitativeTheme:
        """
        Ajoute un thème ou sous-thème.
        """

        name = str(name).strip()

        if not name:
            raise ValueError(
                "Le nom du thème ne peut pas être vide."
            )

        if parent_theme_id is not None:
            if (
                parent_theme_id
                not in self._themes
            ):
                raise ValueError(
                    "Thème parent introuvable : "
                    f"{parent_theme_id}"
                )

        normalized_name = (
            name.casefold()
        )

        for theme in self._themes.values():
            if (
                theme.name.casefold()
                == normalized_name
                and theme.parent_theme_id
                == parent_theme_id
            ):
                raise ValueError(
                    "Un thème portant ce nom "
                    "existe déjà à ce niveau : "
                    f"{name}"
                )

        theme = QualitativeTheme.create(
            name=name,
            description=description,
            parent_theme_id=parent_theme_id,
            theme_id=theme_id,
        )

        if theme.theme_id in self._themes:
            raise ValueError(
                "Identifiant de thème déjà utilisé : "
                f"{theme.theme_id}"
            )

        self._themes[
            theme.theme_id
        ] = theme

        self._theme_codes[
            theme.theme_id
        ] = set()

        return theme

    def get_theme(
        self,
        theme_id: str,
    ) -> QualitativeTheme | None:

        return self._themes.get(
            str(theme_id)
        )

    def link_code(
        self,
        *,
        theme_id: str,
        code_id: str,
    ) -> None:
        """
        Associe un code du codebook à un thème.
        """

        theme_id = str(
            theme_id
        ).strip()

        code_id = str(
            code_id
        ).strip()

        if theme_id not in self._themes:
            raise ValueError(
                "Thème introuvable : "
                f"{theme_id}"
            )

        if (
            self.codebook.get_code(
                code_id
            )
            is None
        ):
            raise ValueError(
                "Code introuvable : "
                f"{code_id}"
            )

        self._theme_codes[
            theme_id
        ].add(
            code_id
        )

    def unlink_code(
        self,
        *,
        theme_id: str,
        code_id: str,
    ) -> None:
        """
        Retire un code d'un thème.
        """

        if theme_id not in self._themes:
            raise ValueError(
                "Thème introuvable : "
                f"{theme_id}"
            )

        self._theme_codes[
            theme_id
        ].discard(
            str(code_id)
        )

    def codes_for_theme(
        self,
        theme_id: str,
    ) -> list[str]:
        """
        Retourne les identifiants des codes
        associés à un thème.
        """

        if theme_id not in self._themes:
            raise ValueError(
                "Thème introuvable : "
                f"{theme_id}"
            )

        return sorted(
            self._theme_codes[
                theme_id
            ]
        )

    def child_themes(
        self,
        theme_id: str,
    ) -> list[QualitativeTheme]:
        """
        Retourne les sous-thèmes directs.
        """

        if theme_id not in self._themes:
            raise ValueError(
                "Thème introuvable : "
                f"{theme_id}"
            )

        return [
            theme
            for theme
            in self._themes.values()
            if (
                theme.parent_theme_id
                == theme_id
            )
        ]

    def remove_theme(
        self,
        theme_id: str,
    ) -> QualitativeTheme:
        """
        Supprime un thème uniquement s'il ne possède
        aucun sous-thème.
        """

        theme_id = str(
            theme_id
        )

        if theme_id not in self._themes:
            raise ValueError(
                "Thème introuvable : "
                f"{theme_id}"
            )

        children = self.child_themes(
            theme_id
        )

        if children:
            raise ValueError(
                "Impossible de supprimer un thème "
                "possédant des sous-thèmes."
            )

        self._theme_codes.pop(
            theme_id,
            None,
        )

        return self._themes.pop(
            theme_id
        )

    def to_dict(self):
        return {
            "themes": [
                {
                    **theme.to_dict(),
                    "code_ids": (
                        self.codes_for_theme(
                            theme.theme_id
                        )
                    ),
                }
                for theme
                in self.themes
            ]
        }
