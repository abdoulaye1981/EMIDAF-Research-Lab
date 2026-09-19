import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from emidaf_core.visualization import (
    VisualizationResult,
    UnivariateVisualizer,
    BivariateVisualizer,
    MultivariateVisualizer,
    DistributionVisualizer,
    CategoricalVisualizer,
    TimeSeriesVisualizer,
    DiagnosticsVisualizer,
    StatisticalVisualizer,
)

from emidaf_core.visualization.univariate import (
    frequency_table,
)


# ==========================================================
# FIXTURES
# ==========================================================

@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


@pytest.fixture
def data():
    rng = np.random.default_rng(42)

    n = 80

    return pd.DataFrame(
        {
            "x": rng.normal(
                10,
                2,
                n,
            ),
            "y": rng.normal(
                20,
                5,
                n,
            ),
            "z": rng.normal(
                5,
                1,
                n,
            ),
            "group": np.resize(
                ["A", "B", "C", "D"],
                n,
            ),
            "category": np.resize(
                ["Yes", "No"],
                n,
            ),
            "date": pd.date_range(
                "2026-01-01",
                periods=n,
                freq="D",
            ),
        }
    )


def assert_visualization_result(result):
    assert isinstance(
        result,
        VisualizationResult,
    )

    assert result.figure is not None
    assert result.axes is not None


# ==========================================================
# VISUALIZATION RESULT
# ==========================================================

def test_visualization_result_save(
    data,
    tmp_path,
):
    visualizer = UnivariateVisualizer()

    result = visualizer.histogram(
        data,
        "x",
    )

    path = tmp_path / "histogram.png"

    returned = result.save(
        path
    )

    assert returned == path
    assert path.exists()
    assert path.stat().st_size > 0


def test_visualization_result_without_figure_cannot_save(
    tmp_path,
):
    result = VisualizationResult()

    with pytest.raises(
        RuntimeError
    ):
        result.save(
            tmp_path / "invalid.png"
        )


# ==========================================================
# UNIVARIATE
# ==========================================================

def test_univariate_histogram(data):
    result = (
        UnivariateVisualizer()
        .histogram(
            data,
            "x",
        )
    )

    assert_visualization_result(
        result
    )

    assert len(result.data) == len(data)


def test_univariate_boxplot(data):
    result = (
        UnivariateVisualizer()
        .boxplot(
            data,
            "x",
        )
    )

    assert_visualization_result(
        result
    )


def test_univariate_barplot(data):
    result = (
        UnivariateVisualizer()
        .barplot(
            data,
            "group",
        )
    )

    assert_visualization_result(
        result
    )

    assert result.data.sum() == len(data)


def test_univariate_piechart(data):
    result = (
        UnivariateVisualizer()
        .piechart(
            data,
            "category",
        )
    )

    assert_visualization_result(
        result
    )


def test_univariate_density(data):
    result = (
        UnivariateVisualizer()
        .density(
            data,
            "x",
        )
    )

    assert_visualization_result(
        result
    )


def test_univariate_frequency_table(data):
    table = frequency_table(
        data,
        "group",
    )

    assert isinstance(
        table,
        pd.DataFrame,
    )

    assert {
        "effectif",
        "frequence",
        "pourcentage",
    }.issubset(
        table.columns
    )

    assert table["effectif"].sum() == len(
        data
    )

    assert table["frequence"].sum() == pytest.approx(
        1.0
    )

    assert table["pourcentage"].sum() == pytest.approx(
        100.0
    )


# ==========================================================
# BIVARIATE
# ==========================================================

def test_bivariate_scatterplot(data):
    result = (
        BivariateVisualizer()
        .scatterplot(
            data,
            "x",
            "y",
        )
    )

    assert_visualization_result(
        result
    )


def test_bivariate_lineplot(data):
    result = (
        BivariateVisualizer()
        .lineplot(
            data,
            "x",
            "y",
        )
    )

    assert_visualization_result(
        result
    )


def test_bivariate_grouped_boxplot(data):
    result = (
        BivariateVisualizer()
        .grouped_boxplot(
            data,
            "group",
            "x",
        )
    )

    assert_visualization_result(
        result
    )


def test_bivariate_mean_plot(data):
    result = (
        BivariateVisualizer()
        .mean_plot(
            data,
            "group",
            "x",
        )
    )

    assert_visualization_result(
        result
    )


def test_bivariate_correlation_heatmap(data):
    result = (
        BivariateVisualizer()
        .correlation_heatmap(
            data[
                [
                    "x",
                    "y",
                    "z",
                ]
            ]
        )
    )

    assert_visualization_result(
        result
    )


