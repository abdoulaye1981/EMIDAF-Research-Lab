"""
=========================================================
EMIDAF Framework v1.0
EQAE - Qualitative Codebook
=========================================================
"""

from __future__ import annotations

from uuid import uuid4

from ..result import (
    CodebookResult,
    QualitativeCodeResult,
)


class Codebook:
    """
    Gestionnaire de codes qualitatifs.

    Un codebook contient les codes définis par le
    chercheur et conserve leur organisation hiérarchique.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
    ) -> None:

        name = str(name).strip()

        if not name:
            raise ValueError(
                "Le nom du codebook ne peut pas être vide."
            )

        self.name = name
        self.description = str(
            description
        ).strip()

        self._codes: dict[
            str,
            QualitativeCodeResult,
        ] = {}

    @property
    def codes(
        self,
    ) -> list[QualitativeCodeResult]:

        return list(
            self._codes.values()
        )

    def add_code(
        self,
        name: str,
        *,
        description: str = "",
        parent_code_id: str | None = None,
        color: str | None = None,
        code_id: str | None = None,
    ) -> QualitativeCodeResult:
        """
        Ajoute un code qualitatif.

        Un code peut éventuellement dépendre
        d'un autre code.
        """

        name = str(name).strip()

        if not name:
            raise ValueError(
                "Le nom du code ne peut pas être vide."
            )

        if parent_code_id is not None:
            if parent_code_id not in self._codes:
                raise ValueError(
                    "Le code parent est introuvable : "
                    f"{parent_code_id}"
                )

        normalized_name = (
            name.casefold()
        )

        for code in self._codes.values():
            if (
                code.name.casefold()
                == normalized_name
            ):
                raise ValueError(
                    "Un code portant ce nom existe déjà : "
                    f"{name}"
                )

        identifier = (
            str(code_id).strip()
            if code_id is not None
            else uuid4().hex
        )

        if not identifier:
            raise ValueError(
                "L'identifiant du code ne peut pas être vide."
            )

        if identifier in self._codes:
            raise ValueError(
                "Identifiant de code déjà utilisé : "
                f"{identifier}"
            )

        code = QualitativeCodeResult(
            code_id=identifier,
            name=name,
            description=str(
                description
            ).strip(),
            parent_code_id=parent_code_id,
            color=(
                str(color).strip()
                if color is not None
                else None
            ),
        )

        self._codes[
            identifier
        ] = code

        return code

    def get_code(
        self,
        code_id: str,
    ) -> QualitativeCodeResult | None:
        """
        Retourne un code à partir de son identifiant.
        """

        return self._codes.get(
            str(code_id)
        )

    def remove_code(
        self,
        code_id: str,
    ) -> QualitativeCodeResult:
        """
        Supprime un code sans supprimer implicitement
        ses enfants.
        """

        code_id = str(
            code_id
        )

        if code_id not in self._codes:
            raise ValueError(
                "Code introuvable : "
                f"{code_id}"
            )

        children = [
            code
            for code in self._codes.values()
            if (
                code.parent_code_id
                == code_id
            )
        ]

        if children:
            raise ValueError(
                "Impossible de supprimer un code "
                "possédant des sous-codes."
            )

        return self._codes.pop(
            code_id
        )

    def to_result(
        self,
    ) -> CodebookResult:
        """
        Produit une représentation immuable
        et sérialisable du codebook.
        """

        return CodebookResult(
            name=self.name,
            description=self.description,
            codes=self.codes,
        )

    def to_dict(self):
        return self.to_result().to_dict()
