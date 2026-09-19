import numpy as np
import pandas as pd

from emidaf_core.dataset.profiler.analyzers.missing_analyzer import (
    MissingAnalyzer,
)
from emidaf_core.dataset.profiler.profile_context import (
    ProfileContext,
)


def run_case(name: str, df: pd.DataFrame):

    print("\n")
    print("=" * 70)
    print(name)
    print("=" * 70)

    context = ProfileContext(
        dataframe=df
    )

    analyzer = MissingAnalyzer()

    result = analyzer.execute(
        context
    )

    print("SUCCESS :", result.success)
    print("STATUS  :", result.status)
    print("TIME    :", result.execution_time)

    if result.errors:
        print("ERRORS  :", result.errors)

    report = result.result

    if report is None:
        print("No report returned.")
        return

    print("\nGLOBAL MISSING RATE:")
    print(
        report.get(
            "missing_rate"
        )
    )

    print("\nMISSING MECHANISM:")

    mechanism = report.get(
        "missing_mechanism",
        {}
    )

    for key in (
        "status",
        "candidate",
        "detected",
        "confidence",
        "pvalue",
        "statistic",
        "test_name",
        "explanation",
    ):
        print(
            f"{key:15}:",
            mechanism.get(key)
        )

    print("\nTEST DETAILS:")

    tests = mechanism.get(
        "tests",
        {}
    )

    for test_name, details in tests.items():

        print(
            f"\n--- {test_name.upper()} ---"
        )

        for key, value in details.items():
            print(
                f"{key:25}: {value}"
            )


# ==========================================================
# RANDOM GENERATOR
# ==========================================================

rng = np.random.default_rng(
    42
)


# ==========================================================
# CASE 1 - MCAR
# ==========================================================

n = 1500

df_mcar = pd.DataFrame(
    {
        "age": rng.normal(
            40,
            10,
            n,
        ),
        "income": rng.normal(
            500,
            100,
            n,
        ),
        "score": rng.normal(
            70,
            15,
            n,
        ),
    }
)

mask_age = (
    rng.random(n) < 0.08
)

mask_income = (
    rng.random(n) < 0.10
)

mask_score = (
    rng.random(n) < 0.06
)

df_mcar.loc[
    mask_age,
    "age"
] = np.nan

df_mcar.loc[
    mask_income,
    "income"
] = np.nan

df_mcar.loc[
    mask_score,
    "score"
] = np.nan


# ==========================================================
# CASE 2 - MAR
# ==========================================================

n = 1500

age = rng.normal(
    40,
    10,
    n,
)

income = rng.normal(
    500,
    100,
    n,
)

score = rng.normal(
    70,
    15,
    n,
)

df_mar = pd.DataFrame(
    {
        "age": age,
        "income": income,
        "score": score,
    }
)

# La probabilité de missingness de income
# dépend d'une variable observée : age.

mask_mar = (
    df_mar["age"] > 45
)

df_mar.loc[
    mask_mar,
    "income"
] = np.nan


# ==========================================================
# CASE 3 - POSSIBLE MNAR RISK
# ==========================================================

n = 1500

age = rng.normal(
    40,
    10,
    n,
)

income = rng.normal(
    500,
    100,
    n,
)

score = rng.normal(
    70,
    15,
    n,
)

df_mnar = pd.DataFrame(
    {
        "age": age,
        "income": income,
        "score": score,
    }
)

# Simulation artificielle :
# la missingness dépend de la valeur elle-même.
#
# Ici on utilise la valeur AVANT de la masquer,
# uniquement pour générer un scénario MNAR connu.

mask_mnar = (
    df_mnar["income"] > 550
)

df_mnar.loc[
    mask_mnar,
    "income"
] = np.nan


# ==========================================================
# EXECUTION
# ==========================================================

run_case(
    "CASE 1 - MCAR",
    df_mcar,
)

run_case(
    "CASE 2 - MAR",
    df_mar,
)

run_case(
    "CASE 3 - POSSIBLE MNAR",
    df_mnar,
)
