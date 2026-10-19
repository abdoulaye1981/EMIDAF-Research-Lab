from __future__ import annotations

import logging

from flask import session

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
    get_all_analyses,
    get_eaie_run,
    register_analysis,
)


from emidaf_core.assistant import (
    AssistantService,
    OpenRouterProvider,
)


logger = logging.getLogger(__name__)


def _current_user_id() -> int | None:
    # Utilisateur EMIDAF connecté.
    value = session.get("user_id")

    if value is None:
        return None

    try:
        return int(value)

    except (TypeError, ValueError):
        return None


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
            observation_ids=context.get(
                "test_observation_ids"
            ),
            student_ids=context.get(
                "test_student_ids"
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
                "observation_ids": context.get(
                    "test_observation_ids"
                ),
                "student_ids": context.get(
                    "test_student_ids"
                ),
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



# =========================================================
# TABLEAU DE BORD D'ACCORD ENSEIGNANT - EMIDAF
# =========================================================


def _algorithmic_detection_class(validation):
    """
    Convertit la prédiction persistée en classe métier
    difficulty / no_difficulty.

    La positive_label sauvegardée lors de la validation
    est prioritaire.
    """

    predicted = validation.predicted_class

    if predicted is None:
        return None

    predicted_str = str(
        predicted
    ).strip()

    diagnosis = (
        validation.algorithmic_diagnosis
        if isinstance(
            validation.algorithmic_diagnosis,
            dict,
        )
        else {}
    )

    positive_label = diagnosis.get(
        "positive_label"
    )

    if positive_label is not None:

        return (
            "difficulty"
            if predicted_str
            == str(positive_label).strip()
            else "no_difficulty"
        )

    # Compatibilité avec les validations créées
    # avant l'enregistrement de positive_label.
    if predicted_str in {
        "1",
        "1.0",
        "True",
        "true",
        "difficulty",
    }:
        return "difficulty"

    if predicted_str in {
        "0",
        "0.0",
        "False",
        "false",
        "no_difficulty",
    }:
        return "no_difficulty"

    return None


@callback(
    Output(
        "edse-validation-metrics",
        "children",
    ),

    Input(
        "edse-validation-observation",
        "value",
    ),
    Input(
        "edse-validation-save",
        "n_clicks",
    ),

    State(
        "edse-project-id",
        "data",
    ),
    State(
        "edse-dataset-id",
        "data",
    ),
)
def update_teacher_agreement_dashboard(
    _observation_id,
    _n_clicks,
    project_id,
    dataset_id,
):
    """
    Calcule l'accord entre la détection EMIDAF
    et le jugement indépendant de l'enseignant.

    Une seule validation est retenue par observation :
    la validation la plus récente.
    """

    if (
        project_id is None
        or dataset_id is None
    ):

        return dbc.Alert(
            "Projet ou jeu de données indisponible.",
            color="secondary",
        )

    try:
        from emidaf_core.bootstrap.bootstrap import (
            Bootstrap,
        )

        bootstrap = Bootstrap()
        bootstrap.initialize()

        validations = (
            bootstrap
            .teacher_validation_controller
            .get_for_dataset(
                int(project_id),
                int(dataset_id),
            )
        )

    except Exception:

        logger.exception(
            "Impossible de charger les validations "
            "pour les indicateurs d'accord."
        )

        return dbc.Alert(
            "Indicateurs d'accord indisponibles.",
            color="warning",
        )

    if not validations:

        return dbc.Alert(
            (
                "Aucune validation humaine disponible. "
                "Les indicateurs d'accord apparaîtront "
                "après les premières validations."
            ),
            color="secondary",
        )

    # -----------------------------------------------------
    # Une validation la plus récente par observation
    # -----------------------------------------------------

    latest = {}

    for validation in validations:

        key = str(
            validation.observation_id
        )

        current = latest.get(
            key
        )

        if (
            current is None
            or validation.created_at
            > current.created_at
        ):
            latest[key] = validation

    latest_values = list(
        latest.values()
    )

    # Seules les validations finalisées participent
    # aux indicateurs d'accord humain-machine.
    latest_values = [
        value
        for value in latest_values
        if (
            getattr(
                value,
                "validation_status",
                "completed",
            )
            or "completed"
        ) == "completed"
    ]

    if not latest_values:

        return dbc.Alert(
            (
                "Des jugements indépendants peuvent déjà "
                "être verrouillés, mais aucune validation "
                "finalisée n'est encore disponible pour "
                "calculer l'accord humain-machine."
            ),
            color="secondary",
        )

    # -----------------------------------------------------
    # Statistiques de validation déclarée
    # -----------------------------------------------------

    total = len(
        latest_values
    )

    confirmed = sum(
        1
        for value in latest_values
        if value.detection_validation
        == "confirmed"
    )

    partially_confirmed = sum(
        1
        for value in latest_values
        if value.detection_validation
        == "partially_confirmed"
    )

    declared_disagreement = sum(
        1
        for value in latest_values
        if value.detection_validation
        == "not_confirmed"
    )

    # -----------------------------------------------------
    # Paires indépendantes humain / machine
    # -----------------------------------------------------

    machine_labels = []
    human_labels = []

    for validation in latest_values:

        human = (
            validation.teacher_detected_class
        )

        if human not in {
            "difficulty",
            "no_difficulty",
        }:
            continue

        machine = (
            _algorithmic_detection_class(
                validation
            )
        )

        if machine not in {
            "difficulty",
            "no_difficulty",
        }:
            continue

        human_labels.append(
            human
        )

        machine_labels.append(
            machine
        )

    n_evaluable = len(
        human_labels
    )

    n_not_evaluable = (
        total - n_evaluable
    )

    agreement_rate = None
    kappa = None

    tn = fp = fn = tp = 0

    if n_evaluable > 0:

        agreements = sum(
            machine == human
            for machine, human in zip(
                machine_labels,
                human_labels,
            )
        )

        agreement_rate = (
            agreements
            / n_evaluable
        )

        try:
            from sklearn.metrics import (
                cohen_kappa_score,
                confusion_matrix,
            )

            matrix = confusion_matrix(
                human_labels,
                machine_labels,
                labels=[
                    "no_difficulty",
                    "difficulty",
                ],
            )

            (
                (
                    tn,
                    fp,
                ),
                (
                    fn,
                    tp,
                ),
            ) = matrix.tolist()

            kappa_value = (
                cohen_kappa_score(
                    human_labels,
                    machine_labels,
                )
            )

            if (
                kappa_value
                == kappa_value
            ):
                kappa = float(
                    kappa_value
                )

        except Exception:

            logger.exception(
                "Calcul des métriques d'accord "
                "impossible."
            )

    # -----------------------------------------------------
    # Présentation
    # -----------------------------------------------------

    agreement_text = (
        f"{agreement_rate * 100:.1f} %"
        if agreement_rate is not None
        else "Non calculable"
    )

    kappa_text = (
        f"{kappa:.3f}"
        if kappa is not None
        else "Non calculable"
    )

    confirmation_rate = (
        confirmed / total
        if total
        else 0.0
    )

    partial_rate = (
        partially_confirmed / total
        if total
        else 0.0
    )

    disagreement_rate = (
        declared_disagreement / total
        if total
        else 0.0
    )

    cards = dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Small(
                                "Validations"
                            ),
                            html.H4(
                                str(total)
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
                            html.Small(
                                "Accord humain-machine"
                            ),
                            html.H4(
                                agreement_text
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
                            html.Small(
                                "Cohen κ"
                            ),
                            html.H4(
                                kappa_text
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
                            html.Small(
                                "Paires évaluables"
                            ),
                            html.H4(
                                str(
                                    n_evaluable
                                )
                            ),
                        ]
                    )
                ),
                md=3,
            ),
        ],
        className="g-3 mb-3",
    )

    declared_table = dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th(
                            "Appréciation"
                        ),
                        html.Th(
                            "Nombre"
                        ),
                        html.Th(
                            "Taux"
                        ),
                    ]
                )
            ),

            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(
                                "Confirmée"
                            ),
                            html.Td(
                                confirmed
                            ),
                            html.Td(
                                f"{confirmation_rate * 100:.1f} %"
                            ),
                        ]
                    ),

                    html.Tr(
                        [
                            html.Td(
                                "Partiellement confirmée"
                            ),
                            html.Td(
                                partially_confirmed
                            ),
                            html.Td(
                                f"{partial_rate * 100:.1f} %"
                            ),
                        ]
                    ),

                    html.Tr(
                        [
                            html.Td(
                                "Non confirmée"
                            ),
                            html.Td(
                                declared_disagreement
                            ),
                            html.Td(
                                f"{disagreement_rate * 100:.1f} %"
                            ),
                        ]
                    ),

                    html.Tr(
                        [
                            html.Td(
                                "Non évaluables pour "
                                "l'accord binaire"
                            ),
                            html.Td(
                                n_not_evaluable
                            ),
                            html.Td(
                                (
                                    f"{n_not_evaluable / total * 100:.1f} %"
                                    if total
                                    else "0.0 %"
                                )
                            ),
                        ]
                    ),
                ]
            ),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
    )

    confusion = dbc.Table(
        [
            html.Thead(
                [
                    html.Tr(
                        [
                            html.Th(
                                ""
                            ),
                            html.Th(
                                "EMIDAF : "
                                "pas de difficulté"
                            ),
                            html.Th(
                                "EMIDAF : "
                                "difficulté"
                            ),
                        ]
                    )
                ]
            ),

            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Th(
                                "Enseignant : "
                                "pas de difficulté"
                            ),
                            html.Td(
                                tn
                            ),
                            html.Td(
                                fp
                            ),
                        ]
                    ),

                    html.Tr(
                        [
                            html.Th(
                                "Enseignant : "
                                "difficulté"
                            ),
                            html.Td(
                                fn
                            ),
                            html.Td(
                                tp
                            ),
                        ]
                    ),
                ]
            ),
        ],
        bordered=True,
        responsive=True,
        size="sm",
    )

    methodological_note = dbc.Alert(
        (
            "Les indicateurs sont calculés uniquement "
            "sur les observations pour lesquelles "
            "l'enseignant fournit un jugement binaire "
            "indépendant. Pour chaque observation, "
            "seule la validation la plus récente est "
            "retenue. Le κ de Cohen n'est pas interprété "
            "comme une mesure de causalité."
        ),
        color="light",
    )

    return html.Div(
        [
            html.H5(
                "Accord enseignant – EMIDAF"
            ),
            cards,

            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H6(
                                "Validation déclarée"
                            ),
                            declared_table,
                        ],
                        md=6,
                    ),

                    dbc.Col(
                        [
                            html.H6(
                                "Matrice de confusion"
                            ),
                            confusion,
                        ],
                        md=6,
                    ),
                ],
                className="g-3",
            ),

            methodological_note,
        ]
    )


