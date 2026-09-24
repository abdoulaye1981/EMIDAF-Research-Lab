from __future__ import annotations

import pandas as pd

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
        dataframe.round(6),
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        size="sm",
    )


@callback(
    Output("exaie-status", "children"),
    Output("exaie-summary", "children"),
    Output("exaie-native", "children"),
    Output("exaie-permutation", "children"),
    Output("exaie-local", "children"),

    Input("exaie-run", "n_clicks"),

    State("exaie-row", "value"),
    State("exaie-project-id", "data"),
    State("exaie-dataset-id", "data"),

    prevent_initial_call=True,
)
def run_exaie(
    n_clicks,
    row,
    project_id,
    dataset_id,
):

    if not n_clicks:

        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
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
            "",
        )

    try:

        from emidaf_core.exaie import (
            EXAIEEngine,
        )

        engine = EXAIEEngine(
            context["estimator"],
            context["X_test"],
            context["y_test"],
        )

        native = engine.global_importance()

        permutation = (
            engine.permutation_importance(
                n_repeats=10,
                random_state=42,
            )
        )

        local = engine.local_explanation(
            row=int(row or 0),
        )

        summary = engine.summary()

        cv_mean = context.get(
            "cv_mean"
        )

        test_score = context.get(
            "test_score"
        )

        predictive_warning = None

        if (
            context.get("task") == "regression"
            and (
                (
                    cv_mean is not None
                    and cv_mean <= 0
                )
                or
                (
                    test_score is not None
                    and test_score <= 0
                )
            )
        ):
            predictive_warning = (
                "La capacité prédictive du modèle "
                "n'est pas convaincante sur les données "
                "évaluées. Les explications ci-dessous "
                "décrivent son comportement algorithmique, "
                "mais ne doivent pas être utilisées pour "
                "tirer des conclusions métier fortes."
            )


        # ==================================================
        # Persistance de session EXAIE
        # ==================================================

        register_analysis(
            project_id,
            dataset_id,
            "exaie",
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
                "cv_mean": context.get(
                    "cv_mean"
                ),
                "cv_std": context.get(
                    "cv_std"
                ),
                "test_score": context.get(
                    "test_score"
                ),
                "native_importance": native,
                "permutation_importance": permutation,
                "local_explanation": local,
                "summary": summary,
                "predictive_warning": predictive_warning,
                "limitations": [
                    (
                        "Les résultats d'explicabilité "
                        "décrivent le comportement prédictif "
                        "du modèle et ne constituent pas "
                        "une preuve de causalité."
                    )
                ],
            },
        )

    except Exception as exc:

        message = dbc.Alert(
            [
                html.Strong(
                    "EXAIE n'a pas pu terminer "
                    "l'analyse : "
                ),
                str(exc),
            ],
            color="danger",
        )

        return (
            message,
            "",
            "",
            "",
            "",
        )

    status = dbc.Alert(
        (
            "Explication terminée pour le modèle "
            f"« {context['model_name']} »."
        ),
        color="success",
    )

    summary_view = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    "Synthèse EXAIE"
                ),

                html.P(
                    [
                        html.Strong(
                            "Modèle expliqué : "
                        ),
                        context["model_name"],
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Variable cible : "
                        ),
                        context["target"],
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Type de problème : "
                        ),
                        (
                            "Régression"
                            if context["task"] == "regression"
                            else "Classification"
                        ),
                    ]
                ),

                (
                    dbc.Alert(
                        predictive_warning,
                        color="warning",
                    )
                    if predictive_warning
                    else html.Div()
                ),

                dbc.Alert(
                    summary[
                        "native_interpretation"
                    ],
                    color="info",
                ),

                dbc.Alert(
                    summary.get(
                        "permutation_interpretation",
                        (
                            "Importance par permutation "
                            "non disponible."
                        ),
                    ),
                    color="secondary",
                ),

                html.P(
                    (
                        "Les résultats décrivent le "
                        "comportement prédictif du modèle. "
                        "Ils ne constituent pas une preuve "
                        "de causalité."
                    ),
                    className="text-muted",
                ),
            ]
        )
    )

    native_view = [
        html.H5(
            "Importance globale native"
        ),

        html.P(
            (
                "Importance extraite directement "
                "du modèle lorsque cette information "
                "est disponible."
            ),
            className="text-muted",
        ),

        _table(native),
    ]

    permutation_view = [
        html.H5(
            "Importance par permutation"
        ),

        html.P(
            (
                "La variable est perturbée afin de "
                "mesurer la diminution de performance "
                "du modèle sur le jeu de test."
            ),
            className="text-muted",
        ),

        _table(permutation),
    ]

    if local.get(
        "available"
    ):

        contributions = local[
            "contributions"
        ].copy()

        local_view = [
            html.H5(
                (
                    "Explication de "
                    f"l'observation {local['row']}"
                )
            ),

            html.P(
                [
                    html.Strong(
                        "Prédiction : "
                    ),
                    str(
                        local["prediction"]
                    ),
                ]
            ),

            html.P(
                (
                    "La contribution correspond ici "
                    "au produit entre la valeur "
                    "transformée et le coefficient "
                    "du modèle linéaire."
                ),
                className="text-muted",
            ),

            _table(
                contributions.head(20)
            ),
        ]

    else:

        local_view = dbc.Alert(
            local.get(
                "reason",
                (
                    "L'explication locale n'est "
                    "pas disponible pour ce modèle."
                ),
            ),
            color="secondary",
        )

    return (
        status,
        summary_view,
        native_view,
        permutation_view,
        local_view,
    )
