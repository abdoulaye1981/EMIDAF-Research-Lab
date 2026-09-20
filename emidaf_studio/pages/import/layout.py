from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def import_layout(project_id):

    return dbc.Container(
        [
            # ==================================================
            # HERO
            # ==================================================

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span(
                                        "IMPORTATION",
                                        className="import-v2-kicker",
                                    ),
                                    html.Span(
                                        "ACQUISITION DES DONNÉES",
                                        className="import-v2-eyebrow",
                                    ),
                                ],
                                className=(
                                    "d-flex align-items-center "
                                    "gap-2 mb-3"
                                ),
                            ),

                            html.H1(
                                "Importer un jeu de données",
                                className="import-v2-title",
                            ),

                            html.P(
                                (
                                    "Ajoutez un fichier de données au "
                                    "projet actif, vérifiez son contenu "
                                    "puis enregistrez-le dans l'espace "
                                    "de travail EMIDAF."
                                ),
                                className="import-v2-subtitle",
                            ),
                        ]
                    ),

                    html.Div(
                        [
                            html.Div(
                                html.I(
                                    className=(
                                        "bi bi-cloud-arrow-up "
                                        "import-v2-hero-icon"
                                    )
                                ),
                                className="import-v2-hero-icon-box",
                            )
                        ],
                        className="import-v2-hero-visual",
                    ),
                ],
                className="import-v2-hero",
            ),

            # ==================================================
            # PROJET ACTIF
            # ==================================================

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                html.I(
                                    className=(
                                        "bi bi-folder2-open "
                                        "import-v2-project-icon"
                                    )
                                ),
                                className="import-v2-project-icon-box",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "PROJET ACTIF",
                                        className="import-v2-project-label",
                                    ),

                                    html.Div(
                                        f"Projet #{project_id}",
                                        className="import-v2-project-value",
                                    ),
                                ]
                            ),

                            html.Div(
                                [
                                    html.I(
                                        className=(
                                            "bi bi-check-circle-fill me-2"
                                        )
                                    ),
                                    "Contexte actif",
                                ],
                                className="import-v2-project-status",
                            ),
                        ],
                        className="import-v2-project-card",
                    )
                ],
                className="import-v2-project-section",
            ),

            # ==================================================
            # PROCESSUS
            # ==================================================

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                "PROCESSUS D'IMPORTATION",
                                className="import-v2-section-kicker",
                            ),

                            html.H2(
                                "Ajouter un nouveau jeu de données",
                                className="import-v2-section-title",
                            ),

                            html.P(
                                (
                                    "Chargez votre fichier, contrôlez "
                                    "l'aperçu puis renseignez son nom "
                                    "avant l'enregistrement."
                                ),
                                className="import-v2-section-subtitle",
                            ),
                        ],
                        className="import-v2-section-heading",
                    ),

                    # ------------------------------------------
                    # Étapes
                    # ------------------------------------------

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "01",
                                        className="import-v2-step-number",
                                    ),
                                    html.I(
                                        className=(
                                            "bi bi-file-earmark-arrow-up "
                                            "import-v2-step-icon"
                                        )
                                    ),
                                    html.Div(
                                        "Sélectionner",
                                        className="import-v2-step-title",
                                    ),
                                    html.Div(
                                        "CSV ou Excel",
                                        className="import-v2-step-text",
                                    ),
                                ],
                                className="import-v2-step",
                            ),

                            html.Div(
                                className="import-v2-step-line"
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "02",
                                        className="import-v2-step-number",
                                    ),
                                    html.I(
                                        className=(
                                            "bi bi-table "
                                            "import-v2-step-icon"
                                        )
                                    ),
                                    html.Div(
                                        "Vérifier",
                                        className="import-v2-step-title",
                                    ),
                                    html.Div(
                                        "Aperçu des données",
                                        className="import-v2-step-text",
                                    ),
                                ],
                                className="import-v2-step",
                            ),

                            html.Div(
                                className="import-v2-step-line"
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "03",
                                        className="import-v2-step-number",
                                    ),
                                    html.I(
                                        className=(
                                            "bi bi-database-check "
                                            "import-v2-step-icon"
                                        )
                                    ),
                                    html.Div(
                                        "Enregistrer",
                                        className="import-v2-step-title",
                                    ),
                                    html.Div(
                                        "Persistance EMIDAF",
                                        className="import-v2-step-text",
                                    ),
                                ],
                                className="import-v2-step",
                            ),
                        ],
                        className="import-v2-steps",
                    ),

                    # ------------------------------------------
                    # Upload
                    # ------------------------------------------

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-cloud-arrow-up"
                                            )
                                        ),
                                        className="import-v2-drop-icon",
                                    ),

                                    html.H3(
                                        "Déposer un fichier",
                                        className="import-v2-drop-title",
                                    ),

                                    html.P(
                                        (
                                            "Sélectionnez un fichier "
                                            "CSV ou Excel depuis votre "
                                            "ordinateur."
                                        ),
                                        className="import-v2-drop-text",
                                    ),

                                    dcc.Upload(
                                        id="dataset-upload",
                                        children=html.Div(
                                            [
                                                html.I(
                                                    className=(
                                                        "bi bi-folder2-open me-2"
                                                    )
                                                ),
                                                html.Span(
                                                    "Choisir un fichier"
                                                ),
                                            ],
                                            className=(
                                                "import-v2-upload-button"
                                            ),
                                        ),
                                        multiple=False,
                                        className="import-v2-upload",
                                    ),

                                    html.Div(
                                        [
                                            html.Span(
                                                "CSV",
                                                className=(
                                                    "import-v2-format"
                                                ),
                                            ),
                                            html.Span(
                                                "XLSX",
                                                className=(
                                                    "import-v2-format"
                                                ),
                                            ),
                                            html.Span(
                                                "XLS",
                                                className=(
                                                    "import-v2-format"
                                                ),
                                            ),
                                        ],
                                        className="import-v2-formats",
                                    ),
                                ],
                                className="import-v2-dropzone",
                            ),

                            html.Div(
                                id="upload-status",
                                className="import-v2-status",
                            ),
                        ],
                        className="import-v2-upload-section",
                    ),
                ],
                className="import-v2-main-section",
            ),

            # ==================================================
            # APERÇU
            # ==================================================

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "APERÇU",
                                        className=(
                                            "import-v2-section-kicker"
                                        ),
                                    ),

                                    html.H2(
                                        "Prévisualisation des données",
                                        className=(
                                            "import-v2-section-title"
                                        ),
                                    ),
                                ]
                            ),

                            html.Div(
                                [
                                    html.I(
                                        className=(
                                            "bi bi-eye me-2"
                                        )
                                    ),
                                    "10 premières lignes",
                                ],
                                className="import-v2-preview-badge",
                            ),
                        ],
                        className="import-v2-preview-header",
                    ),

                    html.Div(
                        id="dataset-preview",
                        className="import-v2-preview",
                    ),
                ],
                className="import-v2-preview-section",
            ),

            # ==================================================
            # ENREGISTREMENT
            # ==================================================

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                "ENREGISTREMENT",
                                className="import-v2-section-kicker",
                            ),

                            html.H2(
                                "Informations du jeu de données",
                                className="import-v2-section-title",
                            ),

                            html.P(
                                (
                                    "Attribuez un nom clair au jeu de "
                                    "données avant de l'enregistrer "
                                    "dans le projet actif."
                                ),
                                className="import-v2-section-subtitle",
                            ),
                        ],
                        className="import-v2-section-heading",
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    dbc.Label(
                                        "Nom du jeu de données",
                                        html_for="dataset-name",
                                        className="import-v2-label",
                                    ),

                                    dbc.Input(
                                        id="dataset-name",
                                        type="text",
                                        placeholder=(
                                            "Exemple : "
                                            "Données étudiants 2026"
                                        ),
                                        className="import-v2-input",
                                    ),

                                    html.Div(
                                        (
                                            "Utilisez un nom descriptif "
                                            "et facilement identifiable."
                                        ),
                                        className="import-v2-help",
                                    ),
                                ],
                                className="import-v2-form-group",
                            ),

                            dbc.Button(
                                [
                                    html.I(
                                        className=(
                                            "bi bi-database-check me-2"
                                        )
                                    ),
                                    "Enregistrer le jeu de données",
                                ],
                                id="btn-save-dataset",
                                disabled=True,
                                className="import-v2-save-button",
                            ),
                        ],
                        className="import-v2-save-card",
                    ),

                    html.Div(
                        id="dataset-save-status",
                        className="import-v2-save-status",
                    ),
                ],
                className="import-v2-save-section",
            ),

            # ==================================================
            # STORES
            # ==================================================

            dcc.Store(
                id="uploaded-dataset-data"
            ),

            dcc.Store(
                id="uploaded-dataset-filename"
            ),

            dcc.Store(
                id="uploaded-dataset-contents"
            ),

            dcc.Store(
                id="current-project-id",
                data=project_id,
            ),
        ],
        fluid=True,
        className="import-v2-page",
    )