# ==========================================================
# ASSISTANT CONTEXTUEL EMIDAF
# ==========================================================

@callback(
    Output(
        "edse-assistant-status",
        "children",
    ),
    Output(
        "edse-assistant-response",
        "children",
    ),
    Input(
        "edse-assistant-run",
        "n_clicks",
    ),
    State(
        "edse-assistant-question",
        "value",
    ),
    State(
        "edse-assistant-level",
        "value",
    ),
    State(
        "edse-assistant-scope",
        "value",
    ),
    State(
        "edse-project-id",
        "data",
    ),
    State(
        "edse-dataset-id",
        "data",
    ),
    running=[
        (
            Output(
                "edse-assistant-run",
                "disabled",
            ),
            True,
            False,
        ),
        (
            Output(
                "edse-assistant-run",
                "children",
            ),
            "Génération en cours…",
            "Observer, expliquer et interpréter",
        ),
    ],
    prevent_initial_call=True,
)
def run_contextual_assistant(
    n_clicks,
    question,
    level,
    scope,
    project_id,
    dataset_id,
):

    if not n_clicks:
        return (
            no_update,
            no_update,
        )

    if (
        not question
        or not str(question).strip()
    ):
        return (
            dbc.Alert(
                "Veuillez saisir une question.",
                color="warning",
            ),
            no_update,
        )

    try:
        analyses = get_all_analyses(
            project_id,
            dataset_id,
        )

    except Exception as exc:
        logger.exception(
            "Impossible de charger les analyses "
            "pour l'assistant contextuel."
        )

        return (
            dbc.Alert(
                (
                    "Impossible de charger les "
                    f"résultats EMIDAF : {exc}"
                ),
                color="danger",
            ),
            no_update,
        )

    if not analyses:
        return (
            dbc.Alert(
                (
                    "Aucun résultat analytique "
                    "persisté n'est disponible."
                ),
                color="warning",
            ),
            no_update,
        )

    scope = (
        scope
        or "all"
    )

    if scope == "all":
        selected_analyses = analyses

    elif scope == "teacher_validation":

        selected_analyses = {
            key: value
            for key, value in analyses.items()
            if key in {
                "edse",
                "teacher_validation",
                "teacher_validations",
            }
        }

        if not selected_analyses:
            selected_analyses = {
                "edse": analyses.get(
                    "edse"
                )
            }

    else:
        selected_analyses = {
            scope: analyses.get(
                scope
            )
        }

    selected_analyses = {
        key: value
        for key, value
        in selected_analyses.items()
        if value is not None
    }

    if not selected_analyses:
        return (
            dbc.Alert(
                (
                    "Aucun résultat n'est disponible "
                    "pour le périmètre sélectionné."
                ),
                color="warning",
            ),
            no_update,
        )

    provider = OpenRouterProvider(
        models=[
            "google/gemini-2.5-flash",
        ]
    )

    if not provider.available():
        return (
            dbc.Alert(
                (
                    "Le service d'IA générative n'est pas configuré. "
                    "Les résultats EMIDAF restent "
                    "disponibles normalement."
                ),
                color="secondary",
            ),
            no_update,
        )

    service = AssistantService(
        provider
    )

    contextual_question = (
        "PÉRIMÈTRE DEMANDÉ : "
        f"{scope}\n\n"
        "RÈGLES DE RÉPONSE :\n"
        "- Observe les résultats présents.\n"
        "- Explique leur signification.\n"
        "- Interprète uniquement ce qui est "
        "soutenu par les résultats.\n"
        "- Mets en relation les résultats "
        "disponibles lorsque c'est pertinent.\n"
        "- Formule une conclusion prudente.\n"
        "- Présente les limites et précautions.\n"
        "- Ne calcule aucune nouvelle valeur.\n"
        "- N'invente aucun résultat.\n"
        "- Ne modifie aucune valeur.\n"
        "- Ne déduis aucune causalité non démontrée.\n"
        "- Distingue résultat algorithmique, "
        "explicabilité, aide à la décision et "
        "validation humaine.\n\n"
        "QUESTION :\n"
        + str(question).strip()
    )

    try:
        response = service.explain(
            analyses=selected_analyses,
            question=contextual_question,
            level=(
                level
                or "intermediate"
            ),
            max_output_tokens=800,
            regenerate_on_inconsistency=True,
        )

    except Exception as exc:

        logger.exception(
            "Erreur Assistant contextuel EMIDAF."
        )

        error_text = str(exc)

        if (
            "PERMISSION_DENIED"
            in error_text
            or "403"
            in error_text
        ):
            message = (
                "Le service d'IA générative est actuellement inaccessible "
                "pour ce projet Google. "
                "EMIDAF et ses résultats ne sont "
                "pas affectés."
            )

        elif (
            "API_KEY_INVALID"
            in error_text
            or "API key not valid"
            in error_text
        ):
            message = (
                "La clé API configurée n'est "
                "pas acceptée par Google. "
                "EMIDAF continue de fonctionner "
                "sans l'assistant."
            )

        else:
            message = (
                "L'assistant contextuel est "
                "temporairement indisponible. "
                "Les résultats EMIDAF restent "
                "inchangés."
            )

        return (
            dbc.Alert(
                message,
                color="warning",
            ),
            no_update,
        )

    return (
        dbc.Alert(
            (
                "Interprétation générée à partir "
                "des résultats EMIDAF disponibles. "
                "Aucun recalcul scientifique "
                "n'a été demandé au modèle."
            ),
            color="success",
        ),
        response,
    )
