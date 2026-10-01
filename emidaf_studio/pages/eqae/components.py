"""
=========================================================
EMIDAF Studio
EQAE - UI Components
=========================================================
"""

from __future__ import annotations

import dash_bootstrap_components as dbc

from dash import dcc, html


def eqae_intro_component(
    title: str,
    description: str,
    *,
    note: str | None = None,
):
    """
    Composant introductif homogène pour les onglets EQAE.
    """

    children = [
        html.H4(
            title,
            className="mb-3",
        ),
        html.P(
            description,
            className="text-muted",
        ),
    ]

    if note:
        children.append(
            dbc.Alert(
                note,
                color="light",
                className="mt-3 mb-0",
            )
        )

    return dbc.Card(
        dbc.CardBody(
            children
        ),
        className="shadow-sm",
    )


def eqae_metric_card(
    title: str,
    value,
    *,
    subtitle: str | None = None,
):
    """
    Carte métrique homogène pour EQAE.
    """

    children = [
        html.Div(
            title,
            className="text-muted small",
        ),
        html.Div(
            value,
            className="fs-4 fw-semibold",
        ),
    ]

    if subtitle:
        children.append(
            html.Div(
                subtitle,
                className="text-muted small mt-1",
            )
        )

    return dbc.Card(
        dbc.CardBody(
            children
        ),
        className="h-100 shadow-sm",
    )


def eqae_corpus_component(
    *,
    n_rows: int,
    n_valid_documents: int,
    n_missing: int,
    n_empty: int,
    n_segments: int,
    preview,
    column: str,
):
    """
    Affiche la synthèse du corpus qualitatif initial.
    """

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        eqae_metric_card(
                            "Lignes du dataset",
                            n_rows,
                        ),
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        eqae_metric_card(
                            "Documents valides",
                            n_valid_documents,
                        ),
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        eqae_metric_card(
                            "Valeurs manquantes",
                            n_missing,
                        ),
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        eqae_metric_card(
                            "Segments initiaux",
                            n_segments,
                        ),
                        md=3,
                        className="mb-3",
                    ),
                ],
                className="g-3",
            ),

            dbc.Alert(
                [
                    html.Strong(
                        "Unité de segmentation actuelle : "
                    ),
                    (
                        "chaque valeur textuelle valide de "
                        f"« {column} » est considérée comme "
                        "un document et produit un segment initial. "
                        "Cette segmentation pourra ensuite être "
                        "raffinée par le chercheur."
                    ),
                ],
                color="light",
                className="mt-2",
            ),

            html.H5(
                "Aperçu des unités qualitatives",
                className="mt-4 mb-3",
            ),

            dbc.Table.from_dataframe(
                preview,
                striped=True,
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
            ),

            dbc.Alert(
                (
                    f"{n_empty} valeur(s) vide(s) ont été "
                    "exclue(s) du corpus initial."
                ),
                color="secondary",
                className="mt-3 mb-0",
            )
            if n_empty
            else None,
        ]
    )



def _eqae_codebook_options(
    payload,
):
    """
    Construit les options de sélection
    à partir d'un codebook sérialisé.
    """

    if not isinstance(payload, dict):
        return []

    codes = payload.get(
        "codes",
        [],
    )

    return [
        {
            "label": code.get(
                "name",
                code.get("code_id", ""),
            ),
            "value": code.get(
                "code_id"
            ),
        }
        for code in codes
        if code.get("code_id")
    ]


def eqae_codebook_table(
    payload,
):
    """
    Tableau lisible du codebook EQAE.
    """

    if not isinstance(payload, dict):
        payload = {}

    codes = payload.get(
        "codes",
        [],
    )

    if not codes:
        return dbc.Alert(
            (
                "Aucun code n'a encore été créé. "
                "Commencez par définir un premier code."
            ),
            color="light",
            className="mb-0",
        )

    names = {
        code.get("code_id"): code.get(
            "name",
            "",
        )
        for code in codes
    }

    header = html.Thead(
        html.Tr(
            [
                html.Th("Code"),
                html.Th("Description"),
                html.Th("Parent"),
                html.Th("Couleur"),
                html.Th("Statut"),
            ]
        )
    )

    rows = []

    for code in codes:

        parent_id = code.get(
            "parent_code_id"
        )

        rows.append(
            html.Tr(
                [
                    html.Td(
                        code.get(
                            "name",
                            "",
                        )
                    ),
                    html.Td(
                        code.get(
                            "description",
                            "",
                        )
                    ),
                    html.Td(
                        names.get(
                            parent_id,
                            "—",
                        )
                        if parent_id
                        else "—"
                    ),
                    html.Td(
                        html.Span(
                            "■",
                            style={
                                "color": (
                                    code.get("color")
                                    or "#6c757d"
                                ),
                                "fontSize": "1.25rem",
                            },
                        )
                    ),
                    html.Td(
                        (
                            "Actif"
                            if code.get(
                                "is_active",
                                True,
                            )
                            else "Inactif"
                        )
                    ),
                ]
            )
        )

    return dbc.Table(
        [
            header,
            html.Tbody(
                rows
            ),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
        className="mb-0",
    )


def eqae_codebook_component(
    payload=None,
):
    """
    Workspace de gestion du codebook EQAE.
    """

    payload = (
        payload
        if isinstance(payload, dict)
        else {}
    )

    name = payload.get(
        "name",
        "Codebook qualitatif",
    )

    description = payload.get(
        "description",
        "",
    )

    options = _eqae_codebook_options(
        payload
    )

    return html.Div(
        [
            dbc.Alert(
                [
                    html.Strong(
                        "Codebook qualitatif : "
                    ),
                    (
                        "les codes sont définis et validés "
                        "par le chercheur. Les contraintes "
                        "de hiérarchie sont contrôlées par "
                        "le moteur EQAE."
                    ),
                ],
                color="light",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Paramètres du codebook",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Nom du codebook"
                                        ),
                                        dbc.Input(
                                            id="eqae-codebook-name",
                                            value=name,
                                            placeholder=(
                                                "Nom du codebook"
                                            ),
                                        ),
                                    ],
                                    md=5,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Description"
                                        ),
                                        dbc.Input(
                                            id=(
                                                "eqae-codebook-"
                                                "description"
                                            ),
                                            value=description,
                                            placeholder=(
                                                "Description du "
                                                "codebook"
                                            ),
                                        ),
                                    ],
                                    md=7,
                                ),
                            ],
                            className="g-3",
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Ajouter un code",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Nom du code"
                                        ),
                                        dbc.Input(
                                            id="eqae-code-name",
                                            value="",
                                            placeholder=(
                                                "Ex. Motivation"
                                            ),
                                        ),
                                    ],
                                    md=4,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Code parent"
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-code-parent"
                                            ),
                                            options=options,
                                            value=None,
                                            clearable=True,
                                            placeholder=(
                                                "Aucun parent"
                                            ),
                                        ),
                                    ],
                                    md=4,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Couleur"
                                        ),
                                        dbc.Input(
                                            id="eqae-code-color",
                                            type="color",
                                            value="#6c757d",
                                        ),
                                    ],
                                    md=4,
                                ),
                            ],
                            className="g-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Description du code",
                                            className="mt-3",
                                        ),
                                        dbc.Textarea(
                                            id=(
                                                "eqae-code-"
                                                "description"
                                            ),
                                            value="",
                                            placeholder=(
                                                "Définition "
                                                "opérationnelle "
                                                "du code"
                                            ),
                                            rows=3,
                                        ),
                                    ],
                                    md=9,
                                ),

                                dbc.Col(
                                    dbc.Button(
                                        "Ajouter le code",
                                        id="eqae-add-code",
                                        color="primary",
                                        className=(
                                            "w-100 mt-4"
                                        ),
                                        n_clicks=0,
                                    ),
                                    md=3,
                                ),
                            ],
                            className="g-3",
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            html.Div(
                id="eqae-codebook-feedback",
                className="mb-3",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Codes du codebook",
                            className="mb-3",
                        ),

                        html.Div(
                            id="eqae-codebook-table",
                            children=(
                                eqae_codebook_table(
                                    payload
                                )
                            ),
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Supprimer un code",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id=(
                                            "eqae-delete-code-id"
                                        ),
                                        options=options,
                                        value=None,
                                        clearable=True,
                                        placeholder=(
                                            "Sélectionner un code"
                                        ),
                                    ),
                                    md=9,
                                ),

                                dbc.Col(
                                    dbc.Button(
                                        "Supprimer",
                                        id="eqae-delete-code",
                                        color="danger",
                                        outline=True,
                                        className="w-100",
                                        n_clicks=0,
                                    ),
                                    md=3,
                                ),
                            ],
                            className="g-3",
                        ),

                        dbc.Alert(
                            (
                                "Un code parent possédant "
                                "des sous-codes ne peut pas "
                                "être supprimé directement."
                            ),
                            color="warning",
                            className="mt-3 mb-0 py-2",
                        ),
                    ]
                ),
                className="shadow-sm",
            ),
        ]
    )


