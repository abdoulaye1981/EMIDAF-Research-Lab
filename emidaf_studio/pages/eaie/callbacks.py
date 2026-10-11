from __future__ import annotations


import logging

import pandas as pd

from dash import (
    Input,
    Output,
    State,
    callback,
    ctx,
    html,
    no_update,
)

import dash_bootstrap_components as dbc

logger = logging.getLogger(__name__)

from emidaf_studio.pages.inspection.layout import (
    load_dataset,
)
from emidaf_studio.services.model_registry import (
    register_eaie_run,
)

from emidaf_core.eaie.roles import (
    FeatureRoles,
)

from emidaf_core.eaie.blocks import (
    FeatureBlocks,
)


def _load_eaie_dataframe(
    project_id,
    dataset_id,
):
    _, _, result = load_dataset(
        project_id,
        dataset_id,
    )

    if isinstance(result, str):
        raise ValueError(result)

    if not isinstance(
        result,
        pd.DataFrame,
    ):
        raise ValueError(
            "Le dataset EAIE est indisponible."
        )

    return result


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


# ============================================================
# FEATURE ROLES
# ============================================================

@callback(
    Output(
        "eaie-role-summary",
        "children",
    ),
    Output(
        "eaie-feature-roles",
        "data",
    ),
    Input(
        "eaie-target",
        "value",
    ),
    Input(
        "eaie-manual-exclusions",
        "value",
    ),
    State(
        "eaie-project-id",
        "data",
    ),
    State(
        "eaie-dataset-id",
        "data",
    ),
)
def update_eaie_feature_roles(
    target,
    manual_exclusions,
    project_id,
    dataset_id,
):

    if not target:
        return (
            dbc.Alert(
                (
                    "Sélectionnez une variable cible "
                    "pour déterminer les rôles."
                ),
                color="secondary",
            ),
            None,
        )

    try:
        dataframe = _load_eaie_dataframe(
            project_id,
            dataset_id,
        )

        roles = FeatureRoles.resolve(
            dataframe,
            target=target,
            excluded=list(
                manual_exclusions or []
            ),
        )

    except Exception as exc:
        logger.exception(
            "EAIE feature role resolution failed "
            "(target=%s)",
            target,
        )

        return (
            dbc.Alert(
                (
                    "Impossible de déterminer les "
                    "rôles de modélisation."
                ),
                color="danger",
            ),
            None,
        )

    payload = roles.to_dict()

    if not roles.valid:
        return (
            dbc.Alert(
                [
                    html.Strong(
                        "Configuration des rôles invalide."
                    ),
                    html.Ul(
                        [
                            html.Li(message)
                            for message
                            in roles.conflicts
                        ],
                        className="mb-0 mt-2",
                    ),
                ],
                color="danger",
            ),
            payload,
        )

    summary = dbc.Alert(
        [
            html.Strong(
                "Configuration des rôles valide."
            ),

            html.Div(
                [
                    html.Span(
                        (
                            f"Prédicteurs : "
                            f"{len(roles.predictors)}"
                        ),
                        className="me-3",
                    ),
                    html.Span(
                        (
                            f"Identifiants exclus : "
                            f"{len(roles.identifiers)}"
                        ),
                        className="me-3",
                    ),
                    html.Span(
                        (
                            f"Qualité exclue : "
                            f"{len(roles.quality)}"
                        ),
                        className="me-3",
                    ),
                    html.Span(
                        (
                            f"Texte libre exclu : "
                            f"{len(roles.text)}"
                        ),
                        className="me-3",
                    ),
                    html.Span(
                        (
                            f"Exclusions manuelles : "
                            f"{len(roles.excluded)}"
                        ),
                    ),
                ],
                className="mt-2",
            ),

            html.Div(
                [
                    html.Strong(
                        "Prédicteurs retenus : "
                    ),
                    ", ".join(
                        roles.predictors
                    ),
                ],
                className="small mt-2",
            ),

            html.Div(
                [
                    html.Strong(
                        "Variables protégées : "
                    ),
                    ", ".join(
                        roles.protected
                    ),
                ],
                className="small mt-1",
            ),
        ],
        color="success",
    )

    return summary, payload


