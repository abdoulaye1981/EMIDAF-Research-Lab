"""
=========================================================
EMIDAF Studio
ETAE - Callbacks
=========================================================
"""

from __future__ import annotations

import logging

import pandas as pd

from dash import (
    Input,
    Output,
    callback,
)

import dash_bootstrap_components as dbc

from emidaf_studio.pages.inspection.layout import (
    load_dataset,
)


logger = logging.getLogger(__name__)


def _load_etae_dataframe(
    project_id,
    dataset_id,
) -> pd.DataFrame:
    """
    Recharge le dataset à partir de ses identifiants.

    Le DataFrame complet ne transite pas par dcc.Store.
    """

    _, _, result = load_dataset(
        project_id,
        dataset_id,
    )

    if isinstance(
        result,
        str,
    ):
        raise ValueError(
            result
        )

    if not isinstance(
        result,
        pd.DataFrame,
    ):
        raise ValueError(
            "Le dataset ETAE est indisponible."
        )

    return result


@callback(
    Output(
        "etae-text-column",
        "options",
    ),
    Output(
        "etae-text-column",
        "value",
    ),
    Output(
        "etae-text-column-status",
        "children",
    ),
    Input(
        "etae-project-id",
        "data",
    ),
    Input(
        "etae-dataset-id",
        "data",
    ),
)
def initialize_etae_text_columns(
    project_id,
    dataset_id,
):
    """
    Détecte automatiquement les variables
    contenant vraisemblablement du texte libre.
    """

    if (
        project_id is None
        or dataset_id is None
    ):
        return (
            [],
            None,
            dbc.Alert(
                "Projet ou dataset indisponible.",
                color="warning",
                className="py-2 mb-0",
            ),
        )

    try:
        dataframe = (
            _load_etae_dataframe(
                project_id,
                dataset_id,
            )
        )

        # Import différé pour préserver
        # le démarrage léger de Studio.
        from emidaf_core.etae import (
            ETAEEngine,
        )

        engine = ETAEEngine()

        candidates = (
            engine.inspect_text_columns(
                dataframe
            )
        )

        detected = [
            candidate
            for candidate in candidates
            if candidate.is_text
        ]

    except Exception:
        logger.exception(
            "ETAE text-column detection failed "
            "(project_id=%s, dataset_id=%s)",
            project_id,
            dataset_id,
        )

        return (
            [],
            None,
            dbc.Alert(
                (
                    "Impossible d'analyser les "
                    "colonnes textuelles du dataset."
                ),
                color="danger",
                className="py-2 mb-0",
            ),
        )

    if not detected:
        return (
            [],
            None,
            dbc.Alert(
                (
                    "Aucune variable de texte libre "
                    "n'a été détectée automatiquement."
                ),
                color="warning",
                className="py-2 mb-0",
            ),
        )

    options = [
        {
            "label": (
                f"{candidate.column} "
                f"— {candidate.mean_words:.1f} "
                "mots/doc."
            ),
            "value": candidate.column,
        }
        for candidate in detected
    ]

    selected = (
        detected[0].column
    )

    count = len(
        detected
    )

    message = (
        f"{count} variable"
        f"{'s' if count > 1 else ''} "
        "de texte libre détectée"
        f"{'s' if count > 1 else ''}."
    )

    return (
        options,
        selected,
        dbc.Alert(
            message,
            color="success",
            className="py-2 mb-0",
        ),
    )


