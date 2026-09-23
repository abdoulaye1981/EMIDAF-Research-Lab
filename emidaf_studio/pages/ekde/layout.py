
from dash import dcc, html
import dash_bootstrap_components as dbc

from emidaf_studio.pages.inspection.layout import load_dataset

from emidaf_studio.pages.ekde.callbacks import (
    structure_analysis,
    pca_analysis,
    association_analysis,
    knowledge_summary,
)


def _metric_card(title, value, subtitle=None):

    children = [
        html.H6(
            title,
            className="text-muted",
        ),
        html.H4(str(value)),
    ]

    if subtitle:
        children.append(
            html.Small(
                subtitle,
                className="text-muted",
            )
        )

    return dbc.Card(
        dbc.CardBody(children),
        className="h-100",
    )


def _numeric_like_columns(df, threshold=0.95):

    import pandas as pd

    columns = []

    for column in df.columns:

        series = df[column]

        if pd.api.types.is_numeric_dtype(series):
            columns.append(column)
            continue

        if not (
            pd.api.types.is_object_dtype(series)
            or pd.api.types.is_string_dtype(series)
        ):
            continue

        non_missing = series.dropna()

        if non_missing.empty:
            continue

        converted = pd.to_numeric(
            non_missing,
            errors="coerce",
        )

        if converted.notna().mean() >= threshold:
            columns.append(column)

    return columns


