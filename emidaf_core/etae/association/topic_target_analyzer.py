"""
=========================================================
EMIDAF Framework v1.0
ETAE - Topic / Target Association
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import numpy as np
import pandas as pd

from scipy.stats import (
    f,
    f_oneway,
    kruskal,
    levene,
)

from ..semantics import TopicModeler


@dataclass(frozen=True)
class TopicTargetGroup:
    topic: int
    n: int
    mean: float
    median: float
    std: float | None
    minimum: float
    maximum: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StatisticalTestResult:
    """
    Résultat d'un test statistique global.
    """

    test: str
    statistic: float | None
    p_value: float | None
    significant: bool | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EffectSizeResult:
    """
    Taille d'effet globale.
    """

    measure: str
    value: float | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TopicTargetInference:
    """
    Synthèse inférentielle globale.
    """

    alpha: float

    levene: StatisticalTestResult
    anova: StatisticalTestResult
    welch_anova: StatisticalTestResult
    kruskal: StatisticalTestResult

    eta_squared: EffectSizeResult
    omega_squared: EffectSizeResult
    epsilon_squared: EffectSizeResult

    equal_variances: bool | None
    recommended_test: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "alpha": self.alpha,
            "levene": self.levene.to_dict(),
            "anova": self.anova.to_dict(),
            "welch_anova": (
                self.welch_anova.to_dict()
            ),
            "kruskal": self.kruskal.to_dict(),
            "eta_squared": (
                self.eta_squared.to_dict()
            ),
            "omega_squared": (
                self.omega_squared.to_dict()
            ),
            "epsilon_squared": (
                self.epsilon_squared.to_dict()
            ),
            "equal_variances": (
                self.equal_variances
            ),
            "recommended_test": (
                self.recommended_test
            ),
        }


@dataclass(frozen=True)
class TopicTargetResult:
    text_column: str
    target_column: str
    n_documents: int
    n_topics: int
    groups: list[TopicTargetGroup]
    inference: TopicTargetInference | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "text_column": self.text_column,
            "target_column": self.target_column,
            "n_documents": self.n_documents,
            "n_topics": self.n_topics,
            "groups": [
                group.to_dict()
                for group in self.groups
            ],
            "inference": (
                self.inference.to_dict()
                if self.inference is not None
                else None
            ),
        }


class TopicTargetAnalyzer:
    """
    Analyse l'association entre le thème dominant
    d'un document et une variable quantitative.
    """

    def __init__(self) -> None:
        self._topic_modeler = TopicModeler()

    def analyze(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        target_column: str,
        *,
        n_topics: int = 3,
        alpha: float = 0.05,
        run_inference: bool = True,
        **topic_kwargs,
    ) -> TopicTargetResult:

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe doit être un DataFrame pandas."
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

        if not 0 < alpha < 1:
            raise ValueError(
                "alpha doit être compris entre 0 et 1."
            )

        topic_result = (
            self._topic_modeler.analyze(
                dataframe=dataframe,
                text_column=text_column,
                n_topics=n_topics,
                **topic_kwargs,
            )
        )

        if topic_result.n_documents == 0:
            return TopicTargetResult(
                text_column=text_column,
                target_column=target_column,
                n_documents=0,
                n_topics=0,
                groups=[],
                inference=None,
            )

        aligned = pd.DataFrame(
            {
                "topic": (
                    topic_result.dominant_topics
                ),
                "index": (
                    topic_result.indices
                ),
            }
        )

        target_values = (
            dataframe[target_column]
            .reindex(
                topic_result.indices
            )
        )

        aligned[target_column] = list(
            target_values
        )

        aligned = aligned.dropna(
            subset=[target_column]
        )

        groups: list[
            TopicTargetGroup
        ] = []

        samples: list[np.ndarray] = []

        for topic_id, group in (
            aligned.groupby(
                "topic",
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
                TopicTargetGroup(
                    topic=int(
                        topic_id
                    ),
                    n=int(
                        len(values)
                    ),
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

            samples.append(
                values.to_numpy(
                    dtype=float
                )
            )

        inference = None

        if run_inference:
            inference = self._run_inference(
                samples=samples,
                alpha=alpha,
            )

        return TopicTargetResult(
            text_column=text_column,
            target_column=target_column,
            n_documents=int(
                len(aligned)
            ),
            n_topics=topic_result.n_topics,
            groups=groups,
            inference=inference,
        )

    @staticmethod
    def _run_inference(
        *,
        samples: list[np.ndarray],
        alpha: float,
    ) -> TopicTargetInference | None:

        valid_samples = [
            np.asarray(
                sample[
                    np.isfinite(sample)
                ],
                dtype=float,
            )
            for sample in samples
            if len(sample) > 0
        ]

        valid_samples = [
            sample
            for sample in valid_samples
            if len(sample) > 0
        ]

        if len(valid_samples) < 2:
            return None

        levene_result = (
            TopicTargetAnalyzer
            ._safe_test(
                "Levene",
                levene,
                valid_samples,
                alpha,
            )
        )

        anova_result = (
            TopicTargetAnalyzer
            ._safe_test(
                "ANOVA",
                f_oneway,
                valid_samples,
                alpha,
            )
        )

        welch_result = (
            TopicTargetAnalyzer
            ._welch_anova(
                samples=valid_samples,
                alpha=alpha,
            )
        )

        kruskal_result = (
            TopicTargetAnalyzer
            ._safe_test(
                "Kruskal-Wallis",
                kruskal,
                valid_samples,
                alpha,
            )
        )

        eta_squared = (
            TopicTargetAnalyzer
            ._eta_squared(
                valid_samples
            )
        )

        omega_squared = (
            TopicTargetAnalyzer
            ._omega_squared(
                valid_samples
            )
        )

        epsilon_squared = (
            TopicTargetAnalyzer
            ._epsilon_squared(
                samples=valid_samples,
                kruskal_result=kruskal_result,
            )
        )

        equal_variances = None

        if levene_result.p_value is not None:
            equal_variances = bool(
                levene_result.p_value
                >= alpha
            )

        if equal_variances is True:
            recommended_test = "ANOVA"

        elif equal_variances is False:
            recommended_test = (
                "Welch ANOVA"
            )

        else:
            recommended_test = None

        return TopicTargetInference(
            alpha=float(alpha),
            levene=levene_result,
            anova=anova_result,
            welch_anova=welch_result,
            kruskal=kruskal_result,
            eta_squared=eta_squared,
            omega_squared=omega_squared,
            epsilon_squared=epsilon_squared,
            equal_variances=equal_variances,
            recommended_test=recommended_test,
        )

    @staticmethod
    def _safe_test(
        name: str,
        test_function,
        samples: list[np.ndarray],
        alpha: float,
    ) -> StatisticalTestResult:

        try:
            result = test_function(
                *samples
            )

            statistic = float(
                result.statistic
            )

            p_value = float(
                result.pvalue
            )

            if not (
                np.isfinite(statistic)
                and np.isfinite(p_value)
            ):
                return StatisticalTestResult(
                    test=name,
                    statistic=None,
                    p_value=None,
                    significant=None,
                )

            return StatisticalTestResult(
                test=name,
                statistic=statistic,
                p_value=p_value,
                significant=bool(
                    p_value < alpha
                ),
            )

        except (
            ValueError,
            ZeroDivisionError,
        ):
            return StatisticalTestResult(
                test=name,
                statistic=None,
                p_value=None,
                significant=None,
            )

    @staticmethod
    def _welch_anova(
        *,
        samples: list[np.ndarray],
        alpha: float,
    ) -> StatisticalTestResult:
        """
        Welch ANOVA indépendante de la version
        de scipy.stats.f_oneway.
        """

        if len(samples) < 2:
            return StatisticalTestResult(
                test="Welch ANOVA",
                statistic=None,
                p_value=None,
                significant=None,
            )

        sizes = np.array(
            [
                len(sample)
                for sample in samples
            ],
            dtype=float,
        )

        if np.any(
            sizes < 2
        ):
            return StatisticalTestResult(
                test="Welch ANOVA",
                statistic=None,
                p_value=None,
                significant=None,
            )

        means = np.array(
            [
                np.mean(sample)
                for sample in samples
            ],
            dtype=float,
        )

        variances = np.array(
            [
                np.var(
                    sample,
                    ddof=1,
                )
                for sample in samples
            ],
            dtype=float,
        )

        if (
            np.any(
                ~np.isfinite(variances)
            )
            or np.any(
                variances <= 0
            )
        ):
            return StatisticalTestResult(
                test="Welch ANOVA",
                statistic=None,
                p_value=None,
                significant=None,
            )

        weights = (
            sizes
            / variances
        )

        weight_sum = (
            weights.sum()
        )

        weighted_mean = (
            np.sum(
                weights * means
            )
            / weight_sum
        )

        k = float(
            len(samples)
        )

        numerator = (
            np.sum(
                weights
                * (
                    means
                    - weighted_mean
                ) ** 2
            )
            / (
                k - 1.0
            )
        )

        correction_terms = (
            (
                1.0
                - (
                    weights
                    / weight_sum
                )
            ) ** 2
            / (
                sizes - 1.0
            )
        )

        correction_sum = (
            correction_terms.sum()
        )

        denominator = (
            1.0
            + (
                (
                    2.0
                    * (
                        k - 2.0
                    )
                )
                / (
                    k ** 2
                    - 1.0
                )
            )
            * correction_sum
        )

        statistic = (
            numerator
            / denominator
        )

        df1 = (
            k - 1.0
        )

        df2 = (
            (
                k ** 2
                - 1.0
            )
            / (
                3.0
                * correction_sum
            )
        )

        p_value = float(
            f.sf(
                statistic,
                df1,
                df2,
            )
        )

        if not (
            np.isfinite(statistic)
            and np.isfinite(p_value)
        ):
            return StatisticalTestResult(
                test="Welch ANOVA",
                statistic=None,
                p_value=None,
                significant=None,
            )

        return StatisticalTestResult(
            test="Welch ANOVA",
            statistic=float(
                statistic
            ),
            p_value=p_value,
            significant=bool(
                p_value < alpha
            ),
        )

    @staticmethod
    def _anova_components(
        samples: list[np.ndarray],
    ) -> tuple[
        float,
        float,
        float,
        int,
        int,
    ] | None:

        if len(samples) < 2:
            return None

        n_total = sum(
            len(sample)
            for sample in samples
        )

        k = len(samples)

        if n_total <= k:
            return None

        concatenated = np.concatenate(
            samples
        )

        grand_mean = float(
            concatenated.mean()
        )

        ss_between = sum(
            len(sample)
            * (
                float(
                    sample.mean()
                )
                - grand_mean
            ) ** 2
            for sample in samples
        )

        ss_within = sum(
            float(
                np.sum(
                    (
                        sample
                        - sample.mean()
                    ) ** 2
                )
            )
            for sample in samples
        )

        ss_total = (
            ss_between
            + ss_within
        )

        return (
            float(ss_between),
            float(ss_within),
            float(ss_total),
            int(n_total),
            int(k),
        )

    @staticmethod
    def _eta_squared(
        samples: list[np.ndarray],
    ) -> EffectSizeResult:

        components = (
            TopicTargetAnalyzer
            ._anova_components(
                samples
            )
        )

        if components is None:
            return EffectSizeResult(
                measure="eta_squared",
                value=None,
            )

        (
            ss_between,
            _,
            ss_total,
            _,
            _,
        ) = components

        if ss_total <= 0:
            value = None
        else:
            value = float(
                ss_between
                / ss_total
            )

        return EffectSizeResult(
            measure="eta_squared",
            value=value,
        )

    @staticmethod
    def _omega_squared(
        samples: list[np.ndarray],
    ) -> EffectSizeResult:

        components = (
            TopicTargetAnalyzer
            ._anova_components(
                samples
            )
        )

        if components is None:
            return EffectSizeResult(
                measure="omega_squared",
                value=None,
            )

        (
            ss_between,
            ss_within,
            ss_total,
            n_total,
            k,
        ) = components

        df_between = (
            k - 1
        )

        df_within = (
            n_total - k
        )

        if (
            df_within <= 0
            or ss_total <= 0
        ):
            value = None

        else:
            ms_within = (
                ss_within
                / df_within
            )

            numerator = (
                ss_between
                - (
                    df_between
                    * ms_within
                )
            )

            denominator = (
                ss_total
                + ms_within
            )

            if denominator <= 0:
                value = None

            else:
                value = float(
                    max(
                        0.0,
                        numerator
                        / denominator,
                    )
                )

        return EffectSizeResult(
            measure="omega_squared",
            value=value,
        )

    @staticmethod
    def _epsilon_squared(
        *,
        samples: list[np.ndarray],
        kruskal_result: StatisticalTestResult,
    ) -> EffectSizeResult:

        statistic = (
            kruskal_result.statistic
        )

        if statistic is None:
            return EffectSizeResult(
                measure="epsilon_squared",
                value=None,
            )

        n_total = sum(
            len(sample)
            for sample in samples
        )

        k = len(samples)

        denominator = (
            n_total - k
        )

        if denominator <= 0:
            value = None

        else:
            value = (
                statistic
                - k
                + 1
            ) / denominator

            value = float(
                min(
                    1.0,
                    max(
                        0.0,
                        value,
                    ),
                )
            )

        return EffectSizeResult(
            measure="epsilon_squared",
            value=value,
        )
