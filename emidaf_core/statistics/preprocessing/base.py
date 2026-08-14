"""
=========================================================
EMIDAF Framework
Preprocessing Base Classes
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class PreprocessingResult:

    def __init__(
        self,
        data,
        target=None,
        metadata=None
    ):

        self.data = data

        self.target = target

        self.metadata = (
            {}
            if metadata is None
            else metadata
        )

    def __repr__(self):

        return (
            "PreprocessingResult("
            f"data_shape={self.data.shape}, "
            f"target={'yes' if self.target is not None else 'no'}"
            ")"
        )


class BasePreprocessing(
    ABC
):

    name = "Base Preprocessing"

    def __init__(
        self,
        verbose=True
    ):

        self.verbose = verbose

        self.is_fitted_ = False

        self.feature_names_in_ = None

        self.feature_names_out_ = None

    @abstractmethod
    def fit(
        self,
        X,
        y=None
    ):

        raise NotImplementedError

    @abstractmethod
    def transform(
        self,
        X,
        y=None
    ):

        raise NotImplementedError

    def fit_transform(
        self,
        X,
        y=None
    ):

        self.fit(
            X,
            y
        )

        return self.transform(
            X,
            y
        )

    def _validate_input(
        self,
        X
    ):

        if not isinstance(
            X,
            pd.DataFrame
        ):

            raise TypeError(
                "X doit être un "
                "pandas.DataFrame."
            )

        if X.empty:

            raise ValueError(
                "Le DataFrame X est vide."
            )

        return True

    def _set_feature_names_in(
        self,
        X
    ):

        if isinstance(
            X,
            pd.DataFrame
        ):

            self.feature_names_in_ = (
                list(X.columns)
            )

    def _set_feature_names_out(
        self,
        X
    ):

        if isinstance(
            X,
            pd.DataFrame
        ):

            self.feature_names_out_ = (
                list(X.columns)
            )

    def _mark_fitted(
        self
    ):

        self.is_fitted_ = True

        return self

    def check_is_fitted(
        self
    ):

        if not self.is_fitted_:

            raise RuntimeError(
                "Le preprocessing n'a pas "
                "encore été ajusté. "
                "Appelez fit() avant transform()."
            )

        return True

    def summary(self):

        return pd.DataFrame({

            "attribute": [
                "name",
                "is_fitted",
                "n_features_in",
                "n_features_out"
            ],

            "value": [

                self.name,

                self.is_fitted_,

                (
                    len(
                        self.feature_names_in_
                    )
                    if self.feature_names_in_
                    is not None
                    else None
                ),

                (
                    len(
                        self.feature_names_out_
                    )
                    if self.feature_names_out_
                    is not None
                    else None
                )

            ]

        })

    def get_feature_names_out(
        self
    ):

        if (
            self.feature_names_out_
            is None
        ):

            if (
                self.feature_names_in_
                is not None
            ):

                return list(
                    self.feature_names_in_
                )

            return None

        return list(
            self.feature_names_out_
        )

    def reset(
        self
    ):

        self.is_fitted_ = False

        self.feature_names_in_ = None

        self.feature_names_out_ = None

        return self
