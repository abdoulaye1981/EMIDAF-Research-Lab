from __future__ import annotations

from io import StringIO

import logging
import re

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

logger = logging.getLogger(__name__)

from emidaf_core.eaie import EAIEEngine
from emidaf_studio.services.model_registry import (
    register_eaie_run,
)


def _df(data):
    return pd.read_json(
        StringIO(data),
        orient="split",
    )


def _table(dataframe):

    if dataframe is None or dataframe.empty:

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
    Output("eaie-status", "children"),
    Output("eaie-summary", "children"),
    Output("eaie-comparison", "children"),
    Output("eaie-best-model", "children"),
    Output("eaie-evaluation", "children"),
    Input("eaie-run", "n_clicks"),
    State("eaie-target", "value"),
    State("eaie-task", "value"),
    State("eaie-test-size", "value"),
    State("eaie-cv", "value"),
    State("eaie-data", "data"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def run_eaie(
    n_clicks,
    target,
    task,
    test_size,
    cv,
    data,
    pathname,
):

    if not n_clicks:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    if not target:

        message = dbc.Alert(
            "Sélectionnez une variable cible.",
            color="warning",
        )

        return (
            message,
            "",
            "",
            "",
            "",
        )

    dataframe = _df(data)

    task_value = (
        None
        if task == "auto"
        else task
    )

    try:

        engine = EAIEEngine(
            test_size=float(test_size),
            random_state=42,
            cv=int(cv),
        )

        engine.run(
            dataframe,
            target=target,
            task=task_value,
        )

        summary = engine.summary()

        comparison = engine.compare()

        best = engine.best()

        # --------------------------------------------------
        # Transmission EAIE -> EXAIE
        # --------------------------------------------------

        route_match = re.fullmatch(
            (
                r"/projects/(\d+)/datasets/"
                r"(\d+)/eaie/?"
            ),
            pathname or "",
        )

        if route_match is not None:

            project_id = int(
                route_match.group(1)
            )

            dataset_id = int(
                route_match.group(2)
            )



            register_eaie_run(
                project_id,
                dataset_id,
                engine.explainability_context(),
            )



    except Exception as exc:

        logger.exception(
            "EAIE modelling failed "
            "(target=%s, task=%s, cv=%s)",
            target,
            task,
            cv,
        )

        message = dbc.Alert(
            [
                html.Strong(
                    "EAIE n'a pas pu terminer l'analyse : "
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
            f"Analyse terminée : "
            f"{summary['models']} modèles évalués."
        ),
        color="success",
    )

    # ======================================================
    # SUMMARY
    # ======================================================

    baseline_text = (
        "Non disponible"
        if summary["baseline_cv_mean"] is None
        else f"{summary['baseline_cv_mean']:.4f}"
    )

    cv_text = (
        "Non disponible"
        if summary["cv_mean"] is None
        else f"{summary['cv_mean']:.4f}"
    )

    test_text = (
        "Non disponible"
        if summary["test_score"] is None
        else f"{summary['test_score']:.4f}"
    )

    summary_view = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    "Synthèse EAIE"
                ),

                html.P(
                    [
                        html.Strong(
                            "Type de problème : "
                        ),
                        summary["task"],
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Modèle sélectionné par CV : "
                        ),
                        summary["best_model"],
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Métrique de sélection : "
                        ),
                        summary["selection_metric"],
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "CV moyenne : "
                        ),
                        cv_text,
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Baseline CV : "
                        ),
                        baseline_text,
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Score test final : "
                        ),
                        test_text,
                    ]
                ),

                dbc.Alert(
                    summary["interpretation"],
                    color=(
                        "success"
                        if summary[
                            "better_than_baseline"
                        ] is True
                        else "warning"
                    ),
                ),
            ]
        )
    )

    # ======================================================
    # COMPARISON
    # ======================================================

    comparison_view = [
        html.H5(
            "Comparaison des modèles"
        ),
        html.P(
            (
                "Le classement affiché ci-dessous "
                "doit être interprété conjointement "
                "avec la validation croisée."
            ),
            className="text-muted",
        ),
        _table(comparison),
    ]

    # ======================================================
    # BEST MODEL
    # ======================================================

    best_view = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    best.model_name
                ),

                html.P(
                    f"Tâche : {best.task}"
                ),

                html.P(
                    (
                        "Observations entraînement : "
                        f"{best.train_size}"
                    )
                ),

                html.P(
                    (
                        "Observations test : "
                        f"{best.test_size}"
                    )
                ),

                html.P(
                    (
                        "Variables explicatives : "
                        f"{len(best.features)}"
                    )
                ),

                html.P(
                    (
                        "CV moyenne : "
                        f"{best.metadata.get('cv_mean', float('nan')):.4f}"
                    )
                ),

                html.P(
                    (
                        "CV écart-type : "
                        f"{best.metadata.get('cv_std', float('nan')):.4f}"
                    )
                ),
            ]
        )
    )

    # ======================================================
    # FINAL TEST EVALUATION
    # ======================================================

    if best.task == "classification":

        metrics = pd.DataFrame(
            {
                "Métrique": [
                    "Accuracy",
                    "Precision",
                    "Recall",
                    "F1-score",
                    "ROC-AUC",
                    "Log-loss",
                ],
                "Valeur": [
                    best.accuracy,
                    best.precision,
                    best.recall,
                    best.f1_score,
                    best.roc_auc,
                    best.log_loss,
                ],
            }
        )

        confusion = pd.DataFrame(
            best.confusion_matrix
        )

        evaluation_view = [
            html.H5(
                "Métriques sur le jeu test"
            ),
            _table(metrics),
            html.H5(
                "Matrice de confusion",
                className="mt-4",
            ),
            _table(confusion),
        ]

    else:

        metrics = pd.DataFrame(
            {
                "Métrique": [
                    "MAE",
                    "MSE",
                    "RMSE",
                    "R²",
                ],
                "Valeur": [
                    best.mae,
                    best.mse,
                    best.rmse,
                    best.r2,
                ],
            }
        )

        evaluation_view = [
            html.H5(
                "Métriques sur le jeu test"
            ),
            _table(metrics),
        ]

    return (
        status,
        summary_view,
        comparison_view,
        best_view,
        evaluation_view,
    )
