"""
=========================================================
EMIDAF Framework
Data Splitting
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.model_selection import (
    train_test_split,
    KFold,
    StratifiedKFold,
    RepeatedKFold,
    RepeatedStratifiedKFold,
    TimeSeriesSplit
)

from .base import (
    BasePreprocessing,
    PreprocessingResult
)


# ==========================================================
# SPLITTING
# ==========================================================

class DataSplitter(
    BasePreprocessing
):

    """
    Complete data splitting engine.
    """

    name = "Data Splitting"

    def __init__(
        self,
        test_size=0.2,
        validation_size=None,
        random_state=42,
        stratify=False
    ):

        self.test_size = test_size
        self.validation_size = validation_size
        self.random_state = random_state
        self.stratify = stratify

        self.result = None


    # ======================================================
    # BASIC TRAIN / TEST SPLIT
    # ======================================================

    @staticmethod
    def train_test(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=False
    ):

        stratify_value = (
            y
            if stratify
            else None
        )

        return train_test_split(

            X,
            y,

            test_size=test_size,

            random_state=random_state,

            stratify=stratify_value

        )


    # ======================================================
    # TRAIN / VALIDATION / TEST
    # ======================================================

    @staticmethod
    def train_validation_test(
        X,
        y,
        test_size=0.2,
        validation_size=0.2,
        random_state=42,
        stratify=False
    ):

        if (
            test_size + validation_size
            >= 1
        ):

            raise ValueError(
                "test_size + validation_size "
                "doit être inférieur à 1."
            )

        stratify_value = (
            y
            if stratify
            else None
        )

        (
            X_temp,
            X_test,
            y_temp,
            y_test
        ) = train_test_split(

            X,
            y,

            test_size=test_size,

            random_state=random_state,

            stratify=stratify_value

        )

        relative_validation = (
            validation_size
            /
            (1 - test_size)
        )

        stratify_temp = (
            y_temp
            if stratify
            else None
        )

        (
            X_train,
            X_validation,
            y_train,
            y_validation
        ) = train_test_split(

            X_temp,
            y_temp,

            test_size=relative_validation,

            random_state=random_state,

            stratify=stratify_temp

        )

        return {

            "X_train":
                X_train,

            "X_validation":
                X_validation,

            "X_test":
                X_test,

            "y_train":
                y_train,

            "y_validation":
                y_validation,

            "y_test":
                y_test

        }


    # ======================================================
    # INDEX SPLIT
    # ======================================================

    @staticmethod
    def split_indices(
        n_samples,
        test_size=0.2,
        validation_size=None,
        random_state=42
    ):

        indices = np.arange(
            n_samples
        )

        train_indices, test_indices = (
            train_test_split(

                indices,

                test_size=test_size,

                random_state=random_state

            )
        )

        if validation_size is None:

            return {

                "train":
                    train_indices,

                "test":
                    test_indices

            }

        relative_validation = (
            validation_size
            /
            (1 - test_size)
        )

        train_indices, validation_indices = (
            train_test_split(

                train_indices,

                test_size=relative_validation,

                random_state=random_state

            )
        )

        return {

            "train":
                train_indices,

            "validation":
                validation_indices,

            "test":
                test_indices

        }


    # ======================================================
    # K-FOLD
    # ======================================================

    @staticmethod
    def kfold(
        X,
        y=None,
        n_splits=5,
        shuffle=True,
        random_state=42
    ):

        if shuffle:

            splitter = KFold(

                n_splits=n_splits,

                shuffle=True,

                random_state=random_state

            )

        else:

            splitter = KFold(

                n_splits=n_splits,

                shuffle=False

            )

        if y is None:

            iterator = splitter.split(
                X
            )

        else:

            iterator = splitter.split(
                X,
                y
            )

        folds = []

        for fold, (
            train_index,
            test_index
        ) in enumerate(
            iterator,
            start=1
        ):

            folds.append({

                "fold":
                    fold,

                "train_index":
                    train_index,

                "test_index":
                    test_index

            })

        return folds


    # ======================================================
    # STRATIFIED K-FOLD
    # ======================================================

    @staticmethod
    def stratified_kfold(
        X,
        y,
        n_splits=5,
        shuffle=True,
        random_state=42
    ):

        splitter = StratifiedKFold(

            n_splits=n_splits,

            shuffle=shuffle,

            random_state=(
                random_state
                if shuffle
                else None
            )

        )

        folds = []

        for fold, (
            train_index,
            test_index
        ) in enumerate(

            splitter.split(
                X,
                y
            ),

            start=1

        ):

            folds.append({

                "fold":
                    fold,

                "train_index":
                    train_index,

                "test_index":
                    test_index

            })

        return folds


    # ======================================================
    # REPEATED K-FOLD
    # ======================================================

    @staticmethod
    def repeated_kfold(
        X,
        y=None,
        n_splits=5,
        n_repeats=3,
        random_state=42
    ):

        splitter = RepeatedKFold(

            n_splits=n_splits,

            n_repeats=n_repeats,

            random_state=random_state

        )

        folds = []

        for fold, (
            train_index,
            test_index
        ) in enumerate(

            splitter.split(
                X
            ),

            start=1

        ):

            folds.append({

                "fold":
                    fold,

                "train_index":
                    train_index,

                "test_index":
                    test_index

            })

        return folds


    # ======================================================
    # REPEATED STRATIFIED K-FOLD
    # ======================================================

    @staticmethod
    def repeated_stratified_kfold(
        X,
        y,
        n_splits=5,
        n_repeats=3,
        random_state=42
    ):

        splitter = (
            RepeatedStratifiedKFold(

                n_splits=n_splits,

                n_repeats=n_repeats,

                random_state=random_state

            )
        )

        folds = []

        for fold, (
            train_index,
            test_index
        ) in enumerate(

            splitter.split(
                X,
                y
            ),

            start=1

        ):

            folds.append({

                "fold":
                    fold,

                "train_index":
                    train_index,

                "test_index":
                    test_index

            })

        return folds


    # ======================================================
    # TIME SERIES SPLIT
    # ======================================================

    @staticmethod
    def time_series(
        X,
        y=None,
        n_splits=5,
        test_size=None,
        gap=0
    ):

        splitter = TimeSeriesSplit(

            n_splits=n_splits,

            test_size=test_size,

            gap=gap

        )

        folds = []

        for fold, (
            train_index,
            test_index
        ) in enumerate(

            splitter.split(
                X
            ),

            start=1

        ):

            folds.append({

                "fold":
                    fold,

                "train_index":
                    train_index,

                "test_index":
                    test_index

            })

        return folds


    # ======================================================
    # TIME SERIES DATAFRAME
    # ======================================================

    @staticmethod
    def time_series_split(
        df,
        target=None,
        date_column=None,
        test_size=0.2
    ):

        data = df.copy()

        if date_column is not None:

            if date_column not in data.columns:

                raise KeyError(
                    f"Variable absente : "
                    f"{date_column}"
                )

            data = data.sort_values(
                date_column
            ).reset_index(
                drop=True
            )

        n = len(data)

        split_index = int(
            n * (1 - test_size)
        )

        train = data.iloc[
            :split_index
        ].copy()

        test = data.iloc[
            split_index:
        ].copy()

        result = {

            "train":
                train,

            "test":
                test

        }

        if target is not None:

            if target not in data.columns:

                raise KeyError(
                    f"Variable cible absente : "
                    f"{target}"
                )

            result["X_train"] = (
                train.drop(
                    columns=[target]
                )
            )

            result["y_train"] = (
                train[target]
            )

            result["X_test"] = (
                test.drop(
                    columns=[target]
                )
            )

            result["y_test"] = (
                test[target]
            )

        return result


    # ======================================================
    # STRATIFICATION CHECK
    # ======================================================

    @staticmethod
    def class_distribution(
        y
    ):

        series = pd.Series(
            y
        )

        return (
            series
            .value_counts(
                normalize=True
            )
            .sort_index()
            * 100
        )


    # ======================================================
    # COMPARE DISTRIBUTIONS
    # ======================================================

    @staticmethod
    def compare_distributions(
        y_train,
        y_test
    ):

        train = (
            DataSplitter
            .class_distribution(
                y_train
            )
            .rename(
                "train_percentage"
            )
        )

        test = (
            DataSplitter
            .class_distribution(
                y_test
            )
            .rename(
                "test_percentage"
            )
        )

        result = pd.concat(
            [
                train,
                test
            ],
            axis=1
        )

        result[
            "difference"
        ] = (
            result[
                "train_percentage"
            ]
            -
            result[
                "test_percentage"
            ]
        )

        return result


    # ======================================================
    # CHECK DATA LEAKAGE
    # ======================================================

    @staticmethod
    def check_overlap(
        train_index,
        test_index
    ):

        train_set = set(
            train_index
        )

        test_set = set(
            test_index
        )

        overlap = (
            train_set
            .intersection(
                test_set
            )
        )

        return {

            "overlap":
                len(overlap),

            "has_leakage":
                len(overlap) > 0,

            "overlapping_indices":
                list(overlap)

        }


    # ======================================================
    # SPLIT DATAFRAME
    # ======================================================

    @staticmethod
    def dataframe_split(
        df,
        target,
        test_size=0.2,
        random_state=42,
        stratify=False
    ):

        if target not in df.columns:

            raise KeyError(
                f"Variable cible absente : "
                f"{target}"
            )

        X = df.drop(
            columns=[target]
        )

        y = df[target]

        (
            X_train,
            X_test,
            y_train,
            y_test
        ) = DataSplitter.train_test(

            X,
            y,

            test_size=test_size,

            random_state=random_state,

            stratify=stratify

        )

        return {

            "X_train":
                X_train,

            "X_test":
                X_test,

            "y_train":
                y_train,

            "y_test":
                y_test

        }


    # ======================================================
    # FIT
    # ======================================================

    def fit(
        self,
        X,
        y=None
    ):

        self.result = {

            "n_samples":
                len(X),

            "test_size":
                self.test_size,

            "validation_size":
                self.validation_size,

            "random_state":
                self.random_state,

            "stratify":
                self.stratify

        }

        return self


    # ======================================================
    # TRANSFORM
    # ======================================================

    def transform(
        self,
        X,
        y
    ):

        if self.validation_size is None:

            return (
                DataSplitter
                .train_test(
                    X,
                    y,
                    test_size=
                        self.test_size,
                    random_state=
                        self.random_state,
                    stratify=
                        self.stratify
                )
            )

        return (
            DataSplitter
            .train_validation_test(
                X,
                y,
                test_size=
                    self.test_size,
                validation_size=
                    self.validation_size,
                random_state=
                    self.random_state,
                stratify=
                    self.stratify
            )
        )


    # ======================================================
    # INSPECT
    # ======================================================

    @staticmethod
    def inspect(
        X,
        y=None
    ):

        result = PreprocessingResult(

            step="Data Splitting",

            input_shape=X.shape,

            output_shape=X.shape,

            variables=list(
                X.columns
            )

        )

        result.statistics = {

            "number_of_observations":
                len(X),

            "number_of_variables":
                X.shape[1],

            "target_present":
                y is not None

        }

        return result


# ==========================================================
# PUBLIC API
# ==========================================================

class Splitter:

    train_test = (
        DataSplitter.train_test
    )

    train_validation_test = (
        DataSplitter
        .train_validation_test
    )

    split_indices = (
        DataSplitter.split_indices
    )

    kfold = (
        DataSplitter.kfold
    )

    stratified_kfold = (
        DataSplitter
        .stratified_kfold
    )

    repeated_kfold = (
        DataSplitter
        .repeated_kfold
    )

    repeated_stratified_kfold = (
        DataSplitter
        .repeated_stratified_kfold
    )

    time_series = (
        DataSplitter.time_series
    )

    time_series_split = (
        DataSplitter.time_series_split
    )

    class_distribution = (
        DataSplitter
        .class_distribution
    )

    compare_distributions = (
        DataSplitter
        .compare_distributions
    )

    check_overlap = (
        DataSplitter
        .check_overlap
    )

    dataframe_split = (
        DataSplitter
        .dataframe_split
    )

    inspect = (
        DataSplitter.inspect
    )