@callback(
    Output(
        "etae-tab-content",
        "children",
    ),
    Input(
        "etae-tabs",
        "active_tab",
    ),
    Input(
        "etae-text-column",
        "value",
    ),
    Input(
        "etae-project-id",
        "data",
    ),
    Input(
        "etae-dataset-id",
        "data",
    ),
    Input(
        "etae-association-target",
        "value",
    ),
)
def render_etae_tab(
    active_tab,
    text_column,
    project_id,
    dataset_id,
    association_target,
):
    """
    Rend le contenu de l'onglet ETAE actif.
    """

    if not text_column:
        return dbc.Alert(
            (
                "Sélectionnez une variable "
                "textuelle pour commencer "
                "l'analyse."
            ),
            color="secondary",
        )

    if active_tab in {
        "etae-tab-lexique",
        "etae-tab-ngrams",
    }:
        try:
            dataframe = (
                _load_etae_dataframe(
                    project_id,
                    dataset_id,
                )
            )

            from emidaf_core.etae import (
                ETAEEngine,
            )

            from emidaf_core.etae.preprocessing import (
                TextPreprocessingConfig,
            )

            from .components import (
                lexical_table_component,
            )

            engine = ETAEEngine()

            ngram_size = (
                1
                if active_tab
                == "etae-tab-lexique"
                else 2
            )

            result = engine.analyze_frequencies(
                dataframe,
                text_column,
                ngram_size=ngram_size,
                top_n=30,
                config=TextPreprocessingConfig(
                    remove_stopwords=True,
                    preserve_negations=True,
                ),
            )

            title = (
                "Fréquences lexicales"
                if ngram_size == 1
                else "Bigrammes"
            )

            return html.Div(
                [
                    html.H4(
                        title,
                        className="mb-1",
                    ),
                    html.P(
                        [
                            "Variable analysée : ",
                            html.Strong(
                                text_column
                            ),
                        ],
                        className="text-muted mb-4",
                    ),
                    lexical_table_component(
                        result
                    ),
                ]
            )

        except Exception:
            logger.exception(
                "ETAE lexical analysis failed "
                "(project_id=%s, dataset_id=%s, "
                "text_column=%s)",
                project_id,
                dataset_id,
                text_column,
            )

            return dbc.Alert(
                (
                    "ETAE n'a pas pu produire "
                    "l'analyse lexicale."
                ),
                color="danger",
            )

    if active_tab == "etae-tab-tfidf":
        try:
            dataframe = (
                _load_etae_dataframe(
                    project_id,
                    dataset_id,
                )
            )

            from emidaf_core.etae import (
                ETAEEngine,
            )

            from emidaf_core.etae.preprocessing import (
                TextPreprocessingConfig,
            )

            from .components import (
                tfidf_component,
            )

            engine = ETAEEngine()

            result = engine.analyze_tfidf(
                dataframe,
                text_column,
                max_features=5000,
                ngram_range=(1, 2),
                top_n=30,
                config=TextPreprocessingConfig(
                    remove_stopwords=True,
                    preserve_negations=True,
                ),
            )

            return html.Div(
                [
                    html.H4(
                        "Analyse TF-IDF",
                        className="mb-1",
                    ),
                    html.P(
                        [
                            "Variable analysée : ",
                            html.Strong(
                                text_column
                            ),
                        ],
                        className="text-muted mb-4",
                    ),

                    tfidf_component(
                        result
                    ),
                ]
            )

        except Exception:
            logger.exception(
                "ETAE TF-IDF analysis failed "
                "(project_id=%s, dataset_id=%s, "
                "text_column=%s)",
                project_id,
                dataset_id,
                text_column,
            )

            return dbc.Alert(
                (
                    "ETAE n'a pas pu produire "
                    "l'analyse TF-IDF."
                ),
                color="danger",
            )

    if active_tab == "etae-tab-sentiment":
        try:
            dataframe = (
                _load_etae_dataframe(
                    project_id,
                    dataset_id,
                )
            )

            from emidaf_core.etae import (
                ETAEEngine,
            )

            from .components import (
                sentiment_component,
            )

            engine = ETAEEngine()

            result = engine.analyze_sentiment(
                dataframe,
                text_column,
            )

            return html.Div(
                [
                    html.H4(
                        "Analyse de sentiment",
                        className="mb-1",
                    ),
                    html.P(
                        [
                            "Variable analysée : ",
                            html.Strong(
                                text_column
                            ),
                        ],
                        className="text-muted mb-4",
                    ),

                    sentiment_component(
                        result
                    ),
                ]
            )

        except Exception:
            logger.exception(
                "ETAE sentiment analysis failed "
                "(project_id=%s, dataset_id=%s, "
                "text_column=%s)",
                project_id,
                dataset_id,
                text_column,
            )

            return dbc.Alert(
                (
                    "ETAE n'a pas pu produire "
                    "l'analyse de sentiment."
                ),
                color="danger",
            )

    if active_tab == "etae-tab-topics":
        try:
            dataframe = (
                _load_etae_dataframe(
                    project_id,
                    dataset_id,
                )
            )

            from emidaf_core.etae import (
                ETAEEngine,
            )

            from emidaf_core.etae.preprocessing import (
                TextPreprocessingConfig,
            )

            from .components import (
                topics_component,
            )

            engine = ETAEEngine()

            result = engine.analyze_topics(
                dataframe,
                text_column,
                n_topics=3,
                top_terms=10,
                ngram_range=(1, 2),
                config=TextPreprocessingConfig(
                    remove_stopwords=True,
                    preserve_negations=True,
                ),
            )

            return html.Div(
                [
                    html.H4(
                        "Analyse thématique",
                        className="mb-1",
                    ),
                    html.P(
                        [
                            "Variable analysée : ",
                            html.Strong(
                                text_column
                            ),
                        ],
                        className="text-muted mb-4",
                    ),

                    topics_component(
                        result
                    ),
                ]
            )

        except Exception:
            logger.exception(
                "ETAE topic modeling failed "
                "(project_id=%s, dataset_id=%s, "
                "text_column=%s)",
                project_id,
                dataset_id,
                text_column,
            )

            return dbc.Alert(
                (
                    "ETAE n'a pas pu produire "
                    "l'analyse thématique."
                ),
                color="danger",
            )

    if active_tab == "etae-tab-clusters":
        try:
            dataframe = (
                _load_etae_dataframe(
                    project_id,
                    dataset_id,
                )
            )

            from emidaf_core.etae import (
                ETAEEngine,
            )

            from emidaf_core.etae.preprocessing import (
                TextPreprocessingConfig,
            )

            from .components import (
                text_clusters_component,
            )

            engine = ETAEEngine()

            result = engine.cluster_texts(
                dataframe,
                text_column,
                n_clusters=3,
                top_terms=10,
                ngram_range=(1, 2),
                random_state=42,
                config=TextPreprocessingConfig(
                    remove_stopwords=True,
                    preserve_negations=True,
                ),
            )

            return html.Div(
                [
                    html.H4(
                        "Clustering textuel",
                        className="mb-1",
                    ),
                    html.P(
                        [
                            "Variable analysée : ",
                            html.Strong(
                                text_column
                            ),
                        ],
                        className="text-muted mb-4",
                    ),

                    text_clusters_component(
                        result
                    ),
                ]
            )

        except Exception:
            logger.exception(
                "ETAE text clustering failed "
                "(project_id=%s, dataset_id=%s, "
                "text_column=%s)",
                project_id,
                dataset_id,
                text_column,
            )

            return dbc.Alert(
                (
                    "ETAE n'a pas pu produire "
                    "le clustering textuel."
                ),
                color="danger",
            )

    if active_tab == "etae-tab-associations":

        if not association_target:
            return dbc.Alert(
                (
                    "Sélectionnez une variable structurée "
                    "pour lancer les analyses d'association."
                ),
                color="secondary",
            )

        try:
            dataframe = (
                _load_etae_dataframe(
                    project_id,
                    dataset_id,
                )
            )

            from emidaf_core.etae import (
                ETAEEngine,
            )

            from .components import (
                interpretation_component,
                sentiment_categorical_component,
                sentiment_numeric_component,
                topic_target_component,
            )

            engine = ETAEEngine()

            if pd.api.types.is_numeric_dtype(
                dataframe[
                    association_target
                ]
            ):
                topic_result = (
                    engine.analyze_topic_target(
                        dataframe,
                        text_column,
                        association_target,
                        n_topics=3,
                    )
                )

                sentiment_result = (
                    engine.analyze_sentiment_numeric(
                        dataframe,
                        text_column,
                        association_target,
                    )
                )

                topic_interpretation = (
                    engine.interpret_topic_target(
                        topic_result
                    )
                )

                sentiment_interpretation = (
                    engine.interpret_sentiment_numeric(
                        sentiment_result
                    )
                )

                return html.Div(
                    [
                        html.H4(
                            "Associations texte / données",
                            className="mb-1",
                        ),
                        html.P(
                            [
                                "Texte : ",
                                html.Strong(
                                    text_column
                                ),
                                " — Variable : ",
                                html.Strong(
                                    association_target
                                ),
                            ],
                            className="text-muted mb-4",
                        ),

                        topic_target_component(
                            topic_result
                        ),

                        interpretation_component(
                            topic_interpretation
                        ),

                        html.Hr(
                            className="my-4"
                        ),

                        sentiment_numeric_component(
                            sentiment_result
                        ),

                        interpretation_component(
                            sentiment_interpretation
                        ),
                    ]
                )

            sentiment_result = (
                engine.analyze_sentiment_categorical(
                    dataframe,
                    text_column,
                    association_target,
                )
            )

            interpretation = (
                engine.interpret_sentiment_categorical(
                    sentiment_result
                )
            )

            return html.Div(
                [
                    html.H4(
                        "Associations texte / données",
                        className="mb-1",
                    ),
                    html.P(
                        [
                            "Texte : ",
                            html.Strong(
                                text_column
                            ),
                            " — Variable : ",
                            html.Strong(
                                association_target
                            ),
                        ],
                        className="text-muted mb-4",
                    ),

                    sentiment_categorical_component(
                        sentiment_result
                    ),

                    interpretation_component(
                        interpretation
                    ),
                ]
            )

        except Exception:
            logger.exception(
                "ETAE association analysis failed "
                "(project_id=%s, dataset_id=%s, "
                "text_column=%s, target=%s)",
                project_id,
                dataset_id,
                text_column,
                association_target,
            )

            return dbc.Alert(
                (
                    "ETAE n'a pas pu produire "
                    "l'analyse d'association."
                ),
                color="danger",
            )

    if active_tab != "etae-tab-corpus":
        labels = {
            "etae-tab-tfidf": "TF-IDF",
            "etae-tab-sentiment": "Sentiment",
            "etae-tab-topics": "Thèmes",
            "etae-tab-clusters": "Clusters",
            "etae-tab-associations": (
                "Associations"
            ),
        }

        return dbc.Alert(
            [
                html.Strong(
                    labels.get(
                        active_tab,
                        "Analyse",
                    )
                ),
                (
                    " — cette analyse sera "
                    "activée dans l'étape suivante."
                ),
            ],
            color="light",
        )

    try:
        dataframe = (
            _load_etae_dataframe(
                project_id,
                dataset_id,
            )
        )

        from emidaf_core.etae import (
            ETAEEngine,
        )

        from .components import (
            corpus_profile_component,
        )

        engine = ETAEEngine()

        result = engine.profile_corpus(
            dataframe,
            text_column,
        )

        return html.Div(
            [
                html.Div(
                    [
                        html.H4(
                            "Profil du corpus",
                            className="mb-1",
                        ),
                        html.P(
                            [
                                (
                                    "Variable analysée : "
                                ),
                                html.Strong(
                                    text_column
                                ),
                            ],
                            className=(
                                "text-muted mb-4"
                            ),
                        ),
                    ]
                ),

                corpus_profile_component(
                    result
                ),
            ]
        )

    except Exception:
        logger.exception(
            "ETAE corpus profiling failed "
            "(project_id=%s, dataset_id=%s, "
            "text_column=%s)",
            project_id,
            dataset_id,
            text_column,
        )

        return dbc.Alert(
            [
                html.Strong(
                    "ETAE n'a pas pu analyser "
                    "le corpus. "
                ),
                (
                    "Vérifiez la variable "
                    "textuelle sélectionnée."
                ),
            ],
            color="danger",
        )


