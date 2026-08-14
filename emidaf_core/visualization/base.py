"""
=========================================================
EMIDAF Framework
Visualization - Base
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import matplotlib.pyplot as plt


class BaseVisualizer(ABC):

    name = "Base Visualizer"

    def __init__(
        self,
        figsize=(10, 6),
        title=None
    ):

        self.figsize = figsize
        self.title = title

        self.figure_ = None
        self.axes_ = None
        self.fitted_ = False

    def fit(
        self,
        X,
        y=None
    ):

        self.fitted_ = True

        return self

    @abstractmethod
    def plot(
        self,
        X,
        y=None
    ):

        raise NotImplementedError

    def fit_plot(
        self,
        X,
        y=None
    ):

        self.fit(
            X,
            y
        )

        return self.plot(
            X,
            y
        )

    def show(self):

        if self.figure_ is None:

            raise RuntimeError(
                "Aucune figure disponible."
            )

        plt.show()

        return self

    def save(
        self,
        path,
        dpi=300,
        bbox_inches="tight"
    ):

        if self.figure_ is None:

            raise RuntimeError(
                "Aucune figure disponible."
            )

        self.figure_.savefig(
            path,
            dpi=dpi,
            bbox_inches=bbox_inches
        )

        return path

    def close(self):

        if self.figure_ is not None:

            plt.close(
                self.figure_
            )

        return self

    def _create_figure(self):

        self.figure_, self.axes_ = (
            plt.subplots(
                figsize=self.figsize
            )
        )

        if self.title is not None:

            self.axes_.set_title(
                self.title
            )

        return (
            self.figure_,
            self.axes_
        )


class VisualizationResult:

    def __init__(
        self,
        figure=None,
        axes=None,
        data=None
    ):

        self.figure = figure
        self.axes = axes
        self.data = data

    def show(self):

        if self.figure is not None:

            plt.show()

        return self

    def save(
        self,
        path,
        dpi=300,
        bbox_inches="tight"
    ):

        if self.figure is None:

            raise RuntimeError(
                "Aucune figure disponible."
            )

        self.figure.savefig(
            path,
            dpi=dpi,
            bbox_inches=bbox_inches
        )

        return path

    def close(self):

        if self.figure is not None:

            plt.close(
                self.figure
            )

        return self
