"""
=========================================================
EMIDAF Framework
Missing Data Hypothesis Tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Tests statistiques des mécanismes de données manquantes.

Contient

- Little MCAR Test
- MCAR Chi-Square
- MAR Detection
- Missing Pattern Analysis

=========================================================
"""

from __future__ import annotations

from abc import ABC

import numpy as np
import pandas as pd

from scipy.stats import chi2_contingency
from scipy.stats import mannwhitneyu

from ...common.results import HypothesisResult
from ..base.hypothesis_test import HypothesisTest


# ==========================================================
# BASE
# ==========================================================

class MissingDataTest(HypothesisTest, ABC):

    category = "Missing Data"


# ==========================================================
# LITTLE MCAR
# ==========================================================

class LittleMCAR(MissingDataTest):
    """
    Implémentation simplifiée.

    Une implémentation complète sera développée
    dans EMIDAF Advanced.
    """

    name = "Little MCAR"

    @classmethod
    def compute(
        cls,
        dataframe: pd.DataFrame,
        alpha: float = 0.05,
    ) -> HypothesisResult:

        total_missing = int(

            dataframe.isna().sum().sum()

        )

        total_cells = (

            dataframe.shape[0]

            * dataframe.shape[1]

        )

        missing_rate = (

            total_missing

            / total_cells

            if total_cells

            else 0

        )

        return HypothesisResult(

            test_name="Little MCAR",

            statistic=np.nan,

            p_value=np.nan,

            alpha=alpha,

            sample_size=len(dataframe),

            interpretation=(

                "Little MCAR test "

                "requires the dedicated "

                "implementation."

            ),

            diagnostics={

                "missing_values":

                    total_missing,

                "missing_rate":

                    missing_rate

            }

        )


# ==========================================================
# MCAR CHI SQUARE
# ==========================================================

class MCARChiSquare(MissingDataTest):

    name = "MCAR Chi Square"

    @classmethod
    def compute(

        cls,

        dataframe: pd.DataFrame,

        alpha=0.05,

    ):

        results = {}

        columns = dataframe.columns

        for target in columns:

            missing = dataframe[target].isna()

            if (

                missing.sum() == 0

            ):

                continue

            for predictor in columns:

                if predictor == target:

                    continue

                if (

                    dataframe[predictor]

                    .dtype

                    == "object"

                ):

                    table = pd.crosstab(

                        missing,

                        dataframe[predictor]

                    )

                    statistic, pvalue, _, _ = (

                        chi2_contingency(

                            table

                        )

                    )

                    results[

                        predictor

                    ] = {

                        "chi2":

                            float(statistic),

                        "p_value":

                            float(pvalue),

                        "dependent":

                            pvalue < alpha

                    }

        return HypothesisResult(

            test_name="MCAR Chi Square",

            sample_size=len(dataframe),

            interpretation=(

                "Chi-Square "

                "analysis completed."

            ),

            diagnostics=results

        )


# ==========================================================
# MAR DETECTION
# ==========================================================

class MARDetection(MissingDataTest):

    """
    Détection simplifiée MAR.

    Compare les distributions entre
    groupes manquants et non manquants.
    """

    name = "MAR Detection"

    @classmethod
    def compute(

        cls,

        dataframe: pd.DataFrame,

        alpha=0.05,

    ):

        diagnostics = {}

        columns = dataframe.columns

        numeric = dataframe.select_dtypes(

            include="number"

        ).columns

        for target in columns:

            missing = dataframe[target].isna()

            if missing.sum() == 0:

                continue

            for variable in numeric:

                if variable == target:

                    continue

                group_missing = dataframe.loc[

                    missing,

                    variable

                ].dropna()

                group_present = dataframe.loc[

                    ~missing,

                    variable

                ].dropna()

                if (

                    len(group_missing) < 2

                    or

                    len(group_present) < 2

                ):

                    continue

                statistic, pvalue = (

                    mannwhitneyu(

                        group_missing,

                        group_present,

                        alternative="two-sided"

                    )

                )

                diagnostics[

                    f"{target}->{variable}"

                ] = {

                    "statistic":

                        float(statistic),

                    "p_value":

                        float(pvalue),

                    "mar":

                        pvalue < alpha

                }

        return HypothesisResult(

            test_name="MAR Detection",

            sample_size=len(dataframe),

            interpretation=(

                "MAR diagnostic completed."

            ),

            diagnostics=diagnostics

        )


# ==========================================================
# MISSING PATTERN
# ==========================================================

class MissingPatternAnalysis(MissingDataTest):

    name = "Missing Pattern"

    @classmethod
    def compute(

        cls,

        dataframe: pd.DataFrame,

    ):

        pattern = (

            dataframe

            .isna()

            .astype(int)

        )

        frequencies = (

            pattern

            .value_counts()

            .to_dict()

        )

        return HypothesisResult(

            test_name="Missing Pattern",

            sample_size=len(dataframe),

            interpretation=(

                "Missing-value "

                "patterns extracted."

            ),

            diagnostics={

                "patterns":

                    {

                        str(k): v

                        for k, v

                        in frequencies.items()

                    }

            }

        )


# ==========================================================
# SERVICE
# ==========================================================

class MissingDataTests:

    @staticmethod
    def compute(

        dataframe,

        alpha=0.05,

    ):

        return {

            "little_mcar":

                LittleMCAR.compute(

                    dataframe,

                    alpha

                ),

            "mcar_chi_square":

                MCARChiSquare.compute(

                    dataframe,

                    alpha

                ),

            "mar_detection":

                MARDetection.compute(

                    dataframe,

                    alpha

                ),

            "missing_pattern":

                MissingPatternAnalysis.compute(

                    dataframe

                )

        }