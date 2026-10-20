from __future__ import annotations

import logging
import hashlib
from pathlib import Path

import pandas as pd

import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, html, no_update
from flask import session

from emidaf_studio.services.model_registry import (
    get_eaie_run,
    register_analysis,
)


logger = logging.getLogger(__name__)


TEACHER_VISIBLE_FEATURES = [
    "cycle",
    "niveau",
    "interet_maths",
    "stress",
    "exercices_semaine",
    "eval_formatives_prevues",
    "ressources_educatives",
    "usage_tice_maison",
    "motivation",
    "niveau_etude",
    "implication",
    "temps_aide_hebdo",
    "formation_continue",
    "pratiques_pedagogiques",
    "heures_par_semaine",
    "region",
    "type_ecole",
    "genre",
]




H7_STUDY_ID = 1
H7_PROJECT_ID = 2
H7_DATASET_ID = 7

H7_DATASET_PATH = Path(
    "workspace/projects/EDUCATION/datasets/"
    "dataset_senegal_2500.csv"
)


def _is_h7_context(
    project_id,
    dataset_id,
):
    try:
        return (
            int(project_id) == H7_PROJECT_ID
            and int(dataset_id) == H7_DATASET_ID
        )
    except (TypeError, ValueError):
        return False


def _verify_h7_dataset(
    study,
):
    if not H7_DATASET_PATH.exists():
        raise FileNotFoundError(
            "Dataset doctoral H7 introuvable : "
            f"{H7_DATASET_PATH}"
        )

    config = (
        study.sampling_config
        if isinstance(
            study.sampling_config,
            dict,
        )
        else {}
    )

    provenance = config.get(
        "provenance",
        {}
    )

    expected_hash = provenance.get(
        "source_dataset_sha256"
    )

    if not expected_hash:
        return

    digest = hashlib.sha256(
        H7_DATASET_PATH.read_bytes()
    ).hexdigest()

    if digest != expected_hash:
        raise RuntimeError(
            "Le fichier dataset H7 ne correspond "
            "plus à la version scientifique figée. "
            "Validation interrompue."
        )


def _load_h7_student_row(
    study,
    student_id,
):
    _verify_h7_dataset(
        study
    )

    dataframe = pd.read_csv(
        H7_DATASET_PATH,
        sep=",",
        encoding="utf-8",
    )

    if "id_eleve" not in dataframe.columns:
        raise RuntimeError(
            "La colonne id_eleve est absente "
            "du dataset doctoral."
        )

    identifier = str(
        student_id
    ).strip()

    mask = (
        dataframe[
            "id_eleve"
        ]
        .astype(str)
        .str.strip()
        == identifier
    )

    rows = dataframe.loc[
        mask
    ]

    if len(rows) != 1:
        raise RuntimeError(
            "Impossible d'identifier "
            "de manière unique l'élève "
            f"{identifier} dans le dataset H7."
        )

    return rows.iloc[0]


def _get_h7_bundle(
    assignment_id,
    teacher_user_id,
):
    bootstrap = _bootstrap()

    assignment_service = (
        bootstrap
        .teacher_validation_assignment_service
    )

    assignment = (
        assignment_service
        .get_assignment_for_teacher(
            assignment_id=int(
                assignment_id
            ),
            teacher_user_id=int(
                teacher_user_id
            ),
        )
    )

    if assignment is None:
        raise PermissionError(
            "Cette affectation n'appartient pas "
            "à l'enseignant connecté."
        )

    if int(
        assignment.study_id
    ) != H7_STUDY_ID:
        raise PermissionError(
            "Cette affectation n'appartient pas "
            "à l'étude doctorale H7."
        )

    case = (
        assignment_service
        .get_case(
            assignment.case_id
        )
    )

    if case is None:
        raise RuntimeError(
            "Cas H7 introuvable."
        )

    if int(
        case.study_id
    ) != H7_STUDY_ID:
        raise RuntimeError(
            "Incohérence étude/cas H7."
        )

    study = (
        bootstrap
        .teacher_validation_study_repository
        .get_study(
            H7_STUDY_ID
        )
    )

    if study is None:
        raise RuntimeError(
            "Étude H7 introuvable."
        )

    if (
        int(study.project_id)
        != H7_PROJECT_ID
        or int(study.dataset_id)
        != H7_DATASET_ID
    ):
        raise RuntimeError(
            "Métadonnées de l'étude H7 "
            "incohérentes."
        )

    row = _load_h7_student_row(
        study,
        case.student_id,
    )

    return {
        "bootstrap": bootstrap,
        "assignment_service":
            assignment_service,
        "assignment": assignment,
        "case": case,
        "study": study,
        "row": row,
    }


