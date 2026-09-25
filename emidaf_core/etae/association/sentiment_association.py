"""
=========================================================
EMIDAF Framework v1.0
ETAE - Sentiment Association
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import numpy as np
import pandas as pd

from scipy.stats import (
    chi2_contingency,
    f_oneway,
    kruskal,
)

from ..sentiment import (
    LexiconSentimentAnalyzer,
)


@dataclass(frozen=True)
class SentimentNumericGroup:
    sentiment: str
    n: int
    mean: float
    median: float
    std: float | None
    minimum: float
    maximum: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SentimentNumericResult:
    text_column: str
    target_column: str
    n_documents: int
    groups: list[SentimentNumericGroup]
    anova_statistic: float | None
    anova_p_value: float | None
    kruskal_statistic: float | None
    kruskal_p_value: float | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "text_column": self.text_column,
            "target_column": self.target_column,
            "n_documents": self.n_documents,
            "groups": [
                group.to_dict()
                for group in self.groups
            ],
            "anova_statistic": self.anova_statistic,
            "anova_p_value": self.anova_p_value,
            "kruskal_statistic": self.kruskal_statistic,
            "kruskal_p_value": self.kruskal_p_value,
        }


@dataclass(frozen=True)
class SentimentCategoricalResult:
    text_column: str
    target_column: str
    n_documents: int
    contingency_table: dict[str, dict[str, int]]
    chi2_statistic: float | None
    p_value: float | None
    dof: int | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "text_column": self.text_column,
            "target_column": self.target_column,
            "n_documents": self.n_documents,
            "contingency_table": (
                self.contingency_table
            ),
            "chi2_statistic": self.chi2_statistic,
            "p_value": self.p_value,
            "dof": self.dof,
        }


class SentimentAssociationAnalyzer:
    """
    Analyse les relations entre sentiment textuel
    et variables structurées.
    """

    def __init__(self) -> None:
        self._sentiment = (
            LexiconSentimentAnalyzer()
        )

    def analyze_numeric(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        target_column: str,
    ) -> SentimentNumericResult:

        self._validate_dataframe(
            dataframe
        )

        if target_column not in dataframe.columns:
            raise ValueError(
                f"Variable cible introuvable : "
                f"{target_column}"
            )

        if not pd.api.types.is_numeric_dtype(
            dataframe[target_column]
        ):
            raise TypeError(
                "La variable cible doit être numérique."
            )

        sentiment_result = (
            self._sentiment.analyze(
                dataframe,
                text_column,
            )
        )

        aligned = self._align(
            dataframe=dataframe,
            sentiment_result=sentiment_result,
            target_column=target_column,
        )

        aligned = aligned.dropna(
            subset=[target_column]
        )

        groups = []
        samples = []

        for label, group in (
            aligned.groupby(
                "sentiment",
                sort=True,
            )
        ):
            values = (
                group[target_column]
                .astype(float)
            )

            std = values.std(
                ddof=1
            )

            groups.append(
                SentimentNumericGroup(
                    sentiment=str(label),
                    n=int(len(values)),
                    mean=float(
                        values.mean()
                    ),
                    median=float(
                        values.median()
                    ),
                    std=(
                        float(std)
                        if pd.notna(std)
                        else None
                    ),
                    minimum=float(
                        values.min()
                    ),
                    maximum=float(
                        values.max()
                    ),
                )
            )

            if len(values) > 0:
                samples.append(
                    values.to_numpy(
                        dtype=float
                    )
                )

        anova_statistic = None
        anova_p_value = None
        kruskal_statistic = None
        kruskal_p_value = None

        if len(samples) >= 2:
            try:
                anova = f_oneway(
                    *samples
                )

                if (
                    np.isfinite(
                        anova.statistic
                    )
                    and np.isfinite(
                        anova.pvalue
                    )
                ):
                    anova_statistic = float(
                        anova.statistic
                    )
                    anova_p_value = float(
                        anova.pvalue
                    )
            except ValueError:
                pass

            try:
                kw = kruskal(
                    *samples
                )

                if (
                    np.isfinite(
                        kw.statistic
                    )
                    and np.isfinite(
                        kw.pvalue
                    )
                ):
                    kruskal_statistic = float(
                        kw.statistic
                    )
                    kruskal_p_value = float(
                        kw.pvalue
                    )
            except ValueError:
                pass

        return SentimentNumericResult(
            text_column=text_column,
            target_column=target_column,
            n_documents=int(
                len(aligned)
            ),
            groups=groups,
            anova_statistic=anova_statistic,
            anova_p_value=anova_p_value,
            kruskal_statistic=kruskal_statistic,
            kruskal_p_value=kruskal_p_value,
        )

    def analyze_categorical(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        target_column: str,
    ) -> SentimentCategoricalResult:

        self._validate_dataframe(
            dataframe
        )

        if target_column not in dataframe.columns:
            raise ValueError(
                f"Variable cible introuvable : "
                f"{target_column}"
            )

        sentiment_result = (
            self._sentiment.analyze(
                dataframe,
                text_column,
            )
        )

        aligned = self._align(
            dataframe=dataframe,
            sentiment_result=sentiment_result,
            target_column=target_column,
        )

        aligned = aligned.dropna(
            subset=[target_column]
        )

        if aligned.empty:
            return SentimentCategoricalResult(
                text_column=text_column,
                target_column=target_column,
                n_documents=0,
                contingency_table={},
                chi2_statistic=None,
                p_value=None,
                dof=None,
            )

        table = pd.crosstab(
            aligned["sentiment"],
            aligned[target_column],
        )

        chi2_statistic = None
        p_value = None
        dof = None

        if (
            table.shape[0] >= 2
            and table.shape[1] >= 2
        ):
            try:
                chi2, p, degrees, _ = (
                    chi2_contingency(
                        table
                    )
                )

                chi2_statistic = float(
                    chi2
                )
                p_value = float(
                    p
                )
                dof = int(
                    degrees
                )

            except ValueError:
                pass

        contingency = {
            str(row): {
                str(column): int(
                    table.loc[
                        row,
                        column,
                    ]
                )
                for column
                in table.columns
            }
            for row
            in table.index
        }

        return SentimentCategoricalResult(
            text_column=text_column,
            target_column=target_column,
            n_documents=int(
                len(aligned)
            ),
            contingency_table=contingency,
            chi2_statistic=chi2_statistic,
            p_value=p_value,
            dof=dof,
        )

    @staticmethod
    def _align(
        *,
        dataframe: pd.DataFrame,
        sentiment_result,
        target_column: str,
    ) -> pd.DataFrame:

        rows = []

        for document in (
            sentiment_result.documents
        ):
            rows.append(
                {
                    "index": document.index,
                    "sentiment": (
                        document.label
                    ),
                }
            )

        aligned = pd.DataFrame(
            rows
        )

        if aligned.empty:
            return pd.DataFrame(
                columns=[
                    "index",
                    "sentiment",
                    target_column,
                ]
            )

        values = (
            dataframe[target_column]
            .reindex(
                aligned["index"]
                .tolist()
            )
        )

        aligned[target_column] = list(
            values
        )

        return aligned

    @staticmethod
    def _validate_dataframe(
        dataframe: pd.DataFrame,
    ) -> None:

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe doit être un DataFrame pandas."
            )
