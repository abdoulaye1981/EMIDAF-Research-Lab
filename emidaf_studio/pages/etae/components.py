"""
=========================================================
EMIDAF Studio
ETAE - UI Components
=========================================================
"""

from __future__ import annotations

import dash_bootstrap_components as dbc

from dash import html


def metric_card(
    title: str,
    value,
    *,
    subtitle: str | None = None,
):
    """
    Carte métrique homogène pour ETAE.
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


def corpus_profile_component(
    result,
):
    """
    Affiche un CorpusProfileResult.
    """

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        metric_card(
                            "Documents",
                            result.n_documents,
                        ),
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "Documents valides",
                            result.n_valid_documents,
                        ),
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "Valeurs manquantes",
                            result.n_missing,
                        ),
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "Textes vides",
                            result.n_empty,
                        ),
                        md=3,
                        className="mb-3",
                    ),
                ],
                className="g-3",
            ),

            dbc.Row(
                [
                    dbc.Col(
                        metric_card(
                            "Nombre total de mots",
                            f"{result.total_words:,}",
                        ),
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "Vocabulaire",
                            f"{result.vocabulary_size:,}",
                        ),
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "Mots / document",
                            (
                                f"{result.mean_words:.2f}"
                            ),
                            subtitle=(
                                "moyenne"
                            ),
                        ),
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "Mots / document",
                            (
                                f"{result.median_words:.2f}"
                            ),
                            subtitle=(
                                "médiane"
                            ),
                        ),
                        md=3,
                        className="mb-3",
                    ),
                ],
                className="g-3",
            ),

            dbc.Row(
                [
                    dbc.Col(
                        metric_card(
                            "Caractères / document",
                            (
                                f"{result.mean_characters:.2f}"
                            ),
                            subtitle="moyenne",
                        ),
                        md=4,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "Caractères / document",
                            (
                                f"{result.median_characters:.2f}"
                            ),
                            subtitle="médiane",
                        ),
                        md=4,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "Diversité lexicale",
                            (
                                f"{result.lexical_diversity:.3f}"
                            ),
                            subtitle=(
                                "types / tokens"
                            ),
                        ),
                        md=4,
                        className="mb-3",
                    ),
                ],
                className="g-3",
            ),

            dbc.Alert(
                [
                    html.Strong(
                        "Lecture : "
                    ),
                    (
                        "la diversité lexicale présentée "
                        "correspond au rapport entre le "
                        "nombre de formes lexicales distinctes "
                        "et le nombre total de mots du corpus. "
                        "Elle dépend notamment de la taille "
                        "du corpus."
                    ),
                ],
                color="light",
                className="mt-2",
            ),
        ]
    )


def lexical_table_component(
    result,
):
    """
    Affiche les fréquences lexicales / n-grams.
    """

    if not result.items:
        return dbc.Alert(
            "Aucun élément lexical disponible.",
            color="secondary",
        )

    rows = [
        {
            "Terme": item.term,
            "Fréquence": item.count,
            "Fréquence relative": (
                f"{item.relative_frequency:.4f}"
            ),
        }
        for item in result.items
    ]

    import pandas as pd

    dataframe = pd.DataFrame(
        rows
    )

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        metric_card(
                            "Documents",
                            result.n_documents,
                        ),
                        md=4,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "Occurrences",
                            result.total_tokens,
                        ),
                        md=4,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "Vocabulaire",
                            result.vocabulary_size,
                        ),
                        md=4,
                        className="mb-3",
                    ),
                ],
                className="g-3",
            ),

            dbc.Table.from_dataframe(
                dataframe,
                striped=True,
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
            ),
        ]
    )


def tfidf_component(
    result,
):
    """
    Affiche la synthèse TF-IDF.
    """

    if not result.top_terms:
        return dbc.Alert(
            "Aucun résultat TF-IDF disponible.",
            color="secondary",
        )

    import pandas as pd

    dataframe = pd.DataFrame(
        [
            {
                "Terme": item.term,
                "Score TF-IDF moyen": (
                    item.mean_score
                ),
            }
            for item in result.top_terms
        ]
    )

    dataframe[
        "Score TF-IDF moyen"
    ] = dataframe[
        "Score TF-IDF moyen"
    ].round(4)

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        metric_card(
                            "Documents",
                            result.n_documents,
                        ),
                        md=4,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "Variables TF-IDF",
                            result.n_features,
                        ),
                        md=4,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "Sparsité",
                            (
                                f"{result.sparsity * 100:.2f} %"
                            ),
                        ),
                        md=4,
                        className="mb-3",
                    ),
                ],
                className="g-3",
            ),

            html.H5(
                "Termes les plus représentatifs",
                className="mt-2 mb-3",
            ),

            dbc.Table.from_dataframe(
                dataframe,
                striped=True,
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
            ),

            dbc.Alert(
                [
                    html.Strong(
                        "Lecture : "
                    ),
                    (
                        "un score TF-IDF élevé indique "
                        "qu'un terme contribue davantage "
                        "à distinguer les documents du corpus. "
                        "Le score affiché ici correspond à "
                        "la moyenne du TF-IDF du terme sur "
                        "l'ensemble des documents analysés."
                    ),
                ],
                color="light",
                className="mt-3",
            ),
        ]
    )


def sentiment_component(
    result,
):
    """
    Affiche les résultats d'analyse de sentiment.
    """

    if result.n_documents == 0:
        return dbc.Alert(
            "Aucun document exploitable pour l'analyse de sentiment.",
            color="secondary",
        )

    import pandas as pd

    summary = dbc.Row(
        [
            dbc.Col(
                metric_card(
                    "Documents analysés",
                    result.n_documents,
                ),
                md=3,
                className="mb-3",
            ),
            dbc.Col(
                metric_card(
                    "Score moyen",
                    f"{result.mean_score:.3f}",
                ),
                md=3,
                className="mb-3",
            ),
            dbc.Col(
                metric_card(
                    "Couverture lexicale",
                    f"{result.mean_coverage * 100:.2f} %",
                ),
                md=3,
                className="mb-3",
            ),
            dbc.Col(
                metric_card(
                    "Méthode",
                    result.method,
                ),
                md=3,
                className="mb-3",
            ),
        ],
        className="g-3",
    )

    distribution = pd.DataFrame(
        [
            {
                "Polarité": "Positive",
                "Effectif": result.positive_count,
            },
            {
                "Polarité": "Neutre",
                "Effectif": result.neutral_count,
            },
            {
                "Polarité": "Négative",
                "Effectif": result.negative_count,
            },
        ]
    )

    details = pd.DataFrame(
        [
            {
                "Index": document.index,
                "Score": round(
                    document.score,
                    4,
                ),
                "Polarité": document.label,
                "Tokens reconnus": (
                    document.matched_tokens
                ),
                "Tokens totaux": (
                    document.total_tokens
                ),
                "Couverture": (
                    f"{document.coverage * 100:.1f} %"
                ),
            }
            for document in result.documents
        ]
    )

    return html.Div(
        [
            summary,

            html.H5(
                "Distribution des polarités",
                className="mt-2 mb-3",
            ),

            dbc.Table.from_dataframe(
                distribution,
                striped=True,
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
            ),

            html.H5(
                "Détail par document",
                className="mt-4 mb-3",
            ),

            dbc.Table.from_dataframe(
                details,
                striped=True,
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
            ),

            dbc.Alert(
                [
                    html.Strong(
                        "Précaution : "
                    ),
                    (
                        "la polarité repose actuellement sur "
                        "un analyseur lexical de référence. "
                        "Une couverture faible signifie que "
                        "peu de mots du document ont contribué "
                        "au score. Le résultat ne doit donc pas "
                        "être interprété comme une mesure "
                        "exhaustive de l'état émotionnel."
                    ),
                ],
                color="light",
                className="mt-3",
            ),
        ]
    )


def topics_component(
    result,
):
    """
    Affiche les résultats du topic modeling NMF.
    """

    if result.n_documents == 0:
        return dbc.Alert(
            "Aucun document exploitable pour l'analyse thématique.",
            color="secondary",
        )

    import pandas as pd

    overview = dbc.Row(
        [
            dbc.Col(
                metric_card(
                    "Documents analysés",
                    result.n_documents,
                ),
                md=4,
                className="mb-3",
            ),
            dbc.Col(
                metric_card(
                    "Nombre de thèmes",
                    result.n_topics,
                ),
                md=4,
                className="mb-3",
            ),
            dbc.Col(
                metric_card(
                    "Méthode",
                    result.method,
                ),
                md=4,
                className="mb-3",
            ),
        ],
        className="g-3",
    )

    distribution = pd.DataFrame(
        [
            {
                "Thème": topic.topic,
                "Documents": topic.document_count,
                "Pourcentage": (
                    f"{topic.percentage:.2f} %"
                ),
                "Termes caractéristiques": (
                    ", ".join(
                        topic.top_terms
                    )
                ),
            }
            for topic in result.topics
        ]
    )

    cards = []

    for topic in result.topics:
        cards.append(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5(
                                f"Thème {topic.topic}",
                                className="card-title",
                            ),
                            html.P(
                                (
                                    f"{topic.document_count} "
                                    "documents "
                                    f"({topic.percentage:.2f} %)"
                                ),
                                className="text-muted",
                            ),
                            html.Div(
                                [
                                    dbc.Badge(
                                        term,
                                        color="secondary",
                                        className="me-1 mb-1",
                                    )
                                    for term
                                    in topic.top_terms
                                ]
                            ),
                        ]
                    ),
                    className="h-100 shadow-sm",
                ),
                md=4,
                className="mb-3",
            )
        )

    return html.Div(
        [
            overview,

            html.H5(
                "Synthèse des thèmes",
                className="mt-2 mb-3",
            ),

            dbc.Table.from_dataframe(
                distribution,
                striped=True,
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
            ),

            html.H5(
                "Termes caractéristiques par thème",
                className="mt-4 mb-3",
            ),

            dbc.Row(
                cards,
                className="g-3",
            ),

            dbc.Alert(
                [
                    html.Strong(
                        "Interprétation : "
                    ),
                    (
                        "les thèmes sont obtenus automatiquement "
                        "par factorisation NMF de la matrice TF-IDF. "
                        "Les termes affichés servent à caractériser "
                        "les dimensions latentes détectées. "
                        "L'attribution d'un intitulé conceptuel "
                        "à chaque thème doit être réalisée avec "
                        "prudence et idéalement validée par "
                        "une analyse qualitative."
                    ),
                ],
                color="light",
                className="mt-3",
            ),
        ]
    )


def text_clusters_component(
    result,
):
    """
    Affiche les résultats du clustering textuel.
    """

    if result.n_documents == 0:
        return dbc.Alert(
            "Aucun document exploitable pour le clustering textuel.",
            color="secondary",
        )

    import pandas as pd

    def metric_value(
        value,
    ):
        if value is None:
            return "N/A"

        return f"{value:.4f}"

    overview = dbc.Row(
        [
            dbc.Col(
                metric_card(
                    "Documents",
                    result.n_documents,
                ),
                md=3,
                className="mb-3",
            ),
            dbc.Col(
                metric_card(
                    "Clusters",
                    result.n_clusters,
                ),
                md=3,
                className="mb-3",
            ),
            dbc.Col(
                metric_card(
                    "Silhouette",
                    metric_value(
                        result.silhouette_score
                    ),
                    subtitle="plus élevé = mieux",
                ),
                md=3,
                className="mb-3",
            ),
            dbc.Col(
                metric_card(
                    "Davies-Bouldin",
                    metric_value(
                        result.davies_bouldin_score
                    ),
                    subtitle="plus faible = mieux",
                ),
                md=3,
                className="mb-3",
            ),
        ],
        className="g-3",
    )

    quality = dbc.Row(
        [
            dbc.Col(
                metric_card(
                    "Calinski-Harabasz",
                    metric_value(
                        result.calinski_harabasz_score
                    ),
                    subtitle="plus élevé = mieux",
                ),
                md=4,
                className="mb-3",
            ),
        ],
        className="g-3",
    )

    dataframe = pd.DataFrame(
        [
            {
                "Cluster": cluster.cluster,
                "Documents": cluster.size,
                "Pourcentage": (
                    f"{cluster.percentage:.2f} %"
                ),
                "Termes caractéristiques": (
                    ", ".join(
                        cluster.top_terms
                    )
                ),
            }
            for cluster in result.clusters
        ]
    )

    cards = [
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            f"Cluster {cluster.cluster}",
                            className="card-title",
                        ),
                        html.P(
                            (
                                f"{cluster.size} documents "
                                f"({cluster.percentage:.2f} %)"
                            ),
                            className="text-muted",
                        ),
                        html.Div(
                            [
                                dbc.Badge(
                                    term,
                                    color="secondary",
                                    className="me-1 mb-1",
                                )
                                for term
                                in cluster.top_terms
                            ]
                        ),
                    ]
                ),
                className="h-100 shadow-sm",
            ),
            md=4,
            className="mb-3",
        )
        for cluster in result.clusters
    ]

    return html.Div(
        [
            overview,
            quality,

            html.H5(
                "Composition des clusters",
                className="mt-2 mb-3",
            ),

            dbc.Table.from_dataframe(
                dataframe,
                striped=True,
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
            ),

            html.H5(
                "Profils lexicaux",
                className="mt-4 mb-3",
            ),

            dbc.Row(
                cards,
                className="g-3",
            ),

            dbc.Alert(
                [
                    html.Strong(
                        "Lecture scientifique : "
                    ),
                    (
                        "les clusters représentent des groupes "
                        "de documents proches dans l'espace "
                        "TF-IDF. Ils ne correspondent pas "
                        "nécessairement à des catégories "
                        "conceptuelles réelles. Les métriques "
                        "de qualité doivent être examinées "
                        "avant toute interprétation substantielle."
                    ),
                ],
                color="light",
                className="mt-3",
            ),
        ]
    )


def interpretation_component(
    interpretation,
):
    """
    Affiche une interprétation scientifique structurée.
    """

    if interpretation is None:
        return html.Div()

    badges = {
        "descriptive": "secondary",
        "diagnostic": "info",
        "inference": "primary",
        "effect_size": "success",
        "caution": "warning",
        "warning": "warning",
    }

    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    interpretation.title,
                    className="mb-3",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dbc.Badge(
                                    statement.level,
                                    color=badges.get(
                                        statement.level,
                                        "secondary",
                                    ),
                                    className="me-2",
                                ),
                                html.Span(
                                    statement.message
                                ),
                            ],
                            className="mb-3",
                        )
                        for statement
                        in interpretation.statements
                    ]
                ),
            ]
        ),
        className="mt-4 shadow-sm",
    )


def topic_target_component(
    result,
):
    """
    Affiche l'association thèmes / cible quantitative.
    """

    import pandas as pd

    if not result.groups:
        return dbc.Alert(
            "Aucun résultat d'association thème/cible.",
            color="secondary",
        )

    groups = pd.DataFrame(
        [
            {
                "Thème": group.topic,
                "n": group.n,
                "Moyenne": round(
                    group.mean,
                    4,
                ),
                "Médiane": round(
                    group.median,
                    4,
                ),
                "Écart-type": (
                    None
                    if group.std is None
                    else round(
                        group.std,
                        4,
                    )
                ),
                "Min": round(
                    group.minimum,
                    4,
                ),
                "Max": round(
                    group.maximum,
                    4,
                ),
            }
            for group in result.groups
        ]
    )

    children = [
        html.H5(
            "Thèmes × variable quantitative",
            className="mb-3",
        ),

        dbc.Table.from_dataframe(
            groups,
            striped=True,
            bordered=True,
            hover=True,
            responsive=True,
            size="sm",
        ),
    ]

    inference = result.inference

    if inference is not None:
        tests = pd.DataFrame(
            [
                {
                    "Test": (
                        inference.levene.test
                    ),
                    "Statistique": (
                        inference.levene.statistic
                    ),
                    "p-value": (
                        inference.levene.p_value
                    ),
                },
                {
                    "Test": (
                        inference.anova.test
                    ),
                    "Statistique": (
                        inference.anova.statistic
                    ),
                    "p-value": (
                        inference.anova.p_value
                    ),
                },
                {
                    "Test": (
                        inference.welch_anova.test
                    ),
                    "Statistique": (
                        inference
                        .welch_anova
                        .statistic
                    ),
                    "p-value": (
                        inference
                        .welch_anova
                        .p_value
                    ),
                },
                {
                    "Test": (
                        inference.kruskal.test
                    ),
                    "Statistique": (
                        inference.kruskal.statistic
                    ),
                    "p-value": (
                        inference.kruskal.p_value
                    ),
                },
            ]
        )

        children.extend(
            [
                html.H6(
                    "Tests globaux",
                    className="mt-4 mb-3",
                ),

                dbc.Table.from_dataframe(
                    tests.round(4),
                    striped=True,
                    bordered=True,
                    hover=True,
                    responsive=True,
                    size="sm",
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            metric_card(
                                "η²",
                                (
                                    "N/A"
                                    if inference
                                    .eta_squared
                                    .value
                                    is None
                                    else (
                                        f"{inference.eta_squared.value:.3f}"
                                    )
                                ),
                            ),
                            md=4,
                            className="mb-3",
                        ),
                        dbc.Col(
                            metric_card(
                                "ω²",
                                (
                                    "N/A"
                                    if inference
                                    .omega_squared
                                    .value
                                    is None
                                    else (
                                        f"{inference.omega_squared.value:.3f}"
                                    )
                                ),
                            ),
                            md=4,
                            className="mb-3",
                        ),
                        dbc.Col(
                            metric_card(
                                "ε²",
                                (
                                    "N/A"
                                    if inference
                                    .epsilon_squared
                                    .value
                                    is None
                                    else (
                                        f"{inference.epsilon_squared.value:.3f}"
                                    )
                                ),
                            ),
                            md=4,
                            className="mb-3",
                        ),
                    ],
                    className="g-3 mt-2",
                ),
            ]
        )

    return html.Div(
        children
    )


def sentiment_numeric_component(
    result,
):
    """
    Affiche sentiment / cible quantitative.
    """

    import pandas as pd

    dataframe = pd.DataFrame(
        [
            {
                "Polarité": group.sentiment,
                "n": group.n,
                "Moyenne": round(
                    group.mean,
                    4,
                ),
                "Médiane": round(
                    group.median,
                    4,
                ),
                "Écart-type": (
                    None
                    if group.std is None
                    else round(
                        group.std,
                        4,
                    )
                ),
            }
            for group in result.groups
        ]
    )

    return html.Div(
        [
            html.H5(
                "Sentiment × variable quantitative",
                className="mb-3",
            ),

            dbc.Table.from_dataframe(
                dataframe,
                striped=True,
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
            ),

            dbc.Row(
                [
                    dbc.Col(
                        metric_card(
                            "ANOVA p-value",
                            (
                                "N/A"
                                if result.anova_p_value
                                is None
                                else (
                                    f"{result.anova_p_value:.4g}"
                                )
                            ),
                        ),
                        md=6,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "Kruskal-Wallis p-value",
                            (
                                "N/A"
                                if result.kruskal_p_value
                                is None
                                else (
                                    f"{result.kruskal_p_value:.4g}"
                                )
                            ),
                        ),
                        md=6,
                        className="mb-3",
                    ),
                ],
                className="g-3",
            ),
        ]
    )


def sentiment_categorical_component(
    result,
):
    """
    Affiche sentiment / cible catégorielle.
    """

    import pandas as pd

    if not result.contingency_table:
        return dbc.Alert(
            "Aucune table de contingence disponible.",
            color="secondary",
        )

    dataframe = (
        pd.DataFrame(
            result.contingency_table
        )
        .T
        .reset_index()
        .rename(
            columns={
                "index": "Polarité"
            }
        )
    )

    return html.Div(
        [
            html.H5(
                "Sentiment × variable catégorielle",
                className="mb-3",
            ),

            dbc.Table.from_dataframe(
                dataframe,
                striped=True,
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
            ),

            dbc.Row(
                [
                    dbc.Col(
                        metric_card(
                            "Khi²",
                            (
                                "N/A"
                                if result.chi2_statistic
                                is None
                                else (
                                    f"{result.chi2_statistic:.4f}"
                                )
                            ),
                        ),
                        md=4,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "p-value",
                            (
                                "N/A"
                                if result.p_value
                                is None
                                else (
                                    f"{result.p_value:.4g}"
                                )
                            ),
                        ),
                        md=4,
                        className="mb-3",
                    ),
                    dbc.Col(
                        metric_card(
                            "ddl",
                            (
                                "N/A"
                                if result.dof is None
                                else result.dof
                            ),
                        ),
                        md=4,
                        className="mb-3",
                    ),
                ],
                className="g-3",
            ),
        ]
    )
