"""
=========================================================
EMIDAF Framework
Preprocessing - Report
=========================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .summary import preprocessing_summary


class PreprocessingReport:

    name = "Preprocessing Report"

    def __init__(
        self,
        title="Rapport de prétraitement"
    ):

        self.title = title
        self.summary_ = None
        self.fitted_ = False

    def fit(
        self,
        X,
        y=None
    ):

        self.summary_ = (
            preprocessing_summary(X)
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

        return X.copy()

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

    def get_summary(self):

        if not self.fitted_:

            raise RuntimeError(
                "Le rapport n'est pas disponible."
            )

        return self.summary_

    def to_dict(self):

        if not self.fitted_:

            raise RuntimeError(
                "Le rapport n'est pas disponible."
            )

        return self.summary_

    def print_report(self):

        if not self.fitted_:

            raise RuntimeError(
                "Le rapport n'est pas disponible."
            )

        summary = self.summary_

        print("=" * 70)
        print(self.title)
        print("=" * 70)

        print("\nDIMENSIONS")
        print(
            summary["shape"]
        )

        print("\nTYPES DE DONNÉES")
        print(
            summary["data_types"]
        )

        print("\nVARIABLES NUMÉRIQUES")
        print(
            summary["numeric"]
        )

        print("\nVARIABLES CATÉGORIELLES")
        print(
            summary["categorical"]
        )

        print("\nVALEURS MANQUANTES")
        print(
            summary["missing"]
        )

        print("\nDOUBLONS")
        print(
            summary["duplicates"]
        )

        print("\nCOLONNES CONSTANTES")
        print(
            summary["constant_columns"]
        )

        print("\nOBSERVATIONS COMPLÈTES")
        print(
            summary["complete_cases"]
        )

        return summary

    def save_csv(
        self,
        path
    ):

        if not self.fitted_:

            raise RuntimeError(
                "Le rapport n'est pas disponible."
            )

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.summary_[
            "missing"
        ].to_csv(
            path,
            index=True
        )

        return path

    def save_excel(
        self,
        path
    ):

        if not self.fitted_:

            raise RuntimeError(
                "Le rapport n'est pas disponible."
            )

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with pd.ExcelWriter(
            path,
            engine="openpyxl"
        ) as writer:

            self.summary_[
                "numeric"
            ].to_excel(
                writer,
                sheet_name="Numeriques"
            )

            self.summary_[
                "categorical"
            ].to_excel(
                writer,
                sheet_name="Categorical",
                index=False
            )

            self.summary_[
                "missing"
            ].to_excel(
                writer,
                sheet_name="Missing"
            )

            self.summary_[
                "unique"
            ].to_excel(
                writer,
                sheet_name="Unique",
                index=False
            )

            self.summary_[
                "data_types"
            ].to_excel(
                writer,
                sheet_name="Data_Types",
                index=False
            )

        return path


def generate_report(
    X,
    title="Rapport de prétraitement"
):

    report = PreprocessingReport(
        title=title
    )

    report.fit(X)

    return report


def report_to_dict(
    X
):

    return preprocessing_summary(
        X
    )


def save_missing_report(
    X,
    path
):

    summary = preprocessing_summary(
        X
    )

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    summary[
        "missing"
    ].to_csv(
        path
    )

    return path


def save_numeric_report(
    X,
    path
):

    summary = preprocessing_summary(
        X
    )

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    summary[
        "numeric"
    ].to_csv(
        path
    )

    return path


def save_categorical_report(
    X,
    path
):

    summary = preprocessing_summary(
        X
    )

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    summary[
        "categorical"
    ].to_csv(
        path,
        index=False
    )

    return path


def save_report_excel(
    X,
    path
):

    report = generate_report(
        X
    )

    return report.save_excel(
        path
    )