@callback(
    Output(
        "etae-association-target",
        "options",
    ),
    Output(
        "etae-association-target",
        "value",
    ),
    Input(
        "etae-text-column",
        "value",
    ),
    Input(
        "etae-project-id",
        "data",
    ),
    Input(
        "etae-dataset-id",
        "data",
    ),
)
def initialize_etae_association_target(
    text_column,
    project_id,
    dataset_id,
):
    """
    Prépare les variables structurées utilisables
    dans les analyses d'association ETAE.
    """

    if (
        not text_column
        or project_id is None
        or dataset_id is None
    ):
        return (
            [],
            None,
        )

    try:
        dataframe = (
            _load_etae_dataframe(
                project_id,
                dataset_id,
            )
        )

    except Exception:
        logger.exception(
            "ETAE association target loading failed "
            "(project_id=%s, dataset_id=%s)",
            project_id,
            dataset_id,
        )

        return (
            [],
            None,
        )

    excluded = {
        text_column,
    }

    options = []

    numeric_columns = list(
        dataframe
        .select_dtypes(
            include="number"
        )
        .columns
    )

    for column in dataframe.columns:
        if column in excluded:
            continue

        kind = (
            "Numérique"
            if column in numeric_columns
            else "Catégorielle"
        )

        options.append(
            {
                "label": (
                    f"{column} — {kind}"
                ),
                "value": column,
            }
        )

    selected = None

    if "note_maths" in dataframe.columns:
        selected = "note_maths"

    return (
        options,
        selected,
    )


