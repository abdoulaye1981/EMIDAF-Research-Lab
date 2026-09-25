from dash import dcc
from dash import html
from dash import Input
from dash import Output
from dash import callback

import re
from flask import session
import dash_bootstrap_components as dbc

from emidaf_studio.layouts.home import layout as home_layout


# ==========================================================
# Zone de contenu pilotée par l'URL
# ==========================================================

content = html.Div(
    id="page-content"
)


# ==========================================================
# Gestion du routage
# ==========================================================


# ==========================================================
# Page d'entrée moderne des modules
# ==========================================================

def _module_home(
    title,
    description,
    objective,
    approach,
    result,
    instruction,
    icon,
):
    """
    Construit une page d'entrée moderne et homogène
    pour les modules EMIDAF.
    """

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
                                        "EMIDAF",
                                        className=(
                                            "module-home-v2-kicker"
                                        ),
                                    ),

                                    html.Span(
                                        "ENVIRONNEMENT SCIENTIFIQUE",
                                        className=(
                                            "module-home-v2-eyebrow"
                                        ),
                                    ),
                                ],
                                className=(
                                    "d-flex align-items-center "
                                    "gap-2 mb-3"
                                ),
                            ),

                            html.H1(
                                title,
                                className="module-home-v2-title",
                            ),

                            html.P(
                                description,
                                className=(
                                    "module-home-v2-subtitle"
                                ),
                            ),
                        ],
                    ),

                    html.Div(
                        html.I(
                            className=(
                                f"bi {icon} "
                                "module-home-v2-hero-icon"
                            ),
                        ),
                        className=(
                            "module-home-v2-hero-icon-box"
                        ),
                    ),
                ],
                className="module-home-v2-hero",
            ),

            # ==================================================
            # POSITION DANS LE CYCLE
            # ==================================================

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                html.I(
                                    className=(
                                        f"bi {icon} "
                                        "module-home-v2-context-icon"
                                    )
                                ),
                                className=(
                                    "module-home-v2-context-icon-box"
                                ),
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "MODULE ANALYTIQUE",
                                        className=(
                                            "module-home-v2-context-label"
                                        ),
                                    ),

                                    html.Div(
                                        title,
                                        className=(
                                            "module-home-v2-context-title"
                                        ),
                                    ),
                                ]
                            ),

                            html.Div(
                                [
                                    html.I(
                                        className=(
                                            "bi bi-diagram-3 me-2"
                                        )
                                    ),
                                    "Cycle EMIDAF",
                                ],
                                className=(
                                    "module-home-v2-context-badge"
                                ),
                            ),
                        ],
                        className=(
                            "module-home-v2-context-card"
                        ),
                    )
                ],
                className=(
                    "module-home-v2-context-section"
                ),
            ),

            # ==================================================
            # PRÉSENTATION
            # ==================================================

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                "CADRE SCIENTIFIQUE",
                                className=(
                                    "module-home-v2-section-kicker"
                                ),
                            ),

                            html.H2(
                                "Rôle du module",
                                className=(
                                    "module-home-v2-section-title"
                                ),
                            ),

                            html.P(
                                (
                                    "Ce module s'inscrit dans le "
                                    "cycle analytique intégré "
                                    "d'EMIDAF."
                                ),
                                className=(
                                    "module-home-v2-section-subtitle"
                                ),
                            ),
                        ],
                        className=(
                            "module-home-v2-section-heading"
                        ),
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "01",
                                        className=(
                                            "module-home-v2-card-number"
                                        ),
                                    ),

                                    html.I(
                                        className=(
                                            "bi bi-bullseye "
                                            "module-home-v2-card-icon"
                                        )
                                    ),

                                    html.H3(
                                        "Objectif",
                                        className=(
                                            "module-home-v2-card-title"
                                        ),
                                    ),

                                    html.P(
                                        objective,
                                        className=(
                                            "module-home-v2-card-text"
                                        ),
                                    ),
                                ],
                                className=(
                                    "module-home-v2-card"
                                ),
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "02",
                                        className=(
                                            "module-home-v2-card-number"
                                        ),
                                    ),

                                    html.I(
                                        className=(
                                            "bi bi-list-check "
                                            "module-home-v2-card-icon"
                                        )
                                    ),

                                    html.H3(
                                        "Approche",
                                        className=(
                                            "module-home-v2-card-title"
                                        ),
                                    ),

                                    html.P(
                                        approach,
                                        className=(
                                            "module-home-v2-card-text"
                                        ),
                                    ),
                                ],
                                className=(
                                    "module-home-v2-card"
                                ),
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "03",
                                        className=(
                                            "module-home-v2-card-number"
                                        ),
                                    ),

                                    html.I(
                                        className=(
                                            "bi bi-check2-circle "
                                            "module-home-v2-card-icon"
                                        )
                                    ),

                                    html.H3(
                                        "Résultat attendu",
                                        className=(
                                            "module-home-v2-card-title"
                                        ),
                                    ),

                                    html.P(
                                        result,
                                        className=(
                                            "module-home-v2-card-text"
                                        ),
                                    ),
                                ],
                                className=(
                                    "module-home-v2-card"
                                ),
                            ),
                        ],
                        className=(
                            "module-home-v2-cards"
                        ),
                    ),
                ],
                className="module-home-v2-section",
            ),

            # ==================================================
            # DÉMARRAGE
            # ==================================================

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "DÉMARRER",
                                        className=(
                                            "module-home-v2-section-kicker"
                                        ),
                                    ),

                                    html.H2(
                                        "Accéder au module",
                                        className=(
                                            "module-home-v2-section-title"
                                        ),
                                    ),

                                    html.P(
                                        instruction,
                                        className=(
                                            "module-home-v2-section-subtitle"
                                        ),
                                    ),
                                ]
                            ),

                            dcc.Link(
                                [
                                    html.I(
                                        className=(
                                            "bi bi-folder2-open me-2"
                                        )
                                    ),
                                    "Ouvrir mes projets",
                                ],
                                href="/projects",
                                className=(
                                    "module-home-v2-primary-link"
                                ),
                            ),
                        ],
                        className=(
                            "module-home-v2-start-card"
                        ),
                    ),
                ],
                className="module-home-v2-start-section",
            ),
        ],
        fluid=True,
        className="module-home-v2-page",
    )



