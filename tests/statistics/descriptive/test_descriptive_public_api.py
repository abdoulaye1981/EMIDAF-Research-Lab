from __future__ import annotations

import emidaf_core.statistics.descriptive as descriptive


EXPECTED_PUBLIC_API = {
    "DescriptiveStatistic",
    "StatisticsValidator",
    "CentralTendency",
    "LocationStatistics",
    "Dispersion",
    "Position",
    "Shape",
    "Robust",
    "Weighted",
    "Circular",
    "Multivariate",
    "FrequencyStatistics",
    "DistributionStatistics",
    "StatisticalProfiler",
    "Profiling",
    "DescriptiveSummary",
    "Summary",
    "SummaryStatistics",
    "DescriptiveInterpreter",
    "Interpretation",
    "DescriptiveReport",
    "Report",
}


TECHNICAL_NAMES = {
    "np",
    "pd",
    "ABC",
    "json",
    "stats",
    "euclidean",
    "mahalanobis",
    "minkowski",
    "winsorize",
    "trim_mean",
}


AMBIGUOUS_ATOMIC_NAMES = {
    "Mean",
    "Median",
    "Minimum",
    "Maximum",
    "Variance",
    "Skewness",
    "Kurtosis",
    "Quantiles",
    "Percentiles",
    "TrimmedMean",
    "MedianAbsoluteDeviation",
}


def test_descriptive_public_api_is_complete():

    assert set(
        descriptive.__all__
    ) == EXPECTED_PUBLIC_API


def test_every_public_symbol_exists():

    missing = [
        name
        for name in descriptive.__all__
        if not hasattr(
            descriptive,
            name,
        )
    ]

    assert missing == []


def test_technical_names_are_not_public():

    assert (
        TECHNICAL_NAMES
        .intersection(
            descriptive.__all__
        )
        == set()
    )


def test_ambiguous_atomic_names_are_not_in_root_public_api():

    assert (
        AMBIGUOUS_ATOMIC_NAMES
        .intersection(
            descriptive.__all__
        )
        == set()
    )


def test_atomic_statistics_remain_available_in_submodules():

    from emidaf_core.statistics.descriptive.location import (
        Mean,
        Median,
    )

    from emidaf_core.statistics.descriptive.dispersion import (
        Variance,
    )

    from emidaf_core.statistics.descriptive.shape import (
        Skewness,
        Kurtosis,
    )

    assert Mean is not None
    assert Median is not None
    assert Variance is not None
    assert Skewness is not None
    assert Kurtosis is not None


def test_star_import_contract_matches_all():

    namespace = {}

    exec(
        "from emidaf_core.statistics.descriptive import *",
        {},
        namespace,
    )

    exported = {
        name
        for name in namespace
        if not name.startswith("__")
    }

    assert exported == EXPECTED_PUBLIC_API
