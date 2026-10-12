"""
=========================================================
EMIDAF Framework
EXAIE - Feature Importance Aggregation
=========================================================

Agrégation des variables transformées vers les variables
d'origine pour une restitution scientifique interprétable.

Exemples :

numeric__motivation
    -> motivation

categorical__region_Dakar
categorical__region_Ziguinchor
    -> region

L'agrégation reste indépendante du domaine étudié.
=========================================================
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


class FeatureImportanceAggregator:
    """
    Agrège les sorties explicatives obtenues après
    preprocessing vers les variables d'entrée originales.
    """

    @staticmethod
    def original_feature(
        transformed_name: str,
        original_features: Iterable[str],
    ) -> str:
        """
        Retrouve la variable originale correspondant
        à un nom produit par get_feature_names_out().

        La recherche utilise le plus long préfixe valide
        parmi les variables originales. Cela permet de
        gérer correctement les noms contenant des "_".
        """

        transformed_name = str(
            transformed_name
        )

        # ColumnTransformer génère généralement :
        # numeric__x
        # categorical__x_modalite
        if "__" in transformed_name:
            candidate = transformed_name.split(
                "__",
                1,
            )[1]
        else:
            candidate = transformed_name

        features = sorted(
            [
                str(feature)
                for feature in original_features
            ],
            key=len,
            reverse=True,
        )

        # Correspondance exacte prioritaire.
        if candidate in features:
            return candidate

        # Une modalité OneHot apparaît généralement après
        # le nom original et un underscore.
        for feature in features:

            prefix = (
                feature
                + "_"
            )

            if candidate.startswith(
                prefix
            ):
                return feature

        # Certains transformeurs peuvent conserver
        # un préfixe plus complexe. Dernier repli prudent.
        for feature in features:

            if (
                transformed_name == feature
                or transformed_name.endswith(
                    "__" + feature
                )
            ):
                return feature

        # On ne doit pas inventer une correspondance.
        return transformed_name

    @classmethod
    def mapping(
        cls,
        transformed_features: Iterable[str],
        original_features: Iterable[str],
    ) -> dict[str, str]:
        """
        Construit :
        variable transformée -> variable originale.
        """

        originals = list(
            original_features
        )

        return {
            str(feature):
                cls.original_feature(
                    feature,
                    originals,
                )
            for feature
            in transformed_features
        }

    @classmethod
    def global_importance(
        cls,
        dataframe: pd.DataFrame,
        *,
        original_features: Iterable[str],
        feature_column: str = "feature",
        importance_column: str = "importance",
    ) -> pd.DataFrame:
        """
        Agrège une importance globale non négative.

        Les importances des colonnes transformées issues
        d'une même variable originale sont additionnées.

        Cette opération conserve la masse totale
        d'importance.
        """

        if dataframe is None:
            raise ValueError(
                "Le tableau d'importance est absent."
            )

        if dataframe.empty:
            return dataframe.copy()

        required = {
            feature_column,
            importance_column,
        }

        missing = required.difference(
            dataframe.columns
        )

        if missing:
            raise ValueError(
                "Colonnes manquantes : "
                + ", ".join(
                    sorted(missing)
                )
            )

        table = dataframe.copy()

        table[
            "original_feature"
        ] = [
            cls.original_feature(
                feature,
                original_features,
            )
            for feature
            in table[
                feature_column
            ]
        ]

        table[
            importance_column
        ] = pd.to_numeric(
            table[
                importance_column
            ],
            errors="coerce",
        )

        grouped = (
            table
            .groupby(
                "original_feature",
                as_index=False,
                sort=False,
            )[
                importance_column
            ]
            .sum(
                min_count=1
            )
        )

        grouped = grouped.rename(
            columns={
                "original_feature":
                    "feature",
            }
        )

        total = grouped[
            importance_column
        ].sum()

        if (
            np.isfinite(total)
            and total > 0
        ):
            grouped[
                "importance_share"
            ] = (
                grouped[
                    importance_column
                ]
                / total
            )
        else:
            grouped[
                "importance_share"
            ] = np.nan

        return (
            grouped
            .sort_values(
                importance_column,
                ascending=False,
                na_position="last",
            )
            .reset_index(
                drop=True
            )
        )

    @classmethod
    def shap_importance(
        cls,
        feature_importance: dict,
        *,
        original_features: Iterable[str],
    ) -> pd.DataFrame:
        """
        Agrège le dictionnaire d'importance globale SHAP.
        """

        table = pd.DataFrame(
            {
                "feature": list(
                    feature_importance.keys()
                ),
                "importance": list(
                    feature_importance.values()
                ),
            }
        )

        return cls.global_importance(
            table,
            original_features=original_features,
        )

    @classmethod
    def local_contributions(
        cls,
        dataframe: pd.DataFrame,
        *,
        original_features: Iterable[str],
    ) -> pd.DataFrame:
        """
        Agrège les contributions locales signées.

        La contribution scientifique d'une variable
        catégorielle est la somme des contributions
        de ses colonnes one-hot.

        On ne somme PAS les valeurs absolues avant
        l'agrégation, afin de préserver le signe net.
        """

        if dataframe is None:
            raise ValueError(
                "Le tableau local est absent."
            )

        if dataframe.empty:
            return dataframe.copy()

        required = {
            "feature",
            "contribution",
        }

        missing = required.difference(
            dataframe.columns
        )

        if missing:
            raise ValueError(
                "Colonnes manquantes : "
                + ", ".join(
                    sorted(missing)
                )
            )

        table = dataframe.copy()

        table[
            "original_feature"
        ] = [
            cls.original_feature(
                feature,
                original_features,
            )
            for feature
            in table["feature"]
        ]

        table[
            "contribution"
        ] = pd.to_numeric(
            table[
                "contribution"
            ],
            errors="coerce",
        )

        grouped = (
            table
            .groupby(
                "original_feature",
                as_index=False,
                sort=False,
            )[
                "contribution"
            ]
            .sum(
                min_count=1
            )
        )

        grouped = grouped.rename(
            columns={
                "original_feature":
                    "feature",
            }
        )

        grouped[
            "abs_contribution"
        ] = grouped[
            "contribution"
        ].abs()

        return (
            grouped
            .sort_values(
                "abs_contribution",
                ascending=False,
                na_position="last",
            )
            .reset_index(
                drop=True
            )
        )


def aggregate_global_importance(
    dataframe: pd.DataFrame,
    *,
    original_features: Iterable[str],
) -> pd.DataFrame:

    return (
        FeatureImportanceAggregator
        .global_importance(
            dataframe,
            original_features=original_features,
        )
    )


def aggregate_local_contributions(
    dataframe: pd.DataFrame,
    *,
    original_features: Iterable[str],
) -> pd.DataFrame:

    return (
        FeatureImportanceAggregator
        .local_contributions(
            dataframe,
            original_features=original_features,
        )
    )
