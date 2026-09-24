"""
=========================================================
EMIDAF Framework
EAIE - Ordinary Least Squares
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Régression linéaire par moindres carrés ordinaires
avec inférence statistique.
=========================================================
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd
import statsmodels.api as sm

from emidaf_core.common.results import (
    OLSResult,
)


class OLSRegression:
    """
    Régression linéaire par moindres carrés ordinaires.

    Ce composant est destiné à l'inférence statistique.
    Il complète, sans remplacer, LinearRegression de
    scikit-learn déjà disponible dans EAIE.
    """

    name = "OLS Regression"
    task = "regression"
    library = "statsmodels"

    @classmethod
    def fit(
        cls,
        dataframe: pd.DataFrame,
        *,
        target: str,
        features: list[str] | None = None,
        add_constant: bool = True,
        alpha: float = 0.05,
    ) -> OLSResult:

        start = time.perf_counter()

        # =================================================
        # Validation du dataframe
        # =================================================

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "OLSRegression attend un pandas.DataFrame."
            )

        if dataframe.empty:
            raise ValueError(
                "Le dataframe est vide."
            )

        if target not in dataframe.columns:
            raise ValueError(
                f"La variable cible '{target}' "
                "n'existe pas dans le dataframe."
            )

        # =================================================
        # Variables explicatives
        # =================================================

        if features is None:

            features = [
                column
                for column in dataframe.columns
                if column != target
            ]

        else:
            features = list(features)

        if not features:
            raise ValueError(
                "Au moins une variable explicative "
                "est nécessaire."
            )

        if len(features) != len(set(features)):
            raise ValueError(
                "La liste des variables explicatives "
                "contient des doublons."
            )

        missing_columns = [
            column
            for column in features
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                "Variables explicatives absentes : "
                f"{missing_columns}"
            )

        if target in features:
            raise ValueError(
                "La variable cible ne peut pas être "
                "utilisée comme variable explicative."
            )

        # =================================================
        # Sélection des données
        # =================================================

        selected = dataframe[
            features + [target]
        ].copy()

        if selected.isna().any().any():
            raise ValueError(
                "OLSRegression ne peut pas être exécutée "
                "avec des valeurs manquantes."
            )

        # =================================================
        # Types numériques
        # =================================================

        non_numeric = [
            column
            for column in selected.columns
            if not pd.api.types.is_numeric_dtype(
                selected[column]
            )
        ]

        if non_numeric:
            raise ValueError(
                "Toutes les variables OLS doivent être "
                "numériques. Variables non numériques : "
                f"{non_numeric}"
            )

        # =================================================
        # Valeurs finies
        # =================================================

        numeric_values = (
            selected
            .astype(float)
            .to_numpy()
        )

        if not np.isfinite(
            numeric_values
        ).all():
            raise ValueError(
                "OLSRegression exige des valeurs "
                "numériques finies."
            )

        # =================================================
        # Alpha
        # =================================================

        try:
            alpha = float(alpha)

        except (
            TypeError,
            ValueError,
        ) as exc:

            raise ValueError(
                "alpha doit être numérique."
            ) from exc

        if not 0 < alpha < 1:
            raise ValueError(
                "alpha doit être strictement compris "
                "entre 0 et 1."
            )

        # =================================================
        # X et y
        # =================================================

        X = (
            selected[
                features
            ]
            .astype(float)
        )

        y = (
            selected[
                target
            ]
            .astype(float)
        )

        if add_constant:

            X_model = sm.add_constant(
                X,
                has_constant="add",
            )

        else:

            X_model = X.copy()

        # =================================================
        # Taille de l'échantillon
        # =================================================

        n_observations = len(
            X_model
        )

        n_parameters = (
            X_model.shape[1]
        )

        if n_observations <= n_parameters:
            raise ValueError(
                "Le nombre d'observations doit être "
                "supérieur au nombre de paramètres "
                "du modèle OLS."
            )

        # =================================================
        # Ajustement OLS
        # =================================================

        model = sm.OLS(
            y,
            X_model,
        )

        fitted_model = model.fit()

        predictions = (
            fitted_model.predict(
                X_model
            )
        )

        residuals = (
            y.to_numpy()
            - np.asarray(
                predictions
            )
        )

        # =================================================
        # Coefficients
        # =================================================

        params = (
            fitted_model.params
        )

        coefficients = {
            str(name): float(value)
            for name, value
            in params.items()
            if name != "const"
        }

        intercept = (
            float(
                params["const"]
            )
            if "const" in params.index
            else None
        )

        # =================================================
        # Inférence
        # =================================================

        standard_errors = {
            str(name): float(value)
            for name, value
            in fitted_model.bse.items()
        }

        t_statistics = {
            str(name): float(value)
            for name, value
            in fitted_model.tvalues.items()
        }

        p_values = {
            str(name): float(value)
            for name, value
            in fitted_model.pvalues.items()
        }

        confidence_frame = (
            fitted_model.conf_int(
                alpha=alpha
            )
        )

        confidence_intervals = {
            str(name): [
                float(row.iloc[0]),
                float(row.iloc[1]),
            ]
            for name, row
            in confidence_frame.iterrows()
        }

        # =================================================
        # Résultat EMIDAF
        # =================================================

        result = OLSResult(
            name=cls.name,
            description=(
                "Régression linéaire par moindres "
                "carrés ordinaires."
            ),

            model_name=cls.name,
            algorithm="OLS",
            model_type="statistical_regressor",
            task="regression",
            library=cls.library,
            fitted=True,

            train_size=n_observations,
            test_size=0,

            features=list(
                features
            ),
            target=target,

            estimator=fitted_model,

            parameters={
                "add_constant": (
                    add_constant
                ),
                "alpha": alpha,
            },

            coefficients=(
                coefficients
            ),

            intercept=intercept,

            predictions=(
                np.asarray(
                    predictions
                ).tolist()
            ),

            residuals=(
                np.asarray(
                    residuals
                ).tolist()
            ),

            r2=float(
                fitted_model.rsquared
            ),

            adjusted_r2=float(
                fitted_model.rsquared_adj
            ),

            aic=float(
                fitted_model.aic
            ),

            bic=float(
                fitted_model.bic
            ),

            log_likelihood=float(
                fitted_model.llf
            ),

            f_statistic=(
                float(
                    fitted_model.fvalue
                )
                if fitted_model.fvalue
                is not None
                else None
            ),

            f_pvalue=(
                float(
                    fitted_model.f_pvalue
                )
                if fitted_model.f_pvalue
                is not None
                else None
            ),

            standard_errors=(
                standard_errors
            ),

            t_statistics=(
                t_statistics
            ),

            p_values=(
                p_values
            ),

            confidence_intervals=(
                confidence_intervals
            ),

            n_observations=int(
                fitted_model.nobs
            ),

            degrees_freedom_model=float(
                fitted_model.df_model
            ),

            degrees_freedom_residual=float(
                fitted_model.df_resid
            ),

            condition_number=float(
                fitted_model.condition_number
            ),

            score=float(
                fitted_model.rsquared
            ),

            execution_time=float(
                time.perf_counter()
                - start
            ),

            metadata={
                "inference": True,
                "method": (
                    "Ordinary Least Squares"
                ),
                "alpha": alpha,
                "constant": add_constant,
            },
        )

        return result

    run = fit