def _h7_student_context_card(
    case,
    row,
):
    rows = []

    for feature in TEACHER_VISIBLE_FEATURES:

        if feature not in row.index:
            continue

        value = row[
            feature
        ]

        try:
            if pd.isna(value):
                value = (
                    "Non disponible"
                )
        except Exception:
            pass

        rows.append(
            html.Tr(
                [
                    html.Th(
                        feature
                        .replace(
                            "_",
                            " ",
                        )
                        .capitalize()
                    ),
                    html.Td(
                        str(value)
                    ),
                ]
            )
        )

    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    "Informations disponibles pour "
                    "le jugement indépendant"
                ),

                html.P(
                    [
                        html.Strong(
                            "Identifiant élève : "
                        ),
                        str(
                            case.student_id
                        ),
                    ]
                ),

                dbc.Alert(
                    (
                        "Phase aveugle H7 : la moyenne "
                        "de mathématiques, la cible, "
                        "la classe prédite, la "
                        "probabilité, le seuil, la "
                        "strate d'échantillonnage et "
                        "les explications du modèle "
                        "ne sont pas transmis à "
                        "l'interface avant le "
                        "verrouillage."
                    ),
                    color="light",
                ),

                dbc.Table(
                    [
                        html.Tbody(
                            rows
                        )
                    ],
                    bordered=True,
                    striped=True,
                    responsive=True,
                    size="sm",
                )
                if rows
                else dbc.Alert(
                    "Aucune caractéristique "
                    "autorisée disponible.",
                    color="secondary",
                ),
            ]
        )
    )


def _get_linked_validation(
    bootstrap,
    assignment,
):
    if assignment.validation_id is None:
        return None

    return (
        bootstrap
        .teacher_validation_repository
        .get_by_id(
            int(
                assignment.validation_id
            )
        )
    )


def _current_user_id():

    value = session.get(
        "user_id"
    )

    if value is None:
        return None

    try:
        return int(
            value
        )

    except (
        TypeError,
        ValueError,
    ):
        return None


def _bootstrap():

    from emidaf_core.bootstrap.bootstrap import Bootstrap

    bootstrap = Bootstrap()

    bootstrap.initialize()

    return bootstrap


def _get_case(
    project_id,
    dataset_id,
    observation_id,
):

    context = get_eaie_run(
        project_id,
        dataset_id,
    )

    if context is None:

        raise ValueError(
            "Contexte EAIE indisponible."
        )

    X_test = context.get(
        "X_test"
    )

    if X_test is None:

        raise ValueError(
            "Jeu de test indisponible."
        )

    observation_ids = context.get(
        "test_observation_ids"
    )

    student_ids = context.get(
        "test_student_ids"
    )

    if observation_ids is None:

        observation_ids = list(
            X_test.index
        )

    ids = [
        str(value)
        for value in observation_ids
    ]

    try:

        position = ids.index(
            str(
                observation_id
            )
        )

    except ValueError as exc:

        raise ValueError(
            "Observation introuvable."
        ) from exc

    row = X_test.iloc[
        [position]
    ]

    student_id = None

    if (
        student_ids is not None
        and position < len(
            student_ids
        )
    ):

        student_id = student_ids[
            position
        ]

    estimator = context.get(
        "estimator"
    )

    if estimator is None:

        raise ValueError(
            "Modèle EAIE indisponible."
        )

    prediction = estimator.predict(
        row
    )[0]

    probability = None

    if hasattr(
        estimator,
        "predict_proba",
    ):

        try:

            probabilities = (
                estimator.predict_proba(
                    row
                )
            )

            if (
                len(
                    probabilities.shape
                ) == 2
                and probabilities.shape[
                    1
                ] >= 2
            ):

                probability = float(
                    probabilities[
                        0,
                        1,
                    ]
                )

        except Exception:

            logger.exception(
                "Probabilité non disponible."
            )

    threshold = 0.50

    try:

        from emidaf_studio.services.model_registry import (
            get_analysis,
        )

        edse_result = get_analysis(
            project_id,
            dataset_id,
            "edse",
        )

        if isinstance(
            edse_result,
            dict,
        ):

            threshold = float(
                edse_result.get(
                    "threshold",
                    0.50,
                )
            )

    except Exception:

        logger.exception(
            "Impossible de récupérer le seuil EDSE."
        )

    return {
        "context": context,
        "X_test": X_test,
        "row": row,
        "position": position,
        "student_id": student_id,
        "prediction": prediction,
        "probability": probability,
        "threshold": threshold,
    }


def _student_context_card(
    observation_id,
    case,
):

    row = case[
        "row"
    ].iloc[
        0
    ]

    rows = []

    for feature in TEACHER_VISIBLE_FEATURES:

        if feature not in row.index:
            continue

        value = row[
            feature
        ]

        try:

            if value != value:
                value = "Non disponible"

        except Exception:
            pass

        rows.append(
            html.Tr(
                [
                    html.Th(
                        feature.replace(
                            "_",
                            " ",
                        ).capitalize()
                    ),
                    html.Td(
                        str(
                            value
                        )
                    ),
                ]
            )
        )

    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    (
                        "Informations disponibles pour "
                        "le jugement indépendant"
                    )
                ),

                html.P(
                    [
                        html.Strong(
                            "Observation : "
                        ),
                        str(
                            observation_id
                        ),
                    ]
                ),

                dbc.Alert(
                    (
                        "La note de mathématiques, la cible, "
                        "la prédiction, la probabilité, le seuil "
                        "et les explications du modèle sont "
                        "masqués pendant cette phase."
                    ),
                    color="light",
                ),

                dbc.Table(
                    [
                        html.Tbody(
                            rows
                        )
                    ],
                    bordered=True,
                    striped=True,
                    responsive=True,
                    size="sm",
                )
                if rows
                else dbc.Alert(
                    (
                        "Aucune information autorisée "
                        "n'est disponible pour cette observation."
                    ),
                    color="secondary",
                ),
            ]
        )
    )


