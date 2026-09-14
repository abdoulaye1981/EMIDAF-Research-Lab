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

    if pathname == "/projects":

        from emidaf_studio.pages.projects.layout import layout

        return layout

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

    if pathname == "/":

        return home_layout

    return html.Div(
        [
            html.H2("Page en préparation"),

            html.P(
                f"La page « {pathname} » sera prochainement disponible."
            )
        ],
        className="p-4"
    )

# ==========================================================
# Callback du routeur
# ==========================================================

@callback(
    Output("page-content", "children"),
    Input("url", "pathname")
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