def _auth_bootstrap():
    from emidaf_core.bootstrap.bootstrap import Bootstrap

    bootstrap = Bootstrap()
    bootstrap.initialize()

    return bootstrap


def _current_user():
    user_id = session.get("user_id")

    if user_id is None:
        return None

    try:
        bootstrap = _auth_bootstrap()
        return bootstrap.auth_service.get_current_user(
            user_id
        )
    except Exception:
        return None


def _redirect(href):
    return dcc.Location(
        href=href,
        id=f"auth-redirect-{href.replace('/', '-')}",
        refresh=True,
    )


def get_page_layout(pathname):
    pathname = pathname or "/"

    print(
        "[EMIDAF ROUTER] PATH:",
        pathname,
        flush=True,
    )

    # ======================================================
    # AUTHENTIFICATION
    # ======================================================

    user = _current_user()

    if pathname == "/login":
        if user is not None:
            destination = (
                "/admin"
                if user.role in {
                    "admin",
                    "super_admin",
                }
                else "/dashboard"
            )
            return _redirect(destination)

        from emidaf_studio.pages.auth.layout import (
            login_layout,
        )

        return login_layout()

    if pathname == "/register":
        if user is not None:
            return _redirect("/dashboard")

        from emidaf_studio.pages.auth.layout import (
            register_layout,
        )

        return register_layout()

    if pathname == "/":
        return home_layout

    # Toutes les routes ci-dessous nécessitent
    # une session utilisateur valide.
    if user is None:
        return _redirect("/login")

    # ======================================================
    # CONTRÔLE DE PROPRIÉTÉ DES PROJETS
    # ======================================================

    project_match = re.match(
        r"^/projects/(\d+)(?:/|$)",
        pathname,
    )

    if project_match:
        project_id = int(
            project_match.group(1)
        )

        bootstrap = _auth_bootstrap()

        owns_project = (
            bootstrap.project_controller
            .exists_for_user(
                project_id,
                int(user.id),
            )
        )

        if not owns_project:
            return dbc.Container(
                dbc.Alert(
                    [
                        html.H4(
                            "Accès non autorisé",
                            className="alert-heading",
                        ),
                        html.P(
                            (
                                "Ce projet n'appartient pas "
                                "à votre espace personnel "
                                "EMIDAF."
                            )
                        ),
                    ],
                    color="danger",
                ),
                fluid=True,
                className="py-4",
            )

        # ==================================================
        # CONTRÔLE D'APPARTENANCE DU DATASET AU PROJET
        # ==================================================

        dataset_match = re.match(
            (
                r"^/projects/(\d+)/datasets/"
                r"(\d+)(?:/|$)"
            ),
            pathname,
        )

        if dataset_match:

            dataset_id = int(
                dataset_match.group(2)
            )

            dataset = (
                bootstrap.dataset_controller
                .get(dataset_id)
            )

            if (
                dataset is None
                or int(dataset.project_id)
                != project_id
            ):
                return dbc.Container(
                    dbc.Alert(
                        [
                            html.H4(
                                "Dataset introuvable",
                                className=(
                                    "alert-heading"
                                ),
                            ),
                            html.P(
                                (
                                    "Ce jeu de données "
                                    "n'existe pas dans le "
                                    "projet demandé ou n'est "
                                    "pas accessible."
                                )
                            ),
                        ],
                        color="danger",
                    ),
                    fluid=True,
                    className="py-4",
                )

    if pathname == "/account":
        from emidaf_studio.pages.account.layout import (
            account_layout,
        )

        return account_layout(user)

    if pathname == "/dashboard":
        from emidaf_studio.pages.dashboard.layout import (
            dashboard_layout,
        )

        return dashboard_layout(user)

    if pathname == "/admin":
        if user.role not in {
            "admin",
            "super_admin",
        }:
            return dbc.Alert(
                "Accès administrateur non autorisé.",
                color="danger",
                className="m-4",
            )

        bootstrap = _auth_bootstrap()

        from emidaf_studio.pages.admin.layout import (
            admin_layout,
        )

        users = (
            bootstrap.user_service
            .get_all()
        )

        project_counts = {
            item.id: (
                bootstrap.project_controller
                .count_for_user(
                    int(item.id)
                )
            )
            for item in users
        }

        return admin_layout(
            user,
            users,
            project_counts,
        )


    # ======================================================
    # Liste des projets
    # ======================================================

    if pathname == "/projects":
        from emidaf_studio.pages.projects.layout import (
            user_projects_layout,
        )

        return user_projects_layout(
            int(user.id)
        )

    # ======================================================
    # EAIE - Page d'entrée
    # ======================================================

    # ======================================================
    # Pages d'entrée génériques des modules EMIDAF
    # ======================================================

    module_entries = {
        "/import": {
            "title": "Importation des données",
            "description": (
                "Ajoutez un jeu de données à un projet afin "
                "de l'intégrer au processus analytique EMIDAF."
            ),
            "objective": (
                "Associer des sources de données aux projets "
                "de recherche et d'analyse."
            ),
            "approach": (
                "Importation contrôlée, rattachement au projet "
                "et préparation à l'inspection."
            ),
            "result": (
                "Un jeu de données disponible dans l'espace "
                "de travail du projet."
            ),
            "instruction": (
                "Ouvrez un projet puis utilisez l'action "
                "d'importation."
            ),
            "icon": "bi-cloud-arrow-up",
        },

        "/inspection": {
            "title": "Inspection des données",
            "description": (
                "Examinez la structure, les types, la qualité "
                "et les principaux indicateurs du jeu de données."
            ),
            "objective": (
                "Comprendre l'état initial des données avant "
                "toute transformation ou modélisation."
            ),
            "approach": (
                "Profilage, qualité, valeurs manquantes, "
                "distributions et diagnostics statistiques."
            ),
            "result": (
                "Un diagnostic structuré mettant en évidence "
                "les caractéristiques et limites des données."
            ),
            "instruction": (
                "Ouvrez un projet puis sélectionnez le jeu "
                "de données à inspecter."
            ),
            "icon": "bi-search",
        },

        "/eidpp": {
            "title": "Prétraitement des données : EIDPP",
            "description": (
                "Préparez et transformez les données avant "
                "les analyses statistiques et prédictives."
            ),
            "objective": (
                "Améliorer la qualité et l'exploitabilité "
                "des données tout en conservant la traçabilité."
            ),
            "approach": (
                "Traitement des valeurs manquantes, doublons, "
                "types, transformations et préparation."
            ),
            "result": (
                "Un jeu de données préparé et documenté pour "
                "les étapes analytiques suivantes."
            ),
            "instruction": (
                "Ouvrez un projet, sélectionnez un jeu de données "
                "puis ouvrez EIDPP."
            ),
            "icon": "bi-sliders",
        },

        "/elae": {
            "title": "Analyse exploratoire des données : ELAE",
            "description": (
                "Explorez les distributions, relations et "
                "caractéristiques essentielles du jeu de données."
            ),
            "objective": (
                "Comprendre les données avant la modélisation "
                "et l'interprétation."
            ),
            "approach": (
                "Statistiques descriptives, distributions, "
                "relations entre variables et visualisations."
            ),
            "result": (
                "Une compréhension structurée des tendances "
                "et relations présentes dans les données."
            ),
            "instruction": (
                "Ouvrez un projet, sélectionnez un jeu de données "
                "puis accédez à ELAE."
            ),
            "icon": "bi-bar-chart-line",
        },

        "/etae": {
            "title": "Analyse textuelle : ETAE",
            "description": (
                "Analysez les corpus textuels et mettez en évidence "
                "leurs structures lexicales et sémantiques."
            ),
            "objective": (
                "Extraire et interpréter des informations à partir "
                "des variables textuelles du jeu de données."
            ),
            "approach": (
                "Profil de corpus, fréquences lexicales, n-grams, "
                "TF-IDF, sentiment, thèmes, clustering textuel "
                "et associations texte/données."
            ),
            "result": (
                "Une analyse textuelle structurée, documentée "
                "et reliée aux variables quantitatives ou "
                "catégorielles disponibles."
            ),
            "instruction": (
                "Ouvrez un projet, sélectionnez un jeu de données "
                "contenant au moins une variable textuelle puis "
                "accédez à ETAE."
            ),
            "icon": "bi-chat-square-text",
        },

        "/ekde": {
            "title": "Découverte de connaissances : EKDE",
            "description": (
                "Identifiez les structures, groupes et relations "
                "latentes présentes dans les données."
            ),
            "objective": (
                "Extraire des connaissances à partir des "
                "structures observées."
            ),
            "approach": (
                "Réduction dimensionnelle, clustering, "
                "segmentation et structures latentes."
            ),
            "result": (
                "Des structures et connaissances exploitables "
                "pour l'analyse."
            ),
            "instruction": (
                "Ouvrez un projet, sélectionnez un jeu de données "
                "puis accédez à EKDE."
            ),
            "icon": "bi-diagram-3",
        },

        "/eaie": {
            "title": "Modélisation prédictive : EAIE",
            "description": (
                "Construisez, validez et comparez des modèles "
                "supervisés."
            ),
            "objective": (
                "Développer un modèle prédictif adapté à la "
                "variable cible."
            ),
            "approach": (
                "Partitionnement, validation croisée, comparaison "
                "et sélection des modèles."
            ),
            "result": (
                "Un modèle sélectionné avec ses performances "
                "de validation et de test."
            ),
            "instruction": (
                "Ouvrez un projet, sélectionnez un jeu de données "
                "puis accédez à EAIE."
            ),
            "icon": "bi-graph-up-arrow",
        },

        "/exaie": {
            "title": "Explicabilité des modèles : EXAIE",
            "description": (
                "Interprétez les contributions des variables "
                "aux prédictions du modèle."
            ),
            "objective": (
                "Rendre le comportement du modèle plus "
                "compréhensible et documenté."
            ),
            "approach": (
                "Explications globales et locales, importance "
                "et contributions des variables."
            ),
            "result": (
                "Une interprétation structurée du modèle "
                "sans inférence causale."
            ),
            "instruction": (
                "Sélectionnez d'abord un modèle dans EAIE "
                "puis accédez à EXAIE."
            ),
            "icon": "bi-lightbulb",
        },

        "/edse": {
            "title": "Aide à la décision : EDSE",
            "description": (
                "Explorez des scénarios et indicateurs pour "
                "soutenir la décision humaine."
            ),
            "objective": (
                "Transformer les résultats analytiques en éléments "
                "d'aide à la décision."
            ),
            "approach": (
                "Scénarios, comparaison d'alternatives, "
                "indicateurs et synthèse."
            ),
            "result": (
                "Des éléments d'aide à la décision documentés, "
                "sans automatiser la décision humaine."
            ),
            "instruction": (
                "Ouvrez un projet et sélectionnez un jeu de données "
                "ayant parcouru les étapes analytiques."
            ),
            "icon": "bi-signpost-split",
        },

        "/reports": {
            "title": "Rapports analytiques",
            "description": (
                "Regroupez les résultats produits par les modules "
                "dans une restitution structurée."
            ),
            "objective": (
                "Documenter le processus analytique et faciliter "
                "la communication des résultats."
            ),
            "approach": (
                "Sélection des sections, synthèse, interprétation "
                "et restitution."
            ),
            "result": (
                "Un rapport analytique structuré et traçable."
            ),
            "instruction": (
                "Ouvrez un projet, sélectionnez un jeu de données "
                "puis accédez aux rapports."
            ),
            "icon": "bi-file-earmark-bar-graph",
        },
    }

    if pathname in module_entries:
        entry = module_entries[pathname]

        return _module_home(
            title=entry["title"],
            description=entry["description"],
            objective=entry["objective"],
            approach=entry["approach"],
            result=entry["result"],
            instruction=entry["instruction"],
            icon=entry["icon"],
        )


    if pathname == "/eaie":

        return html.Div(
            [
                html.H2(
                    "EAIE — Exploratory Artificial "
                    "Intelligence Engine"
                ),

                html.P(
                    (
                        "EAIE réalise la modélisation supervisée, "
                        "la validation croisée et la comparaison "
                        "des modèles de Machine Learning."
                    )
                ),

                html.Div(
                    [
                        html.Strong(
                            "Pour démarrer : "
                        ),
                        (
                            "ouvrez un projet, sélectionnez un "
                            "dataset, puis accédez à EAIE depuis "
                            "EKDE."
                        ),
                    ],
                    className="alert alert-info",
                ),

                dcc.Link(
                    "Ouvrir les projets",
                    href="/projects",
                    className="btn btn-primary",
                ),
            ],
            className="p-4",
        )

    # ======================================================
    # Importation d'un dataset
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)/import",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))

        import importlib

        import_page = importlib.import_module(
            "emidaf_studio.pages.import.layout"
        )

        return import_page.import_layout(project_id)

    # ======================================================
    # EAIE - Artificial Intelligence Engine
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)/datasets/(\d+)/eaie",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))
        dataset_id = int(match.group(2))

        from emidaf_studio.pages.eaie.layout import (
            eaie_layout
        )

        return eaie_layout(
            project_id,
            dataset_id
        )

    # ======================================================
    # EKDE - Knowledge Discovery
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)/datasets/(\d+)/ekde",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))
        dataset_id = int(match.group(2))

        from emidaf_studio.pages.ekde.layout import (
            ekde_layout
        )

        return ekde_layout(
            project_id,
            dataset_id
        )

    # ======================================================
    # ELAE - Analyse exploratoire
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)/datasets/(\d+)/elae",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))
        dataset_id = int(match.group(2))

        from emidaf_studio.pages.elae.layout import (
            elae_layout
        )

        return elae_layout(
            project_id,
            dataset_id
        )

    # ======================================================
    # EIDPP - Prétraitement d'un dataset
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)/datasets/(\d+)/eidpp",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))
        dataset_id = int(match.group(2))

        from emidaf_studio.pages.eidpp.layout import (
            eidpp_layout
        )

        return eidpp_layout(
            project_id,
            dataset_id
        )

    # ======================================================
    # ETAE - Text Analysis Engine
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)/datasets/(\d+)/etae",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))
        dataset_id = int(match.group(2))

        from emidaf_studio.pages.etae.layout import (
            build_etae_layout
        )

        return build_etae_layout(
            project_id=project_id,
            dataset_id=dataset_id,
        )

    # ======================================================
    # EXAIE - Explicabilité des modèles
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)/datasets/(\d+)/exaie",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))
        dataset_id = int(match.group(2))

        from emidaf_studio.pages.exaie.layout import (
            exaie_layout
        )

        return exaie_layout(
            project_id,
            dataset_id
        )

    # ======================================================
    # EDSE - Aide à la décision
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)/datasets/(\d+)/edse",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))
        dataset_id = int(match.group(2))

        from emidaf_studio.pages.edse.layout import (
            edse_layout
        )

        return edse_layout(
            project_id,
            dataset_id
        )

    # ======================================================
    # Rapports analytiques
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)/datasets/(\d+)/reports",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))
        dataset_id = int(match.group(2))

        from emidaf_studio.pages.reports.layout import (
            reports_layout
        )

        return reports_layout(
            project_id,
            dataset_id
        )


    # ======================================================
    # Inspection d'un dataset
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)/datasets/(\d+)",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))
        dataset_id = int(match.group(2))

        from emidaf_studio.pages.inspection.layout import (
            inspection_layout
        )

        return inspection_layout(
            project_id,
            dataset_id
        )

    # ======================================================
    # Page détaillée d'un projet
    # ======================================================

    match = re.fullmatch(
        r"/projects/(\d+)",
        pathname or ""
    )

    if match:

        project_id = int(match.group(1))

        from emidaf_studio.pages.projects.layout import (
            project_detail_layout
        )

        return project_detail_layout(project_id)

    # ======================================================
    # Page inconnue
    # ======================================================

    return html.Div(
        [
            html.H2(
                "Page en préparation"
            ),

            html.P(
                f"La page « {pathname} » "
                "sera prochainement disponible."
            )
        ],
        className="p-4"
    )


# ==========================================================
# Callback du routeur
# ==========================================================

@callback(
    Output(
        "page-content",
        "children"
    ),
    Input(
        "url",
        "pathname"
    )
)
def display_page(pathname):

    return get_page_layout(pathname)


# ==========================================================
# Layout du routeur
# ==========================================================

layout = html.Div(
    [
        dcc.Location(
            id="url",
            refresh=False
        ),

        content
    ]
)