# ============================================================
# SCIENTIFIC FEATURE BLOCKS
# ============================================================

@callback(
    Output(
        "eaie-block-card",
        "style",
    ),
    Input(
        "eaie-analysis-mode",
        "value",
    ),
)
def toggle_eaie_block_card(
    analysis_mode,
):

    if analysis_mode == "blocks":
        return {
            "display": "block"
        }

    return {
        "display": "none"
    }


@callback(
    Output(
        "eaie-block-a",
        "options",
    ),
    Output(
        "eaie-block-b",
        "options",
    ),
    Output(
        "eaie-block-c",
        "options",
    ),
    Output(
        "eaie-block-d",
        "options",
    ),
    Input(
        "eaie-feature-roles",
        "data",
    ),
)
def update_eaie_block_options(
    feature_roles,
):

    if (
        not feature_roles
        or not feature_roles.get(
            "valid"
        )
    ):
        return [], [], [], []

    predictors = (
        feature_roles.get(
            "predictors",
            [],
        )
    )

    options = [
        {
            "label": variable,
            "value": variable,
        }
        for variable
        in predictors
    ]

    return (
        options,
        options,
        options,
        options,
    )


@callback(
    Output(
        "eaie-block-summary",
        "children",
    ),
    Output(
        "eaie-feature-blocks",
        "data",
    ),
    Output(
        "eaie-block-run",
        "disabled",
    ),
    Input(
        "eaie-feature-roles",
        "data",
    ),
    Input(
        "eaie-block-a-name",
        "value",
    ),
    Input(
        "eaie-block-a",
        "value",
    ),
    Input(
        "eaie-block-b-name",
        "value",
    ),
    Input(
        "eaie-block-b",
        "value",
    ),
    Input(
        "eaie-block-c-name",
        "value",
    ),
    Input(
        "eaie-block-c",
        "value",
    ),
    Input(
        "eaie-block-d-name",
        "value",
    ),
    Input(
        "eaie-block-d",
        "value",
    ),
)
def validate_eaie_feature_blocks(
    feature_roles,
    block_a_name,
    block_a,
    block_b_name,
    block_b,
    block_c_name,
    block_c,
    block_d_name,
    block_d,
):

    if (
        not feature_roles
        or not feature_roles.get(
            "valid"
        )
    ):

        return (
            dbc.Alert(
                (
                    "Définissez d'abord une cible "
                    "et une configuration de rôles "
                    "valide."
                ),
                color="secondary",
            ),
            None,
            True,
        )

    blocks = {
        (block_a_name or "Bloc A").strip():
            list(block_a or []),
        (block_b_name or "Bloc B").strip():
            list(block_b or []),
        (block_c_name or "Bloc C").strip():
            list(block_c or []),
        (block_d_name or "Bloc D").strip():
            list(block_d or []),
    }

    result = FeatureBlocks.resolve(
        predictors=feature_roles.get(
            "predictors",
            [],
        ),
        blocks=blocks,
        target=feature_roles.get(
            "target"
        ),
        protected=feature_roles.get(
            "protected",
            [],
        ),
        require_all=True,
    )

    payload = result.to_dict()

    if not result.valid:

        return (
            dbc.Alert(
                [
                    html.Strong(
                        "Configuration des blocs invalide."
                    ),
                    html.Ul(
                        [
                            html.Li(conflict)
                            for conflict
                            in result.conflicts
                        ],
                        className="mb-0 mt-2",
                    ),
                ],
                color="danger",
            ),
            payload,
            True,
        )

    cumulative_rows = []

    for (
        block_name,
        variables,
    ) in result.cumulative.items():

        cumulative_rows.append(
            html.Li(
                (
                    f"{block_name} : "
                    f"{len(variables)} variable(s)"
                )
            )
        )

    summary = dbc.Alert(
        [
            html.Strong(
                "Configuration des blocs valide."
            ),
            html.Div(
                (
                    f"{len(result.assigned)} "
                    "prédicteurs affectés, "
                    f"{len(result.unassigned)} "
                    "non affecté(s)."
                ),
                className="mt-2",
            ),
            html.Div(
                [
                    html.Strong(
                        "Construction cumulative :"
                    ),
                    html.Ul(
                        cumulative_rows,
                        className="mb-0 mt-2",
                    ),
                ],
                className="mt-2",
            ),
        ],
        color="success",
    )

    return (
        summary,
        payload,
        False,
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
    State("eaie-models", "value"),
    State("eaie-manual-exclusions", "value"),
    State("eaie-test-size", "value"),
    State("eaie-cv", "value"),
    State("eaie-project-id", "data"),
    State("eaie-dataset-id", "data"),

    prevent_initial_call=True,
)
def run_eaie(
    n_clicks,
    target,
    task,
    models,
    manual_exclusions,
    test_size,
    cv,
    project_id,

    dataset_id,

):

    from emidaf_core.eaie import (
        EAIEEngine,
    )

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

    try:
        dataframe = _load_eaie_dataframe(
            project_id,
            dataset_id,
        )
    except Exception as exc:
        logger.exception(
            "EAIE dataset loading failed "
            "(project_id=%s, dataset_id=%s)",
            project_id,
            dataset_id,
        )

        message = dbc.Alert(
            (
                "Impossible de charger les données "
                "nécessaires à EAIE."
            ),
            color="danger",
        )

        return (
            message,
            "",
            "",
            "",
            "",
        )

    task_value = (
        None
        if task == "auto"
        else task
    )

    try:

        roles = FeatureRoles.resolve(
            dataframe,
            target=target,
            excluded=list(
                manual_exclusions or []
            ),
        )

        if not roles.valid:
            message = dbc.Alert(
                [
                    html.Strong(
                        "Configuration des rôles invalide."
                    ),
                    html.Ul(
                        [
                            html.Li(message)
                            for message
                            in roles.conflicts
                        ],
                        className="mb-0 mt-2",
                    ),
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

        engine = EAIEEngine(
            test_size=float(test_size),
            random_state=42,
            cv=int(cv),
        )

        engine.run(
            dataframe,
            target=target,
            features=roles.predictors,
            task=task_value,
            models=(
                models
                if models
                else None
            ),
        )

        summary = engine.summary()

        comparison = engine.compare()

        best = engine.best()

        # --------------------------------------------------
        # Transmission EAIE -> EXAIE
        # --------------------------------------------------

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
                    "EAIE n'a pas pu terminer l'analyse. "
                ),
                (
                    "Vérifiez la variable cible, les variables "
                    "sélectionnées et la configuration du modèle."
                ),
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

    comparison_display = (
        comparison[
            [
                "model",
                "task",
                "cv_mean",
                "cv_std",
            ]
        ]
        .copy()
    )

    comparison_display = (
        comparison_display.rename(
            columns={
                "model": "Modèle",
                "task": "Tâche",
                "cv_mean": "CV moyenne",
                "cv_std": "CV écart-type",
            }
        )
    )

    comparison_display.insert(
        2,
        "Métrique CV",
        summary["selection_metric"],
    )

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
        _table(
            comparison_display
        ),
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


# ============================================================
# SCIENTIFIC BLOCK COMPARISON
# ============================================================

@callback(
    Output(
        "eaie-block-status",
        "children",
    ),
    Output(
        "eaie-block-results",
        "children",
    ),
    Input(
        "eaie-block-run",
        "n_clicks",
    ),
    State(
        "eaie-feature-blocks",
        "data",
    ),
    State(
        "eaie-target",
        "value",
    ),
    State(
        "eaie-task",
        "value",
    ),
    State(
        "eaie-models",
        "value",
    ),
    State(
        "eaie-test-size",
        "value",
    ),
    State(
        "eaie-cv",
        "value",
    ),
    State(
        "eaie-project-id",
        "data",
    ),
    State(
        "eaie-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def run_eaie_block_comparison(
    n_clicks,
    feature_blocks,
    target,
    task,
    models,
    test_size,
    cv,
    project_id,
    dataset_id,
):

    if not n_clicks:
        return no_update, no_update

    if (
        not feature_blocks
        or not feature_blocks.get(
            "valid"
        )
    ):
        return (
            dbc.Alert(
                (
                    "La configuration des blocs "
                    "scientifiques doit être valide."
                ),
                color="warning",
            ),
            "",
        )

    if not target:
        return (
            dbc.Alert(
                "Sélectionnez une variable cible.",
                color="warning",
            ),
            "",
        )

    try:

        from emidaf_core.eaie.block_comparison import (
            BlockComparisonEngine,
        )

        dataframe = _load_eaie_dataframe(
            project_id,
            dataset_id,
        )

        # Revalidation côté serveur.
        block_result = FeatureBlocks.resolve(
            predictors=feature_blocks.get(
                "predictors",
                [],
            ),
            blocks=feature_blocks.get(
                "blocks",
                {},
            ),
            target=target,
            protected=feature_blocks.get(
                "protected",
                [],
            ),
            require_all=True,
        )

        if not block_result.valid:

            return (
                dbc.Alert(
                    (
                        "La configuration des blocs "
                        "n'est plus valide."
                    ),
                    color="danger",
                ),
                "",
            )

        task_value = (
            None
            if task == "auto"
            else task
        )

        engine = BlockComparisonEngine(
            test_size=float(
                test_size
            ),
            random_state=42,
            cv=int(
                cv
            ),
        )

        result = engine.run(
            dataframe,
            target=target,
            blocks=block_result,
            task=task_value,
            models=(
                models
                if models
                else None
            ),
        )

    except Exception:

        logger.exception(
            "EAIE scientific block comparison failed "
            "(target=%s, task=%s)",
            target,
            task,
        )

        return (
            dbc.Alert(
                (
                    "La comparaison des blocs "
                    "scientifiques a échoué. "
                    "Consultez les journaux du serveur "
                    "pour le détail."
                ),
                color="danger",
            ),
            "",
        )

    # ======================================================
    # TABLEAU DES PERFORMANCES CUMULATIVES
    # ======================================================

    rows = []

    cumulative_names = []

    for performance in result.performances:

        cumulative_names.append(
            performance.block
        )

        cumulative_label = (
            " + ".join(
                cumulative_names
            )
        )

        rows.append(
            {
                "Bloc cumulatif":
                    cumulative_label,
                "Nb variables":
                    performance.n_features,
                "Meilleur modèle":
                    performance.best_model,
                "Métrique CV":
                    performance.cv_metric,
                "CV moyenne":
                    performance.cv_mean,
                "CV écart-type":
                    performance.cv_std,
                "ΔCV":
                    performance.delta_cv,
            }
        )

    comparison_table = pd.DataFrame(
        rows
    )

    final = result.final_result

    # ======================================================
    # EVALUATION FINALE HOLD-OUT
    # ======================================================

    if result.task == "classification":

        final_metrics = pd.DataFrame(
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
                    final.accuracy,
                    final.precision,
                    final.recall,
                    final.f1_score,
                    final.roc_auc,
                    final.log_loss,
                ],
            }
        )

    else:

        final_metrics = pd.DataFrame(
            {
                "Métrique": [
                    "MAE",
                    "MSE",
                    "RMSE",
                    "R²",
                ],
                "Valeur": [
                    final.mae,
                    final.mse,
                    final.rmse,
                    final.r2,
                ],
            }
        )

    selected_names = []

    for performance in result.performances:

        selected_names.append(
            performance.block
        )

        if (
            performance.block
            == result.selected_block
        ):
            break

    selected_block_label = (
        " + ".join(
            selected_names
        )
    )

    status = dbc.Alert(
        (
            f"Comparaison terminée : "
            f"{len(result.performances)} "
            "configurations cumulatives évaluées."
        ),
        color="success",
    )

    results_view = [
        html.H5(
            "Comparaison scientifique des blocs"
        ),

        html.P(
            (
                "Les blocs sont comparés uniquement "
                "sur la validation croisée. "
                "Le jeu de test est utilisé une seule "
                "fois après la sélection finale."
            ),
            className="text-muted",
        ),

        _table(
            comparison_table
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(
                        "Configuration sélectionnée"
                    ),

                    html.P(
                        [
                            html.Strong(
                                "Bloc cumulatif : "
                            ),
                            selected_block_label,
                        ]
                    ),

                    html.P(
                        [
                            html.Strong(
                                "Modèle : "
                            ),
                            result.selected_model,
                        ]
                    ),

                    html.P(
                        [
                            html.Strong(
                                "Nombre de variables : "
                            ),
                            str(
                                len(
                                    final.features
                                )
                            ),
                        ]
                    ),
                ]
            ),
            className="mt-4",
        ),

        html.H5(
            "Évaluation finale sur le jeu test",
            className="mt-4",
        ),

        _table(
            final_metrics
        ),

        dbc.Alert(
            (
                "ΔCV mesure le gain prédictif "
                "incrémental entre deux ensembles "
                "cumulatifs successifs. "
                "Il ne doit pas être interprété "
                "comme un effet causal."
            ),
            color="info",
            className="mt-3",
        ),
    ]

    return (
        status,
        results_view,
    )


