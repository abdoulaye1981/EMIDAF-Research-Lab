"""
=========================================================
EMIDAF Framework v1.0

Correlation Analyzer

---------------------------------------------------------

Analyse des corrélations entre variables numériques.

Politique méthodologique :
- Spearman par défaut ;
- Spearman pour toute paire impliquant une variable ordinale ;
- Pearson uniquement lorsque les deux variables sont
  quantitatives non ordinales et compatibles avec la normalité.

=========================================================
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from .base_analyzer import BaseAnalyzer
from ..profile_context import ProfileContext


class CorrelationAnalyzer(BaseAnalyzer):

    """
    Analyse les corrélations entre variables numériques.

    Spearman constitue la méthode générale par défaut.
    Pearson est retenu dans l'analyse adaptative seulement
    lorsque les deux variables sont non ordinales et que
    leur normalité n'est pas rejetée.
    """

    name = "CorrelationAnalyzer"
    version = "1.1.0"
    description = (
        "Analyse adaptative des corrélations numériques "
        "avec Spearman par défaut"
    )

    @staticmethod
    def _build_pairs(
        matrix: pd.DataFrame,
        method: str,
    ) -> list[dict[str, Any]]:

        pairs: list[dict[str, Any]] = []

        columns = matrix.columns.tolist()

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):

                column_1 = columns[i]
                column_2 = columns[j]

                correlation = matrix.loc[
                    column_1,
                    column_2
                ]

                if pd.isna(correlation):
                    continue

                pairs.append(
                    {
                        "variable_1": column_1,
                        "variable_2": column_2,
                        "correlation": float(correlation),
                        "method": method,
                    }
                )

        pairs.sort(
            key=lambda item: abs(
                item["correlation"]
            ),
            reverse=True,
        )

        return pairs

    def analyze(
        self,
        context: ProfileContext,
    ) -> dict[str, Any]:

        dataframe = context.dataframe

        datatype_result = context.results.get(
            "DatatypeAnalyzer"
        )

        if datatype_result is None:
            return {
                "columns": [],
                "count": 0,
                "correlation_matrix": {},
                "pairs": [],
                "default_method": "spearman",
                "spearman_matrix": {},
                "spearman_pairs": [],
                "pearson_matrix": {},
                "pearson_pairs": [],
                "adaptive_pairs": [],
                "method_notes": [],
            }

        datatype = datatype_result.result

        numeric_columns = datatype.get(
            "numeric",
            [],
        )

        semantic = datatype.get(
            "semantic",
            {},
        ) or {}

        ordinal_columns = set(
            semantic.get(
                "ordinal",
                [],
            )
            or []
        )

        numeric = dataframe[
            numeric_columns
        ].copy()

        if numeric.empty:
            return {
                "columns": [],
                "count": 0,
                "correlation_matrix": {},
                "pairs": [],
                "default_method": "spearman",
                "spearman_matrix": {},
                "spearman_pairs": [],
                "pearson_matrix": {},
                "pearson_pairs": [],
                "adaptive_pairs": [],
                "method_notes": [],
            }

        numeric = numeric.replace(
            [np.inf, -np.inf],
            np.nan,
        )

        # =====================================================
        # Spearman : méthode par défaut
        # =====================================================

        spearman_matrix = (
            numeric
            .corr(method="spearman")
            .round(4)
        )

        spearman_pairs = self._build_pairs(
            spearman_matrix,
            "spearman",
        )

        # =====================================================
        # Pearson : calculé comme information complémentaire
        # =====================================================

        pearson_matrix = (
            numeric
            .corr(method="pearson")
            .round(4)
        )

        pearson_pairs = self._build_pairs(
            pearson_matrix,
            "pearson",
        )

        # =====================================================
        # Normalité disponible dans le contexte
        # =====================================================

        normality_result = context.results.get(
            "NormalityAnalyzer"
        )

        normality_columns: dict[str, Any] = {}

        if normality_result is not None:
            normality_payload = (
                normality_result.result
                or {}
            )

            normality_columns = (
                normality_payload.get(
                    "columns",
                    {},
                )
                or {}
            )

        def is_normal(
            column: str,
        ) -> bool:

            if column in ordinal_columns:
                return False

            stats = normality_columns.get(
                column,
                {},
            )

            return (
                stats.get("normal")
                is True
            )

        # =====================================================
        # Analyse adaptative paire par paire
        # =====================================================

        adaptive_pairs: list[
            dict[str, Any]
        ] = []

        columns = numeric.columns.tolist()

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):

                column_1 = columns[i]
                column_2 = columns[j]

                involves_ordinal = (
                    column_1 in ordinal_columns
                    or
                    column_2 in ordinal_columns
                )

                both_normal = (
                    is_normal(column_1)
                    and
                    is_normal(column_2)
                )

                if (
                    not involves_ordinal
                    and both_normal
                ):
                    method = "pearson"
                    reason = (
                        "both_variables_compatible_"
                        "with_normality"
                    )

                    correlation = (
                        pearson_matrix.loc[
                            column_1,
                            column_2
                        ]
                    )

                else:
                    method = "spearman"

                    if involves_ordinal:
                        reason = (
                            "ordinal_variable"
                        )
                    elif not normality_columns:
                        reason = (
                            "normality_unavailable"
                        )
                    else:
                        reason = (
                            "normality_not_confirmed"
                        )

                    correlation = (
                        spearman_matrix.loc[
                            column_1,
                            column_2
                        ]
                    )

                if pd.isna(correlation):
                    continue

                adaptive_pairs.append(
                    {
                        "variable_1": column_1,
                        "variable_2": column_2,
                        "correlation": float(
                            correlation
                        ),
                        "method": method,
                        "reason": reason,
                    }
                )

        adaptive_pairs.sort(
            key=lambda item: abs(
                item["correlation"]
            ),
            reverse=True,
        )

        # =====================================================
        # Résultat
        # =====================================================

        result = {
            "columns": columns,
            "count": len(columns),

            # -----------------------------------------------
            # Contrat historique :
            # Spearman devient la méthode par défaut.
            # -----------------------------------------------
            "correlation_matrix": (
                spearman_matrix.to_dict()
            ),
            "pairs": spearman_pairs,

            # -----------------------------------------------
            # Résultats explicites
            # -----------------------------------------------
            "default_method": "spearman",

            "spearman_matrix": (
                spearman_matrix.to_dict()
            ),
            "spearman_pairs": (
                spearman_pairs
            ),

            "pearson_matrix": (
                pearson_matrix.to_dict()
            ),
            "pearson_pairs": (
                pearson_pairs
            ),

            "adaptive_pairs": (
                adaptive_pairs
            ),

            "ordinal_columns": sorted(
                ordinal_columns
            ),

            "method_notes": [
                (
                    "Spearman est utilisé comme méthode "
                    "de corrélation par défaut."
                ),
                (
                    "Toute paire impliquant une variable "
                    "ordinale est analysée avec Spearman."
                ),
                (
                    "Pearson est retenu dans l'analyse "
                    "adaptative uniquement lorsque les "
                    "deux variables sont non ordinales "
                    "et compatibles avec la normalité."
                ),
                (
                    "Une corrélation mesure une "
                    "association et n'implique pas "
                    "une relation causale."
                ),
            ],
        }

        context.add_result(
            self.name,
            result,
        )

        context.put_cache(
            self.name,
            result,
        )

        return result