def _eqae_coding_options(
    codebook_payload,
):
    """
    Options de codes disponibles pour le codage.
    """

    return _eqae_codebook_options(
        codebook_payload
    )


def eqae_assignments_table(
    coding_payload,
    codebook_payload,
):
    """
    Tableau des affectations qualitatives.
    """

    coding_payload = (
        coding_payload
        if isinstance(
            coding_payload,
            dict,
        )
        else {}
    )

    codebook_payload = (
        codebook_payload
        if isinstance(
            codebook_payload,
            dict,
        )
        else {}
    )

    assignments = coding_payload.get(
        "assignments",
        [],
    )

    if not assignments:
        return dbc.Alert(
            (
                "Aucune affectation de code "
                "n'a encore été enregistrée."
            ),
            color="light",
            className="mb-0",
        )

    names = {
        code.get("code_id"): code.get(
            "name",
            code.get("code_id", ""),
        )
        for code in codebook_payload.get(
            "codes",
            [],
        )
        if isinstance(code, dict)
    }

    rows = []

    for assignment in assignments:
        rows.append(
            html.Tr(
                [
                    html.Td(
                        assignment.get(
                            "document_id",
                            "",
                        )
                    ),
                    html.Td(
                        assignment.get(
                            "segment_id",
                            "",
                        )
                    ),
                    html.Td(
                        names.get(
                            assignment.get(
                                "code_id"
                            ),
                            assignment.get(
                                "code_id",
                                "",
                            ),
                        )
                    ),
                    html.Td(
                        assignment.get(
                            "mode",
                            "",
                        )
                    ),
                    html.Td(
                        assignment.get(
                            "memo",
                            "",
                        )
                    ),
                ]
            )
        )

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Document"),
                        html.Th("Segment"),
                        html.Th("Code"),
                        html.Th("Mode"),
                        html.Th("Mémo"),
                    ]
                )
            ),
            html.Tbody(
                rows
            ),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
        className="mb-0",
    )


def eqae_coding_component(
    *,
    segments,
    codebook_payload,
    coding_payload,
):
    """
    Workspace de codage manuel EQAE.
    """

    segment_options = [
        {
            "label": (
                f"{segment.document_id} — "
                f"{segment.text[:100]}"
                + (
                    "…"
                    if len(segment.text) > 100
                    else ""
                )
            ),
            "value": segment.segment_id,
        }
        for segment in segments
    ]

    code_options = _eqae_coding_options(
        codebook_payload
    )

    assignments = (
        coding_payload.get(
            "assignments",
            [],
        )
        if isinstance(
            coding_payload,
            dict,
        )
        else []
    )

    delete_options = [
        {
            "label": (
                f"{assignment.get('document_id', '')} — "
                f"{assignment.get('assignment_id', '')[:8]}"
            ),
            "value": assignment.get(
                "assignment_id"
            ),
        }
        for assignment in assignments
        if assignment.get(
            "assignment_id"
        )
    ]

    return html.Div(
        [
            dbc.Alert(
                [
                    html.Strong(
                        "Codage manuel : "
                    ),
                    (
                        "sélectionnez une unité qualitative "
                        "et affectez-lui un ou plusieurs codes "
                        "validés du Codebook."
                    ),
                ],
                color="light",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Nouvelle affectation",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Segment"
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-coding-"
                                                "segment"
                                            ),
                                            options=(
                                                segment_options
                                            ),
                                            value=None,
                                            placeholder=(
                                                "Sélectionner "
                                                "un segment"
                                            ),
                                        ),
                                    ],
                                    md=7,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Code"
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-coding-"
                                                "code"
                                            ),
                                            options=(
                                                code_options
                                            ),
                                            value=None,
                                            placeholder=(
                                                "Sélectionner "
                                                "un code"
                                            ),
                                        ),
                                    ],
                                    md=5,
                                ),
                            ],
                            className="g-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Mémo de codage",
                                            className="mt-3",
                                        ),
                                        dbc.Textarea(
                                            id=(
                                                "eqae-coding-"
                                                "memo"
                                            ),
                                            value="",
                                            rows=3,
                                            placeholder=(
                                                "Justification ou "
                                                "observation du "
                                                "chercheur"
                                            ),
                                        ),
                                    ],
                                    md=9,
                                ),

                                dbc.Col(
                                    dbc.Button(
                                        "Affecter le code",
                                        id=(
                                            "eqae-assign-code"
                                        ),
                                        color="primary",
                                        className=(
                                            "w-100 mt-4"
                                        ),
                                        n_clicks=0,
                                    ),
                                    md=3,
                                ),
                            ],
                            className="g-3",
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            html.Div(
                id="eqae-coding-feedback",
                className="mb-3",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Affectations enregistrées",
                            className="mb-3",
                        ),

                        html.Div(
                            id=(
                                "eqae-coding-"
                                "assignments-table"
                            ),
                            children=(
                                eqae_assignments_table(
                                    coding_payload,
                                    codebook_payload,
                                )
                            ),
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Supprimer une affectation",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id=(
                                            "eqae-delete-"
                                            "assignment-id"
                                        ),
                                        options=(
                                            delete_options
                                        ),
                                        value=None,
                                        placeholder=(
                                            "Sélectionner une "
                                            "affectation"
                                        ),
                                    ),
                                    md=9,
                                ),

                                dbc.Col(
                                    dbc.Button(
                                        "Supprimer",
                                        id=(
                                            "eqae-delete-"
                                            "assignment"
                                        ),
                                        color="danger",
                                        outline=True,
                                        className="w-100",
                                        n_clicks=0,
                                    ),
                                    md=3,
                                ),
                            ],
                            className="g-3",
                        ),
                    ]
                ),
                className="shadow-sm",
            ),
        ]
    )


