from __future__ import annotations

import logging

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


logger = logging.getLogger(__name__)


def _classification_decision(
    true_label,
    predicted_label,
    positive_label=1,
):
    """
    Classe une prédiction binaire en
    VP, FN, FP ou VN.
    """

    true_positive = (
        true_label == positive_label
    )

    predicted_positive = (
        predicted_label == positive_label
    )

    if (
        true_positive
        and predicted_positive
    ):
        return "tp"

    if (
        true_positive
        and not predicted_positive
    ):
        return "fn"

    if (
        not true_positive
        and predicted_positive
    ):
        return "fp"

    return "tn"


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
    Output("exaie-row", "options"),
    Output("exaie-row", "value"),

    Input(
        "exaie-error-filter",
        "value",
    ),

    State(
        "exaie-project-id",
        "data",
    ),
    State(
        "exaie-dataset-id",
        "data",
    ),
)
def filter_local_observations(
    decision_filter,
    project_id,
    dataset_id,
):

    context = get_eaie_run(
        project_id,
        dataset_id,
    )

    if context is None:
        return [], None

    X_test = context.get(
        "X_test"
    )

    y_test = context.get(
        "y_test"
    )

    estimator = context.get(
        "estimator"
    )

    if (
        X_test is None
        or y_test is None
        or estimator is None
    ):
        return [], None

    n_observations = len(
        X_test
    )

    if (
        context.get("task")
        != "classification"
    ):

        options = [
            {
                "label": (
                    f"Observation {i}"
                ),
                "value": i,
            }
            for i in range(
                n_observations
            )
        ]

        return (
            options,
            (
                options[0]["value"]
                if options
                else None
            ),
        )

    predictions = estimator.predict(
        X_test
    )

    positive_label = context.get(
        "positive_label",
        1,
    )

    selected_rows = []

    for i in range(
        n_observations
    ):

        true_label = (
            y_test.iloc[i]
            if hasattr(
                y_test,
                "iloc",
            )
            else y_test[i]
        )

        predicted_label = (
            predictions[i]
        )

        decision = (
            _classification_decision(
                true_label,
                predicted_label,
                positive_label,
            )
        )

        if (
            decision_filter in {
                None,
                "all",
            }
            or decision
            == decision_filter
        ):

            selected_rows.append(
                (
                    i,
                    decision,
                    true_label,
                    predicted_label,
                )
            )

    all_counts = {
        "tp": 0,
        "fn": 0,
        "fp": 0,
        "tn": 0,
    }

    for i in range(
        n_observations
    ):

        true_label = (
            y_test.iloc[i]
            if hasattr(
                y_test,
                "iloc",
            )
            else y_test[i]
        )

        predicted_label = (
            predictions[i]
        )

        decision = (
            _classification_decision(
                true_label,
                predicted_label,
                positive_label,
            )
        )

        all_counts[
            decision
        ] += 1

    logger.info(
        (
            "EXAIE classification decisions "
            "VP=%s FN=%s FP=%s VN=%s TOTAL=%s"
        ),
        all_counts["tp"],
        all_counts["fn"],
        all_counts["fp"],
        all_counts["tn"],
        sum(
            all_counts.values()
        ),
    )

    labels = {
        "tp": "VP",
        "fn": "FN",
        "fp": "FP",
        "tn": "VN",
    }

    options = [
        {
            "label": (
                f"Observation {i} "
                f"— {labels[decision]} "
                f"(réel={true_label}, "
                f"prédit={predicted_label})"
            ),
            "value": i,
        }
        for (
            i,
            decision,
            true_label,
            predicted_label,
        )
        in selected_rows
    ]

    return (
        options,
        (
            options[0]["value"]
            if options
            else None
        ),
    )


