"""
=========================================================
EMIDAF Framework
Visualization - Matplotlib Style
=========================================================
"""

from __future__ import annotations

import matplotlib.pyplot as plt


DEFAULT_FIGSIZE = (10, 6)


def set_default_style(
    figsize=DEFAULT_FIGSIZE,
    grid=True,
    fontsize=11
):

    plt.rcParams["figure.figsize"] = figsize
    plt.rcParams["font.size"] = fontsize
    plt.rcParams["axes.grid"] = grid

    return plt.rcParams


def reset_style():

    plt.rcdefaults()

    return plt.rcParams


def set_figure_size(
    width,
    height
):

    plt.rcParams["figure.figsize"] = (
        width,
        height
    )

    return plt.rcParams


def set_font_size(
    fontsize
):

    plt.rcParams["font.size"] = fontsize

    return plt.rcParams


def enable_grid():

    plt.rcParams["axes.grid"] = True

    return plt.rcParams


def disable_grid():

    plt.rcParams["axes.grid"] = False

    return plt.rcParams