def eqae_assisted_table(
    assisted_payload,
    codebook_payload,
):
    """
    Tableau des suggestions de codage assisté.
    """

    assisted_payload = (
        assisted_payload
        if isinstance(assisted_payload, dict)
        else {}
    )

    codebook_payload = (
        codebook_payload
        if isinstance(codebook_payload, dict)
        else {}
    )

    suggestions = assisted_payload.get(
        "suggestions",
        [],
    )

    if not suggestions:
        return dbc.Alert(
            "Aucune suggestion assistée enregistrée.",
            color="light",
            className="mb-0",
        )

    names = {
        code.get("code_id"): code.get(
            "name",
            code.get("code_id", ""),
        )
        for code in codebook_payload.get(
            "codes",
            [],
        )
        if isinstance(code, dict)
    }

    rows = []

    for item in suggestions:

        confidence = item.get(
            "confidence"
        )

        confidence_label = (
            f"{confidence:.2f}"
            if isinstance(
                confidence,
                (int, float),
            )
            else "—"
        )

        rows.append(
            html.Tr(
                [
                    html.Td(
                        item.get(
                            "document_id",
                            "",
                        )
                    ),
                    html.Td(
                        item.get(
                            "segment_id",
                            "",
                        )
                    ),
                    html.Td(
                        names.get(
                            item.get(
                                "suggested_code_id"
                            ),
                            item.get(
                                "suggested_code_id",
                                "",
                            ),
                        )
                    ),
                    html.Td(
                        confidence_label
                    ),
                    html.Td(
                        item.get(
                            "rationale",
                            "",
                        )
                    ),
                    html.Td(
                        item.get(
                            "source",
                            "",
                        )
                    ),
                    html.Td(
                        item.get(
                            "status",
                            "",
                        )
                    ),
                    html.Td(
                        names.get(
                            item.get(
                                "reviewed_code_id"
                            ),
                            "—",
                        )
                        if item.get(
                            "reviewed_code_id"
                        )
                        else "—"
                    ),
                    html.Td(
                        item.get(
                            "reviewer_note",
                            "",
                        )
                    ),
                ]
            )
        )

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Document"),
                        html.Th("Segment"),
                        html.Th("Code suggéré"),
                        html.Th("Confiance"),
                        html.Th("Justification"),
                        html.Th("Source"),
                        html.Th("Statut"),
                        html.Th("Code validé"),
                        html.Th("Note chercheur"),
                    ]
                )
            ),
            html.Tbody(
                rows
            ),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
        className="mb-0",
    )


def eqae_assisted_component(
    *,
    segments,
    codebook_payload,
    assisted_payload,
):
    """
    Workspace de codage assisté avec
    validation humaine obligatoire.
    """

    code_options = _eqae_codebook_options(
        codebook_payload
    )

    segment_options = [
        {
            "label": (
                f"{segment.document_id} — "
                f"{segment.text[:100]}"
                + (
                    "…"
                    if len(segment.text) > 100
                    else ""
                )
            ),
            "value": segment.segment_id,
        }
        for segment in segments
    ]

    suggestions = (
        assisted_payload.get(
            "suggestions",
            [],
        )
        if isinstance(
            assisted_payload,
            dict,
        )
        else []
    )

    pending = [
        item
        for item in suggestions
        if isinstance(item, dict)
        and item.get("status") == "pending"
    ]

    pending_options = [
        {
            "label": (
                f"{item.get('document_id', '')} — "
                f"{item.get('suggestion_id', '')[:8]}"
            ),
            "value": item.get(
                "suggestion_id"
            ),
        }
        for item in pending
        if item.get(
            "suggestion_id"
        )
    ]

    return html.Div(
        [
            dbc.Alert(
                [
                    html.Strong(
                        "Validation humaine obligatoire : "
                    ),
                    (
                        "une suggestion assistée reste une "
                        "proposition tant qu'elle n'a pas été "
                        "acceptée ou modifiée par le chercheur."
                    ),
                ],
                color="warning",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Créer une suggestion",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Segment"
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-assisted-"
                                                "segment"
                                            ),
                                            options=(
                                                segment_options
                                            ),
                                            value=None,
                                            placeholder=(
                                                "Sélectionner "
                                                "un segment"
                                            ),
                                        ),
                                    ],
                                    md=6,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Code suggéré"
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-assisted-"
                                                "code"
                                            ),
                                            options=(
                                                code_options
                                            ),
                                            value=None,
                                            placeholder=(
                                                "Sélectionner "
                                                "un code"
                                            ),
                                        ),
                                    ],
                                    md=4,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Confiance"
                                        ),
                                        dbc.Input(
                                            id=(
                                                "eqae-assisted-"
                                                "confidence"
                                            ),
                                            type="number",
                                            min=0,
                                            max=1,
                                            step=0.01,
                                            value=None,
                                            placeholder="0 à 1",
                                        ),
                                    ],
                                    md=2,
                                ),
                            ],
                            className="g-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Justification",
                                            className="mt-3",
                                        ),
                                        dbc.Textarea(
                                            id=(
                                                "eqae-assisted-"
                                                "rationale"
                                            ),
                                            value="",
                                            rows=3,
                                            placeholder=(
                                                "Pourquoi ce code "
                                                "est-il suggéré ?"
                                            ),
                                        ),
                                    ],
                                    md=6,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Source",
                                            className="mt-3",
                                        ),
                                        dbc.Input(
                                            id=(
                                                "eqae-assisted-"
                                                "source"
                                            ),
                                            value="assisted",
                                            placeholder=(
                                                "assisted, ETAE, "
                                                "règle, modèle..."
                                            ),
                                        ),
                                    ],
                                    md=3,
                                ),

                                dbc.Col(
                                    dbc.Button(
                                        "Créer la suggestion",
                                        id=(
                                            "eqae-create-"
                                            "suggestion"
                                        ),
                                        color="primary",
                                        className=(
                                            "w-100 mt-4"
                                        ),
                                        n_clicks=0,
                                    ),
                                    md=3,
                                ),
                            ],
                            className="g-3",
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Examiner une suggestion",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Suggestion pending"
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-assisted-"
                                                "suggestion-id"
                                            ),
                                            options=(
                                                pending_options
                                            ),
                                            value=None,
                                            placeholder=(
                                                "Choisir une "
                                                "suggestion"
                                            ),
                                        ),
                                    ],
                                    md=5,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Code de remplacement"
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-assisted-"
                                                "replacement-code"
                                            ),
                                            options=(
                                                code_options
                                            ),
                                            value=None,
                                            clearable=True,
                                            placeholder=(
                                                "Pour Modifier "
                                                "uniquement"
                                            ),
                                        ),
                                    ],
                                    md=4,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Décision"
                                        ),

                                        dbc.ButtonGroup(
                                            [
                                                dbc.Button(
                                                    "Accepter",
                                                    id=(
                                                        "eqae-accept-"
                                                        "suggestion"
                                                    ),
                                                    color="success",
                                                    n_clicks=0,
                                                ),
                                                dbc.Button(
                                                    "Modifier",
                                                    id=(
                                                        "eqae-modify-"
                                                        "suggestion"
                                                    ),
                                                    color="warning",
                                                    n_clicks=0,
                                                ),
                                                dbc.Button(
                                                    "Rejeter",
                                                    id=(
                                                        "eqae-reject-"
                                                        "suggestion"
                                                    ),
                                                    color="danger",
                                                    outline=True,
                                                    n_clicks=0,
                                                ),
                                            ],
                                            className="w-100",
                                        ),
                                    ],
                                    md=3,
                                ),
                            ],
                            className="g-3",
                        ),

                        dbc.Label(
                            "Note du chercheur",
                            className="mt-3",
                        ),

                        dbc.Textarea(
                            id=(
                                "eqae-assisted-"
                                "reviewer-note"
                            ),
                            value="",
                            rows=2,
                            placeholder=(
                                "Justification de la décision"
                            ),
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            html.Div(
                id="eqae-assisted-feedback",
                className="mb-3",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Suggestions enregistrées",
                            className="mb-3",
                        ),
                        html.Div(
                            id=(
                                "eqae-assisted-"
                                "suggestions-table"
                            ),
                            children=(
                                eqae_assisted_table(
                                    assisted_payload,
                                    codebook_payload,
                                )
                            ),
                        ),
                    ]
                ),
                className="shadow-sm",
            ),
        ]
    )


