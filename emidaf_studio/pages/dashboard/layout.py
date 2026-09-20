from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def dashboard_layout(user):
    return dbc.Container(
        [
            html.Div(
                [
                    html.Div(
                        "ESPACE PERSONNEL",
                        className="module-home-v2-kicker",
                    ),
                    html.H1(
                        f"Bonjour {user.first_name}",
                        className="module-home-v2-title",
                    ),
                    html.P(
                        (
                            "Retrouvez vos projets, jeux de données "
                            "et travaux analytiques EMIDAF."
                        ),
                        className="module-home-v2-subtitle",
                    ),
                ],
                className="module-home-v2-hero",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.I(
                                        className=(
                                            "bi bi-folder2-open "
                                            "fs-2"
                                        )
                                    ),
                                    html.H4(
                                        "Mes projets",
                                        className="mt-3",
                                    ),
                                    html.P(
                                        (
                                            "Créer, consulter et "
                                            "poursuivre vos projets."
                                        )
                                    ),
                                    dcc.Link(
                                        "Ouvrir mes projets",
                                        href="/projects",
                                        className=(
                                            "btn btn-primary"
                                        ),
                                    ),
                                ]
                            )
                        ),
                        md=4,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.I(
                                        className=(
                                            "bi bi-diagram-3 fs-2"
                                        )
                                    ),
                                    html.H4(
                                        "Cycle analytique",
                                        className="mt-3",
                                    ),
                                    html.P(
                                        (
                                            "Inspection, préparation, "
                                            "exploration, modélisation "
                                            "et restitution."
                                        )
                                    ),
                                ]
                            )
                        ),
                        md=4,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.I(
                                        className=(
                                            "bi bi-person-circle fs-2"
                                        )
                                    ),
                                    html.H4(
                                        "Mon compte",
                                        className="mt-3",
                                    ),
                                    html.P(user.email),
                                    html.Small(
                                        f"Rôle : {user.role}"
                                    ),
                                ]
                            )
                        ),
                        md=4,
                    ),
                ],
                className="g-4 mt-3",
            ),
        ],
        fluid=True,
        className="py-4",
    )