def ekde_layout(project_id, dataset_id):

    project, dataset, result = load_dataset(
        project_id,
        dataset_id,
    )

    if isinstance(result, str):

        return dbc.Container(
            dbc.Alert(
                result,
                color="danger",
            ),
            fluid=True,
        )

    df = result

    numeric_like = _numeric_like_columns(df)

    categorical = [
        column
        for column in df.columns
        if column not in numeric_like
    ]

    default_x = (
        numeric_like[0]
        if numeric_like
        else None
    )

    default_y = (
        numeric_like[1]
        if len(numeric_like) > 1
        else default_x
    )

    max_components = max(
        2,
        min(
            len(numeric_like),
            10,
        ),
    )

    tsne_max_perplexity = max(
        1,
        min(
            50,
            len(df) - 1,
        ),
    )

    tsne_default_perplexity = min(
        30,
        tsne_max_perplexity,
    )

    kmeans_max_clusters = max(
        2,
        min(
            10,
            max(
                2,
                len(df) - 1,
            ),
        ),
    )

    kmeans_default_clusters = min(
        3,
        kmeans_max_clusters,
    )

    # ======================================================
    # INITIAL LIGHTWEIGHT RENDERING
    # ======================================================

    # Les analyses scientifiques lourdes sont exécutées
    # uniquement à la demande. Le dataset reste côté serveur.

    initial_structure = dbc.Alert(
        (
            "Aucun calcul n'est lancé automatiquement. "
            "Modifiez le seuil pour exécuter l'analyse "
            "de structure."
        ),
        color="secondary",
    )

    initial_correlation_figure = {}

    initial_pca_summary = dbc.Alert(
        (
            "La PCA sera calculée à la demande. "
            "Modifiez le nombre de composantes "
            "pour lancer l'analyse."
        ),
        color="secondary",
    )

    initial_pca_variance = {}
    initial_pca_projection = {}

    initial_association = dbc.Alert(
        (
            "Sélectionnez les variables à étudier "
            "pour calculer leur association."
        ),
        color="secondary",
    )

    initial_association_figure = {}

    initial_knowledge = dbc.Alert(
        (
            "La synthèse des connaissances sera "
            "disponible après les analyses EKDE."
        ),
        color="secondary",
    )

    return dbc.Container(
        [
            html.H2(
                "Découverte de connaissances : EKDE",
                className="mt-3",
            ),

            html.P(
                (
                    "Identifiez les structures latentes, redondances, "
                    "associations et variables informatives du jeu de données. "
                    "Ces diagnostics exploratoires peuvent orienter la "
                    "modélisation, sans établir à eux seuls de lien causal."
                ),
                className="text-muted",
            ),

            dbc.Alert(
                [
                    html.Strong(
                        "Principe scientifique : "
                    ),
                    (
                        "les préparations nécessaires aux analyses "
                        "(conversion numeric-like, imputation et "
                        "standardisation) sont temporaires. "
                        "Le dataset source n'est pas modifié."
                    ),
                ],
                color="info",
            ),

            dbc.Breadcrumb(
                items=[
                    {
                        "label": "Projets",
                        "href": "/projects",
                    },
                    {
                        "label": project.name,
                        "href": f"/projects/{project_id}",
                    },
                    {
                        "label": dataset.name,
                        "href": (
                            f"/projects/{project_id}"
                            f"/datasets/{dataset_id}"
                        ),
                    },
                    {
                        "label": "EKDE",
                        "active": True,
                    },
                ]
            ),

            # ==================================================
            # OVERVIEW
            # ==================================================

            dbc.Row(
                [
                    dbc.Col(
                        _metric_card(
                            "Observations",
                            df.shape[0],
                        ),
                        md=3,
                    ),

                    dbc.Col(
                        _metric_card(
                            "Variables",
                            df.shape[1],
                        ),
                        md=3,
                    ),

                    dbc.Col(
                        _metric_card(
                            "Variables numériques / numeric-like",
                            len(numeric_like),
                        ),
                        md=3,
                    ),

                    dbc.Col(
                        _metric_card(
                            "Variables catégorielles",
                            len(categorical),
                        ),
                        md=3,
                    ),
                ],
                className="g-3 mb-4",
            ),

            dbc.Tabs(
                [
                    # ==========================================
                    # STRUCTURE
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "🔎 Structure et redondance",
                                className="mt-4",
                            ),

                            html.P(
                                (
                                    "Recherche de variables fortement "
                                    "corrélées et potentiellement "
                                    "redondantes."
                                ),
                                className="text-muted",
                            ),

                            dbc.Label(
                                "Seuil de corrélation absolue"
                            ),

                            dcc.Slider(
                                id="ekde-correlation-threshold",
                                min=0.50,
                                max=0.99,
                                step=0.01,
                                value=0.90,
                                marks={
                                    0.50: "0.50",
                                    0.70: "0.70",
                                    0.80: "0.80",
                                    0.90: "0.90",
                                    0.99: "0.99",
                                },
                            ),

                            dbc.Button(
                                "Lancer l'analyse de structure",
                                id="ekde-structure-run",
                                color="primary",
                                className="mt-3",
                            ),

                            html.Div(
                                initial_structure,
                                id="ekde-structure-summary",
                                className="mt-4",
                            ),

                            dcc.Graph(
                                id="ekde-correlation-graph",
                                figure=initial_correlation_figure,
                            ),
                        ],
                        label="Structure",
                    ),

                    # ==========================================
                    # PCA
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "Réduction dimensionnelle : ACP",
                                className="mt-4",
                            ),

                            html.P(
                                (
                                    "La PCA est exécutée sur les variables "
                                    "numériques après préparation "
                                    "analytique temporaire."
                                ),
                                className="text-muted",
                            ),

                            dbc.Label(
                                "Nombre de composantes"
                            ),

                            dcc.Slider(
                                id="ekde-pca-components",
                                min=2,
                                max=max_components,
                                step=1,
                                value=min(
                                    2,
                                    max_components,
                                ),
                                marks={
                                    i: str(i)
                                    for i in range(
                                        2,
                                        max_components + 1,
                                    )
                                },
                            ),

                            dbc.Button(
                                "Lancer la PCA",
                                id="ekde-pca-run",
                                color="primary",
                                className="mt-3",
                            ),

                            html.Div(
                                initial_pca_summary,
                                id="ekde-pca-summary",
                                className="mt-4",
                            ),

                            dcc.Graph(
                                id="ekde-pca-variance-graph",
                                figure=initial_pca_variance,
                            ),

                            dcc.Graph(
                                id="ekde-pca-projection",
                                figure=initial_pca_projection,
                            ),
                        ],
                        label="PCA",
                    ),

                    # ==========================================
                    # t-SNE
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "Réduction dimensionnelle : t-SNE",
                                className="mt-4",
                            ),
                            html.P(
                                (
                                    "t-SNE produit une représentation "
                                    "bidimensionnelle non linéaire des "
                                    "observations à partir des variables "
                                    "numériques standardisées."
                                ),
                                className="text-muted",
                            ),
                            dbc.Alert(
                                (
                                    "Le calcul t-SNE n'est pas lancé "
                                    "automatiquement. Configurez la "
                                    "perplexité puis cliquez sur "
                                    "« Lancer t-SNE »."
                                ),
                                color="secondary",
                            ),
                            dbc.Label(
                                "Perplexité"
                            ),
                            dbc.Input(
                                id="ekde-tsne-perplexity",
                                type="number",
                                min=1,
                                max=tsne_max_perplexity,
                                step=1,
                                value=tsne_default_perplexity,
                            ),
                            html.Small(
                                (
                                    "La perplexité doit être strictement "
                                    "inférieure au nombre d'observations. "
                                    "EMIDAF ajuste automatiquement la "
                                    "valeur si nécessaire."
                                ),
                                className="text-muted",
                            ),
                            html.Div(
                                [
                                    dbc.Button(
                                        "Lancer t-SNE",
                                        id="ekde-tsne-run",
                                        color="primary",
                                        className="mt-3",
                                    ),
                                ]
                            ),
                            dbc.Spinner(
                                html.Div(
                                    id="ekde-tsne-summary",
                                    className="mt-4",
                                ),
                            ),
                            dcc.Graph(
                                id="ekde-tsne-projection",
                                figure={},
                            ),
                        ],
                        label="t-SNE",
                    ),

                    # ==========================================
                    # UMAP
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "Réduction dimensionnelle : UMAP",
                                className="mt-4",
                            ),
                            html.P(
                                (
                                    "UMAP produit une représentation "
                                    "non linéaire des observations à "
                                    "partir des variables numériques "
                                    "standardisées."
                                ),
                                className="text-muted",
                            ),
                            dbc.Alert(
                                (
                                    "Le calcul UMAP n'est pas lancé "
                                    "automatiquement. Configurez les "
                                    "paramètres puis cliquez sur "
                                    "« Lancer UMAP »."
                                ),
                                color="secondary",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "n_neighbors"
                                            ),
                                            dbc.Input(
                                                id="ekde-umap-neighbors",
                                                type="number",
                                                min=2,
                                                step=1,
                                                value=15,
                                            ),
                                            html.Small(
                                                (
                                                    "Contrôle l'échelle "
                                                    "locale du voisinage."
                                                ),
                                                className="text-muted",
                                            ),
                                        ],
                                        md=4,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "min_dist"
                                            ),
                                            dbc.Input(
                                                id="ekde-umap-min-dist",
                                                type="number",
                                                min=0,
                                                step=0.05,
                                                value=0.1,
                                            ),
                                            html.Small(
                                                (
                                                    "Contrôle la compacité "
                                                    "des groupes dans "
                                                    "l'espace projeté."
                                                ),
                                                className="text-muted",
                                            ),
                                        ],
                                        md=4,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Métrique"
                                            ),
                                            dcc.Dropdown(
                                                id="ekde-umap-metric",
                                                options=[
                                                    {
                                                        "label": "Euclidienne",
                                                        "value": "euclidean",
                                                    },
                                                    {
                                                        "label": "Manhattan",
                                                        "value": "manhattan",
                                                    },
                                                    {
                                                        "label": "Cosinus",
                                                        "value": "cosine",
                                                    },
                                                ],
                                                value="euclidean",
                                                clearable=False,
                                            ),
                                        ],
                                        md=4,
                                    ),
                                ],
                                className="mt-3",
                            ),
                            html.Div(
                                [
                                    dbc.Button(
                                        "Lancer UMAP",
                                        id="ekde-umap-run",
                                        color="primary",
                                        className="mt-3",
                                    ),
                                ]
                            ),
                            dbc.Spinner(
                                html.Div(
                                    id="ekde-umap-summary",
                                    className="mt-4",
                                ),
                            ),
                            dcc.Graph(
                                id="ekde-umap-projection",
                                figure={},
                            ),
                        ],
                        label="UMAP",
                    ),

                    # ==========================================
                    # CLUSTERING - K-MEANS
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "Clustering exploratoire : K-Means",
                                className="mt-4",
                            ),
                            html.P(
                                (
                                    "K-Means partitionne les observations "
                                    "en groupes à partir des variables "
                                    "numériques standardisées."
                                ),
                                className="text-muted",
                            ),
                            dbc.Alert(
                                (
                                    "Le clustering n'est pas exécuté "
                                    "automatiquement. Choisissez le "
                                    "nombre de clusters puis cliquez "
                                    "sur « Lancer K-Means »."
                                ),
                                color="secondary",
                            ),
                            dbc.Label(
                                "Nombre de clusters"
                            ),
                            dcc.Slider(
                                id="ekde-kmeans-clusters",
                                min=2,
                                max=kmeans_max_clusters,
                                step=1,
                                value=kmeans_default_clusters,
                                marks={
                                    i: str(i)
                                    for i in range(
                                        2,
                                        kmeans_max_clusters + 1,
                                    )
                                },
                            ),
                            html.Small(
                                (
                                    "Le nombre choisi représente une "
                                    "hypothèse de partitionnement à "
                                    "évaluer ; il n'est pas présenté "
                                    "comme optimal par défaut."
                                ),
                                className="text-muted",
                            ),
                            html.Div(
                                [
                                    dbc.Button(
                                        "Lancer K-Means",
                                        id="ekde-kmeans-run",
                                        color="primary",
                                        className="mt-3",
                                    ),
                                ]
                            ),
                            dbc.Spinner(
                                html.Div(
                                    id="ekde-kmeans-summary",
                                    className="mt-4",
                                ),
                            ),
                            dcc.Graph(
                                id="ekde-kmeans-projection",
                                figure={},
                            ),

                            html.Hr(
                                className="my-5"
                            ),
                            html.H4(
                                "Clustering exploratoire : DBSCAN",
                                className="mt-4",
                            ),
                            html.P(
                                (
                                    "DBSCAN recherche des groupes "
                                    "denses sans imposer à l'avance "
                                    "leur nombre. Les observations "
                                    "isolées peuvent être identifiées "
                                    "comme bruit."
                                ),
                                className="text-muted",
                            ),
                            dbc.Alert(
                                (
                                    "Les observations identifiées "
                                    "comme bruit ne sont ni supprimées "
                                    "ni modifiées. Elles restent "
                                    "présentes dans l'analyse."
                                ),
                                color="secondary",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "eps"
                                            ),
                                            dbc.Input(
                                                id="ekde-dbscan-eps",
                                                type="number",
                                                min=0.01,
                                                step=0.05,
                                                value=0.5,
                                            ),
                                            html.Small(
                                                (
                                                    "Rayon maximal du "
                                                    "voisinage autour "
                                                    "d'une observation."
                                                ),
                                                className="text-muted",
                                            ),
                                        ],
                                        md=6,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "min_samples"
                                            ),
                                            dbc.Input(
                                                id=(
                                                    "ekde-dbscan-"
                                                    "min-samples"
                                                ),
                                                type="number",
                                                min=2,
                                                step=1,
                                                value=5,
                                            ),
                                            html.Small(
                                                (
                                                    "Nombre minimal "
                                                    "d'observations "
                                                    "nécessaires pour "
                                                    "former une zone "
                                                    "dense."
                                                ),
                                                className="text-muted",
                                            ),
                                        ],
                                        md=6,
                                    ),
                                ],
                                className="mt-3",
                            ),
                            html.Div(
                                [
                                    dbc.Button(
                                        "Lancer DBSCAN",
                                        id="ekde-dbscan-run",
                                        color="primary",
                                        className="mt-3",
                                    ),
                                ]
                            ),
                            dbc.Spinner(
                                html.Div(
                                    id="ekde-dbscan-summary",
                                    className="mt-4",
                                ),
                            ),
                            dcc.Graph(
                                id="ekde-dbscan-projection",
                                figure={},
                            ),

                            html.Hr(
                                className="my-5"
                            ),
                            html.H4(
                                (
                                    "Clustering hiérarchique "
                                    "agglomératif"
                                ),
                                className="mt-4",
                            ),
                            html.P(
                                (
                                    "Le clustering hiérarchique "
                                    "agglomératif construit "
                                    "progressivement des groupes en "
                                    "fusionnant les observations ou "
                                    "clusters les plus proches."
                                ),
                                className="text-muted",
                            ),
                            dbc.Alert(
                                (
                                    "L'analyse n'est pas exécutée "
                                    "automatiquement. Le nombre de "
                                    "clusters représente une hypothèse "
                                    "de partitionnement à évaluer."
                                ),
                                color="secondary",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Nombre de clusters"
                                            ),
                                            dcc.Slider(
                                                id=(
                                                    "ekde-agglomerative-"
                                                    "clusters"
                                                ),
                                                min=2,
                                                max=(
                                                    kmeans_max_clusters
                                                ),
                                                step=1,
                                                value=(
                                                    kmeans_default_clusters
                                                ),
                                                marks={
                                                    i: str(i)
                                                    for i in range(
                                                        2,
                                                        (
                                                            kmeans_max_clusters
                                                            + 1
                                                        ),
                                                    )
                                                },
                                            ),
                                        ],
                                        md=4,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Linkage"
                                            ),
                                            dcc.Dropdown(
                                                id=(
                                                    "ekde-agglomerative-"
                                                    "linkage"
                                                ),
                                                options=[
                                                    {
                                                        "label": "Ward",
                                                        "value": "ward",
                                                    },
                                                    {
                                                        "label": "Complete",
                                                        "value": "complete",
                                                    },
                                                    {
                                                        "label": "Average",
                                                        "value": "average",
                                                    },
                                                    {
                                                        "label": "Single",
                                                        "value": "single",
                                                    },
                                                ],
                                                value="ward",
                                                clearable=False,
                                            ),
                                        ],
                                        md=4,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Métrique"
                                            ),
                                            dcc.Dropdown(
                                                id=(
                                                    "ekde-agglomerative-"
                                                    "metric"
                                                ),
                                                options=[
                                                    {
                                                        "label": "Euclidienne",
                                                        "value": "euclidean",
                                                    },
                                                    {
                                                        "label": "Manhattan",
                                                        "value": "manhattan",
                                                    },
                                                    {
                                                        "label": "Cosinus",
                                                        "value": "cosine",
                                                    },
                                                ],
                                                value="euclidean",
                                                clearable=False,
                                            ),
                                        ],
                                        md=4,
                                    ),
                                ],
                                className="mt-3",
                            ),
                            html.Small(
                                (
                                    "Avec le linkage Ward, la distance "
                                    "euclidienne est imposée par le "
                                    "moteur scientifique, quelle que "
                                    "soit la métrique sélectionnée."
                                ),
                                className="text-muted",
                            ),
                            html.Div(
                                [
                                    dbc.Button(
                                        (
                                            "Lancer le clustering "
                                            "hiérarchique"
                                        ),
                                        id=(
                                            "ekde-agglomerative-run"
                                        ),
                                        color="primary",
                                        className="mt-3",
                                    ),
                                ]
                            ),
                            dbc.Spinner(
                                html.Div(
                                    id=(
                                        "ekde-agglomerative-summary"
                                    ),
                                    className="mt-4",
                                ),
                            ),
                            dcc.Graph(
                                id=(
                                    "ekde-agglomerative-projection"
                                ),
                                figure={},
                            ),
                        ],
                        label="Clustering",
                    ),

                    # ==========================================
                    # ASSOCIATIONS
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "Découverte d'associations",
                                className="mt-4",
                            ),

                            html.P(
                                (
                                    "Analyse des dépendances entre "
                                    "deux variables numériques."
                                ),
                                className="text-muted",
                            ),

                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Variable X"
                                            ),

                                            dcc.Dropdown(
                                                id="ekde-association-x",
                                                options=[
                                                    {
                                                        "label": column,
                                                        "value": column,
                                                    }
                                                    for column
                                                    in numeric_like
                                                ],
                                                value=default_x,
                                                clearable=False,
                                            ),
                                        ],
                                        md=6,
                                    ),

                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Variable Y"
                                            ),

                                            dcc.Dropdown(
                                                id="ekde-association-y",
                                                options=[
                                                    {
                                                        "label": column,
                                                        "value": column,
                                                    }
                                                    for column
                                                    in numeric_like
                                                ],
                                                value=default_y,
                                                clearable=False,
                                            ),
                                        ],
                                        md=6,
                                    ),
                                ],
                                className="g-3",
                            ),

                            dbc.Button(
                                "Analyser l'association",
                                id="ekde-association-run",
                                color="primary",
                                className="mt-3",
                            ),

                            html.Div(
                                initial_association,
                                id="ekde-association-results",
                                className="mt-4",
                            ),

                            dcc.Graph(
                                id="ekde-association-graph",
                                figure=initial_association_figure,
                            ),
                        ],
                        label="Associations",
                    ),

                    # ==========================================
                    # FEATURE SELECTION
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "🎯 Sélection de variables",
                                className="mt-4",
                            ),

                            dbc.Label(
                                "Méthode"
                            ),

                            dcc.Dropdown(
                                id="ekde-selection-method",
                                options=[
                                    {
                                        "label": "Variance",
                                        "value": "variance",
                                    },
                                    {
                                        "label": (
                                            "Corrélation avec une cible"
                                        ),
                                        "value": "correlation",
                                    },
                                    {
                                        "label": (
                                            "Information mutuelle "
                                            "— classification"
                                        ),
                                        "value": "mi_classification",
                                    },
                                    {
                                        "label": (
                                            "Information mutuelle "
                                            "— régression"
                                        ),
                                        "value": "mi_regression",
                                    },
                                ],
                                value="variance",
                                clearable=False,
                            ),

                            dbc.Label(
                                "Variable cible",
                                className="mt-3",
                            ),

                            dcc.Dropdown(
                                id="ekde-target",
                                options=[
                                    {
                                        "label": column,
                                        "value": column,
                                    }
                                    for column in df.columns
                                ],
                                value=None,
                                placeholder=(
                                    "Facultative pour la méthode variance"
                                ),
                            ),

                            dbc.Label(
                                "Seuil de variance",
                                className="mt-3",
                            ),

                            dcc.Input(
                                id="ekde-variance-threshold",
                                type="number",
                                value=0.0,
                                min=0.0,
                                step=0.01,
                                className="form-control",
                            ),

                            dbc.Button(
                                "Analyser les variables",
                                id="ekde-selection-run",
                                color="primary",
                                className="mt-3",
                            ),

                            html.Div(
                                id="ekde-selection-results",
                                className="mt-4",
                            ),
                        ],
                        label="Sélection",
                    ),

                    # ==========================================
                    # KNOWLEDGE SUMMARY
                    # ==========================================

                    dbc.Tab(
                        [
                            html.H4(
                                "Synthèse des connaissances",
                                className="mt-4",
                            ),

                            dbc.Alert(
                                (
                                    "La synthèse n'est pas calculée "
                                    "automatiquement afin de préserver "
                                    "la réactivité de l'application."
                                ),
                                color="secondary",
                            ),

                            dbc.Button(
                                "Générer la synthèse",
                                id="ekde-knowledge-run",
                                color="primary",
                                className="mb-3",
                            ),

                            html.Div(
                                initial_knowledge,
                                id="ekde-knowledge-summary",
                            ),
                        ],
                        label="Synthèse",
                    ),
                ]
            ),

            html.Hr(),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "← ELAE",
                                color="secondary",
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/elae"
                            ),
                        ),
                        md=4,
                    ),

                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "Prétraitement",
                                color="primary",
                                outline=True,
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/eidpp"
                            ),
                        ),
                        md=4,
                    ),

                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "Ouvrir EAIE",
                                color="success",
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/eaie"
                            ),
                        ),
                        md=4,
                    ),
                ],
                className="g-3 mt-3",
            ),

            dcc.Store(
                id="ekde-project-id",
                data=project_id,
            ),

            dcc.Store(
                id="ekde-dataset-id",
                data=dataset_id,
            ),

dcc.Download(
                id="ekde-download-data"
            ),
        ],
        fluid=True,
    )
