import numpy as np
import pandas as pd

from emidaf_core.dataset.profiler.analyzers.missing_analyzer import (
    MissingAnalyzer,
)
from emidaf_core.dataset.profiler.profile_context import (
    ProfileContext,
)


def run_missing_analyzer(
    dataframe: pd.DataFrame,
):

    context = ProfileContext(
        dataframe=dataframe
    )

    analyzer = MissingAnalyzer()

    result = analyzer.execute(
        context
    )

    assert result.success is True
    assert result.result is not None

    return result.result


def test_missing_analyzer_mcar_integration():

    rng = np.random.default_rng(42)

    n = 1500

    df = pd.DataFrame(
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

    # Missingness générée indépendamment
    # des valeurs observées.
    mask_age = (
        rng.random(n) < 0.08
    )

    mask_income = (
        rng.random(n) < 0.10
    )

    mask_score = (
        rng.random(n) < 0.06
    )

    df.loc[
        mask_age,
        "age"
    ] = np.nan

    df.loc[
        mask_income,
        "income"
    ] = np.nan

    df.loc[
        mask_score,
        "score"
    ] = np.nan

    report = run_missing_analyzer(
        df
    )

    mechanism = report[
        "missing_mechanism"
    ]

    assert (
        mechanism["status"]
        == "Compatible"
    )

    assert (
        mechanism["candidate"]
        == "MCAR"
    )

    assert (
        mechanism["detected"]
        is False
    )

    assert (
        mechanism["tests"]["mcar"]["executed"]
        is True
    )

    assert (
        mechanism["tests"]["mcar"][
            "compatible_with_mcar"
        ]
        is True
    )


def test_missing_analyzer_mar_integration():

    rng = np.random.default_rng(123)

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

    df = pd.DataFrame(
        {
            "age": age,
            "income": income,
            "score": score,
        }
    )

    # La missingness de income dépend
    # d'une variable observée : age.
    mask = (
        df["age"] > 45
    )

    df.loc[
        mask,
        "income"
    ] = np.nan

    report = run_missing_analyzer(
        df
    )

    mechanism = report[
        "missing_mechanism"
    ]

    assert (
        mechanism["status"]
        == "Evaluated"
    )

    assert (
        mechanism["candidate"]
        == "MAR"
    )

    assert (
        mechanism["detected"]
        is True
    )

    assert (
        mechanism["tests"]["mcar"]["executed"]
        is True
    )

    assert (
        mechanism["tests"]["mcar"][
            "compatible_with_mcar"
        ]
        is False
    )

    assert (
        mechanism["tests"]["mar"]["executed"]
        is True
    )

    assert (
        mechanism["tests"]["mar"][
            "evidence_detected"
        ]
        is True
    )


def test_missing_analyzer_mnar_scenario_is_not_confirmed():

    rng = np.random.default_rng(999)

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

    df = pd.DataFrame(
        {
            "age": age,
            "income": income,
            "score": score,
        }
    )

    # Scénario généré artificiellement comme MNAR :
    # la missingness dépend de la valeur de income
    # elle-même avant masquage.
    mask = (
        df["income"] > 550
    )

    df.loc[
        mask,
        "income"
    ] = np.nan

    report = run_missing_analyzer(
        df
    )

    mechanism = report[
        "missing_mechanism"
    ]

    # EMIDAF ne doit jamais prétendre
    # confirmer MNAR à partir des seules
    # données observées.
    assert (
        mechanism["candidate"]
        != "MNAR"
    )

    if (
        mechanism["candidate"]
        == "MNAR possible"
    ):
        assert (
            mechanism["detected"]
            is False
        )

        assert (
            mechanism["status"]
            == "Requires review"
        )

    assert (
        mechanism["detected"]
        is not True
        or mechanism["candidate"]
        != "MNAR possible"
    )


def test_missing_mechanism_contract_integration():

    rng = np.random.default_rng(2026)

    n = 500

    df = pd.DataFrame(
        {
            "x1": rng.normal(size=n),
            "x2": rng.normal(size=n),
            "x3": rng.normal(size=n),
        }
    )

    mask = (
        rng.random(n) < 0.12
    )

    df.loc[
        mask,
        "x2"
    ] = np.nan

    report = run_missing_analyzer(
        df
    )

    mechanism = report[
        "missing_mechanism"
    ]

    required_keys = {
        "status",
        "candidate",
        "detected",
        "confidence",
        "pvalue",
        "statistic",
        "test_name",
        "explanation",
        "tests",
    }

    assert required_keys.issubset(
        mechanism.keys()
    )

    assert (
        0.0
        <= mechanism["confidence"]
        <= 1.0
    )

    assert {
        "mcar",
        "mar",
        "mnar",
    }.issubset(
        mechanism["tests"].keys()
    )


def test_missing_summary_consistency():

    rng = np.random.default_rng(77)

    n = 1000

    df = pd.DataFrame(
        {
            "x": rng.normal(size=n),
            "y": rng.normal(size=n),
        }
    )

    mask = (
        rng.random(n) < 0.10
    )

    df.loc[
        mask,
        "y"
    ] = np.nan

    report = run_missing_analyzer(
        df
    )

    missing_rate = report[
        "missing_rate"
    ]

    completeness_score = report[
        "summary"
    ][
        "completeness_score"
    ]

    quality_score = report[
        "quality_score"
    ]

    assert completeness_score == (
        round(
            100.0 - missing_rate,
            2,
        )
    )

    assert quality_score == (
        completeness_score
    )
