"""
EMIDAF Framework
EAIE - Data Preparation
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)


@dataclass(slots=True)
class PreparedData:
    X: pd.DataFrame
    y: pd.Series
    numeric_features: list[str]
    categorical_features: list[str]


class DataPreparation:

    @staticmethod
    def prepare(
        dataframe: pd.DataFrame,
        target: str,
        features: list[str] | None = None,
        numeric_like_threshold: float = 0.95,
    ) -> PreparedData:

        if target not in dataframe.columns:
            raise ValueError(
                f"Cible introuvable : {target}"
            )

        df = dataframe.copy()

        # Une ligne sans cible ne peut servir
        # à l'apprentissage supervisé.
        df = df.loc[
            df[target].notna()
        ].copy()

        if df.empty:
            raise ValueError(
                "Aucune ligne ne possède une cible valide."
            )

        if features is None:
            selected = [
                column
                for column in df.columns
                if column != target
            ]
        else:
            selected = [
                column
                for column in features
                if column != target
            ]

            missing = [
                column
                for column in selected
                if column not in df.columns
            ]

            if missing:
                raise ValueError(
                    "Variables introuvables : "
                    + ", ".join(missing)
                )

        if not selected:
            raise ValueError(
                "Aucune variable explicative disponible."
            )

        X = df[selected].copy()
        y = df[target].copy()

        numeric_features = []
        categorical_features = []

        for column in X.columns:

            series = X[column]

            if pd.api.types.is_numeric_dtype(series):
                numeric_features.append(column)
                continue

            if (
                pd.api.types.is_object_dtype(series)
                or pd.api.types.is_string_dtype(series)
            ):

                non_missing = series.dropna()

                if not non_missing.empty:

                    converted = pd.to_numeric(
                        non_missing,
                        errors="coerce",
                    )

                    rate = converted.notna().mean()

                    if rate >= numeric_like_threshold:

                        X[column] = pd.to_numeric(
                            series,
                            errors="coerce",
                        )

                        numeric_features.append(column)
                        continue

            categorical_features.append(column)

        return PreparedData(
            X=X,
            y=y,
            numeric_features=numeric_features,
            categorical_features=categorical_features,
        )

    @staticmethod
    def build_preprocessor(
        numeric_features: list[str],
        categorical_features: list[str],
        scale_numeric: bool = True,
    ) -> ColumnTransformer:

        transformers = []

        if numeric_features:

            numeric_steps = [
                (
                    "imputer",
                    SimpleImputer(
                        strategy="median"
                    ),
                ),
            ]

            if scale_numeric:
                numeric_steps.append(
                    (
                        "scaler",
                        StandardScaler(),
                    )
                )

            numeric_pipeline = Pipeline(
                numeric_steps
            )

            transformers.append(
                (
                    "numeric",
                    numeric_pipeline,
                    numeric_features,
                )
            )

        if categorical_features:

            categorical_pipeline = Pipeline(
                [
                    (
                        "imputer",
                        SimpleImputer(
                            strategy="most_frequent"
                        ),
                    ),
                    (
                        "encoder",
                        OneHotEncoder(
                            handle_unknown="ignore",
                        ),
                    ),
                ]
            )

            transformers.append(
                (
                    "categorical",
                    categorical_pipeline,
                    categorical_features,
                )
            )

        if not transformers:
            raise ValueError(
                "Aucune variable exploitable."
            )

        return ColumnTransformer(
            transformers=transformers,
            remainder="drop",
        )


def prepare_data(
    dataframe,
    target,
    features=None,
):
    return DataPreparation.prepare(
        dataframe,
        target,
        features=features,
    )