@callback(
    Output("exaie-status", "children"),
    Output("exaie-summary", "children"),
    Output("exaie-native", "children"),
    Output("exaie-permutation", "children"),
    Output("exaie-local", "children"),
    Output("exaie-shap", "children"),

    Input("exaie-run", "n_clicks"),

    Input("exaie-row", "value"),
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
            "",
        )

    try:

        from emidaf_core.exaie import (
            EXAIEEngine,
            FeatureImportanceAggregator,
            ShapExplainer,
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

        selected_row = int(
            row or 0
        )

        local = engine.local_explanation(
            row=selected_row,
        )

        # ==================================================
        # DIAGNOSTIC LOCAL DE CLASSIFICATION
        # ==================================================

        if (
            local.get("available")
            and context.get("task")
            == "classification"
        ):

            estimator = context[
                "estimator"
            ]

            X_test = context[
                "X_test"
            ]

            y_test = context[
                "y_test"
            ]

            if (
                selected_row < 0
                or selected_row >= len(
                    X_test
                )
            ):
                selected_row = 0

            X_row = X_test.iloc[
                [selected_row]
            ]

            true_label = (
                y_test.iloc[
                    selected_row
                ]
                if hasattr(
                    y_test,
                    "iloc",
                )
                else y_test[
                    selected_row
                ]
            )

            predicted_label = (
                estimator.predict(
                    X_row
                )[0]
            )

            positive_label = context.get(
                "positive_label",
                1,
            )

            probability_positive = None

            if hasattr(
                estimator,
                "predict_proba",
            ):

                probabilities = (
                    estimator.predict_proba(
                        X_row
                    )
                )

                classes = list(
                    estimator.classes_
                )

                if (
                    positive_label
                    in classes
                ):

                    positive_index = (
                        classes.index(
                            positive_label
                        )
                    )

                    probability_positive = float(
                        probabilities[
                            0,
                            positive_index
                        ]
                    )

            true_positive = (
                true_label
                == positive_label
            )

            predicted_positive = (
                predicted_label
                == positive_label
            )

            if (
                true_positive
                and predicted_positive
            ):

                decision_type = (
                    "Vrai positif (VP)"
                )

                decision_interpretation = (
                    "Observation réellement positive "
                    "et correctement détectée par "
                    "le modèle."
                )

            elif (
                true_positive
                and not predicted_positive
            ):

                decision_type = (
                    "Faux négatif (FN)"
                )

                decision_interpretation = (
                    "Observation réellement positive "
                    "mais non détectée par le modèle."
                )

            elif (
                not true_positive
                and predicted_positive
            ):

                decision_type = (
                    "Faux positif (FP)"
                )

                decision_interpretation = (
                    "Observation réellement négative "
                    "mais signalée comme positive "
                    "par le modèle."
                )

            else:

                decision_type = (
                    "Vrai négatif (VN)"
                )

                decision_interpretation = (
                    "Observation réellement négative "
                    "et correctement classée par "
                    "le modèle."
                )

            local[
                "true_label"
            ] = true_label

            local[
                "predicted_label"
            ] = predicted_label

            local[
                "positive_label"
            ] = positive_label

            local[
                "probability_positive"
            ] = probability_positive

            local[
                "decision_type"
            ] = decision_type

            local[
                "decision_interpretation"
            ] = (
                decision_interpretation
            )

        summary = engine.summary()

        # ==================================================
        # SHAP
        # ==================================================

        shap_result = None
        shap_error = None
        shap_selected_local = None

        try:

            X_test = context["X_test"]

            selected_row = int(
                row or 0
            )

            if (
                selected_row < 0
                or selected_row >= len(X_test)
            ):
                selected_row = 0

            # Limitation raisonnable du coût SHAP.
            # On conserve toujours l'observation choisie.
            max_shap_samples = 100

            if len(X_test) <= max_shap_samples:

                X_shap = X_test.copy()
                shap_row_position = (
                    selected_row
                )

            else:

                positions = list(
                    range(max_shap_samples)
                )

                if selected_row not in positions:
                    positions[-1] = selected_row

                X_shap = (
                    X_test.iloc[
                        positions
                    ]
                    .copy()
                )

                shap_row_position = (
                    positions.index(
                        selected_row
                    )
                )

            shap_result = (
                ShapExplainer.explain(
                    context["estimator"],
                    X_shap,
                    task=context.get(
                        "task",
                        "",
                    ),
                )
            )

            local_items = (
                shap_result
                .local_explanations
            )

            if (
                0
                <= shap_row_position
                < len(local_items)
            ):
                shap_selected_local = (
                    local_items[
                        shap_row_position
                    ]
                )

        except Exception:

            logger.exception(
                "EXAIE SHAP computation failed "
                "(project_id=%s, dataset_id=%s)",
                project_id,
                dataset_id,
            )

            shap_error = (
                "SHAP n'a pas pu être calculé "
                "pour le modèle sélectionné."
            )

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
        # VUES SCIENTIFIQUES AGREGEES
        # ==================================================

        original_features = list(
            context.get(
                "features",
                [],
            )
        )

        native_scientific = None

        if (
            native is not None
            and not native.empty
            and original_features
        ):
            native_scientific = (
                FeatureImportanceAggregator
                .global_importance(
                    native,
                    original_features=(
                        original_features
                    ),
                )
            )

        local_scientific = None

        if (
            local.get("available")
            and original_features
        ):
            local_scientific = (
                FeatureImportanceAggregator
                .local_contributions(
                    local["contributions"],
                    original_features=(
                        original_features
                    ),
                )
            )

        shap_scientific = None

        if (
            shap_result is not None
            and original_features
        ):
            shap_scientific = (
                FeatureImportanceAggregator
                .shap_global_from_values(
                    shap_result.shap_values,
                    transformed_features=(
                        shap_result.features
                    ),
                    original_features=(
                        original_features
                    ),
                )
            )

        shap_local_scientific = None

        if (
            shap_selected_local is not None
            and original_features
        ):

            raw_shap_local = (
                shap_selected_local.get(
                    "contributions",
                    {},
                )
            )

            scalar_shap_local = {
                feature: value
                for feature, value
                in raw_shap_local.items()
                if isinstance(
                    value,
                    (int, float),
                )
            }

            # Régression et classification binaire :
            # les contributions sont scalaires.
            # En multiclasse, la vue technique est
            # conservée tant qu'une classe explicative
            # explicite n'a pas été sélectionnée.
            if (
                scalar_shap_local
                and len(scalar_shap_local)
                == len(raw_shap_local)
            ):

                shap_local_table = pd.DataFrame(
                    {
                        "feature": list(
                            scalar_shap_local.keys()
                        ),
                        "contribution": list(
                            scalar_shap_local.values()
                        ),
                    }
                )

                shap_local_scientific = (
                    FeatureImportanceAggregator
                    .local_contributions(
                        shap_local_table,
                        original_features=(
                            original_features
                        ),
                    )
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

                "shap": (
                    {
                        "available": True,
                        "model_name": (
                            shap_result.model_name
                        ),
                        "explainer_type": (
                            shap_result.explainer_type
                        ),
                        "n_observations": (
                            shap_result.n_observations
                        ),
                        "feature_importance": (
                            shap_result.feature_importance
                        ),
                        "local_explanation": (
                            shap_selected_local
                        ),
                        "output_names": (
                            shap_result.output_names
                        ),
                    }
                    if shap_result is not None
                    else {
                        "available": False,
                        "reason": shap_error,
                    }
                ),

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
                    "l'analyse. "
                ),
                (
                    "Vérifiez le modèle sélectionné "
                    "et les données disponibles."
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
            "Importance globale — vue scientifique"
        ),

        html.P(
            (
                "Les colonnes issues du prétraitement "
                "sont regroupées selon leur variable "
                "d'origine afin de faciliter "
                "l'interprétation scientifique."
            ),
            className="text-muted",
        ),

        (
            _table(
                native_scientific
            )
            if native_scientific is not None
            else dbc.Alert(
                (
                    "Vue scientifique agrégée "
                    "non disponible."
                ),
                color="secondary",
            )
        ),

        html.H5(
            "Détail technique après prétraitement",
            className="mt-4",
        ),

        html.P(
            (
                "Cette vue conserve les variables "
                "transformées produites par le pipeline "
                "et sert à l'audit technique."
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
                        "Classe réelle : "
                    ),
                    str(
                        local.get(
                            "true_label",
                            "Non disponible",
                        )
                    ),
                ]
            ),

            html.P(
                [
                    html.Strong(
                        "Classe prédite : "
                    ),
                    str(
                        local.get(
                            "predicted_label",
                            local.get(
                                "prediction",
                                "Non disponible",
                            ),
                        )
                    ),
                ]
            ),

            (
                html.P(
                    [
                        html.Strong(
                            "Probabilité classe positive : "
                        ),
                        (
                            f"{local['probability_positive']:.4f}"
                        ),
                    ]
                )
                if local.get(
                    "probability_positive"
                ) is not None
                else html.Div()
            ),

            (
                dbc.Alert(
                    [
                        html.Strong(
                            local.get(
                                "decision_type",
                                "",
                            )
                        ),
                        html.Br(),
                        local.get(
                            "decision_interpretation",
                            "",
                        ),
                    ],
                    color=(
                        "warning"
                        if local.get(
                            "decision_type",
                            ""
                        ).startswith(
                            "Faux négatif"
                        )
                        else (
                            "danger"
                            if local.get(
                                "decision_type",
                                ""
                            ).startswith(
                                "Faux positif"
                            )
                            else "info"
                        )
                    ),
                )
                if local.get(
                    "decision_type"
                )
                else html.Div()
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

            html.H6(
                "Vue scientifique agrégée",
                className="mt-3",
            ),

            (
                _table(
                    local_scientific.head(20)
                )
                if local_scientific is not None
                else dbc.Alert(
                    (
                        "Vue locale agrégée "
                        "non disponible."
                    ),
                    color="secondary",
                )
            ),

            html.H6(
                "Détail technique après prétraitement",
                className="mt-4",
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

    # ======================================================
    # SHAP VIEW
    # ======================================================

    if shap_result is None:

        shap_view = dbc.Alert(
            [
                html.Strong(
                    "SHAP indisponible : "
                ),
                (
                    shap_error
                    or (
                        "L'explication SHAP "
                        "n'a pas pu être calculée."
                    )
                ),
            ],
            color="secondary",
        )

    else:

        importance_rows = [
            {
                "Variable": feature,
                "Importance SHAP moyenne": value,
            }
            for feature, value
            in shap_result.feature_importance.items()
        ]

        importance_df = pd.DataFrame(
            importance_rows
        )

        local_rows = []

        if shap_selected_local is not None:

            contributions = (
                shap_selected_local.get(
                    "contributions",
                    {},
                )
            )

            for feature, value in (
                contributions.items()
            ):

                if isinstance(
                    value,
                    (list, tuple),
                ):

                    local_rows.append(
                        {
                            "Variable": feature,
                            "Contribution SHAP": (
                                str(
                                    [
                                        round(
                                            float(item),
                                            6,
                                        )
                                        for item
                                        in value
                                    ]
                                )
                            ),
                            "Effet": (
                                "Multiclasse"
                            ),
                        }
                    )

                else:

                    numeric_value = float(
                        value
                    )

                    if numeric_value > 0:
                        direction = "Positive"
                    elif numeric_value < 0:
                        direction = "Négative"
                    else:
                        direction = "Nulle"

                    local_rows.append(
                        {
                            "Variable": feature,
                            "Contribution SHAP": (
                                numeric_value
                            ),
                            "Effet": direction,
                        }
                    )

        local_df = pd.DataFrame(
            local_rows
        )

        if not local_df.empty:

            local_df["_abs"] = (
                local_df[
                    "Contribution SHAP"
                ]
                .apply(
                    lambda value: (
                        abs(value)
                        if isinstance(
                            value,
                            (int, float),
                        )
                        else 0
                    )
                )
            )

            local_df = (
                local_df
                .sort_values(
                    "_abs",
                    ascending=False,
                )
                .drop(
                    columns="_abs"
                )
            )

        shap_view = [
            dbc.Alert(
                [
                    html.Strong(
                        "Méthode : "
                    ),
                    "SHAP — ",
                    shap_result.explainer_type,
                    " | ",
                    html.Strong(
                        "Observations analysées : "
                    ),
                    str(
                        shap_result.n_observations
                    ),
                ],
                color="info",
            ),

            html.H5(
                "Importance globale SHAP"
            ),

            html.P(
                (
                    "L'importance correspond à la "
                    "moyenne de la valeur absolue "
                    "des contributions SHAP."
                ),
                className="text-muted",
            ),

            html.H6(
                "Vue scientifique agrégée"
            ),

            (
                _table(
                    shap_scientific.head(30)
                )
                if shap_scientific is not None
                else dbc.Alert(
                    (
                        "Vue SHAP agrégée "
                        "non disponible."
                    ),
                    color="secondary",
                )
            ),

            html.H6(
                "Détail technique après prétraitement",
                className="mt-4",
            ),

            _table(
                importance_df.head(30)
            ),

            html.H5(
                (
                    "Explication SHAP de "
                    f"l'observation {int(row or 0)}"
                ),
                className="mt-4",
            ),

            html.P(
                (
                    "Une contribution positive déplace "
                    "la sortie du modèle dans le sens "
                    "positif par rapport à la valeur "
                    "de référence ; une contribution "
                    "négative agit dans le sens opposé."
                ),
                className="text-muted",
            ),

            html.H6(
                "Vue scientifique agrégée",
                className="mt-3",
            ),

            (
                _table(
                    shap_local_scientific.head(30)
                )
                if (
                    shap_local_scientific
                    is not None
                )
                else dbc.Alert(
                    (
                        "Vue SHAP locale agrégée "
                        "non disponible pour cette "
                        "configuration."
                    ),
                    color="secondary",
                )
            ),

            html.H6(
                "Détail technique après prétraitement",
                className="mt-4",
            ),

            (
                _table(
                    local_df.head(30)
                )
                if not local_df.empty
                else dbc.Alert(
                    (
                        "Aucune contribution locale "
                        "SHAP disponible."
                    ),
                    color="secondary",
                )
            ),

            dbc.Alert(
                (
                    "Les valeurs SHAP expliquent le "
                    "comportement du modèle. Elles ne "
                    "constituent pas une preuve de "
                    "causalité."
                ),
                color="warning",
                className="mt-3",
            ),
        ]

    return (
        status,
        summary_view,
        native_view,
        permutation_view,
        local_view,
        shap_view,
    )
