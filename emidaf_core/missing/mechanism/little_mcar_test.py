"""
=========================================================
EMIDAF Framework v1.0
Little MCAR Test
---------------------------------------------------------
Évaluation statistique de l'hypothèse MCAR.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.stats import chi2


@dataclass(slots=True)
class LittleMCARResult:
    """
    Résultat du test de Little pour l'hypothèse MCAR.
    """

    statistic: float | None
    pvalue: float | None
    degrees_of_freedom: int | None
    is_mcar: bool | None
    executed: bool
    message: str


class LittleMCARTest:
    """
    Test de Little pour évaluer la compatibilité
    des données avec un mécanisme MCAR.

    Hypothèses :

    H0 :
        les données sont compatibles avec MCAR.

    H1 :
        les données ne sont pas compatibles avec MCAR.

    Interprétation :

    - pvalue > alpha :
        H0 n'est pas rejetée.

    - pvalue <= alpha :
        H0 est rejetée.

    Remarque :
        Ne pas rejeter H0 ne constitue pas une preuve
        que les données sont MCAR.
    """

    def run(
        self,
        dataframe: pd.DataFrame,
        alpha: float = 0.05,
    ) -> LittleMCARResult:
        """
        Exécute le test de Little sur les variables numériques.
        """

        # =====================================================
        # VALIDATION
        # =====================================================

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

        if dataframe.empty:
            return LittleMCARResult(
                statistic=None,
                pvalue=None,
                degrees_of_freedom=None,
                is_mcar=None,
                executed=False,
                message="The dataframe is empty.",
            )

        # =====================================================
        # NUMERIC VARIABLES
        # =====================================================

        numeric_df = dataframe.select_dtypes(
            include=[np.number]
        ).copy()

        if numeric_df.empty:
            return LittleMCARResult(
                statistic=None,
                pvalue=None,
                degrees_of_freedom=None,
                is_mcar=None,
                executed=False,
                message=(
                    "No numeric variables are available "
                    "for Little's MCAR test."
                ),
            )

        # Supprimer les variables entièrement vides :
        # elles ne permettent pas d'estimer une moyenne
        # ou une covariance exploitable.
        numeric_df = numeric_df.dropna(
            axis=1,
            how="all",
        )

        if numeric_df.empty:
            return LittleMCARResult(
                statistic=None,
                pvalue=None,
                degrees_of_freedom=None,
                is_mcar=None,
                executed=False,
                message=(
                    "All numeric variables are entirely missing."
                ),
            )

        if not numeric_df.isna().any().any():
            return LittleMCARResult(
                statistic=None,
                pvalue=None,
                degrees_of_freedom=None,
                is_mcar=None,
                executed=False,
                message=(
                    "No missing values detected. "
                    "The MCAR test is not required."
                ),
            )

        # =====================================================
        # GLOBAL PARAMETERS
        # =====================================================

        variable_names = list(
            numeric_df.columns
        )

        n_variables = len(
            variable_names
        )

        global_mean = numeric_df.mean()

        global_covariance = numeric_df.cov()

        if (
            global_covariance.empty
            or global_covariance.isna().all().all()
        ):
            return LittleMCARResult(
                statistic=None,
                pvalue=None,
                degrees_of_freedom=None,
                is_mcar=None,
                executed=False,
                message=(
                    "The covariance matrix could not "
                    "be estimated."
                ),
            )

        # =====================================================
        # MISSINGNESS PATTERNS
        # =====================================================

        missing_matrix = numeric_df.isna().astype(int)

        pattern_series = missing_matrix.apply(
            lambda row: tuple(row.tolist()),
            axis=1,
        )

        unique_patterns = pattern_series.unique()

        statistic = 0.0

        total_observed_variables = 0

        valid_patterns = 0

        # =====================================================
        # LITTLE STATISTIC
        # =====================================================

        for pattern in unique_patterns:

            pattern_mask = (
                pattern_series == pattern
            )

            pattern_data = numeric_df.loc[
                pattern_mask
            ]

            observed_columns = [
                column
                for column, missing_flag
                in zip(
                    variable_names,
                    pattern,
                )
                if missing_flag == 0
            ]

            if not observed_columns:
                continue

            group_size = len(
                pattern_data
            )

            if group_size == 0:
                continue

            pattern_mean = (
                pattern_data[
                    observed_columns
                ].mean()
            )

            mean_difference = (
                pattern_mean
                - global_mean[
                    observed_columns
                ]
            )

            covariance_submatrix = (
                global_covariance.loc[
                    observed_columns,
                    observed_columns,
                ]
            )

            covariance_values = (
                covariance_submatrix.to_numpy(
                    dtype=float
                )
            )

            difference_values = (
                mean_difference.to_numpy(
                    dtype=float
                )
            )

            if (
                np.isnan(covariance_values).any()
                or
                np.isnan(difference_values).any()
            ):
                continue

            try:

                inverse_covariance = (
                    np.linalg.pinv(
                        covariance_values
                    )
                )

            except np.linalg.LinAlgError:

                continue

            contribution = (
                group_size
                * difference_values.T
                @ inverse_covariance
                @ difference_values
            )

            statistic += float(
                contribution
            )

            total_observed_variables += len(
                observed_columns
            )

            valid_patterns += 1

        # =====================================================
        # DEGREES OF FREEDOM
        # =====================================================

        degrees_of_freedom = (
            total_observed_variables
            - n_variables
        )

        if (
            valid_patterns == 0
            or degrees_of_freedom <= 0
        ):
            return LittleMCARResult(
                statistic=None,
                pvalue=None,
                degrees_of_freedom=None,
                is_mcar=None,
                executed=False,
                message=(
                    "Insufficient missingness structure "
                    "to execute Little's MCAR test."
                ),
            )

        # =====================================================
        # P-VALUE
        # =====================================================

        pvalue = float(
            chi2.sf(
                statistic,
                degrees_of_freedom,
            )
        )

        is_mcar = bool(
            pvalue > alpha
        )

        # =====================================================
        # MESSAGE
        # =====================================================

        if is_mcar:

            message = (
                "The null hypothesis of Little's MCAR test "
                "is not rejected. The data are compatible "
                "with an MCAR mechanism."
            )

        else:

            message = (
                "The null hypothesis of Little's MCAR test "
                "is rejected. The data are not compatible "
                "with an MCAR mechanism."
            )

        return LittleMCARResult(
            statistic=round(
                statistic,
                6,
            ),
            pvalue=round(
                pvalue,
                6,
            ),
            degrees_of_freedom=int(
                degrees_of_freedom
            ),
            is_mcar=is_mcar,
            executed=True,
            message=message,
        )
