"""
=========================================================
EMIDAF Framework v1.0
MAR Analyzer
---------------------------------------------------------
Analyse statistique des associations entre missingness
et variables observées.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from scipy.stats import mannwhitneyu


@dataclass(slots=True)
class MARAssociation:
    target: str
    predictor: str
    predictor_type: str
    test_name: str
    statistic: float | None
    pvalue: float | None
    adjusted_pvalue: float | None
    significant: bool
    sample_size: int


@dataclass(slots=True)
class MARVariableResult:
    variable: str
    missing_rate: float
    evidence_detected: bool
    association_count: int
    significant_count: int
    strongest_predictor: str | None
    strongest_pvalue: float | None
    associations: list[MARAssociation] = field(
        default_factory=list
    )


@dataclass(slots=True)
class MARResult:
    executed: bool
    evidence_detected: bool | None
    alpha: float
    variables_tested: int
    variables_with_evidence: int
    results: list[MARVariableResult]
    message: str


class MARAnalyzer:
    """
    Analyse si le missingness d'une variable est associé
    à des variables observées.

    Important :
        cette analyse fournit des éléments compatibles
        avec un mécanisme MAR, mais ne prouve pas MAR.
    """

    def run(
        self,
        dataframe: pd.DataFrame,
        alpha: float = 0.05,
        min_group_size: int = 5,
    ) -> MARResult:

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe must be a pandas DataFrame."
            )

        if not 0 < alpha < 1:
            raise ValueError(
                "alpha must be between 0 and 1."
            )

        if min_group_size < 2:
            raise ValueError(
                "min_group_size must be at least 2."
            )

        if dataframe.empty:
            return MARResult(
                executed=False,
                evidence_detected=None,
                alpha=alpha,
                variables_tested=0,
                variables_with_evidence=0,
                results=[],
                message="The dataframe is empty.",
            )

        missing_columns = [
            column
            for column in dataframe.columns
            if dataframe[column].isna().any()
        ]

        if not missing_columns:
            return MARResult(
                executed=False,
                evidence_detected=None,
                alpha=alpha,
                variables_tested=0,
                variables_with_evidence=0,
                results=[],
                message=(
                    "No missing values detected. "
                    "MAR analysis is not required."
                ),
            )

        variable_results = []

        for target in missing_columns:

            target_missing = dataframe[
                target
            ].isna()

            missing_count = int(
                target_missing.sum()
            )

            observed_count = int(
                (~target_missing).sum()
            )

            missing_rate = round(
                100.0
                * missing_count
                / len(dataframe),
                2,
            )

            if (
                missing_count < min_group_size
                or observed_count < min_group_size
            ):
                variable_results.append(
                    MARVariableResult(
                        variable=target,
                        missing_rate=missing_rate,
                        evidence_detected=False,
                        association_count=0,
                        significant_count=0,
                        strongest_predictor=None,
                        strongest_pvalue=None,
                        associations=[],
                    )
                )
                continue

            associations = []

            for predictor in dataframe.columns:

                if predictor == target:
                    continue

                association = self._analyze_predictor(
                    dataframe=dataframe,
                    target_missing=target_missing,
                    target=target,
                    predictor=predictor,
                    min_group_size=min_group_size,
                )

                if association is not None:
                    associations.append(
                        association
                    )

            self._adjust_pvalues(
                associations=associations,
                alpha=alpha,
            )

            significant = [
                association
                for association in associations
                if association.significant
            ]

            strongest = None

            if associations:
                strongest = min(
                    associations,
                    key=lambda item: (
                        item.adjusted_pvalue
                        if item.adjusted_pvalue is not None
                        else 1.0
                    ),
                )

            variable_results.append(
                MARVariableResult(
                    variable=target,
                    missing_rate=missing_rate,
                    evidence_detected=bool(
                        significant
                    ),
                    association_count=len(
                        associations
                    ),
                    significant_count=len(
                        significant
                    ),
                    strongest_predictor=(
                        strongest.predictor
                        if strongest
                        else None
                    ),
                    strongest_pvalue=(
                        strongest.adjusted_pvalue
                        if strongest
                        else None
                    ),
                    associations=associations,
                )
            )

        variables_with_evidence = sum(
            1
            for result in variable_results
            if result.evidence_detected
        )

        evidence_detected = (
            variables_with_evidence > 0
        )

        return MARResult(
            executed=True,
            evidence_detected=evidence_detected,
            alpha=alpha,
            variables_tested=len(
                variable_results
            ),
            variables_with_evidence=(
                variables_with_evidence
            ),
            results=variable_results,
            message=(
                "Observed-variable associations with "
                "missingness were detected."
                if evidence_detected
                else
                "No statistically significant "
                "observed-variable associations with "
                "missingness were detected."
            ),
        )

    def _analyze_predictor(
        self,
        dataframe: pd.DataFrame,
        target_missing: pd.Series,
        target: str,
        predictor: str,
        min_group_size: int,
    ) -> MARAssociation | None:

        series = dataframe[
            predictor
        ]

        valid = series.notna()

        x = series.loc[
            valid
        ]

        missing_indicator = (
            target_missing.loc[
                valid
            ]
        )

        if len(x) == 0:
            return None

        if pd.api.types.is_numeric_dtype(
            x
        ):
            return self._numeric_association(
                x=x,
                missing_indicator=missing_indicator,
                target=target,
                predictor=predictor,
                min_group_size=min_group_size,
            )

        return self._categorical_association(
            x=x,
            missing_indicator=missing_indicator,
            target=target,
            predictor=predictor,
        )

    @staticmethod
    def _numeric_association(
        x: pd.Series,
        missing_indicator: pd.Series,
        target: str,
        predictor: str,
        min_group_size: int,
    ) -> MARAssociation | None:

        group_missing = x[
            missing_indicator
        ]

        group_observed = x[
            ~missing_indicator
        ]

        if (
            len(group_missing) < min_group_size
            or len(group_observed) < min_group_size
        ):
            return None

        if (
            group_missing.nunique() <= 1
            and group_observed.nunique() <= 1
        ):
            return None

        try:
            statistic, pvalue = mannwhitneyu(
                group_missing,
                group_observed,
                alternative="two-sided",
            )

        except ValueError:
            return None

        return MARAssociation(
            target=target,
            predictor=predictor,
            predictor_type="numeric",
            test_name="Mann-Whitney U",
            statistic=float(
                statistic
            ),
            pvalue=float(
                pvalue
            ),
            adjusted_pvalue=None,
            significant=False,
            sample_size=len(x),
        )

    @staticmethod
    def _categorical_association(
        x: pd.Series,
        missing_indicator: pd.Series,
        target: str,
        predictor: str,
    ) -> MARAssociation | None:

        contingency = pd.crosstab(
            x,
            missing_indicator,
        )

        if (
            contingency.shape[0] < 2
            or contingency.shape[1] < 2
        ):
            return None

        try:
            statistic, pvalue, _, _ = (
                chi2_contingency(
                    contingency
                )
            )

        except ValueError:
            return None

        return MARAssociation(
            target=target,
            predictor=predictor,
            predictor_type="categorical",
            test_name="Chi-square",
            statistic=float(
                statistic
            ),
            pvalue=float(
                pvalue
            ),
            adjusted_pvalue=None,
            significant=False,
            sample_size=int(
                contingency.to_numpy().sum()
            ),
        )

    @staticmethod
    def _adjust_pvalues(
        associations: list[MARAssociation],
        alpha: float,
    ) -> None:
        """
        Correction Benjamini-Hochberg.
        """

        valid = [
            association
            for association in associations
            if association.pvalue is not None
        ]

        if not valid:
            return

        ordered = sorted(
            valid,
            key=lambda item: item.pvalue,
        )

        m = len(
            ordered
        )

        adjusted = [
            1.0
            for _ in range(m)
        ]

        running_min = 1.0

        for index in range(
            m - 1,
            -1,
            -1,
        ):

            rank = index + 1

            raw = (
                ordered[index].pvalue
                * m
                / rank
            )

            running_min = min(
                running_min,
                raw,
                1.0,
            )

            adjusted[index] = (
                running_min
            )

        for association, adjusted_pvalue in zip(
            ordered,
            adjusted,
        ):
            association.adjusted_pvalue = float(
                adjusted_pvalue
            )

            association.significant = bool(
                adjusted_pvalue <= alpha
            )
