from dash import dcc, html
import dash_bootstrap_components as dbc


PROFILE_PHOTO = (
    "https://drive.google.com/thumbnail"
    "?id=1QvThFNQY_Totq3CVNFAQ7rGkDGpwlW7p"
    "&sz=w500"
)

SOCIAL_LINKS = {
    "linkedin": (
        "https://www.linkedin.com/in/"
        "abdoulaye-wakhab-diop-8b4403134/"
    ),
    "youtube": (
        "https://www.youtube.com/"
        "@rendreaccessiblelesmaths7611/videos"
    ),
    "email": "mailto:wakhabdiop@yahoo.fr",
}


def _workflow_step(
    number,
    icon,
    title,
    subtitle,
    href,
):
    return html.Div(
        [
            dcc.Link(
                html.Div(
                    [
                        html.Div(
                            number,
                            className="v3-step-number",
                        ),

                        html.Div(
                            html.I(
                                className=f"bi {icon}"
                            ),
                            className="v3-step-icon",
                        ),

                        html.Div(
                            title,
                            className="v3-step-title",
                        ),

                        html.Div(
                            subtitle,
                            className="v3-step-subtitle",
                        ),
                    ],
                    className="v3-step-card",
                ),
                href=href,
                className="v3-link-reset",
            ),
        ],
        className="v3-step-wrapper",
    )


def _capability(
    number,
    icon,
    title,
    text,
    href,
):
    return html.Div(
        [
            dcc.Link(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span(
                                    number,
                                    className=(
                                        "v3-capability-number"
                                    ),
                                ),

                                html.Div(
                                    html.I(
                                        className=f"bi {icon}"
                                    ),
                                    className=(
                                        "v3-capability-icon"
                                    ),
                                ),
                            ],
                            className=(
                                "v3-capability-top"
                            ),
                        ),

                        html.H3(
                            title,
                            className=(
                                "v3-capability-title"
                            ),
                        ),

                        html.P(
                            text,
                            className=(
                                "v3-capability-text"
                            ),
                        ),

                        html.Div(
                            [
                                "Explorer",
                                html.I(
                                    className=(
                                        "bi bi-arrow-up-right "
                                        "ms-2"
                                    )
                                ),
                            ],
                            className=(
                                "v3-capability-action"
                            ),
                        ),
                    ],
                    className="v3-capability-card",
                ),
                href=href,
                className="v3-link-reset",
            ),
        ],
        className="v3-capability-wrapper",
    )


def _badge(text):
    return html.Span(
        text,
        className="v3-badge",
    )


def _social(icon, label, href, kind):
    return html.A(
        [
            html.I(
                className=f"bi {icon}"
            ),
            html.Span(label),
        ],
        href=href,
        target="_blank",
        rel="noopener noreferrer",
        className=(
            "v3-social "
            f"v3-social-{kind}"
        ),
    )