def _eqae_theme_options(
    themes_payload,
):
    """
    Options Dash des thèmes EQAE.
    """

    themes_payload = (
        themes_payload
        if isinstance(themes_payload, dict)
        else {}
    )

    return [
        {
            "label": item.get(
                "name",
                item.get("theme_id", ""),
            ),
            "value": item.get(
                "theme_id"
            ),
        }
        for item in themes_payload.get(
            "themes",
            [],
        )
        if (
            isinstance(item, dict)
            and item.get("theme_id")
        )
    ]


def eqae_themes_table(
    themes_payload,
    codebook_payload,
):
    """
    Tableau hiérarchique des thèmes EQAE.
    """

    themes_payload = (
        themes_payload
        if isinstance(themes_payload, dict)
        else {}
    )

    codebook_payload = (
        codebook_payload
        if isinstance(codebook_payload, dict)
        else {}
    )

    themes = themes_payload.get(
        "themes",
        [],
    )

    if not themes:
        return dbc.Alert(
            "Aucun thème qualitatif enregistré.",
            color="light",
            className="mb-0",
        )

    theme_names = {
        item.get("theme_id"): item.get(
            "name",
            "",
        )
        for item in themes
        if isinstance(item, dict)
    }

    code_names = {
        item.get("code_id"): item.get(
            "name",
            "",
        )
        for item in codebook_payload.get(
            "codes",
            [],
        )
        if isinstance(item, dict)
    }

    rows = []

    for item in themes:

        parent_id = item.get(
            "parent_theme_id"
        )

        code_ids = item.get(
            "code_ids",
            [],
        )

        linked_codes = [
            code_names.get(
                code_id,
                code_id,
            )
            for code_id in code_ids
        ]

        rows.append(
            html.Tr(
                [
                    html.Td(
                        item.get(
                            "name",
                            "",
                        )
                    ),
                    html.Td(
                        theme_names.get(
                            parent_id,
                            "—",
                        )
                        if parent_id
                        else "—"
                    ),
                    html.Td(
                        item.get(
                            "description",
                            "",
                        )
                    ),
                    html.Td(
                        ", ".join(
                            linked_codes
                        )
                        if linked_codes
                        else "—"
                    ),
                ]
            )
        )

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Thème"),
                        html.Th("Thème parent"),
                        html.Th("Description"),
                        html.Th("Codes associés"),
                    ]
                )
            ),
            html.Tbody(rows),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
        className="mb-0",
    )


