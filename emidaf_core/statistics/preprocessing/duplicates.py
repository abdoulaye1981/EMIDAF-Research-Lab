"""
=========================================================
EMIDAF Framework
Preprocessing - Duplicates
=========================================================
"""

from __future__ import annotations

import pandas as pd


class DuplicateHandler:

    name = "Duplicate Handler"

    def __init__(
        self,
        keep="first"
    ):

        self.keep = keep
        self.duplicates_ = None
        self.fitted_ = False

    def fit(
        self,
        X,
        y=None
    ):

        self.duplicates_ = (
            X.duplicated(
                keep=self.keep
            )
        )

        self.fitted_ = True

        return self

    def transform(
        self,
        X
    ):

        if not self.fitted_:

            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        return X.loc[
            ~X.duplicated(
                keep=self.keep
            )
        ].copy()

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
            X
        )

    def count(
        self,
        X
    ):

        return int(
            X.duplicated(
                keep=self.keep
            ).sum()
        )

    def percentage(
        self,
        X
    ):

        if len(X) == 0:

            return 0.0

        return (
            self.count(X)
            / len(X)
            * 100
        )

    def report(
        self,
        X
    ):

        count = self.count(X)

        percentage = self.percentage(
            X
        )

        return {

            "duplicate_count":
                count,

            "duplicate_percentage":
                percentage,

            "remaining_rows":
                len(X) - count

        }


class DuplicateRemover(
    DuplicateHandler
):

    pass


class DuplicateInspector:

    name = "Duplicate Inspector"

    def __init__(
        self,
        subset=None
    ):

        self.subset = subset

    def mask(
        self,
        X
    ):

        return X.duplicated(
            subset=self.subset,
            keep=False
        )

    def count(
        self,
        X
    ):

        return int(
            self.mask(X).sum()
        )

    def groups(
        self,
        X
    ):

        return X.loc[
            self.mask(X)
        ].copy()

    def report(
        self,
        X
    ):

        mask = self.mask(X)

        return pd.DataFrame({

            "duplicate_rows":
                [int(mask.sum())],

            "percentage":
                [
                    (
                        mask.sum()
                        / len(X)
                        * 100
                    )
                    if len(X) > 0
                    else 0
                ]

        })


def duplicate_mask(
    X,
    subset=None,
    keep="first"
):

    return X.duplicated(
        subset=subset,
        keep=keep
    )


def duplicate_count(
    X,
    subset=None,
    keep="first"
):

    return int(
        X.duplicated(
            subset=subset,
            keep=keep
        ).sum()
    )


def duplicate_percentage(
    X,
    subset=None,
    keep="first"
):

    if len(X) == 0:

        return 0.0

    return (
        duplicate_count(
            X,
            subset=subset,
            keep=keep
        )
        / len(X)
        * 100
    )


def remove_duplicates(
    X,
    subset=None,
    keep="first"
):

    return (
        X.drop_duplicates(
            subset=subset,
            keep=keep
        )
        .reset_index(
            drop=True
        )
    )


def duplicate_summary(
    X,
    subset=None
):

    count_first = duplicate_count(
        X,
        subset=subset,
        keep="first"
    )

    count_all = duplicate_count(
        X,
        subset=subset,
        keep=False
    )

    return {

        "rows":
            len(X),

        "duplicate_rows_after_first":
            count_first,

        "duplicate_rows_total":
            count_all,

        "percentage_after_first":
            (
                count_first
                / len(X)
                * 100
            )
            if len(X) > 0
            else 0,

        "percentage_total":
            (
                count_all
                / len(X)
                * 100
            )
            if len(X) > 0
            else 0

    }


def find_duplicate_groups(
    X,
    subset=None
):

    mask = X.duplicated(
        subset=subset,
        keep=False
    )

    return (
        X.loc[mask]
        .copy()
    )


def remove_duplicate_columns(
    X
):

    return X.loc[
        :,
        ~X.T.duplicated()
    ].copy()