@callback(
    Output(
        "etae-association-target",
        "options",
    ),
    Output(
        "etae-association-target",
        "value",
    ),
    Input(
        "etae-text-column",
        "value",
    ),
    Input(
        "etae-project-id",
        "data",
    ),
    Input(
        "etae-dataset-id",
        "data",
    ),
)
def initialize_etae_association_target(
    text_column,
    project_id,
    dataset_id,
):
    """
    Prépare les variables structurées utilisables
    dans les analyses d'association ETAE.
    """

    if (
        not text_column
        or project_id is None
        or dataset_id is None
    ):
        return (
            [],
            None,
        )

    try:
        dataframe = (
            _load_etae_dataframe(
                project_id,
                dataset_id,
            )
        )

    except Exception:
        logger.exception(
            "ETAE association target loading failed "
            "(project_id=%s, dataset_id=%s)",
            project_id,
            dataset_id,
        )

        return (
            [],
            None,
        )

    excluded = {
        text_column,
    }

    options = []

    numeric_columns = list(
        dataframe
        .select_dtypes(
            include="number"
        )
        .columns
    )

    for column in dataframe.columns:
        if column in excluded:
            continue

        kind = (
            "Numérique"
            if column in numeric_columns
            else "Catégorielle"
        )

        options.append(
            {
                "label": (
                    f"{column} — {kind}"
                ),
                "value": column,
            }
        )

    selected = None

    if "note_maths" in dataframe.columns:
        selected = "note_maths"

    return (
        options,
        selected,
    )