def eqae_themes_component(
    *,
    themes_payload,
    codebook_payload,
):
    """
    Workspace de gestion des thèmes qualitatifs.
    """

    theme_options = _eqae_theme_options(
        themes_payload
    )

    code_options = _eqae_codebook_options(
        codebook_payload
    )

    return html.Div(
        [
            dbc.Alert(
                [
                    html.Strong(
                        "Construction thématique : "
                    ),
                    (
                        "les thèmes et sous-thèmes sont "
                        "définis et validés par le chercheur. "
                        "Ils ne sont pas assimilés "
                        "automatiquement aux topics ETAE."
                    ),
                ],
                color="light",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Créer un thème ou sous-thème",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Nom du thème"
                                        ),
                                        dbc.Input(
                                            id=(
                                                "eqae-theme-name"
                                            ),
                                            value="",
                                            placeholder=(
                                                "Ex. Engagement "
                                                "académique"
                                            ),
                                        ),
                                    ],
                                    md=5,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Thème parent"
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-theme-parent"
                                            ),
                                            options=(
                                                theme_options
                                            ),
                                            value=None,
                                            clearable=True,
                                            placeholder=(
                                                "Aucun parent"
                                            ),
                                        ),
                                    ],
                                    md=4,
                                ),

                                dbc.Col(
                                    dbc.Button(
                                        "Créer le thème",
                                        id=(
                                            "eqae-add-theme"
                                        ),
                                        color="primary",
                                        className=(
                                            "w-100 mt-4"
                                        ),
                                        n_clicks=0,
                                    ),
                                    md=3,
                                ),
                            ],
                            className="g-3",
                        ),

                        dbc.Label(
                            "Description",
                            className="mt-3",
                        ),

                        dbc.Textarea(
                            id=(
                                "eqae-theme-description"
                            ),
                            value="",
                            rows=3,
                            placeholder=(
                                "Définition analytique "
                                "du thème"
                            ),
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Associer les codes aux thèmes",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Thème"),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-theme-link-id"
                                            ),
                                            options=(
                                                theme_options
                                            ),
                                            value=None,
                                            placeholder=(
                                                "Sélectionner "
                                                "un thème"
                                            ),
                                        ),
                                    ],
                                    md=4,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label("Code"),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-theme-code-id"
                                            ),
                                            options=(
                                                code_options
                                            ),
                                            value=None,
                                            placeholder=(
                                                "Sélectionner "
                                                "un code"
                                            ),
                                        ),
                                    ],
                                    md=4,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label("Action"),

                                        dbc.ButtonGroup(
                                            [
                                                dbc.Button(
                                                    "Associer",
                                                    id=(
                                                        "eqae-link-"
                                                        "theme-code"
                                                    ),
                                                    color="success",
                                                    n_clicks=0,
                                                ),
                                                dbc.Button(
                                                    "Retirer",
                                                    id=(
                                                        "eqae-unlink-"
                                                        "theme-code"
                                                    ),
                                                    color="warning",
                                                    outline=True,
                                                    n_clicks=0,
                                                ),
                                            ],
                                            className="w-100",
                                        ),
                                    ],
                                    md=4,
                                ),
                            ],
                            className="g-3",
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            html.Div(
                id="eqae-theme-feedback",
                className="mb-3",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Structure thématique",
                            className="mb-3",
                        ),

                        html.Div(
                            id="eqae-themes-table",
                            children=(
                                eqae_themes_table(
                                    themes_payload,
                                    codebook_payload,
                                )
                            ),
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Supprimer un thème",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id=(
                                            "eqae-delete-theme-id"
                                        ),
                                        options=(
                                            theme_options
                                        ),
                                        value=None,
                                        placeholder=(
                                            "Sélectionner "
                                            "un thème"
                                        ),
                                    ),
                                    md=9,
                                ),

                                dbc.Col(
                                    dbc.Button(
                                        "Supprimer",
                                        id=(
                                            "eqae-delete-theme"
                                        ),
                                        color="danger",
                                        outline=True,
                                        className="w-100",
                                        n_clicks=0,
                                    ),
                                    md=3,
                                ),
                            ],
                            className="g-3",
                        ),

                        dbc.Alert(
                            (
                                "Un thème possédant des "
                                "sous-thèmes ne peut pas "
                                "être supprimé."
                            ),
                            color="warning",
                            className="mt-3 mb-0 py-2",
                        ),
                    ]
                ),
                className="shadow-sm",
            ),
        ]
    )


def eqae_quotations_table(
    quotations_payload,
):
    """
    Tableau des verbatims EQAE.
    """

    quotations_payload = (
        quotations_payload
        if isinstance(
            quotations_payload,
            dict,
        )
        else {}
    )

    quotations = quotations_payload.get(
        "quotations",
        [],
    )

    if not quotations:
        return dbc.Alert(
            "Aucun verbatim enregistré.",
            color="light",
            className="mb-0",
        )

    rows = []

    for item in quotations:
        rows.append(
            html.Tr(
                [
                    html.Td(
                        item.get(
                            "document_id",
                            "",
                        )
                    ),
                    html.Td(
                        item.get(
                            "segment_id",
                            "",
                        )
                    ),
                    html.Td(
                        item.get(
                            "text",
                            "",
                        )
                    ),
                    html.Td(
                        item.get(
                            "note",
                            "",
                        )
                    ),
                ]
            )
        )

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Document"),
                        html.Th("Segment"),
                        html.Th("Verbatim"),
                        html.Th("Note"),
                    ]
                )
            ),
            html.Tbody(rows),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
        className="mb-0",
    )


def eqae_quotations_component(
    *,
    segments,
    quotations_payload,
    codebook_payload,
    themes_payload,
):
    """
    Workspace de gestion des verbatims EQAE.
    """

    segment_options = [
        {
            "label": (
                f"{segment.document_id} — "
                f"{segment.text[:120]}"
                + (
                    "…"
                    if len(segment.text) > 120
                    else ""
                )
            ),
            "value": segment.segment_id,
        }
        for segment in segments
    ]

    quotations = (
        quotations_payload.get(
            "quotations",
            [],
        )
        if isinstance(
            quotations_payload,
            dict,
        )
        else []
    )

    quotation_options = [
        {
            "label": (
                f"{item.get('document_id', '')} — "
                f"{item.get('quotation_id', '')[:8]}"
            ),
            "value": item.get(
                "quotation_id"
            ),
        }
        for item in quotations
        if isinstance(item, dict)
        and item.get("quotation_id")
    ]

    code_options = _eqae_codebook_options(
        codebook_payload
    )

    theme_options = _eqae_theme_options(
        themes_payload
    )

    document_options = sorted(
        {
            item.get("document_id")
            for item in quotations
            if (
                isinstance(item, dict)
                and item.get("document_id")
            )
        }
    )

    document_options = [
        {
            "label": value,
            "value": value,
        }
        for value in document_options
    ]

    return html.Div(
        [
            dbc.Alert(
                [
                    html.Strong(
                        "Verbatims analytiques : "
                    ),
                    (
                        "un verbatim est un extrait retenu "
                        "par le chercheur comme élément "
                        "d'illustration ou de preuve qualitative."
                    ),
                ],
                color="light",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Ajouter un verbatim",
                            className="mb-3",
                        ),

                        dbc.Label("Segment"),

                        dcc.Dropdown(
                            id=(
                                "eqae-quotation-segment"
                            ),
                            options=(
                                segment_options
                            ),
                            value=None,
                            placeholder=(
                                "Sélectionner un segment"
                            ),
                        ),

                        dbc.Label(
                            "Note analytique",
                            className="mt-3",
                        ),

                        dbc.Textarea(
                            id=(
                                "eqae-quotation-note"
                            ),
                            value="",
                            rows=3,
                            placeholder=(
                                "Pourquoi ce verbatim "
                                "est-il important ?"
                            ),
                        ),

                        dbc.Button(
                            "Ajouter le verbatim",
                            id=(
                                "eqae-add-quotation"
                            ),
                            color="primary",
                            className="mt-3",
                            n_clicks=0,
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Explorer les verbatims",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Filtrer par code"
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-quotation-"
                                                "filter-code"
                                            ),
                                            options=(
                                                code_options
                                            ),
                                            value=None,
                                            clearable=True,
                                            placeholder="Tous",
                                        ),
                                    ],
                                    md=4,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Filtrer par thème"
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-quotation-"
                                                "filter-theme"
                                            ),
                                            options=(
                                                theme_options
                                            ),
                                            value=None,
                                            clearable=True,
                                            placeholder="Tous",
                                        ),
                                    ],
                                    md=4,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Filtrer par document"
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-quotation-"
                                                "filter-document"
                                            ),
                                            options=(
                                                document_options
                                            ),
                                            value=None,
                                            clearable=True,
                                            placeholder="Tous",
                                        ),
                                    ],
                                    md=4,
                                ),
                            ],
                            className="g-3",
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            html.Div(
                id="eqae-quotation-feedback",
                className="mb-3",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Verbatims enregistrés",
                            className="mb-3",
                        ),

                        html.Div(
                            id=(
                                "eqae-quotations-table"
                            ),
                            children=(
                                eqae_quotations_table(
                                    quotations_payload
                                )
                            ),
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Supprimer un verbatim",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id=(
                                            "eqae-delete-"
                                            "quotation-id"
                                        ),
                                        options=(
                                            quotation_options
                                        ),
                                        value=None,
                                        placeholder=(
                                            "Sélectionner "
                                            "un verbatim"
                                        ),
                                    ),
                                    md=9,
                                ),

                                dbc.Col(
                                    dbc.Button(
                                        "Supprimer",
                                        id=(
                                            "eqae-delete-"
                                            "quotation"
                                        ),
                                        color="danger",
                                        outline=True,
                                        className="w-100",
                                        n_clicks=0,
                                    ),
                                    md=3,
                                ),
                            ],
                            className="g-3",
                        ),
                    ]
                ),
                className="shadow-sm",
            ),
        ]
    )


