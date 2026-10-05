"""
=========================================================
EMIDAF Framework v1.0
Datatype Analyzer
---------------------------------------------------------
Analyse et classification des types de variables.
=========================================================
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from emidaf_core.core.base_analyzer import BaseAnalyzer

from ..profile_context import ProfileContext


class DatatypeAnalyzer(BaseAnalyzer):

    name = "DatatypeAnalyzer"

    version = "1.1.0"

    # --------------------------------------------------
    # Paramètres de détection sémantique
    # --------------------------------------------------

    CATEGORICAL_MAX_UNIQUE = 50
    CATEGORICAL_MAX_RATIO = 0.05

    ORDINAL_1_5_COLUMNS = {
        "interet_maths",
        "stress",
        "eval_formatives_prevues",
        "ressources_educatives",
        "motivation",
        "implication",
        "pratiques_pedagogiques",
        "feedback_prof",
        "perception_difficultes",
    }

    ORDINAL_COLUMNS = {
        "niveau",
        "niveau_etude",
    }

    TEXT_NAME_HINTS = {
        "text",
        "texte",
        "review",
        "comment",
        "commentaire",
        "verbatim",
        "feedback_text",
        "reponse_libre",
        "response_text",
        "description_libre",
    }

    def _is_identifier(
        self,
        column: str,
    ) -> bool:
        """
        Détecte uniquement les colonnes explicitement nommées
        comme identifiants.

        Cette règle volontairement conservatrice évite de
        transformer automatiquement toute variable à forte
        cardinalité en identifiant.
        """
        normalized = column.strip().lower()

        return (
            normalized == "id"
            or normalized.startswith("id_")
            or normalized.endswith("_id")
        )

    def _is_binary_numeric(
        self,
        series: pd.Series,
    ) -> bool:
        """
        Détecte les variables numériques réellement binaires
        codées 0/1.
        """
        non_missing = series.dropna()

        if non_missing.empty:
            return False

        values = set(
            pd.unique(non_missing)
        )

        return (
            len(values) <= 2
            and values.issubset({0, 1, 0.0, 1.0})
        )

    def _is_free_text_string(
        self,
        column: str,
        series: pd.Series,
    ) -> bool:
        """
        Détecte les variables contenant du texte libre.

        La décision combine :
        - des indices sémantiques dans le nom de colonne ;
        - la longueur moyenne des chaînes ;
        - le nombre moyen de mots.

        La cardinalité seule ne suffit donc pas à transformer
        automatiquement un texte répété en variable catégorielle.
        """
        non_missing = (
            series
            .dropna()
            .astype(str)
            .str.strip()
        )

        non_missing = non_missing[
            non_missing != ""
        ]

        if non_missing.empty:
            return False

        normalized_column = (
            column
            .strip()
            .lower()
        )

        has_text_name_hint = any(
            hint in normalized_column
            for hint in self.TEXT_NAME_HINTS
        )

        average_length = float(
            non_missing.str.len().mean()
        )

        average_words = float(
            non_missing
            .str.split()
            .str.len()
            .mean()
        )

        sentence_like = (
            average_length >= 20.0
            and average_words >= 3.0
        )

        return (
            has_text_name_hint
            and sentence_like
        )

    def _is_categorical_string(
        self,
        series: pd.Series,
    ) -> bool:
        """
        Distingue une chaîne catégorielle d'un texte libre.

        Une chaîne est considérée catégorielle lorsqu'elle
        possède une cardinalité faible, en valeur absolue ou
        relativement au nombre d'observations.
        """
        non_missing = series.dropna()

        if non_missing.empty:
            return False

        n = len(non_missing)
        n_unique = non_missing.nunique(
            dropna=True
        )

        unique_ratio = (
            n_unique / n
            if n > 0
            else 0.0
        )

        return (
            n_unique <= self.CATEGORICAL_MAX_UNIQUE
            or unique_ratio <= self.CATEGORICAL_MAX_RATIO
        )

    def analyze(
        self,
        context: ProfileContext
    ) -> dict[str, Any]:

        dataframe = context.dataframe

        numeric = []
        categorical = []
        boolean = []
        datetime_columns = []
        text = []
        identifier = []
        unknown = []

        dtypes = {}

        semantic = {
            "identifier": [],
            "ordinal": [],
            "nominal": [],
            "binary": [],
            "free_text": [],
        }

        for column in dataframe.columns:

            series = dataframe[column]

            dtype_name = str(series.dtype)

            dtypes[column] = dtype_name

            # ==========================================
            # IDENTIFIANT
            # ==========================================

            if self._is_identifier(
                column
            ):
                identifier.append(
                    column
                )

                semantic[
                    "identifier"
                ].append(
                    column
                )

                continue

            # ==========================================
            # BOOLEAN NATIF
            # ==========================================

            if pd.api.types.is_bool_dtype(
                series
            ):
                boolean.append(
                    column
                )

                semantic[
                    "binary"
                ].append(
                    column
                )

                continue

            # ==========================================
            # NUMERIQUE
            # ==========================================

            if pd.api.types.is_numeric_dtype(
                series
            ):

                if self._is_binary_numeric(
                    series
                ):
                    boolean.append(
                        column
                    )

                    semantic[
                        "binary"
                    ].append(
                        column
                    )

                    continue

                numeric.append(
                    column
                )

                if (
                    column
                    in self.ORDINAL_1_5_COLUMNS
                ):
                    semantic[
                        "ordinal"
                    ].append(
                        column
                    )

                continue

            # ==========================================
            # DATETIME
            # ==========================================

            if (
                pd.api.types
                .is_datetime64_any_dtype(
                    series
                )
            ):
                datetime_columns.append(
                    column
                )

                continue

            # ==========================================
            # CATEGORIE EXPLICITE
            # ==========================================

            if isinstance(
                series.dtype,
                pd.CategoricalDtype
            ):
                categorical.append(
                    column
                )

                if (
                    column
                    in self.ORDINAL_COLUMNS
                ):
                    semantic[
                        "ordinal"
                    ].append(
                        column
                    )
                else:
                    semantic[
                        "nominal"
                    ].append(
                        column
                    )

                continue

            # ==========================================
            # OBJECT / STRING
            # ==========================================

            if (
                pd.api.types.is_object_dtype(
                    series
                )
                or
                pd.api.types.is_string_dtype(
                    series
                )
            ):
                non_missing = series.dropna()

                if len(
                    non_missing
                ) == 0:
                    unknown.append(
                        column
                    )
                    continue

                if self._is_free_text_string(
                    column,
                    series,
                ):
                    text.append(
                        column
                    )

                    semantic[
                        "free_text"
                    ].append(
                        column
                    )

                    continue

                if self._is_categorical_string(
                    series
                ):
                    categorical.append(
                        column
                    )

                    if (
                        column
                        in self.ORDINAL_COLUMNS
                    ):
                        semantic[
                            "ordinal"
                        ].append(
                            column
                        )
                    else:
                        semantic[
                            "nominal"
                        ].append(
                            column
                        )

                    continue

                text.append(
                    column
                )

                semantic[
                    "free_text"
                ].append(
                    column
                )

                continue

            # ==========================================
            # TYPE INCONNU
            # ==========================================

            unknown.append(
                column
            )

        # ==========================================
        # COMPTAGES
        # ==========================================

        count = {
            "numeric": len(
                numeric
            ),
            "categorical": len(
                categorical
            ),
            "boolean": len(
                boolean
            ),
            "datetime": len(
                datetime_columns
            ),
            "text": len(
                text
            ),
            "identifier": len(
                identifier
            ),
            "unknown": len(
                unknown
            ),
        }

        # ==========================================
        # RESULTAT
        # ==========================================

        result = {
            "numeric": numeric,
            "categorical": categorical,
            "boolean": boolean,
            "datetime": datetime_columns,
            "text": text,
            "identifier": identifier,
            "unknown": unknown,
            "semantic": semantic,
            "dtypes": dtypes,
            "count": count,
        }

        context.add_result(
            self.name,
            result
        )

        context.put_cache(
            self.name,
            result
        )

        return result
