import emidaf_core.visualization as visualization


EXPECTED_PUBLIC_API = {
    "BaseVisualizer",
    "VisualizationResult",
    "UnivariateVisualizer",
    "BivariateVisualizer",
    "MultivariateVisualizer",
    "DistributionVisualizer",
    "CategoricalVisualizer",
    "TimeSeriesVisualizer",
    "DiagnosticsVisualizer",
    "StatisticalVisualizer",
    "set_default_style",
    "reset_style",
    "set_figure_size",
    "set_font_size",
    "enable_grid",
    "disable_grid",
}


def test_public_api_exact_contract():
    assert set(
        visualization.__all__
    ) == EXPECTED_PUBLIC_API


def test_all_public_symbols_exist():
    for name in EXPECTED_PUBLIC_API:
        assert hasattr(
            visualization,
            name,
        )


def test_univariate_visualizer_is_public():
    assert (
        "UnivariateVisualizer"
        in visualization.__all__
    )


def test_low_level_plot_functions_not_public():
    forbidden = {
        "histogram",
        "frequency_table",
        "correlation_heatmap",
        "scatterplot",
        "pairplot",
    }

    assert forbidden.isdisjoint(
        visualization.__all__
    )
