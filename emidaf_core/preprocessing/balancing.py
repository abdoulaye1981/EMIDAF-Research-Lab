"""
=========================================================
EMIDAF Framework
Class Balancing
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from collections import Counter

from sklearn.utils.class_weight import (
    compute_class_weight
)

from .base import (
    BasePreprocessing,
    PreprocessingResult
)
# ==========================================================
# BALANCING
# ==========================================================

class Balancing(
    BasePreprocessing
):

    """
    Complete class balancing engine.
    """

    name = "Class Balancing"

    def __init__(
        self,
        method=None
    ):

        self.method = method
        self.classes_ = None
        self.class_weights_ = None
        self.result = None

    # ==========================================================
# CLASS DISTRIBUTION
# ==========================================================

    @staticmethod
    def class_distribution(
        y,
        normalize=False
    ):

        series = pd.Series(
            y,
            name="target"
        )

        counts = (
            series
            .value_counts(
                dropna=False
            )
        )

        if normalize:

            proportions = (
                series
                .value_counts(
                    normalize=True,
                    dropna=False
                )
                * 100
            )

            result = pd.DataFrame({

                "count": counts,

                "percentage":
                    proportions

            })

        else:

            result = pd.DataFrame({

                "count": counts

            })

        result.index.name = "class"

        return result
    # ==========================================================
# IMBALANCE DIAGNOSTIC
# ==========================================================

    @staticmethod
    def imbalance_ratio(
        y
    ):

        distribution = (
            Balancing
            .class_distribution(
                y
            )
        )

        counts = (
            distribution["count"]
        )

        maximum = counts.max()
        minimum = counts.min()

        if minimum == 0:

            ratio = np.inf

        else:

            ratio = (
                maximum / minimum
            )

        return {

            "majority_class":
                counts.idxmax(),

            "minority_class":
                counts.idxmin(),

            "majority_count":
                maximum,

            "minority_count":
                minimum,

            "imbalance_ratio":
                ratio

        }
    # ==========================================================
# IS IMBALANCED
# ==========================================================

    @staticmethod
    def is_imbalanced(
        y,
        threshold=1.5
    ):

        diagnostic = (
            Balancing
            .imbalance_ratio(
                y
            )
        )

        return (
            diagnostic[
                "imbalance_ratio"
            ] >= threshold
        )
    # ==========================================================
# CLASS WEIGHTS
# ==========================================================

    @staticmethod
    def class_weights(
        y,
        strategy="balanced"
    ):

        y_array = np.asarray(
            y
        )

        classes = np.unique(
            y_array
        )

        if strategy == "balanced":

            weights = compute_class_weight(

                class_weight="balanced",

                classes=classes,

                y=y_array

            )

        elif strategy == "balanced_subsample":

            weights = compute_class_weight(

                class_weight="balanced",

                classes=classes,

                y=y_array

            )

        else:

            raise ValueError(
                "strategy doit être "
                "'balanced' ou "
                "'balanced_subsample'."
            )

        result = pd.DataFrame({

            "class":
                classes,

            "weight":
                weights

        })

        return result
    # ==========================================================
# CLASS WEIGHT DICTIONARY
# ==========================================================

    @staticmethod
    def class_weight_dict(
        y
    ):

        result = (
            Balancing
            .class_weights(
                y
            )
        )

        return dict(
            zip(
                result["class"],
                result["weight"]
            )
        )
    # ==========================================================
# RANDOM OVERSAMPLING
# ==========================================================

    @staticmethod
    def random_oversampling(
        X,
        y,
        random_state=42
    ):

        if len(X) != len(y):

            raise ValueError(
                "X et y doivent avoir "
                "le même nombre de lignes."
            )

        X = X.copy()

        y = pd.Series(
            y,
            index=X.index,
            name="target"
        )

        rng = np.random.default_rng(
            random_state
        )

        class_counts = (
            y.value_counts()
        )

        maximum = class_counts.max()

        X_parts = []
        y_parts = []

        for class_value, count in (
            class_counts.items()
        ):

            class_indices = (
                y[
                    y == class_value
                ].index
            )

            additional = (
                maximum - count
            )

            if additional > 0:

                sampled_indices = (
                    rng.choice(
                        class_indices,
                        size=additional,
                        replace=True
                    )
                )

                selected_indices = list(
                    class_indices
                ) + list(
                    sampled_indices
                )

            else:

                selected_indices = list(
                    class_indices
                )

            X_parts.append(
                X.loc[
                    selected_indices
                ]
            )

            y_parts.append(
                y.loc[
                    selected_indices
                ]
            )

        X_balanced = pd.concat(
            X_parts,
            axis=0
        )

        y_balanced = pd.concat(
            y_parts,
            axis=0
        )

        shuffled = (
            rng.permutation(
                len(X_balanced)
            )
        )

        X_balanced = (
            X_balanced
            .iloc[shuffled]
            .reset_index(drop=True)
        )

        y_balanced = (
            y_balanced
            .iloc[shuffled]
            .reset_index(drop=True)
        )

        return (
            X_balanced,
            y_balanced
        )
    # ==========================================================
# RANDOM UNDERSAMPLING
# ==========================================================

    @staticmethod
    def random_undersampling(
        X,
        y,
        random_state=42
    ):

        if len(X) != len(y):

            raise ValueError(
                "X et y doivent avoir "
                "le même nombre de lignes."
            )

        X = X.copy()

        y = pd.Series(
            y,
            index=X.index,
            name="target"
        )

        rng = np.random.default_rng(
            random_state
        )

        class_counts = (
            y.value_counts()
        )

        minimum = class_counts.min()

        selected_indices = []

        for class_value in class_counts.index:

            class_indices = np.asarray(
                y[
                    y == class_value
                ].index
            )

            selected = rng.choice(

                class_indices,

                size=minimum,

                replace=False

            )

            selected_indices.extend(
                selected
            )

        selected_indices = np.asarray(
            selected_indices
        )

        selected_indices = (
            rng.permutation(
                selected_indices
            )
        )

        X_balanced = (
            X.loc[
                selected_indices
            ]
            .reset_index(drop=True)
        )

        y_balanced = (
            y.loc[
                selected_indices
            ]
            .reset_index(drop=True)
        )

        return (
            X_balanced,
            y_balanced
        )
    # ==========================================================
# TARGETED OVERSAMPLING
# ==========================================================

    @staticmethod
    def oversample_classes(
        X,
        y,
        target_size=None,
        random_state=42
    ):

        X = X.copy()

        y = pd.Series(
            y,
            index=X.index,
            name="target"
        )

        rng = np.random.default_rng(
            random_state
        )

        counts = y.value_counts()

        if target_size is None:

            target_size = counts.max()

        X_parts = []
        y_parts = []

        for class_value in counts.index:

            indices = np.asarray(
                y[
                    y == class_value
                ].index
            )

            current_size = len(
                indices
            )

            if current_size < target_size:

                additional = (
                    target_size
                    - current_size
                )

                sampled = rng.choice(

                    indices,

                    size=additional,

                    replace=True

                )

                indices = np.concatenate(
                    [
                        indices,
                        sampled
                    ]
                )

            elif current_size > target_size:

                indices = rng.choice(

                    indices,

                    size=target_size,

                    replace=False

                )

            X_parts.append(
                X.loc[indices]
            )

            y_parts.append(
                y.loc[indices]
            )

        X_result = pd.concat(
            X_parts
        )

        y_result = pd.concat(
            y_parts
        )

        permutation = (
            rng.permutation(
                len(X_result)
            )
        )

        X_result = (
            X_result
            .iloc[permutation]
            .reset_index(drop=True)
        )

        y_result = (
            y_result
            .iloc[permutation]
            .reset_index(drop=True)
        )

        return (
            X_result,
            y_result
        )
    # ==========================================================
# TARGETED UNDERSAMPLING
# ==========================================================

    @staticmethod
    def undersample_classes(
        X,
        y,
        target_size=None,
        random_state=42
    ):

        X = X.copy()

        y = pd.Series(
            y,
            index=X.index,
            name="target"
        )

        rng = np.random.default_rng(
            random_state
        )

        counts = y.value_counts()

        if target_size is None:

            target_size = counts.min()

        X_parts = []
        y_parts = []

        for class_value in counts.index:

            indices = np.asarray(
                y[
                    y == class_value
                ].index
            )

            target = min(
                target_size,
                len(indices)
            )

            selected = rng.choice(

                indices,

                size=target,

                replace=False

            )

            X_parts.append(
                X.loc[selected]
            )

            y_parts.append(
                y.loc[selected]
            )

        X_result = pd.concat(
            X_parts
        )

        y_result = pd.concat(
            y_parts
        )

        permutation = (
            rng.permutation(
                len(X_result)
            )
        )

        X_result = (
            X_result
            .iloc[permutation]
            .reset_index(drop=True)
        )

        y_result = (
            y_result
            .iloc[permutation]
            .reset_index(drop=True)
        )

        return (
            X_result,
            y_result
        )
    # ==========================================================
# AUTOMATIC BALANCING
# ==========================================================

    @staticmethod
    def balance(
        X,
        y,
        method="oversampling",
        random_state=42
    ):

        if method == "oversampling":

            return (
                Balancing
                .random_oversampling(
                    X,
                    y,
                    random_state=
                        random_state
                )
            )

        if method == "undersampling":

            return (
                Balancing
                .random_undersampling(
                    X,
                    y,
                    random_state=
                        random_state
                )
            )

        raise ValueError(
            "method doit être "
            "'oversampling' ou "
            "'undersampling'."
        )
    # ==========================================================
# BEFORE / AFTER
# ==========================================================

    @staticmethod
    def compare(
        y_before,
        y_after
    ):

        before = (
            Balancing
            .class_distribution(
                y_before,
                normalize=True
            )
            .rename(
                columns={
                    "count":
                        "count_before",
                    "percentage":
                        "percentage_before"
                }
            )
        )

        after = (
            Balancing
            .class_distribution(
                y_after,
                normalize=True
            )
            .rename(
                columns={
                    "count":
                        "count_after",
                    "percentage":
                        "percentage_after"
                }
            )
        )

        result = before.join(
            after,
            how="outer"
        )

        return result
    # ==========================================================
# FIT
# ==========================================================

    def fit(
        self,
        X,
        y
    ):

        self.classes_ = np.unique(
            y
        )

        self.class_weights_ = (
            Balancing
            .class_weight_dict(
                y
            )
        )

        self.result = (
            Balancing
            .class_distribution(
                y,
                normalize=True
            )
        )

        return self
    # ==========================================================
# TRANSFORM
# ==========================================================

    def transform(
        self,
        X,
        y
    ):

        if self.method is None:

            raise ValueError(
                "Aucune méthode de "
                "balancement définie."
            )

        return (
            Balancing
            .balance(
                X,
                y,
                method=self.method
            )
        )
    # ==========================================================
# INSPECT
# ==========================================================

    @staticmethod
    def inspect(
        y
    ):

        distribution = (
            Balancing
            .class_distribution(
                y,
                normalize=True
            )
        )

        diagnostic = (
            Balancing
            .imbalance_ratio(
                y
            )
        )

        result = PreprocessingResult(

            step="Class Balancing",

            input_shape=(
                len(y),
                1
            ),

            output_shape=(
                len(y),
                1
            ),

            variables=[
                "target"
            ]

        )

        result.statistics = {

            "distribution":
                distribution,

            "imbalance_ratio":
                diagnostic[
                    "imbalance_ratio"
                ],

            "majority_class":
                diagnostic[
                    "majority_class"
                ],

            "minority_class":
                diagnostic[
                    "minority_class"
                ]

        }

        return result
# ==========================================================
# PUBLIC API
# ==========================================================

class Balancer:

    class_distribution = (
        Balancing.class_distribution
    )

    imbalance_ratio = (
        Balancing.imbalance_ratio
    )

    is_imbalanced = (
        Balancing.is_imbalanced
    )

    class_weights = (
        Balancing.class_weights
    )

    class_weight_dict = (
        Balancing.class_weight_dict
    )

    random_oversampling = (
        Balancing.random_oversampling
    )

    random_undersampling = (
        Balancing.random_undersampling
    )

    oversample_classes = (
        Balancing.oversample_classes
    )

    undersample_classes = (
        Balancing.undersample_classes
    )

    balance = (
        Balancing.balance
    )

    compare = (
        Balancing.compare
    )

    inspect = (
        Balancing.inspect
    )