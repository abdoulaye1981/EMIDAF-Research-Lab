"""
=========================================================
EMIDAF Framework
EAIE - Feature Roles
=========================================================

Résolution scientifique des rôles de variables avant
modélisation supervisée.

Objectifs :
- protéger la cible ;
- exclure les identifiants ;
- exclure le texte libre du pipeline tabulaire EAIE ;
- exclure les variables techniques de qualité ;
- prendre en compte les exclusions explicites ;
- produire la liste finale des prédicteurs admissibles.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from emidaf_core.dataset.profiler import DatasetProfiler


QUALITY_PREFIXES = (
    "statut_",
    "status_",
    "quality_",
    "flag_",
)


@dataclass(slots=True)
class FeatureRoleResult:
    target: str
    predictors: list[str]
    identifiers: list[str]
    quality: list[str]
    text: list[str]
    excluded: list[str]
    protected: list[str]
    valid: bool
    conflicts: list[str]

    def to_dict(self) -> dict:
        return {
            "target": self.target,
            "predictors": list(self.predictors),
            "identifiers": list(self.identifiers),
            "quality": list(self.quality),
            "text": list(self.text),
            "excluded": list(self.excluded),
            "protected": list(self.protected),
            "valid": self.valid,
            "conflicts": list(self.conflicts),
        }


class FeatureRoles:
    """
    Résout les rôles des variables pour EAIE.

    La source de vérité sémantique est DatasetProfiler.
    Les variables de qualité suivent les conventions
    techniques déjà utilisées dans EIDPP.
    """

    @staticmethod
    def resolve(
        dataframe: pd.DataFrame,
        target: str,
        *,
        excluded: list[str] | None = None,
    ) -> FeatureRoleResult:

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "FeatureRoles attend un pandas.DataFrame."
            )

        if target not in dataframe.columns:
            raise ValueError(
                f"Cible introuvable : {target}"
            )

        excluded = list(
            dict.fromkeys(
                excluded or []
            )
        )

        missing_excluded = [
            column
            for column in excluded
            if column not in dataframe.columns
        ]

        if missing_excluded:
            raise ValueError(
                "Variables exclues introuvables : "
                + ", ".join(missing_excluded)
            )

        profiler = DatasetProfiler()

        profile = profiler.profile(
            dataframe
        )

        datatypes = (
            profile.datatypes
            or {}
        )

        identifiers = list(
            dict.fromkeys(
                datatypes.get(
                    "identifier",
                    [],
                )
                or []
            )
        )

        text_columns = list(
            dict.fromkeys(
                datatypes.get(
                    "text",
                    [],
                )
                or []
            )
        )

        quality_columns = [
            column
            for column in dataframe.columns
            if column.lower().startswith(
                QUALITY_PREFIXES
            )
        ]

        conflicts = []

        role_groups = {
            "identifier": identifiers,
            "quality": quality_columns,
            "text": text_columns,
            "excluded": excluded,
        }

        for role, columns in role_groups.items():
            if target in columns:
                conflicts.append(
                    (
                        f"La cible '{target}' est aussi "
                        f"déclarée comme {role}."
                    )
                )

        seen_roles = {}

        for role, columns in role_groups.items():
            for column in columns:

                previous = seen_roles.get(
                    column
                )

                if (
                    previous is not None
                    and previous != role
                ):
                    conflicts.append(
                        (
                            f"'{column}' apparaît dans "
                            f"les rôles {previous} "
                            f"et {role}."
                        )
                    )

                seen_roles[column] = role

        protected = set(
            identifiers
            + quality_columns
            + text_columns
            + excluded
        )

        protected.add(
            target
        )

        predictors = [
            column
            for column in dataframe.columns
            if column not in protected
        ]

        if not predictors:
            conflicts.append(
                "Aucun prédicteur admissible n'est disponible."
            )

        return FeatureRoleResult(
            target=target,
            predictors=predictors,
            identifiers=identifiers,
            quality=quality_columns,
            text=text_columns,
            excluded=excluded,
            protected=sorted(
                protected
            ),
            valid=not conflicts,
            conflicts=conflicts,
        )


def resolve_feature_roles(
    dataframe: pd.DataFrame,
    target: str,
    *,
    excluded: list[str] | None = None,
) -> FeatureRoleResult:
    return FeatureRoles.resolve(
        dataframe,
        target,
        excluded=excluded,
    )