# ============================================================
# MODEL SELECTION
# ============================================================

@callback(
    Output("eaie-models", "options"),
    Output("eaie-models", "value"),
    Input("eaie-task", "value"),
)
def update_eaie_model_options(task):

    regression_models = [
        {
            "label": "Régression linéaire",
            "value": "linear_regression",
        },
        {
            "label": "Ridge",
            "value": "ridge",
        },
        {
            "label": "Arbre de décision",
            "value": "decision_tree",
        },
        {
            "label": "Random Forest",
            "value": "random_forest",
        },
        {
            "label": "KNN Regressor",
            "value": "knn",
        },
        {
            "label": "SVR",
            "value": "svr",
        },
        {
            "label": "Gradient Boosting",
            "value": "gradient_boosting",
        },
        {
            "label": "XGBoost",
            "value": "xgboost",
        },
    ]

    classification_models = [
        {
            "label": "Régression logistique",
            "value": "logistic_regression",
        },
        {
            "label": "Arbre de décision",
            "value": "decision_tree",
        },
        {
            "label": "Random Forest",
            "value": "random_forest",
        },
        {
            "label": "KNN Classifier",
            "value": "knn",
        },
        {
            "label": "SVM",
            "value": "svm",
        },
        {
            "label": "Gradient Boosting",
            "value": "gradient_boosting",
        },
        {
            "label": "XGBoost",
            "value": "xgboost",
        },
    ]

    if task == "regression":
        return regression_models, []

    if task == "classification":
        return classification_models, []

    # En mode automatique, EAIE détermine lui-même
    # la tâche et évalue son registre complet.
    return [], []