def _algorithmic_card(
    validation,
):

    probability = (
        f"{validation.predicted_probability:.4f}"
        if (
            validation.predicted_probability
            is not None
        )
        else "Non disponible"
    )

    threshold = (
        f"{validation.threshold:.2f}"
        if validation.threshold is not None
        else "Non disponible"
    )

    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    "Résultat algorithmique"
                ),

                html.P(
                    [
                        html.Strong(
                            "Observation : "
                        ),
                        str(
                            validation.observation_id
                        ),
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Modèle : "
                        ),
                        str(
                            validation.model_name
                        ),
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Cible : "
                        ),
                        str(
                            validation.target
                            or "Non disponible"
                        ),
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Prédiction : "
                        ),
                        str(
                            validation.predicted_class
                        ),
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Probabilité : "
                        ),
                        probability,
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Seuil EDSE : "
                        ),
                        threshold,
                    ]
                ),

                dbc.Alert(
                    (
                        "Le jugement indépendant de "
                        "l'enseignant a été verrouillé avant "
                        "la révélation de ces informations."
                    ),
                    color="info",
                ),
            ]
        )
    )


def _history(
    validations,
):

    if not validations:

        return dbc.Alert(
            (
                "Aucune validation humaine "
                "enregistrée pour cette observation."
            ),
            color="secondary",
        )

    rows = []

    for validation in validations:

        status = getattr(
            validation,
            "validation_status",
            "completed",
        ) or "completed"

        rows.append(
            {
                "Date": str(
                    validation.created_at
                ),

                "Statut": status,

                "Classe enseignant": (
                    validation.teacher_detected_class
                    or ""
                ),

                "Confiance": (
                    getattr(
                        validation,
                        "teacher_confidence",
                        None,
                    )
                    or ""
                ),

                "Détection": (
                    validation.detection_validation
                    if status == "completed"
                    else ""
                ),

                "Diagnostic": (
                    validation.diagnosis_validation
                    if status == "completed"
                    else ""
                ),

                "Niveau": (
                    validation.difficulty_level
                    or ""
                ),

                "Commentaire initial": (
                    getattr(
                        validation,
                        "teacher_initial_comment",
                        None,
                    )
                    or validation.teacher_comment
                    or ""
                ),

                "Commentaire post-modèle": (
                    getattr(
                        validation,
                        "teacher_post_model_comment",
                        None,
                    )
                    or ""
                ),
            }
        )

    import pandas as pd

    dataframe = pd.DataFrame(
        rows
    )

    return dbc.Table.from_dataframe(
        dataframe,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        size="sm",
    )


# =========================================================
# LISTE DES OBSERVATIONS
# =========================================================

@callback(
    Output(
        "edse-validation-observation",
        "options",
    ),

    Output(
        "edse-validation-observation",
        "value",
    ),

    Input(
        "edse-profiles",
        "children",
    ),

    State(
        "edse-project-id",
        "data",
    ),

    State(
        "edse-dataset-id",
        "data",
    ),

    prevent_initial_call=True,
)
def load_observations(
    _profiles,
    project_id,
    dataset_id,
):

    if _is_h7_context(
        project_id,
        dataset_id,
    ):
        user_id = _current_user_id()

        if user_id is None:
            return [], None

        try:
            bootstrap = _bootstrap()

            service = (
                bootstrap
                .teacher_validation_assignment_service
            )

            assignments = (
                service
                .get_assignments_for_teacher(
                    study_id=H7_STUDY_ID,
                    teacher_user_id=user_id,
                )
            )

            items = []

            for assignment in assignments:
                case = service.get_case(
                    assignment.case_id
                )

                if case is None:
                    continue

                status = str(
                    assignment.status
                    or "pending"
                )

                status_labels = {
                    "pending":
                        "À évaluer",
                    "started":
                        "En cours",
                    "locked":
                        "Jugement verrouillé",
                    "model_revealed":
                        "À finaliser",
                    "completed":
                        "Terminé",
                }

                label = (
                    f"Cas H7 "
                    f"{int(case.sampling_rank):03d}"
                    f" — "
                    f"{status_labels.get(status, status)}"
                )

                items.append(
                    (
                        status == "completed",
                        int(
                            case.sampling_rank
                        ),
                        {
                            "label": label,
                            "value": str(
                                assignment.id
                            ),
                        },
                    )
                )

            items.sort(
                key=lambda item: (
                    item[0],
                    item[1],
                )
            )

            options = [
                item[2]
                for item in items
            ]

            first_value = (
                options[0]["value"]
                if options
                else None
            )

            return (
                options,
                first_value,
            )

        except Exception:
            logger.exception(
                "Chargement des affectations "
                "H7 impossible."
            )

            return [], None

    context = get_eaie_run(
        project_id,
        dataset_id,
    )

    if context is None:
        return [], None

    X_test = context.get(
        "X_test"
    )

    if X_test is None:
        return [], None

    observation_ids = context.get(
        "test_observation_ids"
    )

    student_ids = context.get(
        "test_student_ids"
    )

    if observation_ids is None:
        observation_ids = list(
            X_test.index
        )

    options = []

    for position, observation_id in enumerate(
        observation_ids
    ):
        student_id = None

        if (
            student_ids is not None
            and position
            < len(student_ids)
        ):
            student_id = (
                student_ids[position]
            )

        if student_id is not None:
            label = (
                f"Élève {student_id} — "
                f"observation {observation_id}"
            )
        else:
            label = (
                f"Observation {observation_id}"
            )

        options.append(
            {
                "label": label,
                "value": str(
                    observation_id
                ),
            }
        )

    return (
        options,
        options[0]["value"]
        if options
        else None,
    )


