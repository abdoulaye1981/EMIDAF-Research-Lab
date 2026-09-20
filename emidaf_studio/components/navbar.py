from dash import (
    dcc,
    html,
)

import dash_bootstrap_components as dbc


navbar = dbc.Navbar(
    dbc.Container(
        [
            # ==============================================
            # MARQUE EMIDAF
            # ==============================================

            dbc.NavbarBrand(
                [
                    html.Span(
                        "EMIDAF Research Lab",
                        style={
                            "fontWeight": "700",
                            "letterSpacing": "0.025em",
                        },
                    ),
                    html.Span(
                        (
                            " | Laboratoire de recherche "
                            "et d'analyse des données"
                        ),
                        className="emidaf-navbar-subtitle",
                    ),
                ],
                href="/",
                style={
                    "color": "white",
                },
            ),

            # ==============================================
            # ZONE DROITE
            # ==============================================

            html.Div(
                [
                    # --------------------------------------
                    # Sélecteur de thème
                    # --------------------------------------

                    html.Div(
                        [
                            html.I(
                                className="bi bi-palette me-2",
                                style={
                                    "color": "white",
                                },
                            ),

                            dcc.Dropdown(
                                id="theme-selector",
                                options=[
                                    {
                                        "label": "Gris scientifique",
                                        "value": "scientific",
                                    },
                                    {
                                        "label": "Bleu laboratoire",
                                        "value": "laboratory",
                                    },
                                    {
                                        "label": "Bleu profond",
                                        "value": "deep_blue",
                                    },
                                    {
                                        "label": "Vert recherche",
                                        "value": "research",
                                    },
                                    {
                                        "label": "Vert profond",
                                        "value": "deep_green",
                                    },
                                    {
                                        "label": "Sombre",
                                        "value": "dark",
                                    },
                                ],
                                value="scientific",
                                clearable=False,
                                searchable=False,
                                style={
                                    "width": "190px",
                                    "color": "#212529",
                                },
                            ),
                        ],
                        className="d-flex align-items-center",
                    ),

                    # --------------------------------------
                    # Utilisateur / connexion / déconnexion
                    # --------------------------------------

                    html.Div(
                        id="navbar-user-menu",
                        className="ms-3",
                    ),
                ],
                className="d-flex align-items-center",
            ),
        ],
        fluid=True,
        className="px-3",
    ),

    id="emidaf-navbar",
    dark=True,
)