# ============================================================
# OLS / MULTILEVEL DYNAMIC NUMERIC OPTIONS
# ============================================================

@callback(
    Output(
        "eaie-ols-features",
        "options",
    ),
    Output(
        "eaie-ols-features",
        "value",
    ),
    Input(
        "eaie-ols-target",
        "value",
    ),
    Input(
        "eaie-ols-select-all",
        "n_clicks",
    ),
    Input(
        "eaie-ols-clear",
        "n_clicks",
    ),
    State(
        "eaie-ols-features",
        "value",
    ),
    State(
        "eaie-project-id",
        "data",
    ),
    State(
        "eaie-dataset-id",
        "data",
    ),
)
def update_ols_feature_options(
    target,
    select_all_clicks,
    clear_clicks,
    selected_features,
    project_id,
    dataset_id,
):
    dataframe = _load_eaie_dataframe(
        project_id,
        dataset_id,
    )

    numeric_columns = list(
        dataframe.select_dtypes(
            include="number"
        ).columns
    )

    available_columns = [
        column
        for column in numeric_columns
        if column != target
    ]

    options = [
        {
            "label": column,
            "value": column,
        }
        for column in available_columns
    ]

    trigger = ctx.triggered_id

    if trigger == "eaie-ols-select-all":
        value = available_columns

    elif trigger == "eaie-ols-clear":
        value = []

    else:
        selected_features = (
            selected_features
            or []
        )

        value = [
            column
            for column in selected_features
            if column in available_columns
        ]

    return options, value