def eqae_cooccurrence_pairs_table(
    payload,
    codebook_payload,
):
    """
    Tableau des paires de codes en cooccurrence.
    """

    payload = (
        payload
        if isinstance(payload, dict)
        else {}
    )

    codebook_payload = (
        codebook_payload
        if isinstance(codebook_payload, dict)
        else {}
    )

    names = {
        item.get("code_id"): item.get(
            "name",
            item.get("code_id", ""),
        )
        for item in codebook_payload.get(
            "codes",
            [],
        )
        if isinstance(item, dict)
    }

    items = payload.get(
        "cooccurrences",
        [],
    )

    if not items:
        return dbc.Alert(
            (
                "Aucune cooccurrence observée "
                "au niveau sélectionné."
            ),
            color="light",
            className="mb-0",
        )

    rows = []

    for item in sorted(
        items,
        key=lambda value: value.get(
            "count",
            0,
        ),
        reverse=True,
    ):
        rows.append(
            html.Tr(
                [
                    html.Td(
                        names.get(
                            item.get("code_id_1"),
                            item.get(
                                "code_id_1",
                                "",
                            ),
                        )
                    ),
                    html.Td(
                        names.get(
                            item.get("code_id_2"),
                            item.get(
                                "code_id_2",
                                "",
                            ),
                        )
                    ),
                    html.Td(
                        item.get(
                            "count",
                            0,
                        )
                    ),
                ]
            )
        )

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Code 1"),
                        html.Th("Code 2"),
                        html.Th("Occurrences"),
                    ]
                )
            ),
            html.Tbody(rows),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
        className="mb-0",
    )


def eqae_cooccurrence_matrix_table(
    payload,
    codebook_payload,
):
    """
    Matrice symétrique des cooccurrences.
    """

    payload = (
        payload
        if isinstance(payload, dict)
        else {}
    )

    codebook_payload = (
        codebook_payload
        if isinstance(codebook_payload, dict)
        else {}
    )

    matrix = payload.get(
        "matrix",
        {},
    )

    if not matrix:
        return dbc.Alert(
            "Matrice de cooccurrence indisponible.",
            color="light",
            className="mb-0",
        )

    names = {
        item.get("code_id"): item.get(
            "name",
            item.get("code_id", ""),
        )
        for item in codebook_payload.get(
            "codes",
            [],
        )
        if isinstance(item, dict)
    }

    code_ids = list(
        matrix.keys()
    )

    header = html.Tr(
        [
            html.Th("Code"),
            *[
                html.Th(
                    names.get(
                        code_id,
                        code_id,
                    )
                )
                for code_id in code_ids
            ],
        ]
    )

    rows = []

    for code_id in code_ids:
        row_values = matrix.get(
            code_id,
            {},
        )

        rows.append(
            html.Tr(
                [
                    html.Th(
                        names.get(
                            code_id,
                            code_id,
                        )
                    ),
                    *[
                        html.Td(
                            row_values.get(
                                other_id,
                                0,
                            )
                        )
                        for other_id
                        in code_ids
                    ],
                ]
            )
        )

    return dbc.Table(
        [
            html.Thead(header),
            html.Tbody(rows),
        ],
        bordered=True,
        striped=True,
        responsive=True,
        size="sm",
        className="mb-0",
    )


def eqae_cooccurrence_component(
    *,
    payload,
    codebook_payload,
):
    """
    Workspace d'analyse des cooccurrences EQAE.
    """

    payload = (
        payload
        if isinstance(payload, dict)
        else {}
    )

    level = payload.get(
        "level",
        "segment",
    )

    return html.Div(
        [
            dbc.Alert(
                [
                    html.Strong(
                        "Cooccurrences de codes : "
                    ),
                    (
                        "elles indiquent quels codes "
                        "apparaissent ensemble dans un même "
                        "segment ou un même document. "
                        "Une cooccurrence ne démontre pas "
                        "à elle seule une relation causale "
                        "ou conceptuelle."
                    ),
                ],
                color="light",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Niveau d'analyse"
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-cooccurrence-"
                                                "level"
                                            ),
                                            options=[
                                                {
                                                    "label": (
                                                        "Segment"
                                                    ),
                                                    "value": (
                                                        "segment"
                                                    ),
                                                },
                                                {
                                                    "label": (
                                                        "Document"
                                                    ),
                                                    "value": (
                                                        "document"
                                                    ),
                                                },
                                            ],
                                            value=level,
                                            clearable=False,
                                        ),
                                    ],
                                    md=8,
                                ),

                                dbc.Col(
                                    dbc.Button(
                                        "Calculer",
                                        id=(
                                            "eqae-run-"
                                            "cooccurrence"
                                        ),
                                        color="primary",
                                        className="w-100 mt-4",
                                        n_clicks=0,
                                    ),
                                    md=4,
                                ),
                            ],
                            className="g-3",
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            html.Div(
                id="eqae-cooccurrence-feedback",
                className="mb-3",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Paires de codes",
                            className="mb-3",
                        ),

                        html.Div(
                            id=(
                                "eqae-cooccurrence-"
                                "pairs-table"
                            ),
                            children=(
                                eqae_cooccurrence_pairs_table(
                                    payload,
                                    codebook_payload,
                                )
                            ),
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Matrice de cooccurrence",
                            className="mb-3",
                        ),

                        html.Div(
                            id=(
                                "eqae-cooccurrence-"
                                "matrix-table"
                            ),
                            children=(
                                eqae_cooccurrence_matrix_table(
                                    payload,
                                    codebook_payload,
                                )
                            ),
                        ),
                    ]
                ),
                className="shadow-sm",
            ),
        ]
    )


