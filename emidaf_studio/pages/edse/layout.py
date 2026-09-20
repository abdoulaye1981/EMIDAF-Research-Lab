from dash import dcc, html
import dash_bootstrap_components as dbc

from emidaf_studio.pages.inspection.layout import load_dataset
from emidaf_studio.services.model_registry import get_eaie_run


def edse_layout(project_id, dataset_id):

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
                                    "EDSE",
                                    className="edse-v2-kicker",
                                ),
                                html.Span(
                                    "AIDE À LA DÉCISION",
                                    className="edse-v2-eyebrow",
                                ),
                            ],
                            className=(
                                "d-flex align-items-center "
                                "gap-2 mb-3"
                            ),
                        ),

                        html.H1(
                            "Aide à la décision",
                            className="edse-v2-title",
                        ),

                        html.P(
                            (
                                "Le jeu de données ne peut pas "
                                "être chargé dans son état actuel."
                            ),
                            className="edse-v2-subtitle",
                        ),
                    ],
                    className="edse-v2-hero",
                ),

                dbc.Alert(
                    result,
                    color="danger",
                    className="mt-4",
                ),
            ],
            fluid=True,
            className="edse-v2-page",
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
                                            "EDSE",
                                            className="edse-v2-kicker",
                                        ),
                                        html.Span(
                                            "AIDE À LA DÉCISION",
                                            className="edse-v2-eyebrow",
                                        ),
                                    ],
                                    className=(
                                        "d-flex align-items-center "
                                        "gap-2 mb-3"
                                    ),
                                ),

                                html.H1(
                                    "Aide à la décision",
                                    className="edse-v2-title",
                                ),

                                html.P(
                                    (
                                        "Explorez des scénarios construits "
                                        "à partir d'un modèle prédictif "
                                        "déjà sélectionné dans EAIE."
                                    ),
                                    className="edse-v2-subtitle",
                                ),
                            ]
                        ),

                        html.Div(
                            html.I(
                                className=(
                                    "bi bi-signpost-split "
                                    "edse-v2-hero-icon"
                                )
                            ),
                            className="edse-v2-hero-icon-box",
                        ),
                    ],
                    className="edse-v2-hero",
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
                            "label": "EDSE",
                            "active": True,
                        },
                    ],
                    className="edse-v2-breadcrumb",
                ),

                html.Div(
                    [
                        html.Div(
                            html.I(
                                className=(
                                    "bi bi-exclamation-triangle"
                                )
                            ),
                            className="edse-v2-empty-icon",
                        ),

                        html.H2(
                            "Aucun modèle disponible",
                            className="edse-v2-empty-title",
                        ),

                        html.P(
                            (
                                "EDSE nécessite un modèle déjà "
                                "entraîné et sélectionné dans EAIE "
                                "avant de pouvoir construire "
                                "un scénario d'aide à la décision."
                            ),
                            className="edse-v2-empty-text",
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
                            className="edse-v2-primary-link",
                        ),
                    ],
                    className="edse-v2-empty-state",
                ),
            ],
            fluid=True,
            className="edse-v2-page",
        )

    # ======================================================
    # INFORMATIONS DU MODÈLE
    # ======================================================

    task = context.get(
        "task",
        "Non disponible",
    )

    model_name = context.get(
        "model_name",
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

    X_test = context["X_test"]

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
    # SEUIL INITIAL
    # ======================================================

    try:

        predictions = context[
            "estimator"
        ].predict(
            X_test
        )

        if task == "classification":
            default_threshold = 0.50
        else:
            default_threshold = float(
                sum(predictions)
                / len(predictions)
            )

    except Exception:

        default_threshold = (
            0.50
            if task == "classification"
            else 0.0
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
                                        "EDSE",
                                        className="edse-v2-kicker",
                                    ),

                                    html.Span(
                                        "AIDE À LA DÉCISION",
                                        className="edse-v2-eyebrow",
                                    ),
                                ],
                                className=(
                                    "d-flex align-items-center "
                                    "gap-2 mb-3"
                                ),
                            ),

                            html.H1(
                                "Explorer des scénarios décisionnels",
                                className="edse-v2-title",
                            ),

                            html.P(
                                (
                                    "Analysez des scénarios construits "
                                    "à partir du modèle prédictif afin "
                                    "d'éclairer la décision sans la "
                                    "remplacer."
                                ),
                                className="edse-v2-subtitle",
                            ),
                        ]
                    ),

                    html.Div(
                        html.I(
                            className=(
                                "bi bi-signpost-split "
                                "edse-v2-hero-icon"
                            )
                        ),
                        className="edse-v2-hero-icon-box",
                    ),
                ],
                className="edse-v2-hero",
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
                        "label": "EDSE",
                        "active": True,
                    },
                ],
                className="edse-v2-breadcrumb",
            ),

            # --------------------------------------------------
            # PRINCIPE MÉTHODOLOGIQUE
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        html.I(
                            className="bi bi-info-circle"
                        ),
                        className="edse-v2-method-icon",
                    ),

                    html.Div(
                        [
                            html.Div(
                                "PRINCIPE MÉTHODOLOGIQUE",
                                className="edse-v2-method-label",
                            ),

                            html.P(
                                (
                                    "EDSE fournit une aide à l'analyse "
                                    "de scénarios. Il ne prend pas "
                                    "automatiquement la décision à la "
                                    "place de l'utilisateur. Le seuil "
                                    "utilisé doit être justifié par le "
                                    "contexte métier ou scientifique."
                                ),
                                className="edse-v2-method-text",
                            ),
                        ]
                    ),
                ],
                className="edse-v2-method-card",
            ),

            # --------------------------------------------------
            # MODÈLE ACTIF
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        "MODÈLE ACTIF",
                        className="edse-v2-section-kicker",
                    ),

                    html.H2(
                        "Contexte du scénario",
                        className="edse-v2-section-title",
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className="bi bi-cpu"
                                        ),
                                        className="edse-v2-stat-icon",
                                    ),
                                    html.Div(
                                        "Modèle",
                                        className="edse-v2-stat-label",
                                    ),
                                    html.Div(
                                        str(model_name),
                                        className="edse-v2-stat-value",
                                    ),
                                ],
                                className="edse-v2-stat-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className="bi bi-diagram-2"
                                        ),
                                        className="edse-v2-stat-icon",
                                    ),
                                    html.Div(
                                        "Tâche",
                                        className="edse-v2-stat-label",
                                    ),
                                    html.Div(
                                        task_label,
                                        className="edse-v2-stat-value",
                                    ),
                                ],
                                className="edse-v2-stat-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className="bi bi-bullseye"
                                        ),
                                        className="edse-v2-stat-icon",
                                    ),
                                    html.Div(
                                        "Variable cible",
                                        className="edse-v2-stat-label",
                                    ),
                                    html.Div(
                                        str(target),
                                        className="edse-v2-stat-value",
                                    ),
                                ],
                                className="edse-v2-stat-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className="bi bi-list-ol"
                                        ),
                                        className="edse-v2-stat-icon",
                                    ),
                                    html.Div(
                                        "Observations",
                                        className="edse-v2-stat-label",
                                    ),
                                    html.Div(
                                        str(len(X_test)),
                                        className="edse-v2-stat-value",
                                    ),
                                ],
                                className="edse-v2-stat-card",
                            ),
                        ],
                        className="edse-v2-stats",
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "Validation croisée",
                                        className="edse-v2-score-label",
                                    ),
                                    html.Div(
                                        cv_text,
                                        className="edse-v2-score-value",
                                    ),
                                ],
                                className="edse-v2-score-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "Score test",
                                        className="edse-v2-score-label",
                                    ),
                                    html.Div(
                                        test_text,
                                        className="edse-v2-score-value",
                                    ),
                                ],
                                className="edse-v2-score-card",
                            ),
                        ],
                        className="edse-v2-scores",
                    ),
                ],
                className="edse-v2-section",
            ),

            # --------------------------------------------------
            # CONFIGURATION DU SCÉNARIO
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                "CONFIGURATION",
                                className="edse-v2-section-kicker",
                            ),

                            html.H2(
                                "Définir le scénario",
                                className="edse-v2-section-title",
                            ),

                            html.P(
                                (
                                    "Le seuil ci-dessous constitue "
                                    "un paramètre de scénario défini "
                                    "par l'utilisateur. Il n'est pas "
                                    "présenté comme un seuil optimal."
                                ),
                                className="edse-v2-section-subtitle",
                            ),
                        ],
                        className="edse-v2-section-heading",
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    dbc.Label(
                                        "Seuil du scénario",
                                        html_for="edse-threshold",
                                        className="edse-v2-label",
                                    ),

                                    dbc.Input(
                                        id="edse-threshold",
                                        type="number",
                                        value=default_threshold,
                                        step=0.01,
                                        className="edse-v2-input",
                                    ),

                                    html.Div(
                                        (
                                            "Ce seuil doit être justifié "
                                            "par le contexte métier, "
                                            "scientifique ou opérationnel."
                                        ),
                                        className="edse-v2-help",
                                    ),
                                ],
                                className="edse-v2-field",
                            ),

                            html.Div(
                                [
                                    dbc.Label(
                                        "Sens du critère",
                                        html_for="edse-direction",
                                        className="edse-v2-label",
                                    ),

                                    dcc.Dropdown(
                                        id="edse-direction",
                                        options=[
                                            {
                                                "label": (
                                                    "Supérieur ou égal "
                                                    "au seuil"
                                                ),
                                                "value": "above",
                                            },
                                            {
                                                "label": (
                                                    "Inférieur ou égal "
                                                    "au seuil"
                                                ),
                                                "value": "below",
                                            },
                                        ],
                                        value="above",
                                        clearable=False,
                                        disabled=(
                                            task == "classification"
                                        ),
                                        className="edse-v2-dropdown",
                                    ),

                                    html.Div(
                                        (
                                            "Pour une classification, "
                                            "le sens du critère est "
                                            "déterminé par le scénario "
                                            "de classification."
                                        ),
                                        className="edse-v2-help",
                                    ),
                                ],
                                className="edse-v2-field",
                            ),
                        ],
                        className="edse-v2-config-grid",
                    ),

                    html.Div(
                        [
                            dbc.Button(
                                [
                                    html.I(
                                        className=(
                                            "bi bi-play-fill me-2"
                                        )
                                    ),
                                    "Analyser le scénario",
                                ],
                                id="edse-run",
                                className="edse-v2-run-button",
                            ),

                            dbc.Spinner(
                                html.Div(
                                    id="edse-status",
                                    className="edse-v2-status",
                                )
                            ),
                        ],
                        className="edse-v2-run-area",
                    ),
                ],
                className="edse-v2-config-section",
            ),

            # --------------------------------------------------
            # RÉSULTATS
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        "RÉSULTATS",
                        className="edse-v2-section-kicker",
                    ),

                    html.H2(
                        "Analyse du scénario",
                        className="edse-v2-section-title",
                    ),

                    html.P(
                        (
                            "Les résultats ci-dessous décrivent "
                            "le scénario construit à partir du "
                            "modèle et du seuil choisi."
                        ),
                        className="edse-v2-section-subtitle",
                    ),

                    dbc.Tabs(
                        [
                            dbc.Tab(
                                html.Div(
                                    id="edse-summary",
                                    className="edse-v2-tab-content",
                                ),
                                label="Synthèse",
                                tab_id="edse-tab-summary",
                            ),

                            dbc.Tab(
                                html.Div(
                                    id="edse-scenario",
                                    className="edse-v2-tab-content",
                                ),
                                label="Scénario",
                                tab_id="edse-tab-scenario",
                            ),

                            dbc.Tab(
                                html.Div(
                                    id="edse-profiles",
                                    className="edse-v2-tab-content",
                                ),
                                label="Profils",
                                tab_id="edse-tab-profiles",
                            ),
                        ],
                        active_tab="edse-tab-summary",
                        className="edse-v2-tabs",
                    ),
                ],
                className="edse-v2-results-section",
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
                                        className="edse-v2-section-kicker",
                                    ),

                                    html.H2(
                                        "Poursuivre la restitution",
                                        className="edse-v2-section-title",
                                    ),

                                    html.P(
                                        (
                                            "Revenez vers EXAIE pour "
                                            "l'interprétation du modèle "
                                            "ou poursuivez vers les rapports."
                                        ),
                                        className="edse-v2-section-subtitle",
                                    ),
                                ]
                            ),

                            html.Div(
                                [
                                    dcc.Link(
                                        [
                                            html.I(
                                                className=(
                                                    "bi bi-arrow-left me-2"
                                                )
                                            ),
                                            "EXAIE",
                                        ],
                                        href=(
                                            f"/projects/{project_id}"
                                            f"/datasets/{dataset_id}/exaie"
                                        ),
                                        className="edse-v2-secondary-link",
                                    ),

                                    dcc.Link(
                                        [
                                            "Rapports",
                                            html.I(
                                                className=(
                                                    "bi bi-arrow-right ms-2"
                                                )
                                            ),
                                        ],
                                        href=(
                                            f"/projects/{project_id}"
                                            f"/datasets/{dataset_id}/reports"
                                        ),
                                        className="edse-v2-primary-link",
                                    ),
                                ],
                                className="edse-v2-actions",
                            ),
                        ],
                        className="edse-v2-next-card",
                    ),
                ],
                className="edse-v2-next-section",
            ),

            # --------------------------------------------------
            # STORES
            # --------------------------------------------------

            dcc.Store(
                id="edse-project-id",
                data=int(project_id),
            ),

            dcc.Store(
                id="edse-dataset-id",
                data=int(dataset_id),
            ),
        ],
        fluid=True,
        className="edse-v2-page",
    )
