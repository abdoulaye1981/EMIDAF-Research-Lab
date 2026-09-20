from dash import dcc, html
import dash_bootstrap_components as dbc

from emidaf_studio.pages.inspection.layout import load_dataset
from emidaf_studio.services.model_registry import get_eaie_run


def exaie_layout(project_id, dataset_id):

    project, dataset, result = load_dataset(
        project_id,
        dataset_id,
    )

    # ======================================================
    # ERREUR DE CHARGEMENT
    # ======================================================

    if isinstance(result, str):

        return dbc.Container(
            [
                html.Section(
                    [
                        html.Div(
                            [
                                html.Span(
                                    "EXAIE",
                                    className="exaie-v2-kicker",
                                ),
                                html.Span(
                                    "EXPLICABILITÉ",
                                    className="exaie-v2-eyebrow",
                                ),
                            ],
                            className=(
                                "d-flex align-items-center "
                                "gap-2 mb-3"
                            ),
                        ),

                        html.H1(
                            "Explicabilité des modèles",
                            className="exaie-v2-title",
                        ),

                        html.P(
                            (
                                "Le jeu de données ne peut pas "
                                "être chargé dans son état actuel."
                            ),
                            className="exaie-v2-subtitle",
                        ),
                    ],
                    className="exaie-v2-hero",
                ),

                dbc.Alert(
                    result,
                    color="danger",
                    className="mt-4",
                ),
            ],
            fluid=True,
            className="exaie-v2-page",
        )

    # ======================================================
    # CONTEXTE EAIE
    # ======================================================

    context = get_eaie_run(
        project_id,
        dataset_id,
    )

    # ======================================================
    # AUCUN MODÈLE DISPONIBLE
    # ======================================================

    if context is None:

        return dbc.Container(
            [
                html.Section(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            "EXAIE",
                                            className=(
                                                "exaie-v2-kicker"
                                            ),
                                        ),
                                        html.Span(
                                            "EXPLICABILITÉ",
                                            className=(
                                                "exaie-v2-eyebrow"
                                            ),
                                        ),
                                    ],
                                    className=(
                                        "d-flex align-items-center "
                                        "gap-2 mb-3"
                                    ),
                                ),

                                html.H1(
                                    "Explicabilité des modèles",
                                    className="exaie-v2-title",
                                ),

                                html.P(
                                    (
                                        "Interprétez le comportement "
                                        "du modèle sélectionné par EAIE."
                                    ),
                                    className="exaie-v2-subtitle",
                                ),
                            ]
                        ),

                        html.Div(
                            html.I(
                                className=(
                                    "bi bi-eye "
                                    "exaie-v2-hero-icon"
                                )
                            ),
                            className=(
                                "exaie-v2-hero-icon-box"
                            ),
                        ),
                    ],
                    className="exaie-v2-hero",
                ),

                dbc.Breadcrumb(
                    items=[
                        {
                            "label": "Projets",
                            "href": "/projects",
                        },
                        {
                            "label": project.name,
                            "href": f"/projects/{project_id}",
                        },
                        {
                            "label": dataset.name,
                            "href": (
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}"
                            ),
                        },
                        {
                            "label": "EXAIE",
                            "active": True,
                        },
                    ],
                    className="exaie-v2-breadcrumb",
                ),

                html.Div(
                    [
                        html.Div(
                            html.I(
                                className=(
                                    "bi bi-exclamation-triangle"
                                )
                            ),
                            className=(
                                "exaie-v2-empty-icon"
                            ),
                        ),

                        html.H2(
                            "Aucun modèle disponible",
                            className=(
                                "exaie-v2-empty-title"
                            ),
                        ),

                        html.P(
                            (
                                "EXAIE explique uniquement un "
                                "modèle déjà entraîné et sélectionné "
                                "dans EAIE. Lancez d'abord la "
                                "modélisation prédictive."
                            ),
                            className=(
                                "exaie-v2-empty-text"
                            ),
                        ),

                        dcc.Link(
                            [
                                html.I(
                                    className=(
                                        "bi bi-arrow-left me-2"
                                    )
                                ),
                                "Ouvrir EAIE",
                            ],
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/eaie"
                            ),
                            className=(
                                "exaie-v2-primary-link"
                            ),
                        ),
                    ],
                    className="exaie-v2-empty-state",
                ),
            ],
            fluid=True,
            className="exaie-v2-page",
        )

    # ======================================================
    # INFORMATIONS DU MODÈLE
    # ======================================================

    model_name = context.get(
        "model_name",
        "Non disponible",
    )

    task = context.get(
        "task",
        "Non disponible",
    )

    target = context.get(
        "target",
        "Non disponible",
    )

    cv_mean = context.get("cv_mean")
    test_score = context.get("test_score")

    cv_text = (
        "Non disponible"
        if cv_mean is None
        else f"{cv_mean:.4f}"
    )

    test_text = (
        "Non disponible"
        if test_score is None
        else f"{test_score:.4f}"
    )

    test_size = len(
        context["X_test"]
    )

    task_label = (
        "Régression"
        if task == "regression"
        else (
            "Classification"
            if task == "classification"
            else str(task)
        )
    )

    # ======================================================
    # PAGE
    # ======================================================

    return dbc.Container(
        [
            # --------------------------------------------------
            # HERO
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span(
                                        "EXAIE",
                                        className="exaie-v2-kicker",
                                    ),
                                    html.Span(
                                        "EXPLICABILITÉ DES MODÈLES",
                                        className="exaie-v2-eyebrow",
                                    ),
                                ],
                                className=(
                                    "d-flex align-items-center "
                                    "gap-2 mb-3"
                                ),
                            ),

                            html.H1(
                                "Comprendre le modèle prédictif",
                                className="exaie-v2-title",
                            ),

                            html.P(
                                (
                                    "Analysez les facteurs associés "
                                    "aux prédictions du modèle "
                                    "sélectionné par EAIE, à l'échelle "
                                    "globale et locale."
                                ),
                                className="exaie-v2-subtitle",
                            ),
                        ]
                    ),

                    html.Div(
                        html.I(
                            className=(
                                "bi bi-eye "
                                "exaie-v2-hero-icon"
                            )
                        ),
                        className=(
                            "exaie-v2-hero-icon-box"
                        ),
                    ),
                ],
                className="exaie-v2-hero",
            ),

            # --------------------------------------------------
            # BREADCRUMB
            # --------------------------------------------------

            dbc.Breadcrumb(
                items=[
                    {
                        "label": "Projets",
                        "href": "/projects",
                    },
                    {
                        "label": project.name,
                        "href": f"/projects/{project_id}",
                    },
                    {
                        "label": dataset.name,
                        "href": (
                            f"/projects/{project_id}"
                            f"/datasets/{dataset_id}"
                        ),
                    },
                    {
                        "label": "EXAIE",
                        "active": True,
                    },
                ],
                className="exaie-v2-breadcrumb",
            ),

            # --------------------------------------------------
            # PRINCIPE SCIENTIFIQUE
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        html.I(
                            className="bi bi-info-circle"
                        ),
                        className=(
                            "exaie-v2-method-icon"
                        ),
                    ),

                    html.Div(
                        [
                            html.Div(
                                "PRINCIPE MÉTHODOLOGIQUE",
                                className=(
                                    "exaie-v2-method-label"
                                ),
                            ),

                            html.P(
                                (
                                    "EXAIE explique le modèle "
                                    "sélectionné par EAIE. Les "
                                    "importances décrivent des "
                                    "dépendances prédictives et "
                                    "ne démontrent pas de causalité."
                                ),
                                className=(
                                    "exaie-v2-method-text"
                                ),
                            ),
                        ]
                    ),
                ],
                className="exaie-v2-method-card",
            ),

            # --------------------------------------------------
            # MODÈLE ACTIF
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        "MODÈLE ACTIF",
                        className="exaie-v2-section-kicker",
                    ),

                    html.H2(
                        "Contexte de l'explication",
                        className="exaie-v2-section-title",
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-cpu"
                                            )
                                        ),
                                        className=(
                                            "exaie-v2-stat-icon"
                                        ),
                                    ),
                                    html.Div(
                                        "Modèle",
                                        className=(
                                            "exaie-v2-stat-label"
                                        ),
                                    ),
                                    html.Div(
                                        str(model_name),
                                        className=(
                                            "exaie-v2-stat-value"
                                        ),
                                    ),
                                ],
                                className="exaie-v2-stat-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-diagram-2"
                                            )
                                        ),
                                        className=(
                                            "exaie-v2-stat-icon"
                                        ),
                                    ),
                                    html.Div(
                                        "Tâche",
                                        className=(
                                            "exaie-v2-stat-label"
                                        ),
                                    ),
                                    html.Div(
                                        task_label,
                                        className=(
                                            "exaie-v2-stat-value"
                                        ),
                                    ),
                                ],
                                className="exaie-v2-stat-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-bullseye"
                                            )
                                        ),
                                        className=(
                                            "exaie-v2-stat-icon"
                                        ),
                                    ),
                                    html.Div(
                                        "Variable cible",
                                        className=(
                                            "exaie-v2-stat-label"
                                        ),
                                    ),
                                    html.Div(
                                        str(target),
                                        className=(
                                            "exaie-v2-stat-value"
                                        ),
                                    ),
                                ],
                                className="exaie-v2-stat-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-list-ol"
                                            )
                                        ),
                                        className=(
                                            "exaie-v2-stat-icon"
                                        ),
                                    ),
                                    html.Div(
                                        "Observations expliquées",
                                        className=(
                                            "exaie-v2-stat-label"
                                        ),
                                    ),
                                    html.Div(
                                        str(test_size),
                                        className=(
                                            "exaie-v2-stat-value"
                                        ),
                                    ),
                                ],
                                className="exaie-v2-stat-card",
                            ),
                        ],
                        className="exaie-v2-stats",
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "Validation croisée",
                                        className=(
                                            "exaie-v2-score-label"
                                        ),
                                    ),
                                    html.Div(
                                        cv_text,
                                        className=(
                                            "exaie-v2-score-value"
                                        ),
                                    ),
                                ],
                                className="exaie-v2-score-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "Score test final",
                                        className=(
                                            "exaie-v2-score-label"
                                        ),
                                    ),
                                    html.Div(
                                        test_text,
                                        className=(
                                            "exaie-v2-score-value"
                                        ),
                                    ),
                                ],
                                className="exaie-v2-score-card",
                            ),
                        ],
                        className="exaie-v2-scores",
                    ),
                ],
                className="exaie-v2-section",
            ),

            # --------------------------------------------------
            # LANCEMENT
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "ANALYSE",
                                        className=(
                                            "exaie-v2-section-kicker"
                                        ),
                                    ),

                                    html.H2(
                                        "Lancer l'explicabilité",
                                        className=(
                                            "exaie-v2-section-title"
                                        ),
                                    ),

                                    html.P(
                                        (
                                            "EXAIE exploite le modèle "
                                            "déjà sélectionné. Aucun "
                                            "réentraînement n'est effectué."
                                        ),
                                        className=(
                                            "exaie-v2-section-subtitle"
                                        ),
                                    ),
                                ]
                            ),

                            dbc.Button(
                                [
                                    html.I(
                                        className=(
                                            "bi bi-play-fill me-2"
                                        )
                                    ),
                                    "Lancer l'explication",
                                ],
                                id="exaie-run",
                                className=(
                                    "exaie-v2-run-button"
                                ),
                            ),
                        ],
                        className="exaie-v2-run-header",
                    ),

                    dbc.Spinner(
                        html.Div(
                            id="exaie-status",
                            className="exaie-v2-status",
                        )
                    ),
                ],
                className="exaie-v2-run-section",
            ),

            # --------------------------------------------------
            # RÉSULTATS
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        "RÉSULTATS EXPLICATIFS",
                        className="exaie-v2-section-kicker",
                    ),

                    html.H2(
                        "Interprétation du modèle",
                        className="exaie-v2-section-title",
                    ),

                    html.P(
                        (
                            "Comparez les différentes formes "
                            "d'explication disponibles."
                        ),
                        className=(
                            "exaie-v2-section-subtitle"
                        ),
                    ),

                    dbc.Tabs(
                        [
                            dbc.Tab(
                                html.Div(
                                    id="exaie-summary",
                                    className=(
                                        "exaie-v2-tab-content"
                                    ),
                                ),
                                label="Synthèse",
                                tab_id="exaie-tab-summary",
                            ),

                            dbc.Tab(
                                html.Div(
                                    id="exaie-native",
                                    className=(
                                        "exaie-v2-tab-content"
                                    ),
                                ),
                                label="Importance globale",
                                tab_id="exaie-tab-native",
                            ),

                            dbc.Tab(
                                html.Div(
                                    id="exaie-permutation",
                                    className=(
                                        "exaie-v2-tab-content"
                                    ),
                                ),
                                label="Importance par permutation",
                                tab_id="exaie-tab-permutation",
                            ),

                            dbc.Tab(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    dbc.Label(
                                                        (
                                                            "Observation "
                                                            "à expliquer"
                                                        ),
                                                        className=(
                                                            "exaie-v2-label"
                                                        ),
                                                    ),

                                                    dcc.Dropdown(
                                                        id="exaie-row",
                                                        options=[
                                                            {
                                                                "label": (
                                                                    "Observation "
                                                                    f"{i}"
                                                                ),
                                                                "value": i,
                                                            }
                                                            for i in range(
                                                                test_size
                                                            )
                                                        ],
                                                        value=0,
                                                        clearable=False,
                                                        className=(
                                                            "exaie-v2-dropdown"
                                                        ),
                                                    ),
                                                ],
                                                className=(
                                                    "exaie-v2-local-selector"
                                                ),
                                            ),

                                            html.Div(
                                                id="exaie-local",
                                                className=(
                                                    "exaie-v2-local-result"
                                                ),
                                            ),
                                        ],
                                        className=(
                                            "exaie-v2-tab-content"
                                        ),
                                    ),
                                ],
                                label="Explication locale",
                                tab_id="exaie-tab-local",
                            ),
                        ],
                        active_tab="exaie-tab-summary",
                        className="exaie-v2-tabs",
                    ),
                ],
                className="exaie-v2-results-section",
            ),

            # --------------------------------------------------
            # NAVIGATION
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "CYCLE ANALYTIQUE",
                                        className=(
                                            "exaie-v2-section-kicker"
                                        ),
                                    ),

                                    html.H2(
                                        "Poursuivre l'analyse",
                                        className=(
                                            "exaie-v2-section-title"
                                        ),
                                    ),
                                ]
                            ),

                            html.Div(
                                [
                                    dcc.Link(
                                        [
                                            html.I(
                                                className=(
                                                    "bi bi-arrow-left "
                                                    "me-2"
                                                )
                                            ),
                                            "EAIE",
                                        ],
                                        href=(
                                            f"/projects/{project_id}"
                                            f"/datasets/{dataset_id}/eaie"
                                        ),
                                        className=(
                                            "exaie-v2-secondary-link"
                                        ),
                                    ),

                                    dcc.Link(
                                        [
                                            "EDSE",
                                            html.I(
                                                className=(
                                                    "bi bi-arrow-right "
                                                    "ms-2"
                                                )
                                            ),
                                        ],
                                        href=(
                                            f"/projects/{project_id}"
                                            f"/datasets/{dataset_id}/edse"
                                        ),
                                        className=(
                                            "exaie-v2-primary-link"
                                        ),
                                    ),
                                ],
                                className="exaie-v2-actions",
                            ),
                        ],
                        className="exaie-v2-next-card",
                    ),
                ],
                className="exaie-v2-next-section",
            ),

            # --------------------------------------------------
            # STORES
            # --------------------------------------------------

            dcc.Store(
                id="exaie-project-id",
                data=int(project_id),
            ),

            dcc.Store(
                id="exaie-dataset-id",
                data=int(dataset_id),
            ),
        ],
        fluid=True,
        className="exaie-v2-page",
    )