@callback(
    Output(
        "eaie-ml-features",
        "options",
    ),
    Output(
        "eaie-ml-features",
        "value",
    ),
    Input(
        "eaie-ml-target",
        "value",
    ),
    Input(
        "eaie-ml-select-all",
        "n_clicks",
    ),
    Input(
        "eaie-ml-clear",
        "n_clicks",
    ),
    State(
        "eaie-ml-features",
        "value",
    ),
    State(
        "eaie-project-id",
        "data",
    ),
    State(
        "eaie-dataset-id",
        "data",
    ),
)
def update_multilevel_feature_options(
    target,
    select_all_clicks,
    clear_clicks,
    selected_features,
    project_id,
    dataset_id,
):
    dataframe = _load_eaie_dataframe(
        project_id,
        dataset_id,
    )

    numeric_columns = list(
        dataframe.select_dtypes(
            include="number"
        ).columns
    )

    available_columns = [
        column
        for column in numeric_columns
        if column != target
    ]

    options = [
        {
            "label": column,
            "value": column,
        }
        for column in available_columns
    ]

    trigger = ctx.triggered_id

    if trigger == "eaie-ml-select-all":
        value = available_columns

    elif trigger == "eaie-ml-clear":
        value = []

    else:
        selected_features = (
            selected_features
            or []
        )

        value = [
            column
            for column in selected_features
            if column in available_columns
        ]

    return options, value