def eqae_memos_table(
    memos_payload,
):
    """
    Tableau des mémos analytiques EQAE.
    """

    memos_payload = (
        memos_payload
        if isinstance(memos_payload, dict)
        else {}
    )

    memos = memos_payload.get(
        "memos",
        [],
    )

    if not memos:
        return dbc.Alert(
            "Aucun mémo analytique enregistré.",
            color="light",
            className="mb-0",
        )

    rows = []

    for item in memos:
        rows.append(
            html.Tr(
                [
                    html.Td(
                        item.get(
                            "title",
                            "",
                        )
                    ),
                    html.Td(
                        item.get(
                            "target_type",
                            "",
                        )
                    ),
                    html.Td(
                        item.get(
                            "target_id",
                            "—",
                        )
                        or "—"
                    ),
                    html.Td(
                        item.get(
                            "content",
                            "",
                        )
                    ),
                    html.Td(
                        item.get(
                            "author",
                            "—",
                        )
                        or "—"
                    ),
                    html.Td(
                        item.get(
                            "created_at",
                            "",
                        )
                    ),
                ]
            )
        )

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Titre"),
                        html.Th("Type de cible"),
                        html.Th("Cible"),
                        html.Th("Contenu"),
                        html.Th("Auteur"),
                        html.Th("Créé le"),
                    ]
                )
            ),
            html.Tbody(rows),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
        className="mb-0",
    )


def eqae_memos_component(
    *,
    memos_payload,
    codebook_payload,
    themes_payload,
    quotations_payload,
    segments,
):
    """
    Workspace de gestion des mémos analytiques.
    """

    memos_payload = (
        memos_payload
        if isinstance(memos_payload, dict)
        else {}
    )

    code_options = _eqae_codebook_options(
        codebook_payload
    )

    theme_options = _eqae_theme_options(
        themes_payload
    )

    quotation_options = [
        {
            "label": (
                f"{item.get('document_id', '')} — "
                f"{item.get('text', '')[:80]}"
            ),
            "value": item.get(
                "quotation_id"
            ),
        }
        for item in quotations_payload.get(
            "quotations",
            [],
        )
        if isinstance(item, dict)
        and item.get("quotation_id")
    ]

    segment_options = [
        {
            "label": (
                f"{segment.document_id} — "
                f"{segment.text[:80]}"
            ),
            "value": segment.segment_id,
        }
        for segment in segments
    ]

    document_values = sorted(
        {
            segment.document_id
            for segment in segments
        }
    )

    document_options = [
        {
            "label": value,
            "value": value,
        }
        for value in document_values
    ]

    memos = memos_payload.get(
        "memos",
        [],
    )

    delete_options = [
        {
            "label": (
                f"{item.get('title', '')} — "
                f"{item.get('memo_id', '')[:8]}"
            ),
            "value": item.get(
                "memo_id"
            ),
        }
        for item in memos
        if isinstance(item, dict)
        and item.get("memo_id")
    ]

    return html.Div(
        [
            dbc.Alert(
                [
                    html.Strong(
                        "Mémo analytique : "
                    ),
                    (
                        "un mémo consigne une réflexion, "
                        "une interprétation, une décision "
                        "méthodologique ou une piste "
                        "d'analyse du chercheur."
                    ),
                ],
                color="light",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Créer un mémo",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Titre"),
                                        dbc.Input(
                                            id="eqae-memo-title",
                                            value="",
                                            placeholder=(
                                                "Titre du mémo"
                                            ),
                                        ),
                                    ],
                                    md=6,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Auteur"
                                        ),
                                        dbc.Input(
                                            id="eqae-memo-author",
                                            value="",
                                            placeholder=(
                                                "Nom du chercheur"
                                            ),
                                        ),
                                    ],
                                    md=6,
                                ),
                            ],
                            className="g-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Type de cible",
                                            className="mt-3",
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-memo-"
                                                "target-type"
                                            ),
                                            options=[
                                                {
                                                    "label": (
                                                        "Analyse globale"
                                                    ),
                                                    "value": "analysis",
                                                },
                                                {
                                                    "label": "Document",
                                                    "value": "document",
                                                },
                                                {
                                                    "label": "Segment",
                                                    "value": "segment",
                                                },
                                                {
                                                    "label": "Code",
                                                    "value": "code",
                                                },
                                                {
                                                    "label": "Thème",
                                                    "value": "theme",
                                                },
                                                {
                                                    "label": "Verbatim",
                                                    "value": "quotation",
                                                },
                                            ],
                                            value="analysis",
                                            clearable=False,
                                        ),
                                    ],
                                    md=6,
                                ),

                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Cible",
                                            className="mt-3",
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "eqae-memo-"
                                                "target-id"
                                            ),
                                            options=[],
                                            value=None,
                                            clearable=True,
                                            placeholder=(
                                                "Aucune cible "
                                                "pour un mémo global"
                                            ),
                                            disabled=True,
                                        ),
                                    ],
                                    md=6,
                                ),
                            ],
                            className="g-3",
                        ),

                        dcc.Store(
                            id="eqae-memo-code-options",
                            data=code_options,
                        ),

                        dcc.Store(
                            id="eqae-memo-theme-options",
                            data=theme_options,
                        ),

                        dcc.Store(
                            id="eqae-memo-quotation-options",
                            data=quotation_options,
                        ),

                        dcc.Store(
                            id="eqae-memo-segment-options",
                            data=segment_options,
                        ),

                        dcc.Store(
                            id="eqae-memo-document-options",
                            data=document_options,
                        ),

                        dbc.Label(
                            "Contenu",
                            className="mt-3",
                        ),

                        dbc.Textarea(
                            id="eqae-memo-content",
                            value="",
                            rows=5,
                            placeholder=(
                                "Réflexion analytique "
                                "du chercheur"
                            ),
                        ),

                        dbc.Button(
                            "Enregistrer le mémo",
                            id="eqae-add-memo",
                            color="primary",
                            className="mt-3",
                            n_clicks=0,
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            html.Div(
                id="eqae-memo-feedback",
                className="mb-3",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Mémos enregistrés",
                            className="mb-3",
                        ),

                        html.Div(
                            id="eqae-memos-table",
                            children=(
                                eqae_memos_table(
                                    memos_payload
                                )
                            ),
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Supprimer un mémo",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id=(
                                            "eqae-delete-"
                                            "memo-id"
                                        ),
                                        options=(
                                            delete_options
                                        ),
                                        value=None,
                                        placeholder=(
                                            "Sélectionner "
                                            "un mémo"
                                        ),
                                    ),
                                    md=9,
                                ),

                                dbc.Col(
                                    dbc.Button(
                                        "Supprimer",
                                        id="eqae-delete-memo",
                                        color="danger",
                                        outline=True,
                                        className="w-100",
                                        n_clicks=0,
                                    ),
                                    md=3,
                                ),
                            ],
                            className="g-3",
                        ),
                    ]
                ),
                className="shadow-sm",
            ),
        ]
    )


