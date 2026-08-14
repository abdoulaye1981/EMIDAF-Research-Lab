"""
=========================================================
EMIDAF Framework
Preprocessing Pipeline
=========================================================
"""

from __future__ import annotations

import pandas as pd
from copy import deepcopy

from .base import (
    BasePreprocessing,
    PreprocessingResult
)


class PreprocessingPipeline(BasePreprocessing):

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


    def step_names(self):

        return [
            name
            for name, transformer
            in self.steps
        ]


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
                    f"\n[EMIDAF] Étape : {name}"
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

        self.feature_names_out_ = (
            list(data.columns)
            if isinstance(
                data,
                pd.DataFrame
            )
            else None
        )

        return self


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
                    f"\n[EMIDAF] Transformation : {name}"
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


    def summary(self):

        rows = []

        for name, transformer in (
            self.fitted_steps
        ):

            rows.append({

                "step":
                    name,

                "transformer":
                    transformer.__class__.__name__

            })

        return pd.DataFrame(
            rows
        )


    def clone(self):

        return deepcopy(
            self
        )


    def reset(self):

        self.fitted_steps = []

        self.results = []

        self.feature_names_in_ = None

        self.feature_names_out_ = None

        return self


class ConditionalPipeline(
    PreprocessingPipeline
):

    name = "Conditional Preprocessing Pipeline"

    def __init__(
        self,
        steps=None,
        conditions=None,
        verbose=True
    ):

        super().__init__(
            steps=steps,
            verbose=verbose
        )

        self.conditions = (
            {}
            if conditions is None
            else conditions
        )


    def add_conditional_step(
        self,
        name,
        transformer,
        condition
    ):

        self.steps.append(
            (
                name,
                transformer
            )
        )

        self.conditions[
            name
        ] = condition

        return self


    def fit(
        self,
        X,
        y=None
    ):

        data = X.copy()

        self.fitted_steps = []

        self.results = []

        for name, transformer in self.steps:

            condition = self.conditions.get(
                name,
                lambda X, y: True
            )

            if not condition(
                data,
                y
            ):

                if self.verbose:

                    print(
                        f"\n[EMIDAF] Étape ignorée : {name}"
                    )

                continue

            if self.verbose:

                print(
                    f"\n[EMIDAF] Étape : {name}"
                )

            if hasattr(
                transformer,
                "fit"
            ):

                try:

                    transformer.fit(
                        data,
                        y
                    )

                except TypeError:

                    transformer.fit(
                        data
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

        return self


def make_pipeline(
    *steps,
    verbose=True
):

    pipeline = PreprocessingPipeline(
        verbose=verbose
    )

    for step in steps:

        if not isinstance(
            step,
            tuple
        ):

            raise TypeError(
                "Chaque étape doit être "
                "un tuple (nom, transformateur)."
            )

        if len(step) != 2:

            raise ValueError(
                "Chaque étape doit contenir "
                "(nom, transformateur)."
            )

        pipeline.add_step(
            step[0],
            step[1]
        )

    return pipeline
