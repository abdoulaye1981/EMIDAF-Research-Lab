"""
=========================================================
EMIDAF Framework
Preprocessing - Class Balancing
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class RandomUnderSampler:

    name = "Random Under Sampler"

    def __init__(
        self,
        random_state=42
    ):

        self.random_state = random_state
        self.fitted_ = False
        self.classes_ = None

    def fit(
        self,
        X,
        y
    ):

        y_series = pd.Series(
            y
        ).reset_index(
            drop=True
        )

        self.classes_ = (
            y_series
            .value_counts()
            .index
            .tolist()
        )

        self.fitted_ = True

        return self

    def fit_resample(
        self,
        X,
        y
    ):

        self.fit(
            X,
            y
        )

        X_data = X.reset_index(
            drop=True
        )

        y_data = pd.Series(
            y
        ).reset_index(
            drop=True
        )

        counts = y_data.value_counts()

        target_size = counts.min()

        rng = np.random.default_rng(
            self.random_state
        )

        indices = []

        for class_value in counts.index:

            class_indices = np.where(
                y_data.values
                == class_value
            )[0]

            selected = rng.choice(
                class_indices,
                size=target_size,
                replace=False
            )

            indices.extend(
                selected.tolist()
            )

        rng.shuffle(
            indices
        )

        X_resampled = (
            X_data.iloc[indices]
            .reset_index(drop=True)
        )

        y_resampled = (
            y_data.iloc[indices]
            .reset_index(drop=True)
        )

        return (
            X_resampled,
            y_resampled
        )


class RandomOverSampler:

    name = "Random Over Sampler"

    def __init__(
        self,
        random_state=42
    ):

        self.random_state = random_state
        self.fitted_ = False
        self.classes_ = None

    def fit(
        self,
        X,
        y
    ):

        y_series = pd.Series(
            y
        ).reset_index(
            drop=True
        )

        self.classes_ = (
            y_series
            .value_counts()
            .index
            .tolist()
        )

        self.fitted_ = True

        return self

    def fit_resample(
        self,
        X,
        y
    ):

        self.fit(
            X,
            y
        )

        X_data = X.reset_index(
            drop=True
        )

        y_data = pd.Series(
            y
        ).reset_index(
            drop=True
        )

        counts = y_data.value_counts()

        target_size = counts.max()

        rng = np.random.default_rng(
            self.random_state
        )

        indices = []

        for class_value in counts.index:

            class_indices = np.where(
                y_data.values
                == class_value
            )[0]

            additional = target_size - len(
                class_indices
            )

            if additional > 0:

                extra = rng.choice(
                    class_indices,
                    size=additional,
                    replace=True
                )

                selected = np.concatenate(
                    [
                        class_indices,
                        extra
                    ]
                )

            else:

                selected = class_indices

            indices.extend(
                selected.tolist()
            )

        rng.shuffle(
            indices
        )

        X_resampled = (
            X_data.iloc[indices]
            .reset_index(drop=True)
        )

        y_resampled = (
            y_data.iloc[indices]
            .reset_index(drop=True)
        )

        return (
            X_resampled,
            y_resampled
        )


class RandomSampler:

    name = "Random Sampler"

    def __init__(
        self,
        strategy="undersample",
        random_state=42
    ):

        self.strategy = strategy
        self.random_state = random_state

        if strategy == "undersample":

            self.sampler = (
                RandomUnderSampler(
                    random_state=random_state
                )
            )

        elif strategy == "oversample":

            self.sampler = (
                RandomOverSampler(
                    random_state=random_state
                )
            )

        else:

            raise ValueError(
                "strategy doit être "
                "'undersample' ou "
                "'oversample'."
            )

    def fit_resample(
        self,
        X,
        y
    ):

        return self.sampler.fit_resample(
            X,
            y
        )


def class_distribution(
    y
):

    values = pd.Series(
        y
    )

    counts = (
        values
        .value_counts()
        .sort_index()
    )

    frequencies = (
        values
        .value_counts(
            normalize=True
        )
        .sort_index()
    )

    result = pd.DataFrame({
        "effectif": counts,
        "frequence": frequencies,
        "pourcentage":
            frequencies * 100
    })

    return result


def imbalance_ratio(
    y
):

    counts = (
        pd.Series(y)
        .value_counts()
    )

    if len(counts) < 2:

        return 1.0

    return (
        counts.max()
        / counts.min()
    )


def is_imbalanced(
    y,
    threshold=1.5
):

    return (
        imbalance_ratio(y)
        >= threshold
    )


def undersample(
    X,
    y,
    random_state=42
):

    sampler = RandomUnderSampler(
        random_state=random_state
    )

    return sampler.fit_resample(
        X,
        y
    )


def oversample(
    X,
    y,
    random_state=42
):

    sampler = RandomOverSampler(
        random_state=random_state
    )

    return sampler.fit_resample(
        X,
        y
    )


def balance_classes(
    X,
    y,
    strategy="undersample",
    random_state=42
):

    sampler = RandomSampler(
        strategy=strategy,
        random_state=random_state
    )

    return sampler.fit_resample(
        X,
        y
    )


def balancing_report(
    y
):

    distribution = class_distribution(
        y
    )

    return {
        "distribution":
            distribution,

        "imbalance_ratio":
            imbalance_ratio(y),

        "imbalanced":
            is_imbalanced(y)
    }