def eqae_summary_code_table(
    summary_payload,
):
    """
    Synthèse descriptive par code.
    """

    summary_payload = (
        summary_payload
        if isinstance(summary_payload, dict)
        else {}
    )

    items = summary_payload.get(
        "codes",
        [],
    )

    if not items:
        return dbc.Alert(
            "Aucune synthèse par code disponible.",
            color="light",
            className="mb-0",
        )

    rows = [
        html.Tr(
            [
                html.Td(
                    item.get("name", "")
                ),
                html.Td(
                    item.get(
                        "n_assignments",
                        0,
                    )
                ),
                html.Td(
                    item.get(
                        "n_documents",
                        0,
                    )
                ),
                html.Td(
                    item.get(
                        "n_segments",
                        0,
                    )
                ),
                html.Td(
                    item.get(
                        "n_quotations",
                        0,
                    )
                ),
            ]
        )
        for item in items
    ]

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Code"),
                        html.Th("Affectations"),
                        html.Th("Documents"),
                        html.Th("Segments"),
                        html.Th("Verbatims"),
                    ]
                )
            ),
            html.Tbody(rows),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
        className="mb-0",
    )


def eqae_summary_theme_table(
    summary_payload,
):
    """
    Synthèse descriptive par thème.
    """

    summary_payload = (
        summary_payload
        if isinstance(summary_payload, dict)
        else {}
    )

    items = summary_payload.get(
        "themes",
        [],
    )

    if not items:
        return dbc.Alert(
            "Aucune synthèse par thème disponible.",
            color="light",
            className="mb-0",
        )

    rows = [
        html.Tr(
            [
                html.Td(
                    item.get("name", "")
                ),
                html.Td(
                    item.get(
                        "n_codes",
                        0,
                    )
                ),
                html.Td(
                    item.get(
                        "n_assignments",
                        0,
                    )
                ),
                html.Td(
                    item.get(
                        "n_documents",
                        0,
                    )
                ),
                html.Td(
                    item.get(
                        "n_quotations",
                        0,
                    )
                ),
            ]
        )
        for item in items
    ]

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Thème"),
                        html.Th("Codes"),
                        html.Th("Affectations"),
                        html.Th("Documents"),
                        html.Th("Verbatims"),
                    ]
                )
            ),
            html.Tbody(rows),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
        className="mb-0",
    )


def eqae_summary_component(
    *,
    summary_payload,
    n_memos=0,
):
    """
    Vue de synthèse descriptive EQAE.
    """

    summary_payload = (
        summary_payload
        if isinstance(summary_payload, dict)
        else {}
    )

    global_data = summary_payload.get(
        "global",
        {},
    )

    assisted = summary_payload.get(
        "assisted_coding",
        {},
    )

    def metric_card(
        label,
        value,
        component_id=None,
    ):
        return dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            label,
                            className=(
                                "text-muted small"
                            ),
                        ),
                        html.H3(
                            str(value),
                            className="mb-0",
                            **(
                                {
                                    "id": component_id
                                }
                                if component_id
                                else {}
                            ),
                        ),
                    ]
                ),
                className="h-100 shadow-sm",
            ),
            md=3,
            sm=6,
            className="mb-3",
        )

    return html.Div(
        [
            dbc.Alert(
                [
                    html.Strong(
                        "Synthèse descriptive EQAE : "
                    ),
                    (
                        "cette vue organise les résultats "
                        "du codage qualitatif. Elle ne "
                        "constitue pas, à elle seule, une "
                        "interprétation scientifique."
                    ),
                ],
                color="light",
            ),

            dbc.Button(
                "Actualiser la synthèse",
                id="eqae-run-summary",
                color="primary",
                className="mb-3",
                n_clicks=0,
            ),

            html.Div(
                id="eqae-summary-feedback",
                className="mb-3",
            ),

            html.H5(
                "Indicateurs globaux",
                className="mb-3",
            ),

            dbc.Row(
                [
                    metric_card(
                        "Codes",
                        global_data.get(
                            "n_codes",
                            0,
                        ),
                        "eqae-summary-n-codes",
                    ),
                    metric_card(
                        "Thèmes",
                        global_data.get(
                            "n_themes",
                            0,
                        ),
                        "eqae-summary-n-themes",
                    ),
                    metric_card(
                        "Affectations",
                        global_data.get(
                            "n_assignments",
                            0,
                        ),
                        "eqae-summary-n-assignments",
                    ),
                    metric_card(
                        "Documents codés",
                        global_data.get(
                            "n_documents_coded",
                            0,
                        ),
                        "eqae-summary-n-documents",
                    ),
                    metric_card(
                        "Segments codés",
                        global_data.get(
                            "n_segments_coded",
                            0,
                        ),
                        "eqae-summary-n-segments",
                    ),
                    metric_card(
                        "Verbatims",
                        global_data.get(
                            "n_quotations",
                            0,
                        ),
                        "eqae-summary-n-quotations",
                    ),
                    metric_card(
                        "Suggestions assistées",
                        global_data.get(
                            "n_assisted_suggestions",
                            0,
                        ),
                        "eqae-summary-n-suggestions",
                    ),
                    metric_card(
                        "Mémos analytiques",
                        n_memos,
                    ),
                ],
                className="mb-2",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Synthèse par code",
                            className="mb-3",
                        ),
                        html.Div(
                            id="eqae-summary-code-table",
                            children=(
                                eqae_summary_code_table(
                                    summary_payload
                                )
                            ),
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Synthèse par thème",
                            className="mb-3",
                        ),
                        html.Div(
                            id="eqae-summary-theme-table",
                            children=(
                                eqae_summary_theme_table(
                                    summary_payload
                                )
                            ),
                        ),
                    ]
                ),
                className="mb-3 shadow-sm",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Codage assisté",
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                metric_card(
                                    "Pending",
                                    assisted.get(
                                        "pending",
                                        0,
                                    ),
                                    "eqae-summary-pending",
                                ),
                                metric_card(
                                    "Accepted",
                                    assisted.get(
                                        "accepted",
                                        0,
                                    ),
                                    "eqae-summary-accepted",
                                ),
                                metric_card(
                                    "Modified",
                                    assisted.get(
                                        "modified",
                                        0,
                                    ),
                                    "eqae-summary-modified",
                                ),
                                metric_card(
                                    "Rejected",
                                    assisted.get(
                                        "rejected",
                                        0,
                                    ),
                                    "eqae-summary-rejected",
                                ),
                            ]
                        ),
                    ]
                ),
                className="shadow-sm",
            ),
        ]
    )
