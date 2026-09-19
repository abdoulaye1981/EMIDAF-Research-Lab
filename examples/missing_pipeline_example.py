"""
=========================================================
EMIDAF Framework
Missing Data Pipeline - Reproducible Example
=========================================================
"""

from pathlib import Path

import numpy as np
import pandas as pd

from emidaf_core.missing import (
    MissingPipeline,
    MissingReporter,
)


def build_demo_dataset(
    n: int = 100,
) -> pd.DataFrame:
    """
    Construit un jeu de données synthétique destiné
    à démontrer le pipeline Missing d'EMIDAF.
    """

    dataframe = pd.DataFrame(
        {
            "age": np.linspace(
                20,
                60,
                n,
            ),
            "income": np.linspace(
                200,
                1000,
                n,
            ),
            "score": np.linspace(
                0,
                100,
                n,
            ),
        }
    )

    # ---------------------------------------------
    # Faible taux de valeurs manquantes
    # -> stratégie simple attendue
    # ---------------------------------------------

    dataframe.loc[
        [0, 1, 2],
        "age",
    ] = np.nan

    # ---------------------------------------------
    # Taux modéré de valeurs manquantes
    # -> stratégie multivariée attendue
    # ---------------------------------------------

    dataframe.loc[
        list(
            range(
                10
            )
        ),
        "income",
    ] = np.nan

    return dataframe


def main() -> None:

    # =====================================================
    # 1. DATA
    # =====================================================

    dataframe = (
        build_demo_dataset()
    )

    print(
        "\n=== ORIGINAL DATASET ===\n"
    )

    print(
        dataframe.head(
            12
        )
    )

    print(
        "\nMissing values before:"
    )

    print(
        dataframe
        .isna()
        .sum()
    )

    # =====================================================
    # 2. PIPELINE
    # =====================================================

    pipeline = (
        MissingPipeline()
    )

    result = (
        pipeline.run(
            dataframe=dataframe,
            apply_imputation=True,
        )
    )

    # =====================================================
    # 3. SUMMARY
    # =====================================================

    print(
        "\n=== PIPELINE SUMMARY ===\n"
    )

    print(
        result.summary()
    )

    # =====================================================
    # 4. VARIABLE AUDIT
    # =====================================================

    print(
        "\n=== VARIABLE AUDIT ===\n"
    )

    print(
        result
        .summary_dataframe()
        .to_string(
            index=False
        )
    )

    # =====================================================
    # 5. MISSINGNESS MECHANISMS
    # =====================================================

    reporter = (
        MissingReporter(
            result
        )
    )

    print(
        "\n=== MCAR / MAR / MNAR ===\n"
    )

    print(
        reporter
        .mechanism_dataframe()
        .to_string(
            index=False
        )
    )

    # =====================================================
    # 6. FINAL DATA
    # =====================================================

    print(
        "\n=== FINAL DATASET ===\n"
    )

    print(
        result.dataframe.head(
            12
        )
    )

    print(
        "\nMissing values after:"
    )

    print(
        result.dataframe
        .isna()
        .sum()
    )

    # =====================================================
    # 7. REPORTING
    # =====================================================

    output_directory = Path(
        "outputs/missing_example"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    reporter.to_csv(
        output_directory
        / "missing_audit.csv"
    )

    reporter.to_excel(
        output_directory
        / "missing_report.xlsx"
    )

    reporter.to_scientific_markdown(
        output_directory
        / "missing_scientific_report.md"
    )

    reporter.to_scientific_html(
        output_directory
        / "missing_scientific_report.html"
    )

    reporter.to_scientific_excel(
        output_directory
        / "missing_scientific_report.xlsx"
    )

    print(
        "\n=== REPORTS GENERATED ===\n"
    )

    for path in sorted(
        output_directory.iterdir()
    ):
        print(
            "-",
            path,
        )


if __name__ == "__main__":
    main()
