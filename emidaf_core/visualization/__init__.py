"""
=========================================================
EMIDAF Framework
Visualization
=========================================================
"""

from .base import (
    BaseVisualizer,
    VisualizationResult
)

from .univariate import (
    UnivariateVisualizer
)

from .bivariate import (
    BivariateVisualizer
)

from .multivariate import (
    MultivariateVisualizer
)

from .distribution import (
    DistributionVisualizer
)

from .categorical import (
    CategoricalVisualizer
)

from .time_series import (
    TimeSeriesVisualizer
)

from .diagnostics import (
    DiagnosticsVisualizer
)

from .statistical import (
    StatisticalVisualizer
)

from .matplotlib_style import (
    set_default_style,
    reset_style,
    set_figure_size,
    set_font_size,
    enable_grid,
    disable_grid
)


__all__ = [
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
    "disable_grid"
]