layout = html.Div(
    [

        # ==================================================
        # HERO
        # ==================================================

        html.Section(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                "EMIDAF RESEARCH LAB",
                                className="v3-eyebrow",
                            ),

                            html.H1(
                                [
                                    "Plateforme scientifique de ",
                                    "recherche et d'analyse ",
                                    html.Span(
                                        "des données",
                                        className="v3-accent-text",
                                    ),
                                    html.Br(),
                                    html.Span(
                                        "au service du Sénégal",
                                        className=(
                                            "v3-hero-country-line"
                                        ),
                                    ),
                                ],
                                className="v3-hero-title",
                            ),

                            html.P(
                                (
                                    "EMIDAF Research Lab est un "
                                    "environnement scientifique intégré "
                                    "pour l'analyse des données, la Data "
                                    "Science, l'intelligence artificielle, "
                                    "la recherche, l'éducation et "
                                    "l'aide à la décision."
                                ),
                                className="v3-hero-subtitle",
                            ),

                            html.Div(
                                [
                                    dcc.Link(
                                        dbc.Button(
                                            [
                                                html.I(
                                                    className=(
                                                        "bi bi-folder2-open "
                                                        "me-2"
                                                    )
                                                ),
                                                "Se connecter",
                                            ],
                                            className="v3-btn-primary",
                                        ),
                                        href="/login",
                                    ),

                                    dcc.Link(
                                        dbc.Button(
                                            [
                                                html.I(
                                                    className=(
                                                        "bi bi-cloud-arrow-up "
                                                        "me-2"
                                                    )
                                                ),
                                                "Créer un compte",
                                            ],
                                            className="v3-btn-secondary",
                                        ),
                                        href="/register",
                                    ),
                                ],
                                className="d-flex flex-wrap gap-3 mt-4",
                            ),
                        ],
                        lg=7,
                        className="pe-lg-5",
                    ),

                    dbc.Col(
                        html.Div(
                            html.Img(
                                src=(
                                    "/assets/images/"
                                    "emidaf_senegal_education.png"
                                ),
                                alt=(
                                    "Élèves et étudiants autour "
                                    "des sciences des données "
                                    "et de la carte du Sénégal"
                                ),
                                className="v3-hero-senegal-image",
                            ),
                            className="v3-hero-senegal-visual",
                        ),
                        lg=5,
                        className=(
                            "d-none d-lg-flex "
                            "align-items-center "
                            "justify-content-center"
                        ),
                    ),
                ],
                className="g-4 align-items-center",
            ),
            className="v3-hero",
        ),

        # ==================================================
        # PARCOURS
        # ==================================================

        html.Section(
            [
                html.Div(
                    [
                        html.Div(
                            "PARCOURS ANALYTIQUE EMIDAF",
                            className="v3-section-eyebrow",
                        ),

                        html.H2(
                            "Du jeu de données à la décision",
                            className="v3-section-title",
                        ),

                        html.P(
                            (
                                "Un parcours scientifique continu "
                                "en neuf étapes, de l'acquisition "
                                "des données jusqu'à la restitution."
                            ),
                            className="v3-section-description",
                        ),
                    ],
                    className="v3-section-heading",
                ),

                html.Div(
                    [
                        _workflow_step(
                            "01",
                            "bi-cloud-arrow-up",
                            "Importation",
                            "Acquisition",
                            "/import",
                        ),

                        _workflow_step(
                            "02",
                            "bi-search",
                            "Inspection",
                            "Qualité",
                            "/inspection",
                        ),

                        _workflow_step(
                            "03",
                            "bi-sliders",
                            "Prétraitement",
                            "Préparation",
                            "/eidpp",
                        ),

                        _workflow_step(
                            "04",
                            "bi-bar-chart-line",
                            "Exploration",
                            "Analyse",
                            "/elae",
                        ),

                        _workflow_step(
                            "05",
                            "bi-diagram-3",
                            "Connaissances",
                            "Découverte",
                            "/ekde",
                        ),

                        _workflow_step(
                            "06",
                            "bi-graph-up-arrow",
                            "Modélisation",
                            "Prédiction",
                            "/eaie",
                        ),

                        _workflow_step(
                            "07",
                            "bi-eye",
                            "Explicabilité",
                            "Interprétation",
                            "/exaie",
                        ),

                        _workflow_step(
                            "08",
                            "bi-compass",
                            "Décision",
                            "Scénarios",
                            "/edse",
                        ),

                        _workflow_step(
                            "09",
                            "bi-file-earmark-text",
                            "Rapports",
                            "Restitution",
                            "/reports",
                        ),
                    ],
                    className="v3-workflow-chain",
                ),
            ],
            className="v3-section",
        ),

        # ==================================================
        # CAPACITÉS
        # ==================================================

        html.Section(
            [
                html.Div(
                    [
                        html.Div(
                            "CAPACITÉS SCIENTIFIQUES",
                            className="v3-section-eyebrow",
                        ),

                        html.H2(
                            "Un environnement scientifique intégré",
                            className="v3-section-title",
                        ),

                        html.P(
                            (
                                "Quatre dimensions complémentaires "
                                "structurent l'exploitation scientifique "
                                "des données dans EMIDAF."
                            ),
                            className="v3-section-description",
                        ),
                    ],
                    className="v3-section-heading",
                ),

                html.Div(
                    [
                        _capability(
                            "01",
                            "bi-database-check",
                            "Qualité des données",
                            (
                                "Inspection, valeurs manquantes, "
                                "valeurs aberrantes et préparation."
                            ),
                            "/inspection",
                        ),

                        _capability(
                            "02",
                            "bi-bar-chart-line",
                            "Analyse & connaissances",
                            (
                                "Exploration statistique, structures "
                                "latentes et découverte de connaissances."
                            ),
                            "/elae",
                        ),

                        _capability(
                            "03",
                            "bi-cpu",
                            "Modélisation",
                            (
                                "Construction, comparaison et sélection "
                                "de modèles prédictifs."
                            ),
                            "/eaie",
                        ),

                        _capability(
                            "04",
                            "bi-eye",
                            "Interprétation & décision",
                            (
                                "Explicabilité, scénarios et aide "
                                "à la décision humaine."
                            ),
                            "/exaie",
                        ),
                    ],
                    className="v3-capability-chain",
                ),
            ],
            className="v3-section",
        ),

        # ==================================================
        # À PROPOS + PROFIL
        # ==================================================

        html.Section(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                "À PROPOS D'EMIDAF",
                                className="v3-section-eyebrow",
                            ),

                            html.H2(
                                (
                                    "Recherche, enseignement et "
                                    "science des données."
                                ),
                                className="v3-section-title",
                            ),

                            html.P(
                                (
                                    "EMIDAF Research Lab est un "
                                    "environnement scientifique conçu "
                                    "pour structurer le cycle analytique, "
                                    "de la donnée brute jusqu'à "
                                    "l'interprétation et la restitution."
                                ),
                                className="v3-about-text",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.I(
                                                className=(
                                                    "bi bi-check-circle"
                                                )
                                            ),
                                            "Analyse structurée",
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.I(
                                                className=(
                                                    "bi bi-check-circle"
                                                )
                                            ),
                                            "Traçabilité",
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.I(
                                                className=(
                                                    "bi bi-check-circle"
                                                )
                                            ),
                                            "Interprétation scientifique",
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.I(
                                                className=(
                                                    "bi bi-check-circle"
                                                )
                                            ),
                                            "Aide à la décision humaine",
                                        ]
                                    ),
                                ],
                                className="v3-about-points",
                            ),
                        ],
                        lg=6,
                    ),

                    dbc.Col(
                        html.Div(
                            [
                                html.Img(
                                    src=PROFILE_PHOTO,
                                    alt="Abdoulaye Wakhab DIOP",
                                    className="v3-profile-photo",
                                ),

                                html.Div(
                                    [
                                        html.Div(
                                            (
                                                "CONCEPTEUR "
                                                "ET PROPRIÉTAIRE"
                                            ),
                                            className="v3-profile-role",
                                        ),

                                        html.H3(
                                            "Abdoulaye Wakhab DIOP",
                                            className="v3-profile-name",
                                        ),

                                        html.Div(
                                            [
                                                _badge(
                                                    "Enseignant & chercheur"
                                                ),
                                                _badge(
                                                    "Data Science"
                                                ),
                                                _badge(
                                                    "Intelligence Artificielle"
                                                ),
                                                _badge(
                                                    "Mathématiques appliquées"
                                                ),
                                                _badge(
                                                    "Informatique"
                                                ),
                                            ],
                                            className="v3-badge-list",
                                        ),

                                        html.P(
                                            (
                                                "EMIDAF Research Lab a été "
                                                "conçu et développé dans "
                                                "le cadre de mes travaux "
                                                "de thèse."
                                            ),
                                            className="v3-profile-text",
                                        ),

                                        html.Div(
                                            [
                                                _social(
                                                    "bi-linkedin",
                                                    "LinkedIn",
                                                    SOCIAL_LINKS[
                                                        "linkedin"
                                                    ],
                                                    "linkedin",
                                                ),
                                                _social(
                                                    "bi-youtube",
                                                    "YouTube",
                                                    SOCIAL_LINKS[
                                                        "youtube"
                                                    ],
                                                    "youtube",
                                                ),
                                                _social(
                                                    "bi-envelope",
                                                    "E-mail",
                                                    SOCIAL_LINKS[
                                                        "email"
                                                    ],
                                                    "email",
                                                ),
                                            ],
                                            className="v3-social-list",
                                        ),
                                    ]
                                ),
                            ],
                            className="v3-profile-card",
                        ),
                        lg=6,
                    ),
                ],
                className="g-5 align-items-center",
            ),
            className="v3-about-section",
        ),

        # ==================================================
        # FOOTER
        # ==================================================

        html.Footer(
            [
                html.Div(
                    [
                        html.Div(
                            "EMIDAF Research Lab",
                            className="v3-footer-brand",
                        ),
                        html.Div(
                            (
                                "Environnement scientifique "
                                "d'analyse de données et "
                                "d'intelligence artificielle"
                            ),
                            className="v3-footer-text",
                        ),
                    ]
                ),

                html.Div(
                    "© 2026 EMIDAF Research Lab — Abdoulaye Wakhab DIOP",
                    className="v3-footer-copy",
                ),
            ],
            className="v3-footer",
        ),
    ],
    className="emidaf-home-v3",
)
