"""
=========================================================
EMIDAF Framework
Preprocessing Report
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import numpy as np


# ==========================================================
# PREPROCESSING REPORT
# ==========================================================

class PreprocessingReport:

    """
    Reporting engine for preprocessing analysis.
    """

    name = "Preprocessing Report"

    # ======================================================
    # REPORT HEADER
    # ======================================================

    @staticmethod
    def header(
        title="Preprocessing Report",
        dataset_name=None
    ):

        return {

            "title":
                title,

            "dataset":
                dataset_name,

            "generated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

        }


    # ======================================================
    # DATASET INFORMATION
    # ======================================================

    @staticmethod
    def dataset_info(
        df,
        dataset_name=None
    ):

        numeric_columns = (
            df.select_dtypes(
                include=np.number
            ).columns
        )

        categorical_columns = (
            df.select_dtypes(
                include=[
                    "object",
                    "category",
                    "bool"
                ]
            ).columns
        )

        return {

            "dataset":
                dataset_name,

            "rows":
                df.shape[0],

            "columns":
                df.shape[1],

            "numeric_variables":
                len(numeric_columns),

            "categorical_variables":
                len(categorical_columns),

            "missing_values":
                int(
                    df.isna()
                    .sum()
                    .sum()
                ),

            "duplicate_rows":
                int(
                    df.duplicated()
                    .sum()
                )

        }


    # ======================================================
    # MISSING VALUES
    # ======================================================

    @staticmethod
    def missing_report(
        df
    ):

        result = pd.DataFrame({

            "variable":
                df.columns,

            "missing_count":
                df.isna().sum().values,

            "missing_percentage":
                (
                    df.isna()
                    .mean()
                    .values
                    * 100
                )

        })

        result["status"] = np.where(

            result["missing_count"] == 0,

            "Complete",

            np.where(

                result[
                    "missing_percentage"
                ] < 5,

                "Low",

                np.where(

                    result[
                        "missing_percentage"
                    ] < 20,

                    "Moderate",

                    "High"

                )

            )

        )

        return result.sort_values(

            "missing_percentage",

            ascending=False

        ).reset_index(
            drop=True
        )


    # ======================================================
    # DUPLICATE REPORT
    # ======================================================

    @staticmethod
    def duplicate_report(
        df
    ):

        count = int(
            df.duplicated().sum()
        )

        percentage = (
            count
            / len(df)
            * 100
        )

        return {

            "count":
                count,

            "percentage":
                percentage,

            "status":
                (
                    "No duplicates"
                    if count == 0
                    else
                    "Duplicates detected"
                )

        }


    # ======================================================
    # NUMERIC REPORT
    # ======================================================

    @staticmethod
    def numeric_report(
        df
    ):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        if numeric.empty:

            return pd.DataFrame()

        result = pd.DataFrame({

            "variable":
                numeric.columns,

            "count":
                numeric.count().values,

            "missing":
                numeric.isna()
                .sum()
                .values,

            "mean":
                numeric.mean()
                .values,

            "std":
                numeric.std()
                .values,

            "min":
                numeric.min()
                .values,

            "Q1":
                numeric.quantile(
                    0.25
                ).values,

            "median":
                numeric.median()
                .values,

            "Q3":
                numeric.quantile(
                    0.75
                ).values,

            "max":
                numeric.max()
                .values,

            "skewness":
                numeric.skew()
                .values,

            "kurtosis":
                numeric.kurtosis()
                .values

        })

        result[
            "CV_percentage"
        ] = (

            result["std"]

            /

            result["mean"].abs()

            * 100

        )

        return result


    # ======================================================
    # CATEGORICAL REPORT
    # ======================================================

    @staticmethod
    def categorical_report(
        df
    ):

        categorical = (
            df.select_dtypes(
                include=[
                    "object",
                    "category",
                    "bool"
                ]
            )
        )

        rows = []

        for column in categorical.columns:

            series = categorical[column]

            counts = (
                series
                .value_counts(
                    dropna=False
                )
            )

            if len(counts) == 0:

                mode = None

                mode_count = 0

            else:

                mode = counts.index[0]

                mode_count = int(
                    counts.iloc[0]
                )

            rows.append({

                "variable":
                    column,

                "unique":
                    int(
                        series.nunique(
                            dropna=True
                        )
                    ),

                "missing":
                    int(
                        series.isna()
                        .sum()
                    ),

                "mode":
                    mode,

                "mode_count":
                    mode_count,

                "mode_percentage":
                    (
                        mode_count
                        / len(series)
                        * 100
                    )

            })

        return pd.DataFrame(
            rows
        )


    # ======================================================
    # OUTLIER REPORT
    # ======================================================

    @staticmethod
    def outlier_report(
        df,
        multiplier=1.5
    ):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        rows = []

        for column in numeric.columns:

            values = (
                numeric[column]
                .dropna()
            )

            if values.empty:

                continue

            q1 = values.quantile(
                0.25
            )

            q3 = values.quantile(
                0.75
            )

            iqr = q3 - q1

            lower = (
                q1
                - multiplier * iqr
            )

            upper = (
                q3
                + multiplier * iqr
            )

            mask = (
                (values < lower)
                |
                (values > upper)
            )

            count = int(
                mask.sum()
            )

            rows.append({

                "variable":
                    column,

                "Q1":
                    q1,

                "Q3":
                    q3,

                "IQR":
                    iqr,

                "lower_bound":
                    lower,

                "upper_bound":
                    upper,

                "outlier_count":
                    count,

                "outlier_percentage":
                    (
                        count
                        / len(values)
                        * 100
                    )

            })

        if not rows:

            return pd.DataFrame()

        return (
            pd.DataFrame(rows)
            .sort_values(
                "outlier_percentage",
                ascending=False
            )
            .reset_index(
                drop=True
            )
        )


    # ======================================================
    # CORRELATION REPORT
    # ======================================================

    @staticmethod
    def correlation_report(
        df,
        threshold=0.8,
        method="pearson"
    ):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        if numeric.shape[1] < 2:

            return pd.DataFrame()

        matrix = numeric.corr(
            method=method
        )

        rows = []

        columns = matrix.columns

        for i in range(
            len(columns)
        ):

            for j in range(
                i + 1,
                len(columns)
            ):

                correlation = (
                    matrix.iloc[
                        i,
                        j
                    ]
                )

                if abs(
                    correlation
                ) >= threshold:

                    rows.append({

                        "variable_1":
                            columns[i],

                        "variable_2":
                            columns[j],

                        "correlation":
                            correlation,

                        "absolute_correlation":
                            abs(
                                correlation
                            )

                    })

        if not rows:

            return pd.DataFrame()

        return (
            pd.DataFrame(rows)
            .sort_values(
                "absolute_correlation",
                ascending=False
            )
            .reset_index(
                drop=True
            )
        )


    # ======================================================
    # TARGET REPORT
    # ======================================================

    @staticmethod
    def target_report(
        y
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

        percentages = (
            series
            .value_counts(
                normalize=True,
                dropna=False
            )
            * 100
        )

        result = pd.DataFrame({

            "class":
                counts.index,

            "count":
                counts.values,

            "percentage":
                percentages.values

        })

        return result


    # ======================================================
    # IMBALANCE REPORT
    # ======================================================

    @staticmethod
    def imbalance_report(
        y
    ):

        series = pd.Series(
            y
        )

        counts = (
            series
            .value_counts()
        )

        if counts.empty:

            return {}

        maximum = counts.max()

        minimum = counts.min()

        ratio = (
            np.inf
            if minimum == 0
            else
            maximum / minimum
        )

        return {

            "majority_class":
                counts.idxmax(),

            "minority_class":
                counts.idxmin(),

            "majority_count":
                int(maximum),

            "minority_count":
                int(minimum),

            "imbalance_ratio":
                ratio

        }


    # ======================================================
    # PREPROCESSING STEPS
    # ======================================================

    @staticmethod
    def steps_report(
        pipeline
    ):

        if not hasattr(
            pipeline,
            "summary"
        ):

            raise TypeError(
                "L'objet fourni ne possède "
                "pas de méthode summary()."
            )

        return pipeline.summary()


    # ======================================================
    # COMPLETE REPORT
    # ======================================================

    @staticmethod
    def generate(
        df,
        target=None,
        dataset_name=None,
        pipeline=None
    ):

        report = {

            "header":
                PreprocessingReport
                .header(
                    dataset_name=
                        dataset_name
                ),

            "dataset":
                PreprocessingReport
                .dataset_info(
                    df,
                    dataset_name=
                        dataset_name
                ),

            "missing":
                PreprocessingReport
                .missing_report(
                    df
                ),

            "duplicates":
                PreprocessingReport
                .duplicate_report(
                    df
                ),

            "numeric":
                PreprocessingReport
                .numeric_report(
                    df
                ),

            "categorical":
                PreprocessingReport
                .categorical_report(
                    df
                ),

            "outliers":
                PreprocessingReport
                .outlier_report(
                    df
                ),

            "correlations":
                PreprocessingReport
                .correlation_report(
                    df
                )

        }

        if target is not None:

            if target in df.columns:

                report["target"] = (
                    PreprocessingReport
                    .target_report(
                        df[target]
                    )
                )

                report["imbalance"] = (
                    PreprocessingReport
                    .imbalance_report(
                        df[target]
                    )
                )

        if pipeline is not None:

            report["pipeline"] = (
                PreprocessingReport
                .steps_report(
                    pipeline
                )
            )

        return report


    # ======================================================
    # TEXT REPORT
    # ======================================================

    @staticmethod
    def to_text(
        report
    ):

        lines = []

        header = report.get(
            "header",
            {}
        )

        lines.append(
            "=" * 70
        )

        lines.append(
            header.get(
                "title",
                "Preprocessing Report"
            )
        )

        lines.append(
            "=" * 70
        )

        if header.get(
            "dataset"
        ):

            lines.append(
                f"Dataset : "
                f"{header['dataset']}"
            )

        if header.get(
            "generated_at"
        ):

            lines.append(
                f"Généré le : "
                f"{header['generated_at']}"
            )

        lines.append("")

        dataset = report.get(
            "dataset",
            {}
        )

        lines.append(
            "DATASET"
        )

        lines.append(
            "-" * 70
        )

        for key, value in dataset.items():

            lines.append(
                f"{key} : {value}"
            )

        lines.append("")

        missing = report.get(
            "missing"
        )

        if isinstance(
            missing,
            pd.DataFrame
        ):

            lines.append(
                "VALEURS MANQUANTES"
            )

            lines.append(
                "-" * 70
            )

            lines.append(
                missing.to_string(
                    index=False
                )
            )

            lines.append("")

        duplicates = report.get(
            "duplicates",
            {}
        )

        lines.append(
            "DOUBLONS"
        )

        lines.append(
            "-" * 70
        )

        for key, value in duplicates.items():

            lines.append(
                f"{key} : {value}"
            )

        lines.append("")

        numeric = report.get(
            "numeric"
        )

        if isinstance(
            numeric,
            pd.DataFrame
        ):

            lines.append(
                "VARIABLES NUMERIQUES"
            )

            lines.append(
                "-" * 70
            )

            lines.append(
                numeric.to_string(
                    index=False
                )
            )

            lines.append("")

        categorical = report.get(
            "categorical"
        )

        if isinstance(
            categorical,
            pd.DataFrame
        ):

            lines.append(
                "VARIABLES CATEGORIELLES"
            )

            lines.append(
                "-" * 70
            )

            lines.append(
                categorical.to_string(
                    index=False
                )
            )

            lines.append("")

        outliers = report.get(
            "outliers"
        )

        if isinstance(
            outliers,
            pd.DataFrame
        ):

            lines.append(
                "VALEURS ABERRANTES"
            )

            lines.append(
                "-" * 70
            )

            lines.append(
                outliers.to_string(
                    index=False
                )
            )

            lines.append("")

        correlations = report.get(
            "correlations"
        )

        if isinstance(
            correlations,
            pd.DataFrame
        ):

            lines.append(
                "CORRELATIONS FORTES"
            )

            lines.append(
                "-" * 70
            )

            if correlations.empty:

                lines.append(
                    "Aucune corrélation "
                    "supérieure au seuil."
                )

            else:

                lines.append(
                    correlations.to_string(
                        index=False
                    )
                )

            lines.append("")

        target = report.get(
            "target"
        )

        if isinstance(
            target,
            pd.DataFrame
        ):

            lines.append(
                "VARIABLE CIBLE"
            )

            lines.append(
                "-" * 70
            )

            lines.append(
                target.to_string(
                    index=False
                )
            )

            lines.append("")

        imbalance = report.get(
            "imbalance"
        )

        if isinstance(
            imbalance,
            dict
        ) and imbalance:

            lines.append(
                "EQUILIBRAGE DE LA CIBLE"
            )

            lines.append(
                "-" * 70
            )

            for key, value in (
                imbalance.items()
            ):

                lines.append(
                    f"{key} : {value}"
                )

            lines.append("")

        pipeline = report.get(
            "pipeline"
        )

        if isinstance(
            pipeline,
            pd.DataFrame
        ):

            lines.append(
                "PIPELINE"
            )

            lines.append(
                "-" * 70
            )

            lines.append(
                pipeline.to_string(
                    index=False
                )
            )

            lines.append("")

        lines.append(
            "=" * 70
        )

        return "\n".join(
            lines
        )


    # ======================================================
    # SAVE TEXT REPORT
    # ======================================================

    @staticmethod
    def save_text(
        report,
        filepath
    ):

        text = (
            PreprocessingReport
            .to_text(
                report
            )
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                text
            )

        return filepath


# ==========================================================
# PUBLIC API
# ==========================================================

class Report:

    header = (
        PreprocessingReport.header
    )

    dataset_info = (
        PreprocessingReport.dataset_info
    )

    missing_report = (
        PreprocessingReport.missing_report
    )

    duplicate_report = (
        PreprocessingReport.duplicate_report
    )

    numeric_report = (
        PreprocessingReport.numeric_report
    )

    categorical_report = (
        PreprocessingReport.categorical_report
    )

    outlier_report = (
        PreprocessingReport.outlier_report
    )

    correlation_report = (
        PreprocessingReport.correlation_report
    )

    target_report = (
        PreprocessingReport.target_report
    )

    imbalance_report = (
        PreprocessingReport.imbalance_report
    )

    steps_report = (
        PreprocessingReport.steps_report
    )

    generate = (
        PreprocessingReport.generate
    )

    to_text = (
        PreprocessingReport.to_text
    )

    save_text = (
        PreprocessingReport.save_text
    )