# ==========================================================
# DISTRIBUTION
# ==========================================================

def test_distribution_histogram(data):
    result = (
        DistributionVisualizer()
        .histogram(
            data,
            "x",
        )
    )

    assert_visualization_result(
        result
    )


def test_distribution_empirical_cdf(data):
    result = (
        DistributionVisualizer()
        .empirical_cdf(
            data,
            "x",
        )
    )

    assert_visualization_result(
        result
    )


def test_distribution_qqplot(data):
    result = (
        DistributionVisualizer()
        .qqplot(
            data,
            "x",
        )
    )

    assert_visualization_result(
        result
    )


# ==========================================================
# CATEGORICAL
# ==========================================================

def test_categorical_frequency_barplot(data):
    result = (
        CategoricalVisualizer()
        .frequency_barplot(
            data,
            "group",
        )
    )

    assert_visualization_result(
        result
    )


def test_categorical_frequency_table(data):
    table = (
        CategoricalVisualizer()
        .frequency_table(
            data,
            "group",
        )
    )

    assert isinstance(
        table,
        pd.DataFrame,
    )


def test_categorical_compare_categories(data):
    result = (
        CategoricalVisualizer()
        .compare_categories(
            data,
            "group",
            "category",
        )
    )

    assert_visualization_result(
        result
    )


# ==========================================================
# MULTIVARIATE
# ==========================================================

def test_multivariate_correlation_heatmap(data):
    result = (
        MultivariateVisualizer()
        .correlation_heatmap(
            data[
                [
                    "x",
                    "y",
                    "z",
                ]
            ]
        )
    )

    assert_visualization_result(
        result
    )


def test_multivariate_pairplot(data):
    result = (
        MultivariateVisualizer()
        .pairplot(
            data,
            columns=[
                "x",
                "y",
                "z",
            ],
        )
    )

    assert isinstance(
        result,
        VisualizationResult,
    )

    assert result.figure is not None


# ==========================================================
# TIME SERIES
# ==========================================================

def test_time_series_plot(data):
    result = (
        TimeSeriesVisualizer()
        .plot(
            data,
            "date",
            "x",
        )
    )

    assert_visualization_result(
        result
    )


def test_time_series_rolling_mean(data):
    result = (
        TimeSeriesVisualizer()
        .rolling_mean(
            data,
            "date",
            "x",
            window=7,
        )
    )

    assert_visualization_result(
        result
    )


def test_time_series_rolling_std(data):
    result = (
        TimeSeriesVisualizer()
        .rolling_std(
            data,
            "date",
            "x",
            window=7,
        )
    )

    assert_visualization_result(
        result
    )


# ==========================================================
# DIAGNOSTICS
# ==========================================================

def test_diagnostics_acf(data):
    result = (
        DiagnosticsVisualizer()
        .acf(
            data,
            "x",
            lags=10,
        )
    )

    assert_visualization_result(
        result
    )


def test_diagnostics_pacf(data):
    result = (
        DiagnosticsVisualizer()
        .pacf(
            data,
            "x",
            lags=10,
        )
    )

    assert_visualization_result(
        result
    )


def test_diagnostics_residuals_histogram(data):
    residuals = (
        data["x"]
        - data["x"].mean()
    )

    result = (
        DiagnosticsVisualizer()
        .residuals_histogram(
            residuals,
        )
    )

    assert_visualization_result(
        result
    )


def test_diagnostics_residuals_qqplot(data):
    residuals = (
        data["x"]
        - data["x"].mean()
    )

    result = (
        DiagnosticsVisualizer()
        .residuals_qqplot(
            residuals,
        )
    )

    assert_visualization_result(
        result
    )


# ==========================================================
# STATISTICAL
# ==========================================================

def test_statistical_mean_median(data):
    result = (
        StatisticalVisualizer()
        .mean_median(
            data,
            "x",
        )
    )

    assert_visualization_result(
        result
    )


def test_statistical_confidence_interval(data):
    result = (
        StatisticalVisualizer()
        .confidence_interval(
            data,
            "x",
            confidence=0.95,
        )
    )

    assert_visualization_result(
        result
    )


def test_statistical_group_mean_ci(data):
    result = (
        StatisticalVisualizer()
        .group_mean_ci(
            data,
            "group",
            "x",
            confidence=0.95,
        )
    )

    assert_visualization_result(
        result
    )


def test_statistical_rank_plot(data):
    result = (
        StatisticalVisualizer()
        .rank_plot(
            data,
            "x",
        )
    )

    assert_visualization_result(
        result
    )
