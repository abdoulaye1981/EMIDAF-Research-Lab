"""
=========================================================
EMIDAF Framework
Preprocessing Pipeline
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import pandas as pd
import numpy as np

from copy import deepcopy

from .base import (
    BasePreprocessing,
    PreprocessingResult
)


# ==========================================================
# PREPROCESSING PIPELINE
# ==========================================================

class PreprocessingPipeline(
    BasePreprocessing
):

    """
    Sequential preprocessing pipeline.

    Each step must provide:
        fit()
        transform()

    or simply be callable.
    """

    name = "Preprocessing Pipeline"

    def __init__(
        self,
        steps=None,
        verbose=True
    ):

        self.steps = (
            [] if steps is None
            else list(steps)
        )

        self.verbose = verbose

        self.fitted_steps = []

        self.results = []

        self.feature_names_in_ = None

        self.feature_names_out_ = None


    # ======================================================
    # ADD STEP
    # ======================================================

    def add_step(
        self,
        name,
        transformer
    ):

        self.steps.append(
            (
                name,
                transformer
            )
        )

        return self


    # ======================================================
    # REMOVE STEP
    # ======================================================

    def remove_step(
        self,
        name
    ):

        self.steps = [

            (
                step_name,
                transformer
            )

            for step_name, transformer
            in self.steps

            if step_name != name

        ]

        return self


    # ======================================================
    # STEP NAMES
    # ======================================================

    def step_names(self):

        return [
            name
            for name, transformer
            in self.steps
        ]


    # ======================================================
    # FIT
    # ======================================================

    def fit(
        self,
        X,
        y=None
    ):

        data = X.copy()

        self.feature_names_in_ = (
            list(X.columns)
            if isinstance(
                X,
                pd.DataFrame
            )
            else None
        )

        self.fitted_steps = []

        self.results = []

        for name, transformer in self.steps:

            if self.verbose:

                print(
                    f"\n[EMIDAF] "
                    f"Étape : {name}"
                )

            current = data.copy()

            if hasattr(
                transformer,
                "fit"
            ):

                try:

                    transformer.fit(
                        current,
                        y
                    )

                except TypeError:

                    transformer.fit(
                        current
                    )

            self.fitted_steps.append(
                (
                    name,
                    transformer
                )
            )

            if hasattr(
                transformer,
                "transform"
            ):

                try:

                    transformed = (
                        transformer.transform(
                            current,
                            y
                        )
                    )

                except TypeError:

                    transformed = (
                        transformer.transform(
                            current
                        )
                    )

                data, y = (
                    self._extract_output(
                        transformed,
                        y
                    )
                )

            else:

                data = current

            result = (
                self._create_result(
                    name,
                    current,
                    data
                )
            )

            self.results.append(
                result
            )

        self.feature_names_out_ = (
            list(data.columns)
            if isinstance(
                data,
                pd.DataFrame
            )
            else None
        )

        return self


    # ======================================================
    # TRANSFORM
    # ======================================================

    def transform(
        self,
        X,
        y=None
    ):

        data = X.copy()

        for name, transformer in (
            self.fitted_steps
        ):

            if self.verbose:

                print(
                    f"\n[EMIDAF] "
                    f"Transformation : {name}"
                )

            if not hasattr(
                transformer,
                "transform"
            ):

                continue

            try:

                transformed = (
                    transformer.transform(
                        data,
                        y
                    )
                )

            except TypeError:

                transformed = (
                    transformer.transform(
                        data
                    )
                )

            data, y = (
                self._extract_output(
                    transformed,
                    y
                )
            )

        if y is None:

            return data

        return data, y


    # ======================================================
    # FIT TRANSFORM
    # ======================================================

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


    # ======================================================
    # EXTRACT OUTPUT
    # ======================================================

    @staticmethod
    def _extract_output(
        transformed,
        y
    ):

        if isinstance(
            transformed,
            tuple
        ):

            if len(transformed) == 2:

                return (
                    transformed[0],
                    transformed[1]
                )

        if isinstance(
            transformed,
            dict
        ):

            if "X" in transformed:

                return (
                    transformed["X"],
                    transformed.get(
                        "y",
                        y
                    )
                )

            if "data" in transformed:

                return (
                    transformed["data"],
                    transformed.get(
                        "target",
                        y
                    )
                )

        return (
            transformed,
            y
        )


    # ======================================================
    # CREATE RESULT
    # ======================================================

    @staticmethod
    def _create_result(
        name,
        before,
        after
    ):

        before_shape = (
            before.shape
            if hasattr(
                before,
                "shape"
            )
            else None
        )

        after_shape = (
            after.shape
            if hasattr(
                after,
                "shape"
            )
            else None
        )

        variables_before = (
            list(before.columns)
            if isinstance(
                before,
                pd.DataFrame
            )
            else []
        )

        variables_after = (
            list(after.columns)
            if isinstance(
                after,
                pd.DataFrame
            )
            else []
        )

        result = PreprocessingResult(

            step=name,

            input_shape=before_shape,

            output_shape=after_shape,

            variables=variables_after

        )

        result.statistics = {

            "variables_before":
                variables_before,

            "variables_after":
                variables_after,

            "rows_before":
                before_shape[0]
                if before_shape
                else None,

            "rows_after":
                after_shape[0]
                if after_shape
                else None,

            "columns_before":
                before_shape[1]
                if before_shape
                else None,

            "columns_after":
                after_shape[1]
                if after_shape
                else None

        }

        return result


    # ======================================================
    # RESULTS
    # ======================================================

    def get_results(self):

        return self.results


    # ======================================================
    # SUMMARY
    # ======================================================

    def summary(self):

        rows = []

        for result in self.results:

            statistics = (
                result.statistics
            )

            rows.append({

                "step":
                    result.step,

                "rows_before":
                    statistics[
                        "rows_before"
                    ],

                "rows_after":
                    statistics[
                        "rows_after"
                    ],

                "columns_before":
                    statistics[
                        "columns_before"
                    ],

                "columns_after":
                    statistics[
                        "columns_after"
                    ]

            })

        return pd.DataFrame(
            rows
        )


    # ======================================================
    # CLONE
    # ======================================================

    def clone(self):

        return deepcopy(
            self
        )


    # ======================================================
    # RESET
    # ======================================================

    def reset(self):

        self.fitted_steps = []

        self.results = []

        self.feature_names_in_ = None

        self.feature_names_out_ = None

        return self


    # ======================================================
    # INSPECT
    # ======================================================

    @staticmethod
    def inspect(
        X
    ):

        result = PreprocessingResult(

            step="Preprocessing Pipeline",

            input_shape=X.shape,

            output_shape=X.shape,

            variables=list(
                X.columns
            )

        )

        result.statistics = {

            "number_of_rows":
                X.shape[0],

            "number_of_columns":
                X.shape[1],

            "variables":
                list(X.columns)

        }

        return result