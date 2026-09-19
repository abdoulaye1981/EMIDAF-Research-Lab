from dash import dcc
from dash import html
from dash import Input
from dash import Output
from dash import callback

import re

from emidaf_studio.layouts.home import layout as home_layout


# ==========================================================
# Zone de contenu pilotée par l'URL
# ==========================================================

content = html.Div(
    id="page-content"
)


# ==========================================================
# Gestion du routage
# ==========================================================

def get_page_layout(pathname):

    # ======================================================
    # Accueil
    # ======================================================

    if pathname == "/":
        return home_layout

    # ======================================================
    # Liste des projets
    # ======================================================

    if pathname == "/projects":

        from emidaf_studio.pages.projects.layout import layout

        return layout

    # ======================================================
    # Importation d'un dataset
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)/import",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))

        import importlib

        import_page = importlib.import_module(
            "emidaf_studio.pages.import.layout"
        )

        return import_page.import_layout(project_id)

    # ======================================================
    # EIDPP - Prétraitement d'un dataset
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)/datasets/(\d+)/eidpp",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))
        dataset_id = int(match.group(2))

        from emidaf_studio.pages.eidpp.layout import (
            eidpp_layout
        )

        return eidpp_layout(
            project_id,
            dataset_id
        )

    # ======================================================
    # Inspection d'un dataset
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)/datasets/(\d+)",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))
        dataset_id = int(match.group(2))

        from emidaf_studio.pages.inspection.layout import (
            inspection_layout
        )

        return inspection_layout(
            project_id,
            dataset_id
        )

    # ======================================================
    # Page détaillée d'un projet
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))

        from emidaf_studio.pages.projects.layout import (
            project_detail_layout
        )

        return project_detail_layout(project_id)

    # ======================================================
    # Page inconnue
    # ======================================================

    return html.Div(
        [
            html.H2(
                "Page en préparation"
            ),

            html.P(
                f"La page « {pathname} » "
                "sera prochainement disponible."
            )
        ],
        className="p-4"
    )


# ==========================================================
# Callback du routeur
# ==========================================================

@callback(
    Output(
        "page-content",
        "children"
    ),
    Input(
        "url",
        "pathname"
    )
)
def display_page(pathname):

    return get_page_layout(pathname)


# ==========================================================
# Layout du routeur
# ==========================================================

layout = html.Div(
    [
        dcc.Location(
            id="url",
            refresh=False
        ),

        content
    ]
)
