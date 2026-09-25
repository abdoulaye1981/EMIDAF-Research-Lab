from __future__ import annotations

import logging

from dash import (
    Input,
    Output,
    State,
    callback,
    html,
    no_update,
)

import dash_bootstrap_components as dbc

from emidaf_studio.services.model_registry import (
    get_eaie_run,
    register_analysis,
)


logger = logging.getLogger(__name__)


def _table(dataframe):

    if (
        dataframe is None
        or dataframe.empty
    ):
        return dbc.Alert(
            "Aucun résultat disponible.",
            color="secondary",
        )

    return dbc.Table.from_dataframe(
        dataframe.round(4),
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        size="sm",
    )


@callback(
    Output("edse-status", "children"),
    Output("edse-summary", "children"),
    Output("edse-scenario", "children"),
    Output("edse-profiles", "children"),

    Input("edse-run", "n_clicks"),

    State("edse-threshold", "value"),
    State("edse-direction", "value"),
    State("edse-project-id", "data"),
    State("edse-dataset-id", "data"),

    prevent_initial_call=True,
)
def run_edse(
    n_clicks,
    threshold,
    direction,
    project_id,
    dataset_id,
):

    if not n_clicks:

        return (
            no_update,
            no_update,
            no_update,
            no_update,
        )

    if threshold is None:

        message = dbc.Alert(
            "Veuillez définir un seuil.",
            color="warning",
        )

        return (
            message,
            "",
            "",
            "",
        )

    context = get_eaie_run(
        project_id,
        dataset_id,
    )

    if context is None:

        message = dbc.Alert(
            (
                "Aucun modèle EAIE n'est disponible "
                "pour ce jeu de données."
            ),
            color="warning",
        )

        return (
            message,
            "",
            "",
            "",
        )

    try:

        from emidaf_core.edse import EDSEEngine

        engine = EDSEEngine(
            context["estimator"],
            context["X_test"],
            task=context["task"],
            cv_mean=context.get(
                "cv_mean"
            ),
            test_score=context.get(
                "test_score"
            ),
            better_than_baseline=context.get(
                "better_than_baseline"
            ),
        )

        scenario = engine.scenario(
            threshold=float(threshold),
            direction=direction or "above",
        )

        profiles = engine.profiles()

        summary = engine.summary()

        # ==================================================
        # Persistance de session EDSE
        # ==================================================

        register_analysis(
            project_id,
            dataset_id,
            "edse",
            {
                "model_name": context.get(
                    "model_name"
                ),
                "task": context.get(
                    "task"
                ),
                "target": context.get(
                    "target"
                ),
                "threshold": float(
                    threshold
                ),
                "direction": (
                    direction or "above"
                ),
                "summary": summary,
                "scenario": scenario,
                "profiles": profiles,
            },
        )

    except Exception:

        logger.exception(
            "EDSE analysis failed "
            "(project_id=%s, dataset_id=%s)",
            project_id,
            dataset_id,
        )

        message = dbc.Alert(
            [
                html.Strong(
                    "EDSE n'a pas pu terminer "
                    "l'analyse. "
                ),
                (
                    "Vérifiez le seuil, le sens du scénario "
                    "et le modèle EAIE disponible."
                ),
            ],
            color="danger",
        )

        return (
            message,
            "",
            "",
            "",
        )

    # ======================================================
    # Statut
    # ======================================================

    status = dbc.Alert(
        "Scénario analysé avec succès.",
        color="success",
    )

    # ======================================================
    # Synthèse méthodologique
    # ======================================================

    assessment = summary[
        "assessment"
    ]

    positive_class = summary.get(
        "positive_class"
    )

    classification_context = (
        dbc.Alert(
            [
                html.Strong(
                    "Classification binaire — "
                ),
                "classe analysée : ",
                html.Strong(
                    str(positive_class)
                ),
                " ; seuil de probabilité : ",
                html.Strong(
                    f"{float(threshold):.2f}"
                ),
                ".",
            ],
            color="info",
        )
        if (
            context["task"]
            == "classification"
            and positive_class is not None
        )
        else html.Div()
    )

    reliability_color = (
        "success"
        if assessment["reliable"]
        else "warning"
    )

    warnings = assessment.get(
        "warnings",
        [],
    )

    warning_list = (
        html.Ul(
            [
                html.Li(item)
                for item in warnings
            ]
        )
        if warnings
        else html.P(
            "Avertissement méthodologique majeur non détecté."
        )
    )

    summary_view = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    "Synthèse décisionnelle"
                ),

                html.P(
                    [
                        html.Strong(
                            "Modèle : "
                        ),
                        context["model_name"],
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Cible : "
                        ),
                        context["target"],
                    ]
                ),

                classification_context,

                html.P(
                    [
                        html.Strong(
                            "Niveau méthodologique : "
                        ),
                        assessment["level"],
                    ]
                ),

                dbc.Alert(
                    summary[
                        "interpretation"
                    ],
                    color=reliability_color,
                ),

                warning_list,

                html.P(
                    (
                        "EDSE fournit une aide à "
                        "l'interprétation des scénarios. "
                        "La décision finale reste sous "
                        "la responsabilité de l'utilisateur."
                    ),
                    className="text-muted",
                ),
            ]
        )
    )

    # ======================================================
    # Scénario
    # ======================================================

    scenario_summary = scenario[
        "summary"
    ]

    scenario_view = [
        html.H5(
            "Résultat du scénario"
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Observations",
                                    className="text-muted",
                                ),
                                html.H4(
                                    str(
                                        scenario_summary[
                                            "observations"
                                        ]
                                    )
                                ),
                            ]
                        )
                    ),
                    md=3,
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Sélectionnées",
                                    className="text-muted",
                                ),
                                html.H4(
                                    str(
                                        scenario_summary[
                                            "selected"
                                        ]
                                    )
                                ),
                            ]
                        )
                    ),
                    md=3,
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Non sélectionnées",
                                    className="text-muted",
                                ),
                                html.H4(
                                    str(
                                        scenario_summary[
                                            "not_selected"
                                        ]
                                    )
                                ),
                            ]
                        )
                    ),
                    md=3,
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Taux",
                                    className="text-muted",
                                ),
                                html.H4(
                                    (
                                        f"{scenario_summary['selected_rate'] * 100:.1f} %"
                                    )
                                ),
                            ]
                        )
                    ),
                    md=3,
                ),
            ],
            className="g-3 mb-4",
        ),

        dbc.Alert(
            scenario[
                "interpretation"
            ],
            color="info",
        ),

        _table(
            scenario["table"]
        ),
    ]

    # ======================================================
    # Profils
    # ======================================================

    profiles_view = [
        html.H5(
            "Profils associés aux prédictions"
        ),

        html.P(
            (
                "Le tableau présente les observations "
                "du jeu de test et leurs prédictions. "
                "L'ordre affiché ne constitue pas une "
                "priorisation normative."
            ),
            className="text-muted",
        ),

        _table(
            profiles.head(50)
        ),
    ]

    return (
        status,
        summary_view,
        scenario_view,
        profiles_view,
    )
