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

    version = "1.0.0"

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
        unknown = []

        dtypes = {}

        for column in dataframe.columns:

            series = dataframe[column]

            dtype_name = str(series.dtype)

            dtypes[column] = dtype_name

            # ==========================================
            # BOOLEAN
            # ==========================================

            if pd.api.types.is_bool_dtype(series):
                boolean.append(column)
                continue

            # ==========================================
            # NUMERIQUE
            # ==========================================

            if pd.api.types.is_numeric_dtype(series):
                numeric.append(column)
                continue

            # ==========================================
            # DATETIME
            # ==========================================

            if pd.api.types.is_datetime64_any_dtype(series):
                datetime_columns.append(column)
                continue

            # ==========================================
            # CATEGORIE EXPLICITE
            # ==========================================

            if isinstance(
                series.dtype,
                pd.CategoricalDtype
            ):
                categorical.append(column)
                continue

            # ==========================================
            # OBJECT / STRING
            # ==========================================

            if (
                pd.api.types.is_object_dtype(series)
                or
                pd.api.types.is_string_dtype(series)
            ):
                non_missing = series.dropna()

                if len(non_missing) == 0:
                    unknown.append(column)
                    continue

                # Les variables object/string sont considérées
                # comme textuelles à ce niveau.
                text.append(column)

                continue

            # ==========================================
            # TYPE INCONNU
            # ==========================================

            unknown.append(column)

        # ==========================================
        # COMPTAGES
        # ==========================================

        count = {
            "numeric": len(numeric),
            "categorical": len(categorical),
            "boolean": len(boolean),
            "datetime": len(datetime_columns),
            "text": len(text),
            "unknown": len(unknown)
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
            "unknown": unknown,
            "dtypes": dtypes,
            "count": count
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