# ============================================================
# OLS
# ============================================================

@callback(
    Output(
        "eaie-ols-status",
        "children",
    ),
    Output(
        "eaie-ols-result",
        "children",
    ),
    Input(
        "eaie-ols-run",
        "n_clicks",
    ),
    State(
        "eaie-ols-target",
        "value",
    ),
    State(
        "eaie-ols-features",
        "value",
    ),
    State(
        "eaie-ols-alpha",
        "value",
    ),
    State(
        "eaie-project-id",
        "data",
    ),
    State(
        "eaie-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def run_ols(
    n_clicks,
    target,
    features,
    alpha,
    project_id,
    dataset_id,
):

    if not n_clicks:
        return no_update, no_update

    if not target:
        return (
            dbc.Alert(
                "Sélectionnez une variable dépendante.",
                color="warning",
            ),
            "",
        )

    if not features:
        return (
            dbc.Alert(
                "Sélectionnez au moins une variable explicative.",
                color="warning",
            ),
            "",
        )

    try:
        dataframe = _load_eaie_dataframe(
            project_id,
            dataset_id,
        )

        from emidaf_core.eaie import (
            OLSRegression,
        )

        result = OLSRegression.fit(
            dataframe,
            target=target,
            features=features,
            alpha=float(alpha),
        )

        names = [
            "const",
            *features,
        ]

        rows = []

        for name in names:

            if name == "const":
                coefficient = getattr(
                    result,
                    "intercept",
                    None,
                )
            else:
                coefficient = (
                    getattr(
                        result,
                        "coefficients",
                        {},
                    )
                    .get(name)
                )

            ci = (
                getattr(
                    result,
                    "confidence_intervals",
                    {},
                )
                .get(
                    name,
                    [None, None],
                )
            )

            rows.append(
                {
                    "Variable": name,
                    "Coefficient": coefficient,
                    "Erreur standard": (
                        getattr(
                            result,
                            "standard_errors",
                            {},
                        )
                        .get(name)
                    ),
                    "t": (
                        getattr(
                            result,
                            "t_statistics",
                            {},
                        )
                        .get(name)
                    ),
                    "p-value": (
                        getattr(
                            result,
                            "p_values",
                            {},
                        )
                        .get(name)
                    ),
                    "IC inférieur": (
                        ci[0]
                        if len(ci) > 0
                        else None
                    ),
                    "IC supérieur": (
                        ci[1]
                        if len(ci) > 1
                        else None
                    ),
                }
            )

        inference = pd.DataFrame(rows)

        summary = pd.DataFrame(
            {
                "Indicateur": [
                    "R²",
                    "R² ajusté",
                    "F-statistic",
                    "p-value F",
                    "AIC",
                    "BIC",
                    "Observations",
                    "Condition number",
                ],
                "Valeur": [
                    getattr(
                        result,
                        "r2",
                        None,
                    ),
                    getattr(
                        result,
                        "adjusted_r2",
                        None,
                    ),
                    getattr(
                        result,
                        "f_statistic",
                        None,
                    ),
                    getattr(
                        result,
                        "f_pvalue",
                        None,
                    ),
                    getattr(
                        result,
                        "aic",
                        None,
                    ),
                    getattr(
                        result,
                        "bic",
                        None,
                    ),
                    getattr(
                        result,
                        "n_observations",
                        None,
                    ),
                    getattr(
                        result,
                        "condition_number",
                        None,
                    ),
                ],
            }
        )

        view = [
            html.H5(
                "Synthèse OLS"
            ),
            _table(summary),
            html.H5(
                "Inférence sur les coefficients",
                className="mt-4",
            ),
            _table(inference),
        ]

        return (
            dbc.Alert(
                "Analyse OLS terminée.",
                color="success",
            ),
            view,
        )

    except Exception as exc:

        logger.exception(
            "OLS analysis failed "
            "(target=%s)",
            target,
        )

        return (
            dbc.Alert(
                [
                    html.Strong(
                        "OLS n'a pas pu terminer l'analyse. "
                    ),
                    (
                        "Vérifiez les variables sélectionnées "
                        "et la qualité des données."
                    ),
                ],
                color="danger",
            ),
            "",
        )


# ============================================================
# MULTILEVEL
# ============================================================

@callback(
    Output(
        "eaie-ml-status",
        "children",
    ),
    Output(
        "eaie-ml-result",
        "children",
    ),
    Input(
        "eaie-ml-run",
        "n_clicks",
    ),
    State(
        "eaie-ml-target",
        "value",
    ),
    State(
        "eaie-ml-features",
        "value",
    ),
    State(
        "eaie-ml-group",
        "value",
    ),
    State(
        "eaie-ml-method",
        "value",
    ),
    State(
        "eaie-ml-reml",
        "value",
    ),
    State(
        "eaie-project-id",
        "data",
    ),
    State(
        "eaie-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def run_multilevel(
    n_clicks,
    target,
    features,
    group,
    method,
    reml_values,
    project_id,
    dataset_id,
):

    if not n_clicks:
        return no_update, no_update

    if not target:
        return (
            dbc.Alert(
                "Sélectionnez une variable dépendante.",
                color="warning",
            ),
            "",
        )

    if not features:
        return (
            dbc.Alert(
                "Sélectionnez au moins un effet fixe.",
                color="warning",
            ),
            "",
        )

    if not group:
        return (
            dbc.Alert(
                "Sélectionnez une variable de groupe.",
                color="warning",
            ),
            "",
        )

    try:
        dataframe = _load_eaie_dataframe(
            project_id,
            dataset_id,
        )

        from emidaf_core.eaie import (
            MultilevelLinearModel,
        )

        result = MultilevelLinearModel.fit(
            dataframe,
            target=target,
            group=group,
            features=features,
            reml=(
                "reml"
                in (reml_values or [])
            ),
            method=method or "lbfgs",
            maxiter=500,
            alpha=0.05,
        )

        names = [
            "const",
            *features,
        ]

        rows = []

        for name in names:

            if name == "const":
                coefficient = getattr(
                    result,
                    "intercept",
                    None,
                )
            else:
                coefficient = (
                    getattr(
                        result,
                        "coefficients",
                        {},
                    )
                    .get(name)
                )

            ci = (
                getattr(
                    result,
                    "confidence_intervals",
                    {},
                )
                .get(
                    name,
                    [None, None],
                )
            )

            rows.append(
                {
                    "Effet fixe": name,
                    "Coefficient": coefficient,
                    "Erreur standard": (
                        getattr(
                            result,
                            "standard_errors",
                            {},
                        )
                        .get(name)
                    ),
                    "z": (
                        getattr(
                            result,
                            "z_statistics",
                            {},
                        )
                        .get(name)
                    ),
                    "p-value": (
                        getattr(
                            result,
                            "p_values",
                            {},
                        )
                        .get(name)
                    ),
                    "IC inférieur": (
                        ci[0]
                        if len(ci) > 0
                        else None
                    ),
                    "IC supérieur": (
                        ci[1]
                        if len(ci) > 1
                        else None
                    ),
                }
            )

        inference = pd.DataFrame(rows)

        summary_items = [
            (
                "Variable de groupe",
                group,
            ),
            (
                "Nombre de groupes",
                getattr(
                    result,
                    "n_groups",
                    None,
                ),
            ),
            (
                "ICC",
                getattr(
                    result,
                    "icc",
                    None,
                ),
            ),
            (
                "Variance inter-groupes",
                getattr(
                    result,
                    "group_variance",
                    getattr(
                        result,
                        "random_effect_variance",
                        None,
                    ),
                ),
            ),
            (
                "Variance résiduelle",
                getattr(
                    result,
                    "residual_variance",
                    None,
                ),
            ),
            (
                "AIC",
                getattr(
                    result,
                    "aic",
                    None,
                ),
            ),
            (
                "BIC",
                getattr(
                    result,
                    "bic",
                    None,
                ),
            ),
            (
                "Convergence",
                getattr(
                    result,
                    "converged",
                    None,
                ),
            ),
            (
                "Observations",
                getattr(
                    result,
                    "n_observations",
                    None,
                ),
            ),
        ]

        summary = pd.DataFrame(
            summary_items,
            columns=[
                "Indicateur",
                "Valeur",
            ],
        )

        view = [
            html.H5(
                "Synthèse du modèle multiniveau"
            ),
            _table(summary),
            html.H5(
                "Effets fixes",
                className="mt-4",
            ),
            _table(inference),
        ]

        return (
            dbc.Alert(
                "Modèle multiniveau estimé.",
                color="success",
            ),
            view,
        )

    except Exception as exc:

        logger.exception(
            "Multilevel analysis failed "
            "(target=%s, group=%s)",
            target,
            group,
        )

        return (
            dbc.Alert(
                [
                    html.Strong(
                        "Le modèle multiniveau "
                        "n'a pas pu être estimé. "
                    ),
                    (
                        "Vérifiez la variable de groupe, "
                        "les effets fixes et les données."
                    ),
                ],
                color="danger",
            ),
            "",
        )
