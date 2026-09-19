from __future__ import annotations

from emidaf_core.core.base_analyzer import BaseAnalyzer

from ..profile_context import ProfileContext


class CategoricalAnalyzer(BaseAnalyzer):

    """
    Analyse des variables catégorielles.
    """

    name = "CategoricalAnalyzer"
    version = "1.0.0"

    def analyze(
        self,
        context: ProfileContext
    ) -> dict:

        dataframe = context.dataframe

        datatype_result = context.results.get("DatatypeAnalyzer")


        if datatype_result is None:
            return {}

        datatype = datatype_result.result

        categorical_columns = datatype.get(
            "categorical",
            []
        )


        results = {}

        for column in categorical_columns:
            series = dataframe[column]

            counts = series.value_counts()

            non_missing = int(series.notna().sum())
            missing = int(series.isna().sum())

            if non_missing > 0:
                percentages = (
                    counts / non_missing * 100
                ).round(2)
            else:
                percentages = counts.astype(float)

            results[column] = {
                "unique": int(series.nunique()),
                "mode": series.mode().tolist(),
                "frequencies": counts.to_dict(),
                "percentages": percentages.to_dict(),
                "cardinality": int(series.nunique()),
                "missing": missing,
                "missing_rate": round(
                    missing / len(dataframe) * 100,
                    2
                ) if len(dataframe) > 0 else 0.0
            }

        context.add_result(
            self.name,
            results
        )

        context.put_cache(
            self.name,
            results
        )

        return results
