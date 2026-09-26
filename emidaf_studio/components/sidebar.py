from dash import (
    html,
    Input,
    Output,
    callback,
)

import re

import dash_bootstrap_components as dbc


def nav_item(
    icon,
    label,
    href,
    nav_id=None,
):
    kwargs = {
        "href": href,
        "className": "emidaf-nav-link",
        "style": {
            "padding": "10px 12px",
            "marginBottom": "4px",
            "borderRadius": "9px",
            "fontSize": "0.94rem",
            "lineHeight": "1.3",
            "fontWeight": "500",
        },
    }

    if nav_id is not None:
        kwargs["id"] = nav_id

    return dbc.NavLink(
        [
            html.I(
                className=f"bi {icon} me-2",
                style={
                    "fontSize": "1rem",
                    "width": "20px",
                    "display": "inline-block",
                    "textAlign": "center",
                },
            ),
            html.Span(label),
        ],
        **kwargs,
    )


def section_title(label):
    return html.Div(
        label,
        className="text-muted",
        style={
            "fontSize": "0.68rem",
            "fontWeight": "700",
            "letterSpacing": "0.07em",
            "padding": "12px 12px 7px 12px",
        },
    )


sidebar = html.Div(
    [
        html.Div(
            [
                html.Div(
                    "EMIDAF",
                    style={
                        "fontWeight": "750",
                        "fontSize": "1.08rem",
                        "letterSpacing": "0.05em",
                    },
                ),
                html.Div(
                    "Environnement scientifique d'analyse",
                    className="text-muted",
                    style={
                        "fontSize": "0.76rem",
                        "marginTop": "2px",
                    },
                ),
            ],
            style={
                "padding": "2px 12px 16px 12px",
            },
        ),

        dbc.Nav(
            [
                nav_item(
                    "bi-house-door",
                    "Accueil",
                    "/",
                ),
                nav_item(
                    "bi-folder2-open",
                    "Projets",
                    "/projects",
                ),
                nav_item(
                    "bi-cloud-arrow-up",
                    "Importation",
                    "/import",
                ),
                nav_item(
                    "bi-search",
                    "Inspection",
                    "/inspection",
                ),

                section_title(
                    "ANALYSE DES DONNÉES"
                ),

                nav_item(
                    "bi-sliders",
                    "Prétraitement des données",
                    "/eidpp",
                ),
                nav_item(
                    "bi-bar-chart-line",
                    "Analyse exploratoire",
                    "/elae",
                ),
                nav_item(
                    "bi-chat-square-text",
                    "Analyse textuelle",
                    "/etae",
                ),
                nav_item(
                    "bi-journal-text",
                    "Analyse qualitative",
                    "/eqae",
                ),
                nav_item(
                    "bi-diagram-3",
                    "Découverte de connaissances",
                    "/ekde",
                ),

                section_title(
                    "MODÉLISATION ET INTERPRÉTATION"
                ),

                nav_item(
                    "bi-graph-up-arrow",
                    "Modélisation prédictive",
                    "/eaie",
                ),
                nav_item(
                    "bi-eye",
                    "Explicabilité des modèles",
                    "/exaie",
                ),
                nav_item(
                    "bi-compass",
                    "Aide à la décision",
                    "/edse",
                ),

                section_title(
                    "RESTITUTION"
                ),

                nav_item(
                    "bi-file-earmark-text",
                    "Rapports analytiques",
                    "/reports",
                    nav_id="sidebar-reports-link",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="emidaf-sidebar",
    style={
        "padding": "18px 10px",
        "minHeight": "calc(100vh - 56px)",
    },
)


@callback(
    Output(
        "sidebar-reports-link",
        "href",
    ),
    Input(
        "url",
        "pathname",
    ),
)
def update_reports_link(pathname):

    match = re.match(
        r"^/projects/(\d+)/datasets/(\d+)(?:/.*)?$",
        pathname or "",
    )

    if match:
        project_id = match.group(1)
        dataset_id = match.group(2)

        return (
            f"/projects/{project_id}"
            f"/datasets/{dataset_id}"
            f"/reports"
        )

    return "/reports"
