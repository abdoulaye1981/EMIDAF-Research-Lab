"""
=========================================================
EMIDAF Framework
EAIE - Multilevel Linear Model
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Modèle linéaire multiniveau basé sur statsmodels MixedLM.
=========================================================
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd
import statsmodels.api as sm

from statsmodels.regression.mixed_linear_model import (
    MixedLM,
)

from emidaf_core.common.results import (
    MultilevelResult,
)


class MultilevelLinearModel:
    """
    Modèle linéaire multiniveau à intercept aléatoire.

    V1 :
    - cible continue ;
    - effets fixes numériques ;
    - variable de groupe ;
    - intercept aléatoire ;
    - ICC ;
    - inférence sur les effets fixes.
    """

    name = "Multilevel Linear Model"
    task = "regression"
    library = "statsmodels"

    @classmethod
    def fit(
        cls,
        dataframe: pd.DataFrame,
        *,
        target: str,
        group: str,
        features: list[str] | None = None,
        add_constant: bool = True,
        reml: bool = False,
        method: str = "lbfgs",
        maxiter: int = 500,
        alpha: float = 0.05,
    ) -> MultilevelResult:

        start = time.perf_counter()

        # =================================================
        # Validation générale
        # =================================================

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "MultilevelLinearModel attend "
                "un pandas.DataFrame."
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

        if group not in dataframe.columns:
            raise ValueError(
                f"La variable de groupe '{group}' "
                "n'existe pas dans le dataframe."
            )

        if target == group:
            raise ValueError(
                "La variable cible et la variable "
                "de groupe doivent être différentes."
            )

        # =================================================
        # Features
        # =================================================

        if features is None:

            features = [
                column
                for column in dataframe.columns
                if column not in {
                    target,
                    group,
                }
            ]

        else:

            features = list(
                features
            )

        if not features:
            raise ValueError(
                "Au moins une variable explicative "
                "est nécessaire."
            )

        if len(features) != len(
            set(features)
        ):
            raise ValueError(
                "La liste des variables explicatives "
                "contient des doublons."
            )

        if target in features:
            raise ValueError(
                "La variable cible ne peut pas être "
                "une variable explicative."
            )

        if group in features:
            raise ValueError(
                "La variable de groupe ne doit pas être "
                "incluse dans les effets fixes."
            )

        missing_features = [
            feature
            for feature in features
            if feature not in dataframe.columns
        ]

        if missing_features:
            raise ValueError(
                "Variables explicatives absentes : "
                f"{missing_features}"
            )

        # =================================================
        # Données
        # =================================================

        required = (
            features
            + [
                target,
                group,
            ]
        )

        selected = dataframe[
            required
        ].copy()

        if selected.isna().any().any():
            raise ValueError(
                "Le modèle multiniveau ne peut pas être "
                "exécuté avec des valeurs manquantes."
            )

        non_numeric = [
            feature
            for feature in (
                features
                + [target]
            )
            if not pd.api.types.is_numeric_dtype(
                selected[feature]
            )
        ]

        if non_numeric:
            raise ValueError(
                "La cible et les effets fixes doivent "
                "être numériques. Variables non "
                f"numériques : {non_numeric}"
            )

        numeric = (
            selected[
                features
                + [target]
            ]
            .astype(float)
        )

        if not np.isfinite(
            numeric.to_numpy()
        ).all():
            raise ValueError(
                "Le modèle multiniveau exige des "
                "valeurs numériques finies."
            )

        groups = (
            selected[
                group
            ]
        )

        n_groups = int(
            groups.nunique()
        )

        if n_groups < 2:
            raise ValueError(
                "Un modèle multiniveau nécessite "
                "au moins deux groupes."
            )

        group_counts = (
            groups
            .value_counts()
        )

        if (
            group_counts < 2
        ).any():
            raise ValueError(
                "Chaque groupe doit contenir "
                "au moins deux observations."
            )

        # =================================================
        # Paramètres
        # =================================================

        try:
            alpha = float(
                alpha
            )
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

        try:
            maxiter = int(
                maxiter
            )
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValueError(
                "maxiter doit être un entier."
            ) from exc

        if maxiter < 1:
            raise ValueError(
                "maxiter doit être au moins égal à 1."
            )

        # =================================================
        # X / y
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

        n_observations = len(
            dataframe
        )

        if n_observations <= (
            X_model.shape[1]
            + n_groups
        ):
            raise ValueError(
                "Le nombre d'observations est "
                "insuffisant pour estimer le "
                "modèle multiniveau."
            )

        # =================================================
        # MixedLM
        # =================================================

        model = MixedLM(
            endog=y,
            exog=X_model,
            groups=groups,
        )

        fitted = model.fit(
            reml=reml,
            method=method,
            maxiter=maxiter,
            disp=False,
        )

        predictions = (
            fitted.fittedvalues
        )

        residuals = (
            y.to_numpy()
            - np.asarray(
                predictions
            )
        )

        # =================================================
        # Effets fixes
        # =================================================

        fixed_params = (
            fitted.fe_params
        )

        fixed_effects = {
            str(name): float(value)
            for name, value
            in fixed_params.items()
        }

        intercept = (
            fixed_effects.get(
                "const"
            )
        )

        coefficients = {
            name: value
            for name, value
            in fixed_effects.items()
            if name != "const"
        }

        # =================================================
        # Inférence
        # =================================================

        fixed_names = list(
            fixed_params.index
        )

        standard_errors = {
            str(name): float(
                fitted.bse[
                    name
                ]
            )
            for name in fixed_names
        }

        z_statistics = {
            str(name): float(
                fitted.tvalues[
                    name
                ]
            )
            for name in fixed_names
        }

        p_values = {
            str(name): float(
                fitted.pvalues[
                    name
                ]
            )
            for name in fixed_names
        }

        confidence_frame = (
            fitted.conf_int(
                alpha=alpha
            )
        )

        confidence_intervals = {
            str(name): [
                float(
                    confidence_frame
                    .loc[
                        name
                    ]
                    .iloc[0]
                ),
                float(
                    confidence_frame
                    .loc[
                        name
                    ]
                    .iloc[1]
                ),
            ]
            for name in fixed_names
        }

        # =================================================
        # Variance aléatoire et ICC
        # =================================================

        covariance_random = (
            np.asarray(
                fitted.cov_re
            )
        )

        if (
            covariance_random.size
            > 0
        ):
            group_variance = float(
                covariance_random[
                    0,
                    0,
                ]
            )
        else:
            group_variance = None

        residual_variance = float(
            fitted.scale
        )

        if (
            group_variance is not None
            and (
                group_variance
                + residual_variance
            ) > 0
        ):

            icc = float(
                group_variance
                / (
                    group_variance
                    + residual_variance
                )
            )

        else:

            icc = None

        # =================================================
        # Résultat
        # =================================================

        result = MultilevelResult(
            name=cls.name,

            description=(
                "Modèle linéaire multiniveau "
                "à intercept aléatoire."
            ),

            model_name=cls.name,
            algorithm="MixedLM",
            model_type="mixed_effects_regressor",
            task="regression",
            library=cls.library,
            fitted=True,

            train_size=n_observations,
            test_size=0,

            features=list(
                features
            ),

            target=target,

            estimator=fitted,

            parameters={
                "group": group,
                "add_constant": add_constant,
                "reml": reml,
                "method": method,
                "maxiter": maxiter,
                "alpha": alpha,
            },

            coefficients=coefficients,
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

            fixed_effects=(
                fixed_effects
            ),

            standard_errors=(
                standard_errors
            ),

            z_statistics=(
                z_statistics
            ),

            p_values=(
                p_values
            ),

            confidence_intervals=(
                confidence_intervals
            ),

            group_column=group,

            n_groups=n_groups,

            group_variance=(
                group_variance
            ),

            residual_variance=(
                residual_variance
            ),

            icc=icc,

            log_likelihood=float(
                fitted.llf
            ),

            aic=(
                float(
                    fitted.aic
                )
                if np.isfinite(
                    fitted.aic
                )
                else None
            ),

            bic=(
                float(
                    fitted.bic
                )
                if np.isfinite(
                    fitted.bic
                )
                else None
            ),

            converged=bool(
                fitted.converged
            ),

            execution_time=float(
                time.perf_counter()
                - start
            ),

            metadata={
                "multilevel": True,
                "mixed_effects": True,
                "random_intercept": True,
                "n_groups": n_groups,
            },
        )

        return result

    run = fit
