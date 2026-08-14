"""
=========================================================
EMIDAF Framework
Preprocessing - Data Splitting
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.model_selection import (
    train_test_split,
    KFold,
    StratifiedKFold,
    TimeSeriesSplit
)


class DataSplitter:

    name = "Data Splitter"

    def __init__(
        self,
        test_size=0.2,
        random_state=42,
        shuffle=True,
        stratify=None
    ):

        self.test_size = test_size
        self.random_state = random_state
        self.shuffle = shuffle
        self.stratify = stratify

        self.fitted_ = False

    def fit(self, X, y=None):

        self.fitted_ = True

        return self

    def split(self, X, y=None):

        if not self.fitted_:
            self.fit(X, y)

        stratify_values = None

        if self.stratify is not None:

            if isinstance(
                self.stratify,
                str
            ):

                stratify_values = X[
                    self.stratify
                ]

            else:

                stratify_values = self.stratify

        return train_test_split(
            X,
            y,
            test_size=self.test_size,
            random_state=self.random_state,
            shuffle=self.shuffle,
            stratify=stratify_values
        )

    def fit_split(self, X, y=None):

        self.fit(X, y)

        return self.split(X, y)


class TrainTestSplitter:

    name = "Train Test Splitter"

    def __init__(
        self,
        test_size=0.2,
        random_state=42,
        shuffle=True,
        stratify=False
    ):

        self.test_size = test_size
        self.random_state = random_state
        self.shuffle = shuffle
        self.stratify = stratify

    def split(self, X, y):

        stratify_values = (
            y if self.stratify
            else None
        )

        return train_test_split(
            X,
            y,
            test_size=self.test_size,
            random_state=self.random_state,
            shuffle=self.shuffle,
            stratify=stratify_values
        )


class KFoldSplitter:

    name = "K Fold Splitter"

    def __init__(
        self,
        n_splits=5,
        shuffle=True,
        random_state=42
    ):

        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state

        self.splitter_ = KFold(
            n_splits=n_splits,
            shuffle=shuffle,
            random_state=(
                random_state
                if shuffle
                else None
            )
        )

    def split(self, X, y=None):

        return self.splitter_.split(
            X,
            y
        )

    def get_n_splits(self):

        return self.splitter_.get_n_splits()


class StratifiedKFoldSplitter:

    name = "Stratified K Fold Splitter"

    def __init__(
        self,
        n_splits=5,
        shuffle=True,
        random_state=42
    ):

        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state

        self.splitter_ = StratifiedKFold(
            n_splits=n_splits,
            shuffle=shuffle,
            random_state=(
                random_state
                if shuffle
                else None
            )
        )

    def split(self, X, y):

        return self.splitter_.split(
            X,
            y
        )

    def get_n_splits(self):

        return self.splitter_.get_n_splits()


class TimeSeriesSplitter:

    name = "Time Series Splitter"

    def __init__(
        self,
        n_splits=5,
        max_train_size=None,
        test_size=None,
        gap=0
    ):

        self.n_splits = n_splits
        self.max_train_size = max_train_size
        self.test_size = test_size
        self.gap = gap

        self.splitter_ = TimeSeriesSplit(
            n_splits=n_splits,
            max_train_size=max_train_size,
            test_size=test_size,
            gap=gap
        )

    def split(self, X, y=None):

        return self.splitter_.split(
            X,
            y
        )

    def get_n_splits(self):

        return self.splitter_.get_n_splits()


def train_test_split_data(
    X,
    y,
    test_size=0.2,
    random_state=42,
    shuffle=True,
    stratify=False
):

    stratify_values = (
        y if stratify
        else None
    )

    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        shuffle=shuffle,
        stratify=stratify_values
    )


def split_dataframe(
    df,
    target,
    test_size=0.2,
    random_state=42,
    shuffle=True,
    stratify=False
):

    X = df.drop(
        columns=[target]
    )

    y = df[target]

    return train_test_split_data(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        shuffle=shuffle,
        stratify=stratify
    )


def kfold_split(
    X,
    n_splits=5,
    shuffle=True,
    random_state=42
):

    splitter = KFoldSplitter(
        n_splits=n_splits,
        shuffle=shuffle,
        random_state=random_state
    )

    return splitter.split(X)


def stratified_kfold_split(
    X,
    y,
    n_splits=5,
    shuffle=True,
    random_state=42
):

    splitter = StratifiedKFoldSplitter(
        n_splits=n_splits,
        shuffle=shuffle,
        random_state=random_state
    )

    return splitter.split(
        X,
        y
    )


def time_series_split(
    X,
    n_splits=5,
    max_train_size=None,
    test_size=None,
    gap=0
):

    splitter = TimeSeriesSplitter(
        n_splits=n_splits,
        max_train_size=max_train_size,
        test_size=test_size,
        gap=gap
    )

    return splitter.split(X)


def split_train_validation_test(
    X,
    y,
    test_size=0.2,
    validation_size=0.2,
    random_state=42,
    stratify=True
):

    if test_size + validation_size >= 1:

        raise ValueError(
            "test_size + validation_size "
            "doit être inférieur à 1."
        )

    stratify_values = (
        y if stratify
        else None
    )

    X_temp, X_test, y_temp, y_test = (
        train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=random_state,
            stratify=stratify_values
        )
    )

    relative_validation_size = (
        validation_size
        / (1 - test_size)
    )

    stratify_temp = (
        y_temp if stratify
        else None
    )

    X_train, X_validation, y_train, y_validation = (
        train_test_split(
            X_temp,
            y_temp,
            test_size=relative_validation_size,
            random_state=random_state,
            stratify=stratify_temp
        )
    )

    return (
        X_train,
        X_validation,
        X_test,
        y_train,
        y_validation,
        y_test
    )


def chronological_split(
    df,
    date_column,
    test_size=0.2
):

    data = df.copy()

    data[date_column] = pd.to_datetime(
        data[date_column],
        errors="coerce"
    )

    data = data.sort_values(
        date_column
    ).reset_index(
        drop=True
    )

    n_test = int(
        len(data) * test_size
    )

    if n_test <= 0:

        raise ValueError(
            "test_size produit un ensemble "
            "de test vide."
        )

    train = data.iloc[
        :-n_test
    ].copy()

    test = data.iloc[
        -n_test:
    ].copy()

    return train, test


def get_split_sizes(
    X_train,
    X_test,
    X_validation=None
):

    total = (
        len(X_train)
        + len(X_test)
    )

    if X_validation is not None:

        total += len(
            X_validation
        )

    result = {
        "train_count": len(X_train),
        "test_count": len(X_test),
        "train_percentage": (
            len(X_train)
            / total
            * 100
        ),
        "test_percentage": (
            len(X_test)
            / total
            * 100
        )
    }

    if X_validation is not None:

        result[
            "validation_count"
        ] = len(X_validation)

        result[
            "validation_percentage"
        ] = (
            len(X_validation)
            / total
            * 100
        )

    return result