# =========================================================
# CONTEXTE INITIAL
# =========================================================

@callback(
    Output(
        "edse-validation-student-context",
        "children",
    ),

    Output(
        "edse-validation-history",
        "children",
    ),

    Output(
        "edse-validation-phase-1",
        "style",
    ),

    Output(
        "edse-validation-phase-2",
        "style",
    ),

    Output(
        "edse-validation-algorithmic-result",
        "children",
    ),

    Output(
        "edse-validation-lock-state",
        "data",
    ),

    Output(
        "edse-validation-observation",
        "disabled",
    ),

    Input(
        "edse-validation-observation",
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
)
def show_context(
    observation_id,
    project_id,
    dataset_id,
):

    if observation_id is None:
        return (
            dbc.Alert(
                "Sélectionnez une observation.",
                color="secondary",
            ),
            "",
            {
                "display": "none"
            },
            {
                "display": "none"
            },
            "",
            None,
            False,
        )

    if _is_h7_context(
        project_id,
        dataset_id,
    ):
        user_id = _current_user_id()

        if user_id is None:
            return (
                dbc.Alert(
                    "Utilisateur non connecté.",
                    color="danger",
                ),
                "",
                {
                    "display": "none"
                },
                {
                    "display": "none"
                },
                "",
                None,
                False,
            )

        try:
            bundle = _get_h7_bundle(
                observation_id,
                user_id,
            )

            bootstrap = bundle[
                "bootstrap"
            ]

            service = bundle[
                "assignment_service"
            ]

            assignment = bundle[
                "assignment"
            ]

            case = bundle[
                "case"
            ]

            row = bundle[
                "row"
            ]

            if (
                str(
                    assignment.status
                    or "pending"
                )
                == "pending"
            ):
                assignment = (
                    service
                    .start_assignment(
                        assignment_id=
                            assignment.id,
                        teacher_user_id=
                            user_id,
                    )
                )

            student_card = (
                _h7_student_context_card(
                    case,
                    row,
                )
            )

            validation = (
                _get_linked_validation(
                    bootstrap,
                    assignment,
                )
            )

            history = _history(
                [validation]
                if validation is not None
                else []
            )

            status = str(
                assignment.status
                or "pending"
            )

            if status in {
                "pending",
                "started",
            }:
                return (
                    student_card,
                    history,
                    {
                        "display": "block"
                    },
                    {
                        "display": "none"
                    },
                    "",
                    {
                        "assignment_id":
                            assignment.id,
                        "observation_id":
                            str(
                                case.observation_id
                            ),
                        "status":
                            "started",
                    },
                    False,
                )

            if status == "locked":

                if validation is None:
                    raise RuntimeError(
                        "Aucune validation liée "
                        "à l'affectation verrouillée."
                    )

                validation = (
                    bootstrap
                    .teacher_validation_controller
                    .reveal_model(
                        validation.id
                    )
                )

                assignment = (
                    service
                    .reveal_assignment(
                        assignment_id=
                            assignment.id,
                        teacher_user_id=
                            user_id,
                        validation_id=
                            validation.id,
                    )
                )

                status = (
                    "model_revealed"
                )

            if status == "model_revealed":

                if validation is None:
                    validation = (
                        _get_linked_validation(
                            bootstrap,
                            assignment,
                        )
                    )

                if validation is None:
                    raise RuntimeError(
                        "Validation H7 liée "
                        "introuvable."
                    )

                return (
                    student_card,
                    history,
                    {
                        "display": "none"
                    },
                    {
                        "display": "block"
                    },
                    _algorithmic_card(
                        validation
                    ),
                    {
                        "assignment_id":
                            assignment.id,
                        "validation_id":
                            validation.id,
                        "observation_id":
                            str(
                                case.observation_id
                            ),
                        "status":
                            "model_revealed",
                    },
                    True,
                )

            if status == "completed":

                return (
                    html.Div(
                        [
                            student_card,
                            dbc.Alert(
                                (
                                    "Ce cas H7 a déjà "
                                    "été finalisé par "
                                    "cet enseignant."
                                ),
                                color="success",
                                className="mt-3",
                            ),
                        ]
                    ),
                    history,
                    {
                        "display": "none"
                    },
                    {
                        "display": "none"
                    },
                    "",
                    {
                        "assignment_id":
                            assignment.id,
                        "validation_id":
                            assignment.validation_id,
                        "observation_id":
                            str(
                                case.observation_id
                            ),
                        "status":
                            "completed",
                    },
                    False,
                )

            raise RuntimeError(
                "Statut H7 inattendu : "
                f"{status}"
            )

        except Exception as exc:
            logger.exception(
                "Contexte H7 indisponible."
            )

            return (
                dbc.Alert(
                    str(exc),
                    color="danger",
                ),
                "",
                {
                    "display": "none"
                },
                {
                    "display": "none"
                },
                "",
                None,
                False,
            )

    try:
        case = _get_case(
            project_id,
            dataset_id,
            observation_id,
        )

    except Exception as exc:
        logger.exception(
            "Contexte enseignant indisponible."
        )

        return (
            dbc.Alert(
                str(exc),
                color="danger",
            ),
            "",
            {
                "display": "none"
            },
            {
                "display": "none"
            },
            "",
            None,
            False,
        )

    student_card = (
        _student_context_card(
            observation_id,
            case,
        )
    )

    try:
        bootstrap = _bootstrap()

        validations = (
            bootstrap
            .teacher_validation_controller
            .get_for_observation(
                int(project_id),
                int(dataset_id),
                str(observation_id),
            )
        )

    except Exception:
        logger.exception(
            "Historique indisponible."
        )
        validations = []

    history = _history(
        validations
    )

    user_id = _current_user_id()

    own = [
        item
        for item in validations
        if (
            user_id is not None
            and item.validator_user_id
            == user_id
        )
    ]

    own.sort(
        key=lambda item:
            item.created_at,
        reverse=True,
    )

    latest = (
        own[0]
        if own
        else None
    )

    if latest is None:
        return (
            student_card,
            history,
            {
                "display": "block"
            },
            {
                "display": "none"
            },
            "",
            None,
            False,
        )

    status = getattr(
        latest,
        "validation_status",
        "completed",
    ) or "completed"

    if status == "completed":
        return (
            html.Div(
                [
                    student_card,
                    dbc.Alert(
                        (
                            "Cette observation "
                            "a déjà été validée "
                            "par cet utilisateur."
                        ),
                        color="success",
                        className="mt-3",
                    ),
                ]
            ),
            history,
            {
                "display": "none"
            },
            {
                "display": "none"
            },
            "",
            {
                "validation_id":
                    latest.id,
                "observation_id":
                    str(
                        observation_id
                    ),
                "status":
                    "completed",
            },
            False,
        )

    try:
        if status == "locked":
            bootstrap = _bootstrap()

            latest = (
                bootstrap
                .teacher_validation_controller
                .reveal_model(
                    latest.id
                )
            )

    except Exception:
        logger.exception(
            "Reprise de révélation impossible."
        )

    return (
        student_card,
        history,
        {
            "display": "none"
        },
        {
            "display": "block"
        },
        _algorithmic_card(
            latest
        ),
        {
            "validation_id":
                latest.id,
            "observation_id":
                str(
                    observation_id
                ),
            "status":
                "model_revealed",
        },
        True,
    )


# =========================================================
# VERROUILLAGE DU JUGEMENT INDÉPENDANT
# =========================================================

@callback(
    Output(
        "edse-validation-lock-status",
        "children",
    ),

    Output(
        "edse-validation-lock-state",
        "data",
        allow_duplicate=True,
    ),

    Output(
        "edse-validation-phase-1",
        "style",
        allow_duplicate=True,
    ),

    Output(
        "edse-validation-phase-2",
        "style",
        allow_duplicate=True,
    ),

    Output(
        "edse-validation-algorithmic-result",
        "children",
        allow_duplicate=True,
    ),

    Output(
        "edse-validation-observation",
        "disabled",
        allow_duplicate=True,
    ),

    Input(
        "edse-validation-lock",
        "n_clicks",
    ),

    State(
        "edse-validation-observation",
        "value",
    ),

    State(
        "edse-validation-teacher-class",
        "value",
    ),

    State(
        "edse-validation-confidence",
        "value",
    ),

    State(
        "edse-validation-difficulty",
        "value",
    ),

    State(
        "edse-validation-factors",
        "value",
    ),

    State(
        "edse-validation-initial-comment",
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

    prevent_initial_call=True,
)
def lock_judgment(
    n_clicks,
    observation_id,
    teacher_class,
    confidence,
    difficulty_level,
    factors,
    initial_comment,
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

    if observation_id is None:
        return (
            dbc.Alert(
                "Sélectionnez une observation.",
                color="warning",
            ),
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    if teacher_class is None:
        return (
            dbc.Alert(
                (
                    "Le jugement indépendant "
                    "est obligatoire."
                ),
                color="warning",
            ),
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    if confidence is None:
        return (
            dbc.Alert(
                (
                    "Le niveau de confiance "
                    "est obligatoire."
                ),
                color="warning",
            ),
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    if (
        teacher_class == "difficulty"
        and difficulty_level
        in {
            None,
            "",
            "none",
        }
    ):
        return (
            dbc.Alert(
                (
                    "Précisez le niveau de "
                    "difficulté observé."
                ),
                color="warning",
            ),
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    user_id = _current_user_id()

    if user_id is None:
        return (
            dbc.Alert(
                "Utilisateur non connecté.",
                color="danger",
            ),
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    if _is_h7_context(
        project_id,
        dataset_id,
    ):

        if not (
            initial_comment
            and str(
                initial_comment
            ).strip()
        ):
            return (
                dbc.Alert(
                    (
                        "Le commentaire initial "
                        "est obligatoire pour "
                        "l'étude H7."
                    ),
                    color="warning",
                ),
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
            )

        try:
            bundle = _get_h7_bundle(
                observation_id,
                user_id,
            )

            bootstrap = bundle[
                "bootstrap"
            ]

            service = bundle[
                "assignment_service"
            ]

            assignment = bundle[
                "assignment"
            ]

            case = bundle[
                "case"
            ]

            study = bundle[
                "study"
            ]

            status = str(
                assignment.status
                or "pending"
            )

            if status == "pending":
                assignment = (
                    service
                    .start_assignment(
                        assignment_id=
                            assignment.id,
                        teacher_user_id=
                            user_id,
                    )
                )

                status = "started"

            if status != "started":
                raise RuntimeError(
                    "Ce cas ne peut plus être "
                    "verrouillé depuis le statut "
                    f"'{status}'."
                )

            diagnosis = {
                "observation_id":
                    str(
                        case.observation_id
                    ),
                "student_id":
                    str(
                        case.student_id
                    )
                    if case.student_id
                    is not None
                    else None,
                "prediction":
                    str(
                        case.predicted_class
                    ),
                "probability":
                    float(
                        case.predicted_probability
                    )
                    if case.predicted_probability
                    is not None
                    else None,
                "threshold":
                    float(
                        case.threshold
                    )
                    if case.threshold
                    is not None
                    else None,
                "model_name":
                    study.model_name,
                "target":
                    study.target,
                "source":
                    "teacher_validation_cases",
                "frozen":
                    True,
            }

            validation = (
                bootstrap
                .teacher_validation_controller
                .create_locked_judgment(
                    project_id=
                        H7_PROJECT_ID,
                    dataset_id=
                        H7_DATASET_ID,
                    observation_id=
                        str(
                            case.observation_id
                        ),
                    student_id=
                        str(
                            case.student_id
                        )
                        if case.student_id
                        is not None
                        else None,
                    validator_user_id=
                        user_id,
                    model_name=
                        str(
                            study.model_name
                        ),
                    task=
                        "classification",
                    target=
                        study.target,
                    threshold=
                        case.threshold,
                    predicted_class=
                        str(
                            case.predicted_class
                        ),
                    predicted_probability=
                        case.predicted_probability,
                    teacher_detected_class=
                        teacher_class,
                    teacher_confidence=
                        int(
                            confidence
                        ),
                    difficulty_level=
                        difficulty_level,
                    teacher_factors=
                        factors or [],
                    teacher_initial_comment=
                        str(
                            initial_comment
                        ).strip(),
                    algorithmic_diagnosis=
                        diagnosis,
                )
            )

            assignment = (
                service
                .lock_assignment(
                    assignment_id=
                        assignment.id,
                    teacher_user_id=
                        user_id,
                    validation_id=
                        validation.id,
                )
            )

            validation = (
                bootstrap
                .teacher_validation_controller
                .reveal_model(
                    validation.id
                )
            )

            assignment = (
                service
                .reveal_assignment(
                    assignment_id=
                        assignment.id,
                    teacher_user_id=
                        user_id,
                    validation_id=
                        validation.id,
                )
            )

        except Exception as exc:
            logger.exception(
                "Verrouillage H7 impossible."
            )

            return (
                dbc.Alert(
                    (
                        "Verrouillage H7 "
                        f"impossible : {exc}"
                    ),
                    color="danger",
                ),
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
            )

        return (
            dbc.Alert(
                (
                    "Jugement indépendant "
                    "verrouillé. Le résultat "
                    "EMIDAF est maintenant "
                    "visible."
                ),
                color="success",
            ),
            {
                "assignment_id":
                    assignment.id,
                "validation_id":
                    validation.id,
                "observation_id":
                    str(
                        case.observation_id
                    ),
                "status":
                    "model_revealed",
            },
            {
                "display": "none"
            },
            {
                "display": "block"
            },
            _algorithmic_card(
                validation
            ),
            True,
        )

    try:
        case = _get_case(
            project_id,
            dataset_id,
            observation_id,
        )

        context = case[
            "context"
        ]

        diagnosis = {
            "observation_id":
                str(
                    observation_id
                ),
            "student_id":
                str(
                    case["student_id"]
                )
                if case["student_id"]
                is not None
                else None,
            "prediction":
                str(
                    case["prediction"]
                ),
            "probability":
                case["probability"],
            "threshold":
                case["threshold"],
            "model_name":
                context.get(
                    "model_name"
                ),
            "target":
                context.get(
                    "target"
                ),
            "positive_label":
                context.get(
                    "positive_label"
                ),
        }

        bootstrap = _bootstrap()

        validation = (
            bootstrap
            .teacher_validation_controller
            .create_locked_judgment(
                project_id=
                    int(project_id),
                dataset_id=
                    int(dataset_id),
                observation_id=
                    str(
                        observation_id
                    ),
                student_id=
                    str(
                        case[
                            "student_id"
                        ]
                    )
                    if case[
                        "student_id"
                    ]
                    is not None
                    else None,
                validator_user_id=
                    user_id,
                model_name=
                    str(
                        context.get(
                            "model_name",
                            "unknown",
                        )
                    ),
                task=
                    str(
                        context.get(
                            "task",
                            "classification",
                        )
                    ),
                target=
                    context.get(
                        "target"
                    ),
                threshold=
                    case[
                        "threshold"
                    ],
                predicted_class=
                    str(
                        case[
                            "prediction"
                        ]
                    ),
                predicted_probability=
                    case[
                        "probability"
                    ],
                teacher_detected_class=
                    teacher_class,
                teacher_confidence=
                    int(
                        confidence
                    ),
                difficulty_level=
                    difficulty_level,
                teacher_factors=
                    factors or [],
                teacher_initial_comment=
                    initial_comment,
                algorithmic_diagnosis=
                    diagnosis,
            )
        )

        validation = (
            bootstrap
            .teacher_validation_controller
            .reveal_model(
                validation.id
            )
        )

    except Exception as exc:
        logger.exception(
            "Verrouillage impossible."
        )

        return (
            dbc.Alert(
                (
                    "Verrouillage impossible : "
                    f"{exc}"
                ),
                color="danger",
            ),
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    return (
        dbc.Alert(
            (
                "Jugement indépendant "
                "verrouillé. "
                "Le résultat EMIDAF est "
                "maintenant visible."
            ),
            color="success",
        ),
        {
            "validation_id":
                validation.id,
            "observation_id":
                str(
                    observation_id
                ),
            "status":
                "model_revealed",
        },
        {
            "display": "none"
        },
        {
            "display": "block"
        },
        _algorithmic_card(
            validation
        ),
        True,
    )


# =========================================================
# FINALISATION
# =========================================================

@callback(
    Output(
        "edse-validation-status",
        "children",
    ),

    Output(
        "edse-validation-history",
        "children",
        allow_duplicate=True,
    ),

    Output(
        "edse-validation-phase-2",
        "style",
        allow_duplicate=True,
    ),

    Output(
        "edse-validation-lock-state",
        "data",
        allow_duplicate=True,
    ),

    Output(
        "edse-validation-observation",
        "disabled",
        allow_duplicate=True,
    ),

    Input(
        "edse-validation-save",
        "n_clicks",
    ),

    State(
        "edse-validation-detection",
        "value",
    ),

    State(
        "edse-validation-diagnosis",
        "value",
    ),

    State(
        "edse-validation-disagreement-reasons",
        "value",
    ),

    State(
        "edse-validation-post-model-comment",
        "value",
    ),

    State(
        "edse-validation-lock-state",
        "data",
    ),

    State(
        "edse-project-id",
        "data",
    ),

    State(
        "edse-dataset-id",
        "data",
    ),

    prevent_initial_call=True,
)
def finalize_validation(
    n_clicks,
    detection_validation,
    diagnosis_validation,
    disagreement_reasons,
    post_model_comment,
    lock_state,
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

    if not lock_state:
        return (
            dbc.Alert(
                (
                    "Aucun jugement verrouillé. "
                    "Recommencez par la phase 1."
                ),
                color="warning",
            ),
            no_update,
            no_update,
            no_update,
            no_update,
        )

    if detection_validation is None:
        return (
            dbc.Alert(
                (
                    "La validation de la "
                    "détection est obligatoire."
                ),
                color="warning",
            ),
            no_update,
            no_update,
            no_update,
            no_update,
        )

    if diagnosis_validation is None:
        return (
            dbc.Alert(
                (
                    "La validation du diagnostic "
                    "est obligatoire."
                ),
                color="warning",
            ),
            no_update,
            no_update,
            no_update,
            no_update,
        )

    disagreement = (
        detection_validation
        in {
            "not_confirmed",
            "partially_confirmed",
        }
        or diagnosis_validation
        in {
            "not_confirmed",
            "partially_confirmed",
        }
    )

    if (
        disagreement
        and not (
            post_model_comment
            and str(
                post_model_comment
            ).strip()
        )
    ):
        return (
            dbc.Alert(
                (
                    "En cas de désaccord ou "
                    "d'accord partiel, le "
                    "commentaire post-modèle "
                    "est obligatoire."
                ),
                color="warning",
            ),
            no_update,
            no_update,
            no_update,
            no_update,
        )

    validation_id = lock_state.get(
        "validation_id"
    )

    if _is_h7_context(
        project_id,
        dataset_id,
    ):
        user_id = _current_user_id()

        assignment_id = lock_state.get(
            "assignment_id"
        )

        if (
            user_id is None
            or assignment_id is None
            or validation_id is None
        ):
            return (
                dbc.Alert(
                    (
                        "État de validation H7 "
                        "incomplet."
                    ),
                    color="danger",
                ),
                no_update,
                no_update,
                no_update,
                no_update,
            )

        try:
            bundle = _get_h7_bundle(
                assignment_id,
                user_id,
            )

            bootstrap = bundle[
                "bootstrap"
            ]

            service = bundle[
                "assignment_service"
            ]

            assignment = bundle[
                "assignment"
            ]

            if (
                assignment.validation_id
                is None
                or int(
                    assignment.validation_id
                )
                != int(
                    validation_id
                )
            ):
                raise PermissionError(
                    "La validation ne correspond "
                    "pas à l'affectation H7."
                )

            if str(
                assignment.status
            ) != "model_revealed":
                raise RuntimeError(
                    "Le cas H7 n'est pas dans "
                    "l'état model_revealed."
                )

            validation = (
                bootstrap
                .teacher_validation_controller
                .complete_validation(
                    int(
                        validation_id
                    ),
                    detection_validation=
                        detection_validation,
                    diagnosis_validation=
                        diagnosis_validation,
                    post_model_comment=
                        post_model_comment,
                    disagreement_reasons=
                        disagreement_reasons
                        or [],
                )
            )

            assignment = (
                service
                .complete_assignment(
                    assignment_id=
                        assignment.id,
                    teacher_user_id=
                        user_id,
                    validation_id=
                        validation.id,
                )
            )

            history = _history(
                [validation]
            )

            try:
                register_analysis(
                    H7_PROJECT_ID,
                    H7_DATASET_ID,
                    "teacher_validation",
                    {
                        "study_id":
                            H7_STUDY_ID,
                        "assignment_id":
                            assignment.id,
                        "validation_id":
                            validation.id,
                        "observation_id":
                            validation.observation_id,
                        "validation_status":
                            "completed",
                        "teacher_detected_class":
                            validation
                            .teacher_detected_class,
                        "teacher_confidence":
                            validation
                            .teacher_confidence,
                        "detection_validation":
                            validation
                            .detection_validation,
                        "diagnosis_validation":
                            validation
                            .diagnosis_validation,
                        "disagreement_reasons":
                            validation
                            .disagreement_reasons,
                    },
                )

            except Exception:
                logger.exception(
                    "Résumé H7 non enregistré "
                    "dans analysis_results."
                )

        except Exception as exc:
            logger.exception(
                "Finalisation H7 impossible."
            )

            return (
                dbc.Alert(
                    (
                        "Finalisation H7 "
                        f"impossible : {exc}"
                    ),
                    color="danger",
                ),
                no_update,
                no_update,
                no_update,
                no_update,
            )

        return (
            dbc.Alert(
                (
                    "Validation H7 finalisée "
                    "avec succès — "
                    f"cas {assignment.id}."
                ),
                color="success",
            ),
            history,
            {
                "display": "none"
            },
            {
                "assignment_id":
                    assignment.id,
                "validation_id":
                    validation.id,
                "observation_id":
                    str(
                        validation
                        .observation_id
                    ),
                "status":
                    "completed",
            },
            False,
        )

    try:
        bootstrap = _bootstrap()

        validation = (
            bootstrap
            .teacher_validation_controller
            .complete_validation(
                int(
                    validation_id
                ),
                detection_validation=
                    detection_validation,
                diagnosis_validation=
                    diagnosis_validation,
                post_model_comment=
                    post_model_comment,
                disagreement_reasons=
                    disagreement_reasons
                    or [],
            )
        )

        validations = (
            bootstrap
            .teacher_validation_controller
            .get_for_observation(
                int(
                    project_id
                ),
                int(
                    dataset_id
                ),
                str(
                    validation
                    .observation_id
                ),
            )
        )

        history = _history(
            validations
        )

        try:
            register_analysis(
                project_id,
                dataset_id,
                "teacher_validation",
                {
                    "validation_id":
                        validation.id,
                    "observation_id":
                        validation
                        .observation_id,
                    "validation_status":
                        "completed",
                    "teacher_detected_class":
                        validation
                        .teacher_detected_class,
                    "teacher_confidence":
                        validation
                        .teacher_confidence,
                    "detection_validation":
                        validation
                        .detection_validation,
                    "diagnosis_validation":
                        validation
                        .diagnosis_validation,
                    "disagreement_reasons":
                        validation
                        .disagreement_reasons,
                },
            )

        except Exception:
            logger.exception(
                "Enregistrement du résumé "
                "teacher_validation "
                "impossible."
            )

    except Exception as exc:
        logger.exception(
            "Finalisation impossible."
        )

        return (
            dbc.Alert(
                (
                    "Finalisation impossible : "
                    f"{exc}"
                ),
                color="danger",
            ),
            no_update,
            no_update,
            no_update,
            no_update,
        )

    return (
        dbc.Alert(
            (
                "Validation finalisée avec "
                "succès — identifiant "
                f"{validation.id}."
            ),
            color="success",
        ),
        history,
        {
            "display": "none"
        },
        {
            "validation_id":
                validation.id,
            "observation_id":
                str(
                    validation
                    .observation_id
                ),
            "status":
                "completed",
        },
        False,
    )
