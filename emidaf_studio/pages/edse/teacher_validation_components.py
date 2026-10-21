from __future__ import annotations

from dash import dcc, html
import dash_bootstrap_components as dbc


def teacher_validation_tab():

    return dbc.Tab(
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            "VALIDATION HUMAINE",
                            className="edse-v2-section-kicker",
                        ),

                        html.H4(
                            "Validation enseignant",
                            className="edse-v2-section-title",
                        ),

                        html.P(
                            (
                                "La validation suit un protocole "
                                "séquentiel : jugement enseignant "
                                "indépendant, verrouillage, puis "
                                "révélation du résultat EMIDAF."
                            ),
                            className="edse-v2-section-subtitle",
                        ),
                    ],
                    className="edse-v2-section-heading",
                ),

                dbc.Alert(
                    (
                        "Sélectionnez une observation. "
                        "La prédiction, la probabilité, le seuil "
                        "et les explications du modèle restent "
                        "masqués jusqu'au verrouillage du jugement."
                    ),
                    color="info",
                    id="edse-validation-help",
                ),

                html.Div(
                    id="edse-validation-metrics",
                    className="mb-4",
                ),

                # ==========================================
                # CHOIX DE L'OBSERVATION
                # ==========================================

                html.Div(
                    [
                        dbc.Label(
                            "Élève / observation",
                            html_for="edse-validation-observation",
                            className="edse-v2-label",
                        ),

                        dcc.Dropdown(
                            id="edse-validation-observation",
                            options=[],
                            value=None,
                            clearable=True,
                            placeholder=(
                                "Sélectionner une observation"
                            ),
                            className="edse-v2-dropdown",
                        ),
                    ],
                    className="edse-v2-field mb-4",
                ),

                # Contexte visible sans résultat algorithmique.
                html.Div(
                    id="edse-validation-student-context",
                    className="mb-4",
                ),

                # ==========================================
                # PHASE 1
                # ==========================================

                html.Div(
                    [
                        dbc.Alert(
                            [
                                html.Strong(
                                    "PHASE 1 — Jugement indépendant"
                                ),
                                html.Br(),
                                (
                                    "Évaluez l'élève à partir des "
                                    "seules informations disponibles. "
                                    "Le résultat EMIDAF n'est pas "
                                    "encore visible."
                                ),
                            ],
                            color="primary",
                        ),

                        html.Div(
                            [
                                dbc.Label(
                                    (
                                        "Selon votre propre appréciation, "
                                        "cet élève présente-t-il "
                                        "actuellement une difficulté "
                                        "académique en mathématiques ?"
                                    ),
                                    className="edse-v2-label",
                                ),

                                dcc.Dropdown(
                                    id=(
                                        "edse-validation-"
                                        "teacher-class"
                                    ),
                                    options=[
                                        {
                                            "label": (
                                                "Oui — difficulté "
                                                "observée"
                                            ),
                                            "value": "difficulty",
                                        },
                                        {
                                            "label": (
                                                "Non — aucune difficulté "
                                                "observée"
                                            ),
                                            "value": "no_difficulty",
                                        },
                                        {
                                            "label": "Non évaluable",
                                            "value": "not_evaluable",
                                        },
                                    ],
                                    placeholder=(
                                        "Choisir le jugement "
                                        "de l'enseignant"
                                    ),
                                    clearable=True,
                                ),

                                dbc.FormText(
                                    (
                                        "Ce jugement est enregistré "
                                        "avant toute exposition à la "
                                        "prédiction EMIDAF."
                                    )
                                ),
                            ],
                            className="edse-v2-field mb-4",
                        ),

                        html.Div(
                            [
                                dbc.Label(
                                    (
                                        "Niveau de confiance "
                                        "dans votre jugement"
                                    ),
                                    className="edse-v2-label",
                                ),

                                dcc.Slider(
                                    id="edse-validation-confidence",
                                    min=1,
                                    max=5,
                                    step=1,
                                    value=3,
                                    marks={
                                        1: "1",
                                        2: "2",
                                        3: "3",
                                        4: "4",
                                        5: "5",
                                    },
                                ),

                                dbc.FormText(
                                    (
                                        "1 = très faible ; "
                                        "2 = faible ; "
                                        "3 = moyen ; "
                                        "4 = élevé ; "
                                        "5 = très élevé."
                                    )
                                ),
                            ],
                            className="edse-v2-field mb-4",
                        ),

                        html.Div(
                            [
                                dbc.Label(
                                    "Niveau de difficulté observé",
                                    className="edse-v2-label",
                                ),

                                dcc.Dropdown(
                                    id="edse-validation-difficulty",
                                    options=[
                                        {
                                            "label": "Aucune",
                                            "value": "none",
                                        },
                                        {
                                            "label": "Légère",
                                            "value": "mild",
                                        },
                                        {
                                            "label": "Modérée",
                                            "value": "moderate",
                                        },
                                        {
                                            "label": "Importante",
                                            "value": "severe",
                                        },
                                    ],
                                    placeholder="Choisir",
                                    clearable=True,
                                ),
                            ],
                            className="edse-v2-field mb-4",
                        ),

                        html.Div(
                            [
                                dbc.Label(
                                    (
                                        "Facteurs observés "
                                        "par l'enseignant"
                                    ),
                                    className="edse-v2-label",
                                ),

                                dcc.Checklist(
                                    id="edse-validation-factors",
                                    options=[
                                        {
                                            "label": (
                                                " Difficultés de "
                                                "compréhension des concepts"
                                            ),
                                            "value": "concepts",
                                        },
                                        {
                                            "label": (
                                                " Difficultés de raisonnement"
                                            ),
                                            "value": "reasoning",
                                        },
                                        {
                                            "label": (
                                                " Difficultés de calcul"
                                            ),
                                            "value": "calculation",
                                        },
                                        {
                                            "label": " Faible motivation",
                                            "value": "low_motivation",
                                        },
                                        {
                                            "label": (
                                                " Faible intérêt pour "
                                                "les mathématiques"
                                            ),
                                            "value": "low_interest",
                                        },
                                        {
                                            "label": " Stress / anxiété",
                                            "value": "stress",
                                        },
                                        {
                                            "label": (
                                                " Travail personnel "
                                                "insuffisant"
                                            ),
                                            "value": (
                                                "low_personal_work"
                                            ),
                                        },
                                        {
                                            "label": (
                                                " Manque de pratique"
                                            ),
                                            "value": "low_practice",
                                        },
                                        {
                                            "label": (
                                                " Absences / irrégularité"
                                            ),
                                            "value": "attendance",
                                        },
                                        {
                                            "label": (
                                                " Difficultés "
                                                "méthodologiques"
                                            ),
                                            "value": "methodology",
                                        },
                                        {
                                            "label": " Autre",
                                            "value": "other",
                                        },
                                    ],
                                    value=[],
                                ),
                            ],
                            className="mb-4",
                        ),

                        html.Div(
                            [
                                dbc.Label(
                                    (
                                        "Commentaire initial "
                                        "de l'enseignant"
                                    ),
                                    className="edse-v2-label",
                                ),

                                dbc.Textarea(
                                    id=(
                                        "edse-validation-"
                                        "initial-comment"
                                    ),
                                    placeholder=(
                                        "Justifiez si nécessaire "
                                        "votre appréciation avant "
                                        "de consulter le modèle..."
                                    ),
                                    rows=4,
                                ),
                            ],
                            className="mb-4",
                        ),

                        dbc.Button(
                            [
                                html.I(
                                    className=(
                                        "bi bi-lock-fill me-2"
                                    )
                                ),
                                (
                                    "Valider et verrouiller "
                                    "mon jugement indépendant"
                                ),
                            ],
                            id="edse-validation-lock",
                            color="primary",
                        ),

                        html.Div(
                            id="edse-validation-lock-status",
                            className="mt-3",
                        ),
                    ],
                    id="edse-validation-phase-1",
                ),

                # ==========================================
                # PHASE 2
                # ==========================================

                html.Div(
                    [
                        dbc.Alert(
                            [
                                html.Strong(
                                    (
                                        "PHASE 2 — Confrontation "
                                        "avec EMIDAF"
                                    )
                                ),
                                html.Br(),
                                (
                                    "Votre jugement indépendant "
                                    "est maintenant verrouillé. "
                                    "Le résultat algorithmique peut "
                                    "être consulté."
                                ),
                            ],
                            color="info",
                        ),

                        html.Div(
                            id=(
                                "edse-validation-"
                                "algorithmic-result"
                            ),
                            className="mb-4",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            (
                                                "Validation de "
                                                "la détection"
                                            ),
                                            className=(
                                                "edse-v2-label"
                                            ),
                                        ),

                                        dcc.Dropdown(
                                            id=(
                                                "edse-validation-"
                                                "detection"
                                            ),
                                            options=[
                                                {
                                                    "label": "D'accord",
                                                    "value": "confirmed",
                                                },
                                                {
                                                    "label": (
                                                        "Partiellement "
                                                        "d'accord"
                                                    ),
                                                    "value": (
                                                        "partially_"
                                                        "confirmed"
                                                    ),
                                                },
                                                {
                                                    "label": (
                                                        "Pas d'accord"
                                                    ),
                                                    "value": (
                                                        "not_confirmed"
                                                    ),
                                                },
                                                {
                                                    "label": (
                                                        "Non évaluable"
                                                    ),
                                                    "value": (
                                                        "not_evaluable"
                                                    ),
                                                },
                                            ],
                                            placeholder="Choisir",
                                            clearable=True,
                                        ),
                                    ],
                                    md=6,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            (
                                                "Validation de la "
                                                "caractérisation explicative"
                                            ),
                                            className=(
                                                "edse-v2-label"
                                            ),
                                        ),

                                        dcc.Dropdown(
                                            id=(
                                                "edse-validation-"
                                                "diagnosis"
                                            ),
                                            options=[
                                                {
                                                    "label": "D'accord",
                                                    "value": "confirmed",
                                                },
                                                {
                                                    "label": (
                                                        "Partiellement "
                                                        "d'accord"
                                                    ),
                                                    "value": (
                                                        "partially_"
                                                        "confirmed"
                                                    ),
                                                },
                                                {
                                                    "label": (
                                                        "Pas d'accord"
                                                    ),
                                                    "value": (
                                                        "not_confirmed"
                                                    ),
                                                },
                                                {
                                                    "label": (
                                                        "Non évaluable"
                                                    ),
                                                    "value": (
                                                        "not_evaluable"
                                                    ),
                                                },
                                            ],
                                            placeholder="Choisir",
                                            clearable=True,
                                        ),
                                    ],
                                    md=6,
                                ),
                            ],
                            className="g-3 mb-4",
                        ),

                        html.Div(
                            [
                                dbc.Label(
                                    (
                                        "Raison(s) du désaccord "
                                        "ou de la réserve"
                                    ),
                                    className="edse-v2-label",
                                ),

                                dcc.Checklist(
                                    id=(
                                        "edse-validation-"
                                        "disagreement-reasons"
                                    ),
                                    options=[
                                        {
                                            "label": (
                                                " Information importante "
                                                "absente"
                                            ),
                                            "value": (
                                                "information_missing"
                                            ),
                                        },
                                        {
                                            "label": (
                                                " Difficulté récente"
                                            ),
                                            "value": (
                                                "recent_difficulty"
                                            ),
                                        },
                                        {
                                            "label": " Absentéisme",
                                            "value": "absenteeism",
                                        },
                                        {
                                            "label": (
                                                " Difficulté conceptuelle"
                                            ),
                                            "value": (
                                                "conceptual_difficulty"
                                            ),
                                        },
                                        {
                                            "label": (
                                                " Contexte familial"
                                            ),
                                            "value": "family_context",
                                        },
                                        {
                                            "label": (
                                                " Contexte pédagogique "
                                                "/ classe"
                                            ),
                                            "value": (
                                                "pedagogical_context"
                                            ),
                                        },
                                        {
                                            "label": (
                                                " Seuil jugé trop haut"
                                            ),
                                            "value": (
                                                "threshold_too_high"
                                            ),
                                        },
                                        {
                                            "label": (
                                                " Seuil jugé trop bas"
                                            ),
                                            "value": (
                                                "threshold_too_low"
                                            ),
                                        },
                                        {
                                            "label": " Autre",
                                            "value": "other",
                                        },
                                    ],
                                    value=[],
                                ),
                            ],
                            className="mb-4",
                        ),

                        html.Div(
                            [
                                dbc.Label(
                                    (
                                        "Commentaire après "
                                        "consultation du modèle"
                                    ),
                                    className="edse-v2-label",
                                ),

                                dbc.Textarea(
                                    id=(
                                        "edse-validation-"
                                        "post-model-comment"
                                    ),
                                    placeholder=(
                                        "Précisez notamment les "
                                        "raisons d'un désaccord..."
                                    ),
                                    rows=4,
                                ),
                            ],
                            className="mb-4",
                        ),

                        dbc.Button(
                            [
                                html.I(
                                    className=(
                                        "bi bi-check2-circle me-2"
                                    )
                                ),
                                "Finaliser la validation",
                            ],
                            id="edse-validation-save",
                            color="success",
                        ),
                    ],
                    id="edse-validation-phase-2",
                    style={"display": "none"},
                ),

                html.Div(
                    id="edse-validation-status",
                    className="mb-4 mt-3",
                ),

                dcc.Store(
                    id="edse-validation-lock-state",
                    data=None,
                    storage_type="session",
                ),

                html.H5(
                    "Historique des validations",
                    className="mt-4",
                ),

                html.Div(
                    id="edse-validation-history",
                ),
            ],
            className="edse-v2-tab-content",
        ),
        label="Validation enseignant",
        tab_id="edse-tab-validation",
    )
