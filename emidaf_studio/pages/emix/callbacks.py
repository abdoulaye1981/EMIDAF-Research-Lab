"""
=========================================================
EMIDAF Framework v1.0
EMIX Studio - Callbacks
=========================================================
"""

from __future__ import annotations

import hashlib
import re
import unicodedata

import numpy as np

from dash import (
    Input,
    Output,
    State,
    callback,
    html,
)
import dash_bootstrap_components as dbc
from dash import dcc
from dash import MATCH, ctx

from dash.exceptions import PreventUpdate

from emidaf_core.emix import EMIXEngine

from .components import (
    emix_intro_component,
    emix_source_card,
)


# ==========================================================
# Configuration des sources EMIX v1
# ==========================================================

_SOURCE_CONFIG = {
    "elae": {
        "label": "Analyse exploratoire",
        "family": "Quantitative / exploratoire",
    },
    "eaie": {
        "label": "Modélisation prédictive",
        "family": "Quantitative / modélisation",
    },
    "etae": {
        "label": "Analyse textuelle",
        "family": "Textuelle computationnelle",
    },
    "eqae": {
        "label": "Analyse qualitative",
        "family": "Qualitative",
    },
    "ekde": {
        "label": "Découverte de connaissances",
        "family": "Quantitative / non supervisée",
    },
    "edse": {
        "label": "Aide à la décision",
        "family": "Décision",
    },
}


_TAB_CONTENT = {
    "emix-tab-candidates": (
        "Candidats d'intégration",
        (
            "Examinez les rapprochements potentiels "
            "entre résultats provenant de sources "
            "analytiques distinctes."
        ),
        (
            "Un candidat constitue une suggestion "
            "à examiner, et non une conclusion."
        ),
    ),

    "emix-tab-integration": (
        "Intégration",
        (
            "Qualifiez les relations retenues comme "
            "convergence, complémentarité, divergence "
            "ou relation indéterminée."
        ),
        (
            "La qualification de la relation relève "
            "du chercheur."
        ),
    ),

    "emix-tab-joint-display": (
        "Joint Display",
        (
            "Mettez en regard les résultats "
            "quantitatifs et qualitatifs dans une "
            "structure commune d'interprétation."
        ),
        (
            "Le joint display facilite la lecture "
            "croisée sans fusionner artificiellement "
            "les résultats."
        ),
    ),

    "emix-tab-inferences": (
        "Méta-inférences",
        (
            "Documentez les interprétations intégrées "
            "issues des résultats retenus."
        ),
        (
            "Les méta-inférences doivent être "
            "explicitement validées par le chercheur."
        ),
    ),

    "emix-tab-summary": (
        "Synthèse des méthodes mixtes",
        (
            "Consultez la synthèse des sources, "
            "suggestions, relations, joint displays "
            "et méta-inférences."
        ),
        (
            "La synthèse distingue les suggestions "
            "des relations et conclusions validées."
        ),
    ),
}


# ==========================================================
# Persistance
# ==========================================================

def _load_available_sources(
    project_id,
    dataset_id,
):
    """
    Recharge tous les résultats analytiques persistés.
    """

    from emidaf_studio.services.model_registry import (
        get_all_analyses,
    )

    analyses = get_all_analyses(
        int(project_id),
        int(dataset_id),
    )

    return (
        analyses
        if isinstance(analyses, dict)
        else {}
    )


def _load_emix_sources(
    project_id,
    dataset_id,
):
    """
    Recharge la section EMIX -> sources.
    """

    from emidaf_studio.services.model_registry import (
        get_analysis,
    )

    result = get_analysis(
        int(project_id),
        int(dataset_id),
        "emix",
        default={},
    )

    if not isinstance(result, dict):
        return {}

    section = result.get(
        "sources",
        {},
    )

    return (
        section
        if isinstance(section, dict)
        else {}
    )


def _persist_emix_sources(
    project_id,
    dataset_id,
    payload,
):
    """
    Persiste atomiquement la section
    EMIX -> sources.
    """

    from emidaf_studio.services.model_registry import (
        merge_analysis_section,
    )

    return merge_analysis_section(
        int(project_id),
        int(dataset_id),
        "emix",
        "sources",
        payload,
    )


# ==========================================================
# Adaptation EMIX
# ==========================================================

def _adapt_source(
    stage,
    payload,
):
    """
    Transforme un résultat EMIDAF existant
    en MixedMethodSource.
    """

    engine = EMIXEngine()

    safe_payload = (
        payload
        if isinstance(payload, dict)
        else {}
    )

    return engine.adapt_source(
        engine=stage,
        payload=safe_payload,
        source_id=f"{stage}-source",
    )


def _selection_status(
    selected,
):
    """
    Composant visuel décrivant
    la sélection courante.
    """

    selected = (
        list(selected)
        if selected
        else []
    )

    if not selected:
        return dbc.Alert(
            "Aucune source sélectionnée.",
            color="light",
            className="mb-0",
        )

    labels = [
        _SOURCE_CONFIG[
            stage
        ]["label"]
        for stage in selected
        if stage in _SOURCE_CONFIG
    ]

    return dbc.Alert(
        (
            f"{len(selected)} source(s) "
            "sélectionnée(s) : "
            + ", ".join(labels)
        ),
        color="success",
        className="mb-0",
    )


# ==========================================================
# Sources
# ==========================================================

def _render_sources(
    project_id,
    dataset_id,
):
    """
    Rend l'onglet Sources à partir
    des analyses persistées.
    """

    if (
        project_id is None
        or dataset_id is None
    ):
        return dbc.Alert(
            "Contexte projet/dataset indisponible.",
            color="warning",
        )

    analyses = _load_available_sources(
        project_id,
        dataset_id,
    )

    persisted = _load_emix_sources(
        project_id,
        dataset_id,
    )

    persisted_selected = (
        persisted.get(
            "selected_stages",
            [],
        )
    )

    if not isinstance(
        persisted_selected,
        list,
    ):
        persisted_selected = []

    cards = []
    options = []

    available_stages = []
    available_count = 0

    for stage, config in _SOURCE_CONFIG.items():

        available = (
            stage in analyses
            and analyses.get(stage) is not None
        )

        result_type = None
        description = ""

        if available:

            available_count += 1
            available_stages.append(
                stage
            )

            try:
                source = _adapt_source(
                    stage,
                    analyses.get(stage),
                )

                result_type = (
                    source.result_type
                )

                description = (
                    source.description
                )

            except Exception as exc:
                description = (
                    "Résultat disponible, mais les "
                    "métadonnées EMIX n'ont pas pu "
                    "être construites : "
                    f"{exc}"
                )

            options.append(
                {
                    "label": (
                        f"{config['label']} "
                        f"({stage.upper()})"
                    ),
                    "value": stage,
                }
            )

        cards.append(
            dbc.Col(
                emix_source_card(
                    stage=stage,
                    label=config["label"],
                    family=config["family"],
                    available=available,
                    result_type=result_type,
                    description=description,
                ),
                md=6,
                xl=4,
                className="mb-3",
            )
        )

    # Nettoyage défensif :
    # une source ancienne devenue indisponible
    # n'est pas restaurée dans le sélecteur.
    selected = [
        stage
        for stage in persisted_selected
        if stage in available_stages
    ]

    if options:

        selector = dbc.Card(
            dbc.CardBody(
                [
                    html.H5(
                        "Sélection des sources",
                        className="mb-3",
                    ),

                    html.P(
                        (
                            "Cochez uniquement les "
                            "résultats que vous souhaitez "
                            "mobiliser dans l'intégration."
                        ),
                        className="text-muted",
                    ),

                    dbc.Checklist(
                        id="emix-source-selection",
                        options=options,
                        value=selected,
                        switch=True,
                    ),

                    dbc.Button(
                        "Enregistrer la sélection",
                        id="emix-save-source-selection",
                        color="primary",
                        className="mt-3",
                        n_clicks=0,
                    ),

                    html.Div(
                        _selection_status(
                            selected
                        ),
                        id="emix-source-selection-status",
                        className="mt-3",
                    ),
                ]
            ),
            className="shadow-sm mt-2",
        )

    else:

        selector = dbc.Alert(
            (
                "Aucune analyse compatible avec "
                "EMIX n'est actuellement disponible "
                "pour ce jeu de données."
            ),
            color="warning",
        )

    return html.Div(
        [
            html.Div(
                [
                    html.H4(
                        "Sources analytiques",
                        className="mb-2",
                    ),

                    html.P(
                        (
                            f"{available_count} source(s) "
                            "analytique(s) disponible(s) "
                            "pour l'intégration."
                        ),
                        className="text-muted",
                    ),

                    dbc.Alert(
                        (
                            "EMIX référence des résultats "
                            "déjà produits par les moteurs "
                            "EMIDAF. Il ne les recalcule pas."
                        ),
                        color="light",
                    ),
                ],
                className="mb-3",
            ),

            dbc.Row(
                cards,
                className="g-3",
            ),

            selector,

            dbc.Alert(
                [
                    html.Strong(
                        "EXAIE : "
                    ),
                    (
                        "l'explicabilité n'est pas traitée "
                        "comme une source EMIX autonome. "
                        "Elle reste rattachée au modèle "
                        "EAIE qu'elle explique."
                    ),
                ],
                color="info",
                className="mt-3 mb-0",
            ),
        ]
    )



# ==========================================================
# Éléments scientifiques pour candidats EMIX
# ==========================================================

_STOPWORDS = {
    "de",
    "du",
    "des",
    "la",
    "le",
    "les",
    "et",
    "en",
    "a",
    "au",
    "aux",
    "un",
    "une",
    "pour",
    "par",
    "sur",
    "dans",
    "avec",
    "sans",
}


def _normalize_tokens(
    value,
):
    text = str(
        value or ""
    ).lower()

    text = (
        unicodedata.normalize(
            "NFKD",
            text,
        )
        .encode(
            "ascii",
            "ignore",
        )
        .decode("ascii")
    )

    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text,
    )

    return {
        token
        for token in text.split()
        if (
            len(token) >= 4
            and token not in _STOPWORDS
        )
    }


def _clean_feature_name(
    feature_name,
):
    name = str(
        feature_name
    )

    if "__" in name:
        name = name.split(
            "__",
            1,
        )[1]

    return name


def _is_identifier_feature(
    feature_name,
):
    name = (
        _clean_feature_name(
            feature_name
        )
        .lower()
    )

    return (
        name.startswith("id_")
        or name == "id"
        or name.endswith("_id")
    )


def _categorical_columns(
    preprocessor,
):
    """
    Identifie les colonnes catégorielles originales
    du ColumnTransformer.
    """

    columns = set()

    transformers = getattr(
        preprocessor,
        "transformers_",
        [],
    )

    for name, transformer, cols in transformers:

        if name != "categorical":
            continue

        if isinstance(
            cols,
            (list, tuple),
        ):
            columns.update(
                str(col)
                for col in cols
            )

    return columns


def _is_encoded_category(
    feature_name,
    categorical_columns,
):
    """
    Détecte une modalité produite
    par l'encodage one-hot.
    """

    name = _clean_feature_name(
        feature_name
    )

    return any(
        name.startswith(
            f"{column}_"
        )
        for column
        in categorical_columns
    )


def _extract_eaie_elements(
    payload,
):
    if not isinstance(
        payload,
        dict,
    ):
        return []

    estimator = payload.get(
        "estimator"
    )

    if estimator is None:
        return []

    named_steps = getattr(
        estimator,
        "named_steps",
        {},
    )

    model = named_steps.get(
        "model"
    )

    preprocessor = named_steps.get(
        "preprocessor"
    )

    categorical_columns = (
        _categorical_columns(
            preprocessor
        )
        if preprocessor is not None
        else set()
    )

    if model is None:
        return []

    coefficients = getattr(
        model,
        "coef_",
        None,
    )

    if coefficients is None:
        return []

    coefficients = np.asarray(
        coefficients
    ).reshape(-1)

    feature_names = None

    if preprocessor is not None:
        getter = getattr(
            preprocessor,
            "get_feature_names_out",
            None,
        )

        if callable(getter):
            try:
                feature_names = list(
                    getter()
                )
            except Exception:
                feature_names = None

    if (
        feature_names is None
        or len(feature_names)
        != len(coefficients)
    ):
        raw_features = payload.get(
            "features",
            [],
        )

        if (
            isinstance(
                raw_features,
                list,
            )
            and len(raw_features)
            == len(coefficients)
        ):
            feature_names = list(
                raw_features
            )
        else:
            return []

    target = payload.get(
        "target",
        "variable cible",
    )

    elements = []

    for feature_name, coefficient in zip(
        feature_names,
        coefficients,
    ):
        clean_name = _clean_feature_name(
            feature_name
        )

        if _is_identifier_feature(
            clean_name
        ):
            continue

        if _is_encoded_category(
            clean_name,
            categorical_columns,
        ):
            continue

        value = float(
            coefficient
        )

        elements.append(
            {
                "feature": clean_name,
                "coefficient": value,
                "absolute_coefficient": abs(
                    value
                ),
                "element": (
                    f"{clean_name} — coefficient "
                    f"du modèle Ridge = {value:.4f} "
                    f"pour la cible {target}"
                ),
            }
        )

    elements.sort(
        key=lambda item: (
            item[
                "absolute_coefficient"
            ]
        ),
        reverse=True,
    )

    return elements


def _extract_eqae_elements(
    payload,
):
    if not isinstance(
        payload,
        dict,
    ):
        return []

    elements = []

    themes_section = payload.get(
        "themes",
        {},
    )

    themes = (
        themes_section.get(
            "themes",
            [],
        )
        if isinstance(
            themes_section,
            dict,
        )
        else []
    )

    for theme in themes:
        if not isinstance(
            theme,
            dict,
        ):
            continue

        name = str(
            theme.get(
                "name",
                "",
            )
        ).strip()

        if not name:
            continue

        description = str(
            theme.get(
                "description",
                "",
            )
        ).strip()

        elements.append(
            {
                "kind": "theme",
                "id": theme.get(
                    "theme_id"
                ),
                "name": name,
                "description": description,
                "element": (
                    f"Thème EQAE : {name}"
                    + (
                        f" — {description}"
                        if description
                        else ""
                    )
                ),
            }
        )

    codebook = payload.get(
        "codebook",
        {},
    )

    codes = (
        codebook.get(
            "codes",
            [],
        )
        if isinstance(
            codebook,
            dict,
        )
        else []
    )

    for code in codes:
        if not isinstance(
            code,
            dict,
        ):
            continue

        if code.get(
            "is_active",
            True,
        ) is False:
            continue

        name = str(
            code.get(
                "name",
                "",
            )
        ).strip()

        if not name:
            continue

        description = str(
            code.get(
                "description",
                "",
            )
        ).strip()

        elements.append(
            {
                "kind": "code",
                "id": code.get(
                    "code_id"
                ),
                "name": name,
                "description": description,
                "element": (
                    f"Code EQAE : {name}"
                    + (
                        f" — {description}"
                        if description
                        else ""
                    )
                ),
            }
        )

    return elements


def _candidate_id(
    left,
    right,
):
    raw = (
        f"{left}|{right}"
        .encode("utf-8")
    )

    digest = hashlib.sha256(
        raw
    ).hexdigest()[:16]

    return f"candidate-{digest}"


def _generate_eaie_eqae_candidates(
    eaie_payload,
    eqae_payload,
):
    eaie_elements = (
        _extract_eaie_elements(
            eaie_payload
        )
    )

    eqae_elements = (
        _extract_eqae_elements(
            eqae_payload
        )
    )

    candidates = []

    for quantitative in eaie_elements:

        feature = quantitative[
            "feature"
        ]

        feature_tokens = (
            _normalize_tokens(
                feature
            )
        )

        if not feature_tokens:
            continue

        for qualitative in eqae_elements:

            qualitative_text = " ".join(
                [
                    qualitative[
                        "name"
                    ],
                    qualitative.get(
                        "description",
                        "",
                    ),
                ]
            )

            qualitative_tokens = (
                _normalize_tokens(
                    qualitative_text
                )
            )

            overlap = sorted(
                feature_tokens
                & qualitative_tokens
            )

            if not overlap:
                continue

            candidate_id = _candidate_id(
                feature,
                (
                    qualitative.get("id")
                    or qualitative["name"]
                ),
            )

            candidates.append(
                {
                    "candidate_id": candidate_id,
                    "source_id_1": "eaie-source",
                    "source_id_2": "eqae-source",
                    "element_1": quantitative[
                        "element"
                    ],
                    "element_2": qualitative[
                        "element"
                    ],
                    "rationale": (
                        "Rapprochement lexical à examiner : "
                        + ", ".join(
                            overlap
                        )
                        + "."
                    ),
                    "status": "pending",
                    "metadata": {
                        "eaie_feature": feature,
                        "eaie_coefficient": (
                            quantitative[
                                "coefficient"
                            ]
                        ),
                        "eqae_kind": (
                            qualitative[
                                "kind"
                            ]
                        ),
                        "eqae_id": (
                            qualitative.get(
                                "id"
                            )
                        ),
                        "matched_tokens": overlap,
                    },
                }
            )

    candidates.sort(
        key=lambda item: abs(
            item[
                "metadata"
            ][
                "eaie_coefficient"
            ]
        ),
        reverse=True,
    )

    return candidates


# ==========================================================
# Persistance des candidats EMIX
# ==========================================================

def _load_emix_candidates(
    project_id,
    dataset_id,
):
    from emidaf_studio.services.model_registry import (
        get_analysis,
    )

    result = get_analysis(
        int(project_id),
        int(dataset_id),
        "emix",
        default={},
    )

    if not isinstance(
        result,
        dict,
    ):
        return {}

    section = result.get(
        "candidates",
        {},
    )

    return (
        section
        if isinstance(
            section,
            dict,
        )
        else {}
    )


def _persist_emix_candidates(
    project_id,
    dataset_id,
    payload,
):
    from emidaf_studio.services.model_registry import (
        merge_analysis_section,
    )

    return merge_analysis_section(
        int(project_id),
        int(dataset_id),
        "emix",
        "candidates",
        payload,
    )



def _update_candidate_status(
    project_id,
    dataset_id,
    candidate_id,
    status,
):
    """
    Met à jour le statut d'un candidat EMIX
    et le persiste dans le registre analytique.
    """

    if status not in {
        "pending",
        "accepted",
        "rejected",
    }:
        raise ValueError(
            f"Statut candidat invalide : {status}"
        )

    persisted = _load_emix_candidates(
        project_id,
        dataset_id,
    )

    items = persisted.get(
        "items",
        [],
    )

    if not isinstance(
        items,
        list,
    ):
        items = []

    updated = []
    found = False

    for item in items:

        if not isinstance(
            item,
            dict,
        ):
            continue

        current = dict(
            item
        )

        if (
            current.get(
                "candidate_id"
            )
            == candidate_id
        ):
            current[
                "status"
            ] = status

            found = True

        updated.append(
            current
        )

    if not found:
        raise ValueError(
            f"Candidat inconnu : {candidate_id}"
        )

    _persist_emix_candidates(
        project_id,
        dataset_id,
        {
            "generator": persisted.get(
                "generator",
                "eaie_eqae_lexical_v1",
            ),
            "items": updated,
        },
    )

    return updated




# ==========================================================
# Persistance de l'intégration EMIX
# ==========================================================

_VALID_RELATION_TYPES = {
    "convergence",
    "complementarity",
    "divergence",
    "undetermined",
}


def _load_emix_integration(
    project_id,
    dataset_id,
):
    from emidaf_studio.services.model_registry import (
        get_analysis,
    )

    result = get_analysis(
        int(project_id),
        int(dataset_id),
        "emix",
        default={},
    )

    if not isinstance(
        result,
        dict,
    ):
        return {}

    section = result.get(
        "integration",
        {},
    )

    return (
        section
        if isinstance(
            section,
            dict,
        )
        else {}
    )


def _persist_emix_integration(
    project_id,
    dataset_id,
    payload,
):
    from emidaf_studio.services.model_registry import (
        merge_analysis_section,
    )

    return merge_analysis_section(
        int(project_id),
        int(dataset_id),
        "emix",
        "integration",
        payload,
    )


def _integration_link_id(
    candidate_id,
):
    """
    Identifiant déterministe :
    un candidat accepté correspond à un lien
    d'intégration unique dans Studio v1.
    """

    return (
        f"link-{candidate_id}"
    )


def _create_or_update_integration_link(
    project_id,
    dataset_id,
    candidate_id,
    relation_type,
    researcher_note,
):
    """
    Convertit explicitement un candidat accepté
    en lien d'intégration.

    Le type de relation est toujours choisi
    par le chercheur.
    """

    if relation_type not in _VALID_RELATION_TYPES:
        raise ValueError(
            "Type de relation EMIX invalide : "
            f"{relation_type}"
        )

    candidates_section = (
        _load_emix_candidates(
            project_id,
            dataset_id,
        )
    )

    candidates = candidates_section.get(
        "items",
        [],
    )

    if not isinstance(
        candidates,
        list,
    ):
        candidates = []

    candidate = next(
        (
            item
            for item in candidates
            if (
                isinstance(item, dict)
                and item.get(
                    "candidate_id"
                )
                == candidate_id
            )
        ),
        None,
    )

    if candidate is None:
        raise ValueError(
            f"Candidat introuvable : "
            f"{candidate_id}"
        )

    if (
        candidate.get(
            "status"
        )
        != "accepted"
    ):
        raise ValueError(
            (
                "Seul un candidat accepté peut "
                "être intégré."
            )
        )

    link = {
        "link_id": (
            _integration_link_id(
                candidate_id
            )
        ),
        "source_id_1": candidate.get(
            "source_id_1"
        ),
        "source_id_2": candidate.get(
            "source_id_2"
        ),
        "element_1": candidate.get(
            "element_1"
        ),
        "element_2": candidate.get(
            "element_2"
        ),
        "relation_type": relation_type,
        "researcher_note": str(
            researcher_note or ""
        ).strip(),
        "candidate_id": candidate_id,
        "validated": True,
    }

    persisted = _load_emix_integration(
        project_id,
        dataset_id,
    )

    links = persisted.get(
        "links",
        [],
    )

    if not isinstance(
        links,
        list,
    ):
        links = []

    updated = []
    replaced = False

    for existing in links:

        if not isinstance(
            existing,
            dict,
        ):
            continue

        if (
            existing.get(
                "candidate_id"
            )
            == candidate_id
        ):
            updated.append(
                link
            )
            replaced = True

        else:
            updated.append(
                existing
            )

    if not replaced:
        updated.append(
            link
        )

    _persist_emix_integration(
        project_id,
        dataset_id,
        {
            "links": updated,
        },
    )

    return link


def _accepted_candidates(
    project_id,
    dataset_id,
):
    section = _load_emix_candidates(
        project_id,
        dataset_id,
    )

    items = section.get(
        "items",
        [],
    )

    if not isinstance(
        items,
        list,
    ):
        return []

    return [
        item
        for item in items
        if (
            isinstance(item, dict)
            and item.get(
                "status"
            )
            == "accepted"
        )
    ]


def _existing_link_for_candidate(
    project_id,
    dataset_id,
    candidate_id,
):
    section = _load_emix_integration(
        project_id,
        dataset_id,
    )

    links = section.get(
        "links",
        [],
    )

    if not isinstance(
        links,
        list,
    ):
        return None

    return next(
        (
            link
            for link in links
            if (
                isinstance(link, dict)
                and link.get(
                    "candidate_id"
                )
                == candidate_id
            )
        ),
        None,
    )





# ==========================================================
# Joint Display EMIX
# ==========================================================

def _load_emix_joint_display(
    project_id,
    dataset_id,
):
    from emidaf_studio.services.model_registry import (
        get_analysis,
    )

    result = get_analysis(
        int(project_id),
        int(dataset_id),
        "emix",
        default={},
    )

    if not isinstance(
        result,
        dict,
    ):
        return {}

    section = result.get(
        "joint_display",
        {},
    )

    return (
        section
        if isinstance(
            section,
            dict,
        )
        else {}
    )


def _persist_emix_joint_display(
    project_id,
    dataset_id,
    payload,
):
    from emidaf_studio.services.model_registry import (
        merge_analysis_section,
    )

    return merge_analysis_section(
        int(project_id),
        int(dataset_id),
        "emix",
        "joint_display",
        payload,
    )


def _validated_integration_links(
    project_id,
    dataset_id,
):
    section = _load_emix_integration(
        project_id,
        dataset_id,
    )

    links = section.get(
        "links",
        [],
    )

    if not isinstance(
        links,
        list,
    ):
        return []

    return [
        link
        for link in links
        if (
            isinstance(link, dict)
            and link.get(
                "validated"
            ) is True
        )
    ]


def _joint_display_row_id(
    link_id,
):
    return f"joint-row-{link_id}"


def _split_mixed_results(
    link,
):
    """
    Repère le résultat quantitatif et le résultat
    qualitatif à partir des sources du lien.

    Pour EMIX Studio v1, EAIE est quantitatif
    et EQAE qualitatif.
    """

    source_1 = link.get(
        "source_id_1"
    )

    source_2 = link.get(
        "source_id_2"
    )

    element_1 = link.get(
        "element_1",
        "",
    )

    element_2 = link.get(
        "element_2",
        "",
    )

    if (
        source_1 == "eaie-source"
        and source_2 == "eqae-source"
    ):
        return (
            element_1,
            element_2,
        )

    if (
        source_1 == "eqae-source"
        and source_2 == "eaie-source"
    ):
        return (
            element_2,
            element_1,
        )

    return (
        element_1,
        element_2,
    )


def _existing_joint_row_for_link(
    project_id,
    dataset_id,
    link_id,
):
    section = _load_emix_joint_display(
        project_id,
        dataset_id,
    )

    rows = section.get(
        "rows",
        [],
    )

    if not isinstance(
        rows,
        list,
    ):
        return None

    return next(
        (
            row
            for row in rows
            if (
                isinstance(row, dict)
                and row.get(
                    "source_link_id"
                )
                == link_id
            )
        ),
        None,
    )


def _create_or_update_joint_display_row(
    project_id,
    dataset_id,
    link_id,
    integrated_comment,
):
    """
    Crée ou met à jour une ligne de Joint Display.

    Le commentaire intégré est rédigé
    explicitement par le chercheur.
    """

    links = _validated_integration_links(
        project_id,
        dataset_id,
    )

    link = next(
        (
            item
            for item in links
            if item.get(
                "link_id"
            )
            == link_id
        ),
        None,
    )

    if link is None:
        raise ValueError(
            (
                "Lien d'intégration validé "
                f"introuvable : {link_id}"
            )
        )

    quantitative_result, qualitative_result = (
        _split_mixed_results(
            link
        )
    )

    row = {
        "row_id": (
            _joint_display_row_id(
                link_id
            )
        ),
        "quantitative_result": (
            quantitative_result
        ),
        "qualitative_result": (
            qualitative_result
        ),
        "relation_type": link.get(
            "relation_type",
            "undetermined",
        ),
        "integrated_comment": str(
            integrated_comment or ""
        ).strip(),
        "source_link_id": link_id,
    }

    persisted = _load_emix_joint_display(
        project_id,
        dataset_id,
    )

    rows = persisted.get(
        "rows",
        [],
    )

    if not isinstance(
        rows,
        list,
    ):
        rows = []

    updated = []
    replaced = False

    for existing in rows:

        if not isinstance(
            existing,
            dict,
        ):
            continue

        if (
            existing.get(
                "source_link_id"
            )
            == link_id
        ):
            updated.append(
                row
            )
            replaced = True

        else:
            updated.append(
                existing
            )

    if not replaced:
        updated.append(
            row
        )

    _persist_emix_joint_display(
        project_id,
        dataset_id,
        {
            "rows": updated,
        },
    )

    return row





# ==========================================================
# Méta-inférences EMIX
# ==========================================================

def _load_emix_meta_inferences(
    project_id,
    dataset_id,
):
    from emidaf_studio.services.model_registry import (
        get_analysis,
    )

    result = get_analysis(
        int(project_id),
        int(dataset_id),
        "emix",
        default={},
    )

    if not isinstance(
        result,
        dict,
    ):
        return {}

    section = result.get(
        "meta_inferences",
        {},
    )

    return (
        section
        if isinstance(
            section,
            dict,
        )
        else {}
    )


def _persist_emix_meta_inferences(
    project_id,
    dataset_id,
    payload,
):
    from emidaf_studio.services.model_registry import (
        merge_analysis_section,
    )

    return merge_analysis_section(
        int(project_id),
        int(dataset_id),
        "emix",
        "meta_inferences",
        payload,
    )


def _available_meta_links(
    project_id,
    dataset_id,
):
    """
    Les méta-inférences sont construites
    uniquement à partir de liens déjà présents
    dans le Joint Display.
    """

    section = _load_emix_joint_display(
        project_id,
        dataset_id,
    )

    rows = section.get(
        "rows",
        [],
    )

    if not isinstance(
        rows,
        list,
    ):
        return []

    links = []

    seen = set()

    for row in rows:

        if not isinstance(
            row,
            dict,
        ):
            continue

        link_id = row.get(
            "source_link_id"
        )

        if not link_id:
            continue

        if link_id in seen:
            continue

        seen.add(
            link_id
        )

        links.append(
            {
                "link_id": link_id,
                "quantitative_result": row.get(
                    "quantitative_result",
                    "",
                ),
                "qualitative_result": row.get(
                    "qualitative_result",
                    "",
                ),
                "relation_type": row.get(
                    "relation_type",
                    "undetermined",
                ),
                "integrated_comment": row.get(
                    "integrated_comment",
                    "",
                ),
            }
        )

    return links


def _meta_inference_id(
    statement,
    link_ids,
):
    """
    Identifiant déterministe.

    Une même formulation associée aux mêmes liens
    met à jour la même méta-inférence au lieu
    de créer un doublon.
    """

    normalized_links = "|".join(
        sorted(
            str(link_id)
            for link_id in link_ids
        )
    )

    raw = (
        f"{statement.strip()}|{normalized_links}"
        .encode("utf-8")
    )

    digest = hashlib.sha256(
        raw
    ).hexdigest()[:16]

    return f"meta-{digest}"


def _parse_limitations(
    value,
):
    """
    Une limitation par ligne.
    """

    if value is None:
        return []

    limitations = []

    for line in str(
        value
    ).splitlines():

        cleaned = line.strip()

        if cleaned.startswith("-"):
            cleaned = cleaned[1:].strip()

        if cleaned:
            limitations.append(
                cleaned
            )

    return limitations


def _save_meta_inference(
    project_id,
    dataset_id,
    statement,
    link_ids,
    limitations,
    researcher_note,
    validated,
):
    """
    Persiste une méta-inférence rédigée
    et, éventuellement, validée explicitement
    par le chercheur.
    """

    statement = str(
        statement or ""
    ).strip()

    if not statement:
        raise ValueError(
            "La méta-inférence doit être rédigée."
        )

    if not isinstance(
        link_ids,
        list,
    ):
        link_ids = []

    link_ids = [
        str(link_id)
        for link_id in link_ids
        if link_id
    ]

    if not link_ids:
        raise ValueError(
            (
                "Sélectionnez au moins un lien "
                "du Joint Display."
            )
        )

    available = {
        item["link_id"]
        for item in _available_meta_links(
            project_id,
            dataset_id,
        )
    }

    invalid_links = [
        link_id
        for link_id in link_ids
        if link_id not in available
    ]

    if invalid_links:
        raise ValueError(
            (
                "Certains liens ne sont pas "
                "disponibles dans le Joint Display."
            )
        )

    limitations = [
        str(item).strip()
        for item in limitations
        if str(item).strip()
    ]

    validated = bool(
        validated
    )

    if (
        validated
        and not limitations
    ):
        raise ValueError(
            (
                "Une méta-inférence validée doit "
                "mentionner au moins une limitation."
            )
        )

    inference_id = _meta_inference_id(
        statement,
        link_ids,
    )

    inference = {
        "inference_id": inference_id,
        "statement": statement,
        "link_ids": list(
            link_ids
        ),
        "limitations": list(
            limitations
        ),
        "researcher_note": str(
            researcher_note or ""
        ).strip(),
        "validated": validated,
    }

    persisted = _load_emix_meta_inferences(
        project_id,
        dataset_id,
    )

    items = persisted.get(
        "items",
        [],
    )

    if not isinstance(
        items,
        list,
    ):
        items = []

    updated = []
    replaced = False

    for existing in items:

        if not isinstance(
            existing,
            dict,
        ):
            continue

        if (
            existing.get(
                "inference_id"
            )
            == inference_id
        ):
            updated.append(
                inference
            )
            replaced = True

        else:
            updated.append(
                existing
            )

    if not replaced:
        updated.append(
            inference
        )

    _persist_emix_meta_inferences(
        project_id,
        dataset_id,
        {
            "items": updated,
        },
    )

    return inference





# ==========================================================
# Synthèse EMIX
# ==========================================================

def _load_emix_summary(
    project_id,
    dataset_id,
):
    from emidaf_studio.services.model_registry import (
        get_analysis,
    )

    result = get_analysis(
        int(project_id),
        int(dataset_id),
        "emix",
        default={},
    )

    if not isinstance(
        result,
        dict,
    ):
        return {}

    section = result.get(
        "summary",
        {},
    )

    return (
        section
        if isinstance(
            section,
            dict,
        )
        else {}
    )


def _persist_emix_summary(
    project_id,
    dataset_id,
    payload,
):
    from emidaf_studio.services.model_registry import (
        merge_analysis_section,
    )

    return merge_analysis_section(
        int(project_id),
        int(dataset_id),
        "emix",
        "summary",
        payload,
    )


def _count_candidate_statuses(
    candidates,
):
    counts = {
        "pending": 0,
        "accepted": 0,
        "rejected": 0,
    }

    for candidate in candidates:

        if not isinstance(
            candidate,
            dict,
        ):
            continue

        status = candidate.get(
            "status",
            "pending",
        )

        if status in counts:
            counts[
                status
            ] += 1

    return counts


def _count_relation_types(
    links,
):
    counts = {
        "convergence": 0,
        "complementarity": 0,
        "divergence": 0,
        "undetermined": 0,
    }

    for link in links:

        if not isinstance(
            link,
            dict,
        ):
            continue

        relation_type = link.get(
            "relation_type",
            "undetermined",
        )

        if relation_type in counts:
            counts[
                relation_type
            ] += 1

    return counts


def _build_emix_summary_payload(
    project_id,
    dataset_id,
    researcher_validated=False,
    researcher_note="",
):
    """
    Construit une synthèse descriptive à partir
    des sections EMIX déjà persistées.

    Aucune conclusion scientifique nouvelle
    n'est générée ici.
    """

    source_section = _load_emix_sources(
        project_id,
        dataset_id,
    )

    candidate_section = _load_emix_candidates(
        project_id,
        dataset_id,
    )

    integration_section = _load_emix_integration(
        project_id,
        dataset_id,
    )

    joint_section = _load_emix_joint_display(
        project_id,
        dataset_id,
    )

    meta_section = _load_emix_meta_inferences(
        project_id,
        dataset_id,
    )

    selected_sources = source_section.get(
        "selected_stages",
        [],
    )

    if not isinstance(
        selected_sources,
        list,
    ):
        selected_sources = []

    candidates = candidate_section.get(
        "items",
        [],
    )

    if not isinstance(
        candidates,
        list,
    ):
        candidates = []

    links = integration_section.get(
        "links",
        [],
    )

    if not isinstance(
        links,
        list,
    ):
        links = []

    joint_rows = joint_section.get(
        "rows",
        [],
    )

    if not isinstance(
        joint_rows,
        list,
    ):
        joint_rows = []

    meta_inferences = meta_section.get(
        "items",
        [],
    )

    if not isinstance(
        meta_inferences,
        list,
    ):
        meta_inferences = []

    candidate_statuses = (
        _count_candidate_statuses(
            candidates
        )
    )

    relations = _count_relation_types(
        links
    )

    validated_links = sum(
        1
        for link in links
        if (
            isinstance(link, dict)
            and link.get(
                "validated"
            ) is True
        )
    )

    validated_meta = sum(
        1
        for inference in meta_inferences
        if (
            isinstance(
                inference,
                dict,
            )
            and inference.get(
                "validated"
            ) is True
        )
    )

    unresolved_links = relations[
        "undetermined"
    ]

    return {
        "schema_version": 1,

        "global": {
            "n_sources": len(
                selected_sources
            ),
            "n_candidates": len(
                candidates
            ),
            "n_links": len(
                links
            ),
            "n_joint_display_rows": len(
                joint_rows
            ),
            "n_meta_inferences": len(
                meta_inferences
            ),
            "n_validated_links": (
                validated_links
            ),
            "n_validated_meta_inferences": (
                validated_meta
            ),
        },

        "sources": {
            "selected_stages": list(
                selected_sources
            ),
        },

        "candidate_statuses": (
            candidate_statuses
        ),

        "relations": relations,

        "validation": {
            "suggestions_are_conclusions": False,
            "validated_links": (
                validated_links
            ),
            "validated_meta_inferences": (
                validated_meta
            ),
            "undetermined_links": (
                unresolved_links
            ),
            "researcher_validated": bool(
                researcher_validated
            ),
            "researcher_note": str(
                researcher_note or ""
            ).strip(),
            "principle": (
                "EMIX structure l'intégration "
                "des résultats mais ne transforme "
                "jamais automatiquement les "
                "suggestions, associations ou "
                "rapprochements en conclusions "
                "scientifiques ou causales."
            ),
        },

        "candidates": [
            dict(candidate)
            for candidate in candidates
            if isinstance(
                candidate,
                dict,
            )
        ],

        "links": [
            dict(link)
            for link in links
            if isinstance(
                link,
                dict,
            )
        ],

        "joint_display": [
            dict(row)
            for row in joint_rows
            if isinstance(
                row,
                dict,
            )
        ],

        "meta_inferences": [
            dict(inference)
            for inference in meta_inferences
            if isinstance(
                inference,
                dict,
            )
        ],
    }


def _save_emix_summary(
    project_id,
    dataset_id,
    researcher_validated,
    researcher_note,
):
    summary = _build_emix_summary_payload(
        project_id,
        dataset_id,
        researcher_validated=(
            researcher_validated
        ),
        researcher_note=(
            researcher_note
        ),
    )

    _persist_emix_summary(
        project_id,
        dataset_id,
        summary,
    )

    return summary



def _candidate_card(
    candidate,
):
    """
    Carte d'un candidat d'intégration EMIX.
    """

    status = candidate.get(
        "status",
        "pending",
    )

    colors = {
        "pending": "warning",
        "accepted": "success",
        "rejected": "secondary",
    }

    labels = {
        "pending": "En attente",
        "accepted": "Accepté",
        "rejected": "Rejeté",
    }

    candidate_id = candidate[
        "candidate_id"
    ]

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.H5(
                            "Candidat d'intégration",
                            className="mb-0",
                        ),

                        dbc.Badge(
                            labels.get(
                                status,
                                status,
                            ),
                            color=colors.get(
                                status,
                                "secondary",
                            ),
                        ),
                    ],
                    className=(
                        "d-flex "
                        "justify-content-between "
                        "align-items-center"
                    ),
                ),

                html.Hr(),

                html.P(
                    [
                        html.Strong(
                            "EAIE : "
                        ),
                        candidate.get(
                            "element_1",
                            "",
                        ),
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "EQAE : "
                        ),
                        candidate.get(
                            "element_2",
                            "",
                        ),
                    ]
                ),

                dbc.Alert(
                    candidate.get(
                        "rationale",
                        "",
                    ),
                    color="light",
                ),

                html.P(
                    (
                        "Ce rapprochement est une "
                        "suggestion à examiner. "
                        "Aucun type de relation "
                        "scientifique n'est attribué "
                        "automatiquement."
                    ),
                    className=(
                        "small text-muted"
                    ),
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "Accepter",
                                id={
                                    "type": (
                                        "emix-candidate-accept"
                                    ),
                                    "index": candidate_id,
                                },
                                color="success",
                                outline=True,
                                disabled=(
                                    status
                                    == "accepted"
                                ),
                                className="w-100",
                            ),
                            md=6,
                        ),

                        dbc.Col(
                            dbc.Button(
                                "Rejeter",
                                id={
                                    "type": (
                                        "emix-candidate-reject"
                                    ),
                                    "index": candidate_id,
                                },
                                color="danger",
                                outline=True,
                                disabled=(
                                    status
                                    == "rejected"
                                ),
                                className="w-100",
                            ),
                            md=6,
                        ),
                    ],
                    className="g-2",
                ),
            ]
        ),
        className="shadow-sm mb-3",
    )




def _integration_candidate_card(
    project_id,
    dataset_id,
    candidate,
):
    candidate_id = candidate[
        "candidate_id"
    ]

    existing = (
        _existing_link_for_candidate(
            project_id,
            dataset_id,
            candidate_id,
        )
    )

    selected_relation = (
        existing.get(
            "relation_type"
        )
        if isinstance(
            existing,
            dict,
        )
        else None
    )

    researcher_note = (
        existing.get(
            "researcher_note",
            "",
        )
        if isinstance(
            existing,
            dict,
        )
        else ""
    )

    already_integrated = (
        existing is not None
    )

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.H5(
                            "Candidat accepté",
                            className="mb-0",
                        ),

                        dbc.Badge(
                            (
                                "Lien créé"
                                if already_integrated
                                else "À intégrer"
                            ),
                            color=(
                                "success"
                                if already_integrated
                                else "warning"
                            ),
                        ),
                    ],
                    className=(
                        "d-flex "
                        "justify-content-between "
                        "align-items-center"
                    ),
                ),

                html.Hr(),

                html.P(
                    [
                        html.Strong(
                            "EAIE : "
                        ),
                        candidate.get(
                            "element_1",
                            "",
                        ),
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "EQAE : "
                        ),
                        candidate.get(
                            "element_2",
                            "",
                        ),
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Origine : "
                        ),
                        candidate_id,
                    ],
                    className="small text-muted",
                ),

                html.Label(
                    "Type de relation",
                    className="fw-semibold",
                ),

                dcc.Dropdown(
                    id={
                        "type": (
                            "emix-integration-relation"
                        ),
                        "index": candidate_id,
                    },
                    options=[
                        {
                            "label": (
                                "Convergence"
                            ),
                            "value": (
                                "convergence"
                            ),
                        },
                        {
                            "label": (
                                "Complémentarité"
                            ),
                            "value": (
                                "complementarity"
                            ),
                        },
                        {
                            "label": (
                                "Divergence"
                            ),
                            "value": (
                                "divergence"
                            ),
                        },
                        {
                            "label": (
                                "Indéterminée"
                            ),
                            "value": (
                                "undetermined"
                            ),
                        },
                    ],
                    value=selected_relation,
                    placeholder=(
                        "Choisir explicitement "
                        "la relation..."
                    ),
                    clearable=True,
                    className="mb-3",
                ),

                html.Label(
                    "Note du chercheur",
                    className="fw-semibold",
                ),

                dbc.Textarea(
                    id={
                        "type": (
                            "emix-integration-note"
                        ),
                        "index": candidate_id,
                    },
                    value=researcher_note,
                    placeholder=(
                        "Justifier le classement "
                        "du rapprochement..."
                    ),
                    rows=4,
                    className="mb-3",
                ),

                dbc.Alert(
                    (
                        "Le type de relation est une "
                        "décision analytique du chercheur. "
                        "EMIX ne l'infère pas automatiquement."
                    ),
                    color="info",
                ),

                html.Div(
                    id={
                        "type": (
                            "emix-integration-card-status"
                        ),
                        "index": candidate_id,
                    },
                    className="mb-3",
                ),

                dbc.Button(
                    (
                        "Mettre à jour le lien"
                        if already_integrated
                        else "Créer le lien d'intégration"
                    ),
                    id={
                        "type": (
                            "emix-create-integration-link"
                        ),
                        "index": candidate_id,
                    },
                    color="primary",
                    className="w-100",
                    n_clicks=0,
                ),
            ]
        ),
        className="shadow-sm mb-3",
    )


def _render_integration(
    project_id,
    dataset_id,
):
    accepted = _accepted_candidates(
        project_id,
        dataset_id,
    )

    persisted = _load_emix_integration(
        project_id,
        dataset_id,
    )

    links = persisted.get(
        "links",
        [],
    )

    if not isinstance(
        links,
        list,
    ):
        links = []

    children = [
        html.H4(
            "Intégration",
            className="mb-2",
        ),

        html.P(
            (
                "Cette étape transforme uniquement "
                "les candidats acceptés en liens "
                "d'intégration validés par le chercheur."
            ),
            className="text-muted",
        ),

        dbc.Alert(
            (
                "Convergence, complémentarité et "
                "divergence ne sont jamais attribuées "
                "automatiquement. Le chercheur choisit "
                "et justifie explicitement la relation."
            ),
            color="warning",
        ),

        html.Div(
            id="emix-integration-action-status",
            className="mb-3",
        ),

        html.Div(
            [
                dbc.Badge(
                    (
                        f"{len(accepted)} candidat(s) "
                        "accepté(s)"
                    ),
                    color="primary",
                    className="me-2",
                ),

                dbc.Badge(
                    (
                        f"{len(links)} lien(s) "
                        "d'intégration"
                    ),
                    color="success",
                ),
            ],
            className="mb-3",
        ),
    ]

    if not accepted:

        children.append(
            dbc.Alert(
                (
                    "Aucun candidat accepté. "
                    "Retournez dans l'onglet Candidats "
                    "et acceptez au moins un "
                    "rapprochement avant l'intégration."
                ),
                color="light",
            )
        )

    else:

        children.extend(
            _integration_candidate_card(
                project_id,
                dataset_id,
                candidate,
            )
            for candidate in accepted
        )

    return html.Div(
        children
    )





def _relation_label(
    relation_type,
):
    labels = {
        "convergence": "Convergence",
        "complementarity": "Complémentarité",
        "divergence": "Divergence",
        "undetermined": "Indéterminée",
    }

    return labels.get(
        relation_type,
        relation_type,
    )


def _joint_display_link_card(
    project_id,
    dataset_id,
    link,
):
    link_id = link[
        "link_id"
    ]

    existing = (
        _existing_joint_row_for_link(
            project_id,
            dataset_id,
            link_id,
        )
    )

    comment = (
        existing.get(
            "integrated_comment",
            "",
        )
        if isinstance(
            existing,
            dict,
        )
        else ""
    )

    quantitative_result, qualitative_result = (
        _split_mixed_results(
            link
        )
    )

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.H5(
                            "Lien mixte validé",
                            className="mb-0",
                        ),

                        dbc.Badge(
                            _relation_label(
                                link.get(
                                    "relation_type",
                                    "undetermined",
                                )
                            ),
                            color=(
                                "success"
                                if link.get(
                                    "relation_type"
                                )
                                == "convergence"
                                else "secondary"
                            ),
                        ),
                    ],
                    className=(
                        "d-flex "
                        "justify-content-between "
                        "align-items-center"
                    ),
                ),

                html.Hr(),

                html.P(
                    [
                        html.Strong(
                            "Résultat quantitatif : "
                        ),
                        quantitative_result,
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Résultat qualitatif : "
                        ),
                        qualitative_result,
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Relation : "
                        ),
                        _relation_label(
                            link.get(
                                "relation_type",
                                "undetermined",
                            )
                        ),
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Lien source : "
                        ),
                        link_id,
                    ],
                    className="small text-muted",
                ),

                html.Label(
                    "Commentaire intégré du chercheur",
                    className="fw-semibold",
                ),

                dbc.Textarea(
                    id={
                        "type": (
                            "emix-joint-display-comment"
                        ),
                        "index": link_id,
                    },
                    value=comment,
                    placeholder=(
                        "Décrire ce que la mise en regard "
                        "des résultats quantitatif et "
                        "qualitatif permet d'observer, "
                        "sans dépasser les données."
                    ),
                    rows=5,
                    className="mb-3",
                ),

                dbc.Alert(
                    (
                        "Le commentaire intégré doit rester "
                        "une interprétation du chercheur. "
                        "Le Joint Display ne produit pas "
                        "automatiquement de conclusion "
                        "ou de causalité."
                    ),
                    color="info",
                ),

                html.Div(
                    id={
                        "type": (
                            "emix-joint-display-status"
                        ),
                        "index": link_id,
                    },
                    className="mb-3",
                ),

                dbc.Button(
                    (
                        "Mettre à jour la ligne"
                        if existing
                        else "Ajouter au Joint Display"
                    ),
                    id={
                        "type": (
                            "emix-save-joint-display-row"
                        ),
                        "index": link_id,
                    },
                    color="primary",
                    className="w-100",
                    n_clicks=0,
                ),
            ]
        ),
        className="shadow-sm mb-3",
    )


def _joint_display_table(
    rows,
):
    if not rows:
        return dbc.Alert(
            (
                "Aucune ligne enregistrée dans "
                "le Joint Display."
            ),
            color="light",
        )

    header = html.Thead(
        html.Tr(
            [
                html.Th(
                    "Résultat quantitatif"
                ),
                html.Th(
                    "Résultat qualitatif"
                ),
                html.Th(
                    "Relation"
                ),
                html.Th(
                    "Commentaire intégré"
                ),
            ]
        )
    )

    body = html.Tbody(
        [
            html.Tr(
                [
                    html.Td(
                        row.get(
                            "quantitative_result",
                            "",
                        )
                    ),
                    html.Td(
                        row.get(
                            "qualitative_result",
                            "",
                        )
                    ),
                    html.Td(
                        _relation_label(
                            row.get(
                                "relation_type",
                                "undetermined",
                            )
                        )
                    ),
                    html.Td(
                        row.get(
                            "integrated_comment",
                            "",
                        )
                    ),
                ]
            )
            for row in rows
            if isinstance(
                row,
                dict,
            )
        ]
    )

    return dbc.Table(
        [
            header,
            body,
        ],
        bordered=True,
        hover=True,
        responsive=True,
        size="sm",
    )


def _render_joint_display(
    project_id,
    dataset_id,
):
    links = _validated_integration_links(
        project_id,
        dataset_id,
    )

    persisted = _load_emix_joint_display(
        project_id,
        dataset_id,
    )

    rows = persisted.get(
        "rows",
        [],
    )

    if not isinstance(
        rows,
        list,
    ):
        rows = []

    children = [
        html.H4(
            "Joint Display",
            className="mb-2",
        ),

        html.P(
            (
                "Le Joint Display met en regard "
                "les résultats issus des différentes "
                "composantes méthodologiques."
            ),
            className="text-muted",
        ),

        dbc.Alert(
            (
                "Les lignes affichées proviennent "
                "uniquement de liens d'intégration "
                "déjà validés par le chercheur."
            ),
            color="info",
        ),

        html.Div(
            [
                dbc.Badge(
                    (
                        f"{len(links)} lien(s) "
                        "validé(s)"
                    ),
                    color="primary",
                    className="me-2",
                ),

                dbc.Badge(
                    (
                        f"{len(rows)} ligne(s) "
                        "Joint Display"
                    ),
                    color="success",
                ),
            ],
            className="mb-3",
        ),
    ]

    if not links:

        children.append(
            dbc.Alert(
                (
                    "Aucun lien d'intégration validé "
                    "n'est disponible."
                ),
                color="warning",
            )
        )

        return html.Div(
            children
        )

    children.append(
        html.H5(
            "Construction du Joint Display",
            className="mt-3 mb-3",
        )
    )

    children.extend(
        _joint_display_link_card(
            project_id,
            dataset_id,
            link,
        )
        for link in links
    )

    children.append(
        html.H5(
            "Tableau intégré",
            className="mt-4 mb-3",
        )
    )

    children.append(
        _joint_display_table(
            rows
        )
    )

    return html.Div(
        children
    )





def _meta_link_label(
    link,
):
    relation = _relation_label(
        link.get(
            "relation_type",
            "undetermined",
        )
    )

    quantitative = str(
        link.get(
            "quantitative_result",
            "",
        )
    )

    if len(quantitative) > 80:
        quantitative = (
            quantitative[:77]
            + "..."
        )

    return (
        f"{relation} — {quantitative}"
    )


def _meta_inference_card(
    inference,
):
    validated = bool(
        inference.get(
            "validated"
        )
    )

    limitations = inference.get(
        "limitations",
        [],
    )

    if not isinstance(
        limitations,
        list,
    ):
        limitations = []

    link_ids = inference.get(
        "link_ids",
        [],
    )

    if not isinstance(
        link_ids,
        list,
    ):
        link_ids = []

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.H5(
                            "Méta-inférence",
                            className="mb-0",
                        ),

                        dbc.Badge(
                            (
                                "Validée"
                                if validated
                                else "Brouillon"
                            ),
                            color=(
                                "success"
                                if validated
                                else "warning"
                            ),
                        ),
                    ],
                    className=(
                        "d-flex "
                        "justify-content-between "
                        "align-items-center"
                    ),
                ),

                html.Hr(),

                html.P(
                    inference.get(
                        "statement",
                        "",
                    )
                ),

                html.P(
                    [
                        html.Strong(
                            "Lien(s) mobilisé(s) : "
                        ),
                        ", ".join(
                            link_ids
                        ),
                    ],
                    className="small",
                ),

                html.Div(
                    [
                        html.Strong(
                            "Limites :"
                        ),
                        html.Ul(
                            [
                                html.Li(
                                    limitation
                                )
                                for limitation
                                in limitations
                            ]
                        ),
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Note du chercheur : "
                        ),
                        inference.get(
                            "researcher_note",
                            "",
                        )
                        or "—",
                    ]
                ),

                html.P(
                    [
                        html.Strong(
                            "Identifiant : "
                        ),
                        inference.get(
                            "inference_id",
                            "",
                        ),
                    ],
                    className="small text-muted",
                ),
            ]
        ),
        className="shadow-sm mb-3",
    )


def _render_meta_inferences(
    project_id,
    dataset_id,
):
    available_links = (
        _available_meta_links(
            project_id,
            dataset_id,
        )
    )

    persisted = (
        _load_emix_meta_inferences(
            project_id,
            dataset_id,
        )
    )

    items = persisted.get(
        "items",
        [],
    )

    if not isinstance(
        items,
        list,
    ):
        items = []

    n_validated = sum(
        1
        for item in items
        if (
            isinstance(item, dict)
            and item.get(
                "validated"
            ) is True
        )
    )

    children = [
        html.H4(
            "Méta-inférences",
            className="mb-2",
        ),

        html.P(
            (
                "Une méta-inférence est une "
                "interprétation intégrée rédigée "
                "par le chercheur à partir des "
                "résultats mis en regard."
            ),
            className="text-muted",
        ),

        dbc.Alert(
            (
                "EMIX ne génère pas automatiquement "
                "de conclusion scientifique. "
                "La formulation, les limites et "
                "la validation restent sous la "
                "responsabilité du chercheur."
            ),
            color="warning",
        ),

        html.Div(
            [
                dbc.Badge(
                    (
                        f"{len(available_links)} "
                        "lien(s) disponible(s)"
                    ),
                    color="primary",
                    className="me-2",
                ),

                dbc.Badge(
                    (
                        f"{len(items)} "
                        "méta-inférence(s)"
                    ),
                    color="secondary",
                    className="me-2",
                ),

                dbc.Badge(
                    (
                        f"{n_validated} validée(s)"
                    ),
                    color="success",
                ),
            ],
            className="mb-4",
        ),
    ]

    if not available_links:

        children.append(
            dbc.Alert(
                (
                    "Aucune ligne du Joint Display "
                    "n'est disponible. Construisez "
                    "d'abord le Joint Display."
                ),
                color="light",
            )
        )

        return html.Div(
            children
        )

    options = [
        {
            "label": (
                _meta_link_label(
                    link
                )
            ),
            "value": link[
                "link_id"
            ],
        }
        for link in available_links
    ]

    children.extend(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(
                            "Nouvelle méta-inférence",
                            className="mb-3",
                        ),

                        html.Label(
                            "Lien(s) du Joint Display",
                            className="fw-semibold",
                        ),

                        dcc.Dropdown(
                            id="emix-meta-links",
                            options=options,
                            value=[],
                            multi=True,
                            placeholder=(
                                "Sélectionner le ou "
                                "les liens mobilisés..."
                            ),
                            className="mb-3",
                        ),

                        html.Label(
                            "Méta-inférence",
                            className="fw-semibold",
                        ),

                        dbc.Textarea(
                            id="emix-meta-statement",
                            placeholder=(
                                "Rédiger l'interprétation "
                                "intégrée sans dépasser "
                                "les données disponibles..."
                            ),
                            rows=5,
                            className="mb-3",
                        ),

                        html.Label(
                            (
                                "Limites "
                                "(une par ligne)"
                            ),
                            className="fw-semibold",
                        ),

                        dbc.Textarea(
                            id="emix-meta-limitations",
                            placeholder=(
                                "Exemple :\n"
                                "Matériau qualitatif limité\n"
                                "Absence de preuve causale"
                            ),
                            rows=4,
                            className="mb-3",
                        ),

                        html.Label(
                            "Note du chercheur",
                            className="fw-semibold",
                        ),

                        dbc.Textarea(
                            id="emix-meta-note",
                            placeholder=(
                                "Commentaire méthodologique "
                                "ou justification..."
                            ),
                            rows=3,
                            className="mb-3",
                        ),

                        dbc.Checkbox(
                            id="emix-meta-validated",
                            label=(
                                "Je valide explicitement "
                                "cette méta-inférence"
                            ),
                            value=False,
                            className="mb-3",
                        ),

                        dbc.Alert(
                            (
                                "Une méta-inférence peut "
                                "être enregistrée comme "
                                "brouillon. Pour la valider, "
                                "au moins une limitation "
                                "doit être renseignée."
                            ),
                            color="info",
                        ),

                        html.Div(
                            id="emix-meta-action-status",
                            className="mb-3",
                        ),

                        dbc.Button(
                            "Enregistrer la méta-inférence",
                            id="emix-save-meta-inference",
                            color="primary",
                            n_clicks=0,
                            className="w-100",
                        ),
                    ]
                ),
                className="shadow-sm mb-4",
            ),

            html.H5(
                "Méta-inférences enregistrées",
                className="mb-3",
            ),
        ]
    )

    if items:

        children.extend(
            _meta_inference_card(
                item
            )
            for item in items
            if isinstance(
                item,
                dict,
            )
        )

    else:

        children.append(
            dbc.Alert(
                (
                    "Aucune méta-inférence "
                    "enregistrée."
                ),
                color="light",
            )
        )

    return html.Div(
        children
    )





def _summary_metric_card(
    title,
    value,
    subtitle="",
):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H6(
                    title,
                    className=(
                        "text-muted mb-2"
                    ),
                ),
                html.H3(
                    str(value),
                    className="mb-1",
                ),
                html.Small(
                    subtitle,
                    className="text-muted",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )


def _summary_relation_table(
    relations,
):
    rows = [
        (
            "Convergence",
            relations.get(
                "convergence",
                0,
            ),
        ),
        (
            "Complémentarité",
            relations.get(
                "complementarity",
                0,
            ),
        ),
        (
            "Divergence",
            relations.get(
                "divergence",
                0,
            ),
        ),
        (
            "Indéterminée",
            relations.get(
                "undetermined",
                0,
            ),
        ),
    ]

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th(
                            "Type de relation"
                        ),
                        html.Th(
                            "Nombre"
                        ),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(
                                label
                            ),
                            html.Td(
                                count
                            ),
                        ]
                    )
                    for label, count
                    in rows
                ]
            ),
        ],
        bordered=True,
        hover=True,
        responsive=True,
        size="sm",
    )


def _summary_candidate_table(
    statuses,
):
    rows = [
        (
            "En attente",
            statuses.get(
                "pending",
                0,
            ),
        ),
        (
            "Acceptés",
            statuses.get(
                "accepted",
                0,
            ),
        ),
        (
            "Rejetés",
            statuses.get(
                "rejected",
                0,
            ),
        ),
    ]

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th(
                            "Statut candidat"
                        ),
                        html.Th(
                            "Nombre"
                        ),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(
                                label
                            ),
                            html.Td(
                                count
                            ),
                        ]
                    )
                    for label, count
                    in rows
                ]
            ),
        ],
        bordered=True,
        hover=True,
        responsive=True,
        size="sm",
    )


def _render_emix_summary(
    project_id,
    dataset_id,
):
    persisted = _load_emix_summary(
        project_id,
        dataset_id,
    )

    validation = (
        persisted.get(
            "validation",
            {},
        )
        if isinstance(
            persisted,
            dict,
        )
        else {}
    )

    if not isinstance(
        validation,
        dict,
    ):
        validation = {}

    researcher_validated = bool(
        validation.get(
            "researcher_validated",
            False,
        )
    )

    researcher_note = str(
        validation.get(
            "researcher_note",
            "",
        )
        or ""
    )

    # Synthèse courante toujours recalculée à partir
    # des sections source afin d'éviter un affichage obsolète.
    summary = _build_emix_summary_payload(
        project_id,
        dataset_id,
        researcher_validated=(
            researcher_validated
        ),
        researcher_note=(
            researcher_note
        ),
    )

    global_counts = summary[
        "global"
    ]

    candidate_statuses = summary[
        "candidate_statuses"
    ]

    relations = summary[
        "relations"
    ]

    validation = summary[
        "validation"
    ]

    selected_sources = (
        summary[
            "sources"
        ][
            "selected_stages"
        ]
    )

    source_labels = [
        _SOURCE_CONFIG.get(
            stage,
            {},
        ).get(
            "label",
            stage.upper(),
        )
        for stage in selected_sources
    ]

    children = [
        html.H4(
            "Synthèse EMIX",
            className="mb-2",
        ),

        html.P(
            (
                "Cette page synthétise le processus "
                "d'intégration mixte déjà réalisé. "
                "Elle ne produit pas de nouvelle "
                "conclusion scientifique."
            ),
            className="text-muted",
        ),

        dbc.Alert(
            (
                "Les rapprochements proposés, "
                "les liens d'intégration et les "
                "méta-inférences restent distingués. "
                "Une validation finale du chercheur "
                "ne transforme pas une relation "
                "indéterminée en convergence."
            ),
            color="warning",
        ),

        dbc.Row(
            [
                dbc.Col(
                    _summary_metric_card(
                        "Sources",
                        global_counts[
                            "n_sources"
                        ],
                        "sélectionnées",
                    ),
                    md=4,
                    lg=2,
                ),

                dbc.Col(
                    _summary_metric_card(
                        "Candidats",
                        global_counts[
                            "n_candidates"
                        ],
                        "proposés",
                    ),
                    md=4,
                    lg=2,
                ),

                dbc.Col(
                    _summary_metric_card(
                        "Liens",
                        global_counts[
                            "n_links"
                        ],
                        "d'intégration",
                    ),
                    md=4,
                    lg=2,
                ),

                dbc.Col(
                    _summary_metric_card(
                        "Joint Display",
                        global_counts[
                            "n_joint_display_rows"
                        ],
                        "ligne(s)",
                    ),
                    md=4,
                    lg=2,
                ),

                dbc.Col(
                    _summary_metric_card(
                        "Méta-inférences",
                        global_counts[
                            "n_meta_inferences"
                        ],
                        "rédigée(s)",
                    ),
                    md=4,
                    lg=2,
                ),

                dbc.Col(
                    _summary_metric_card(
                        "Validées",
                        global_counts[
                            "n_validated_meta_inferences"
                        ],
                        "méta-inférence(s)",
                    ),
                    md=4,
                    lg=2,
                ),
            ],
            className="g-3 mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5(
                            "Sources retenues",
                            className="mb-3",
                        ),

                        html.Div(
                            [
                                dbc.Badge(
                                    label,
                                    color="primary",
                                    className=(
                                        "me-2 mb-2"
                                    ),
                                )
                                for label
                                in source_labels
                            ]
                            or [
                                html.Span(
                                    "Aucune source."
                                )
                            ]
                        ),
                    ],
                    md=12,
                ),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5(
                            "Candidats",
                            className="mb-3",
                        ),
                        _summary_candidate_table(
                            candidate_statuses
                        ),
                    ],
                    md=6,
                ),

                dbc.Col(
                    [
                        html.H5(
                            "Relations intégrées",
                            className="mb-3",
                        ),
                        _summary_relation_table(
                            relations
                        ),
                    ],
                    md=6,
                ),
            ],
            className="g-4 mb-4",
        ),

        html.H5(
            "État de validation",
            className="mb-3",
        ),

        dbc.ListGroup(
            [
                dbc.ListGroupItem(
                    (
                        "Liens validés : "
                        f"{validation['validated_links']}"
                    )
                ),

                dbc.ListGroupItem(
                    (
                        "Méta-inférences validées : "
                        f"{validation['validated_meta_inferences']}"
                    )
                ),

                dbc.ListGroupItem(
                    (
                        "Relations indéterminées : "
                        f"{validation['undetermined_links']}"
                    )
                ),

                dbc.ListGroupItem(
                    (
                        "Les suggestions ne sont pas "
                        "des conclusions scientifiques."
                    )
                ),
            ],
            className="mb-4",
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(
                        "Validation finale du chercheur",
                        className="mb-3",
                    ),

                    html.P(
                        (
                            "Cette validation confirme "
                            "que le chercheur a examiné "
                            "la synthèse EMIX. Elle ne "
                            "modifie pas les types de "
                            "relations déjà établis."
                        ),
                        className="text-muted",
                    ),

                    dbc.Textarea(
                        id="emix-summary-researcher-note",
                        value=researcher_note,
                        placeholder=(
                            "Note finale du chercheur "
                            "sur l'état de l'intégration..."
                        ),
                        rows=4,
                        className="mb-3",
                    ),

                    dbc.Checkbox(
                        id="emix-summary-validated",
                        label=(
                            "Je valide explicitement "
                            "cette synthèse EMIX"
                        ),
                        value=researcher_validated,
                        className="mb-3",
                    ),

                    html.Div(
                        id="emix-summary-action-status",
                        className="mb-3",
                    ),

                    dbc.Button(
                        "Enregistrer la synthèse",
                        id="emix-save-summary",
                        color="primary",
                        n_clicks=0,
                        className="w-100",
                    ),
                ]
            ),
            className="shadow-sm mb-4",
        ),

        dbc.Alert(
            validation[
                "principle"
            ],
            color="info",
        ),
    ]

    if researcher_validated:

        children.insert(
            3,
            dbc.Alert(
                (
                    "Synthèse actuellement "
                    "validée par le chercheur."
                ),
                color="success",
            ),
        )

    return html.Div(
        children
    )



def _render_candidates(
    project_id,
    dataset_id,
):
    source_section = _load_emix_sources(
        project_id,
        dataset_id,
    )

    selected = source_section.get(
        "selected_stages",
        [],
    )

    if not isinstance(
        selected,
        list,
    ):
        selected = []

    if (
        "eaie" not in selected
        or "eqae" not in selected
    ):
        return dbc.Alert(
            (
                "Sélectionnez EAIE et EQAE dans "
                "l'onglet Sources avant de générer "
                "des candidats d'intégration."
            ),
            color="warning",
        )

    persisted = _load_emix_candidates(
        project_id,
        dataset_id,
    )

    candidates = persisted.get(
        "items",
        [],
    )

    if not isinstance(
        candidates,
        list,
    ):
        candidates = []

    children = [
        html.H4(
            "Candidats d'intégration",
            className="mb-2",
        ),
        html.P(
            (
                "EMIX propose des rapprochements "
                "potentiels entre résultats EAIE et "
                "éléments qualitatifs EQAE."
            ),
            className="text-muted",
        ),
        dbc.Alert(
            (
                "Ces rapprochements sont des suggestions. "
                "Ils ne constituent ni une convergence, "
                "ni une complémentarité, ni une divergence "
                "tant que le chercheur ne les a pas évalués."
            ),
            color="info",
        ),
        dbc.Button(
            "Générer les candidats",
            id="emix-generate-candidates",
            color="primary",
            n_clicks=0,
            className="mb-3",
        ),
        html.Div(
            id="emix-candidate-action-status",
            className="mb-3",
        ),
    ]

    if candidates:
        children.append(
            html.P(
                f"{len(candidates)} candidat(s) enregistré(s).",
                className="fw-semibold",
            )
        )

        children.extend(
            _candidate_card(
                candidate
            )
            for candidate in candidates
        )

    else:
        children.append(
            dbc.Alert(
                "Aucun candidat enregistré.",
                color="light",
            )
        )

    return html.Div(
        children
    )


# ==========================================================
# Navigation par onglets
# ==========================================================

@callback(
    Output(
        "emix-tab-content",
        "children",
    ),
    Input(
        "emix-tabs",
        "active_tab",
    ),
    State(
        "emix-project-id",
        "data",
    ),
    State(
        "emix-dataset-id",
        "data",
    ),
)
def render_emix_tab(
    active_tab,
    project_id,
    dataset_id,
):

    if active_tab == "emix-tab-sources":

        return _render_sources(
            project_id,
            dataset_id,
        )

    if active_tab == "emix-tab-candidates":

        return _render_candidates(
            project_id,
            dataset_id,
        )

    if active_tab == "emix-tab-integration":

        return _render_integration(
            project_id,
            dataset_id,
        )

    if active_tab == "emix-tab-joint-display":

        return _render_joint_display(
            project_id,
            dataset_id,
        )

    if active_tab == "emix-tab-inferences":

        return _render_meta_inferences(
            project_id,
            dataset_id,
        )

    if active_tab == "emix-tab-summary":

        return _render_emix_summary(
            project_id,
            dataset_id,
        )

    content = _TAB_CONTENT.get(
        active_tab
    )

    if content is None:

        return emix_intro_component(
            "EMIX",
            (
                "Sélectionnez un onglet pour "
                "commencer l'intégration."
            ),
        )

    title, description, note = content

    return emix_intro_component(
        title,
        description,
        note=note,
    )


# ==========================================================
# Sélection + persistance
# ==========================================================

@callback(
    Output(
        "emix-selected-sources",
        "data",
    ),
    Output(
        "emix-source-selection-status",
        "children",
    ),
    Input(
        "emix-save-source-selection",
        "n_clicks",
    ),
    State(
        "emix-source-selection",
        "value",
    ),
    State(
        "emix-project-id",
        "data",
    ),
    State(
        "emix-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def select_emix_sources(
    n_clicks,
    selected,
    project_id,
    dataset_id,
):
    """
    Valide et persiste les sources choisies
    par le chercheur.
    """

    if not n_clicks:
        raise PreventUpdate

    selected = (
        list(selected)
        if selected
        else []
    )

    if (
        project_id is None
        or dataset_id is None
    ):
        return (
            selected,
            dbc.Alert(
                (
                    "Impossible de persister "
                    "la sélection : contexte "
                    "projet/dataset absent."
                ),
                color="warning",
                className="mb-0",
            ),
        )

    analyses = _load_available_sources(
        project_id,
        dataset_id,
    )

    valid_selected = [
        stage
        for stage in selected
        if (
            stage in _SOURCE_CONFIG
            and stage in analyses
            and analyses.get(stage) is not None
        )
    ]

    items = []

    for stage in valid_selected:

        try:
            source = _adapt_source(
                stage,
                analyses.get(stage),
            )

            items.append(
                source.to_dict()
            )

        except Exception:
            # Une erreur d'adaptation ne doit pas
            # produire une fausse source persistée.
            continue

    payload = {
        "selected_stages": (
            valid_selected
        ),
        "items": items,
    }

    _persist_emix_sources(
        project_id,
        dataset_id,
        payload,
    )

    return (
        valid_selected,
        _selection_status(
            valid_selected
        ),
    )


# ==========================================================
# Génération des candidats EMIX
# ==========================================================

@callback(
    Output(
        "emix-candidate-action-status",
        "children",
    ),
    Input(
        "emix-generate-candidates",
        "n_clicks",
    ),
    State(
        "emix-project-id",
        "data",
    ),
    State(
        "emix-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def generate_emix_candidates(
    n_clicks,
    project_id,
    dataset_id,
):
    if not n_clicks:
        raise PreventUpdate

    analyses = _load_available_sources(
        project_id,
        dataset_id,
    )

    generated = (
        _generate_eaie_eqae_candidates(
            analyses.get("eaie"),
            analyses.get("eqae"),
        )
    )

    previous = _load_emix_candidates(
        project_id,
        dataset_id,
    )

    previous_items = previous.get(
        "items",
        [],
    )

    if not isinstance(
        previous_items,
        list,
    ):
        previous_items = []

    previous_status = {
        item.get("candidate_id"): item.get(
            "status",
            "pending",
        )
        for item in previous_items
        if isinstance(item, dict)
    }

    for candidate in generated:
        candidate_id = candidate[
            "candidate_id"
        ]

        if candidate_id in previous_status:
            candidate["status"] = (
                previous_status[
                    candidate_id
                ]
            )

    _persist_emix_candidates(
        project_id,
        dataset_id,
        {
            "generator": (
                "eaie_eqae_lexical_v1"
            ),
            "items": generated,
        },
    )

    return dbc.Alert(
        (
            f"{len(generated)} candidat(s) "
            "généré(s) et persisté(s). "
            "Cliquez de nouveau sur l'onglet "
            "Candidats pour actualiser l'affichage."
        ),
        color="success",
        className="mb-0",
    )


# ==========================================================
# Validation humaine des candidats
# ==========================================================

@callback(
    Output(
        {
            "type": "emix-candidate-accept",
            "index": MATCH,
        },
        "disabled",
    ),
    Output(
        {
            "type": "emix-candidate-reject",
            "index": MATCH,
        },
        "disabled",
    ),
    Input(
        {
            "type": "emix-candidate-accept",
            "index": MATCH,
        },
        "n_clicks",
    ),
    Input(
        {
            "type": "emix-candidate-reject",
            "index": MATCH,
        },
        "n_clicks",
    ),
    State(
        "emix-project-id",
        "data",
    ),
    State(
        "emix-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def update_emix_candidate_status(
    accept_clicks,
    reject_clicks,
    project_id,
    dataset_id,
):
    """
    Le chercheur accepte ou rejette explicitement
    un candidat.

    Cette étape ne crée pas encore
    d'IntegrationLink.
    """

    triggered = ctx.triggered_id

    if not isinstance(
        triggered,
        dict,
    ):
        raise PreventUpdate

    candidate_id = triggered.get(
        "index"
    )

    action_type = triggered.get(
        "type"
    )

    if not candidate_id:
        raise PreventUpdate

    if (
        action_type
        == "emix-candidate-accept"
    ):
        status = "accepted"

    elif (
        action_type
        == "emix-candidate-reject"
    ):
        status = "rejected"

    else:
        raise PreventUpdate

    _update_candidate_status(
        project_id,
        dataset_id,
        candidate_id,
        status,
    )

    return (
        status == "accepted",
        status == "rejected",
    )


# ==========================================================
# Création / mise à jour des liens d'intégration
# ==========================================================

@callback(
    Output(
        {
            "type": (
                "emix-integration-card-status"
            ),
            "index": MATCH,
        },
        "children",
    ),
    Input(
        {
            "type": (
                "emix-create-integration-link"
            ),
            "index": MATCH,
        },
        "n_clicks",
    ),
    State(
        {
            "type": (
                "emix-integration-relation"
            ),
            "index": MATCH,
        },
        "value",
    ),
    State(
        {
            "type": (
                "emix-integration-note"
            ),
            "index": MATCH,
        },
        "value",
    ),
    State(
        "emix-project-id",
        "data",
    ),
    State(
        "emix-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def create_emix_integration_link(
    n_clicks,
    relation_type,
    researcher_note,
    project_id,
    dataset_id,
):
    if not n_clicks:
        raise PreventUpdate

    triggered = ctx.triggered_id

    if not isinstance(
        triggered,
        dict,
    ):
        raise PreventUpdate

    candidate_id = triggered.get(
        "index"
    )

    if not candidate_id:
        raise PreventUpdate

    if relation_type not in _VALID_RELATION_TYPES:
        return dbc.Alert(
            (
                "Choisissez d'abord un type "
                "de relation."
            ),
            color="danger",
            className="mb-0",
        )

    try:
        link = (
            _create_or_update_integration_link(
                project_id,
                dataset_id,
                candidate_id,
                relation_type,
                researcher_note,
            )
        )

    except Exception as exc:
        return dbc.Alert(
            f"Erreur : {exc}",
            color="danger",
            className="mb-0",
        )

    return dbc.Alert(
        (
            "Lien d'intégration enregistré : "
            f"{link['relation_type']}."
        ),
        color="success",
        className="mb-0",
    )


# ==========================================================
# Enregistrement des lignes Joint Display
# ==========================================================

@callback(
    Output(
        {
            "type": (
                "emix-joint-display-status"
            ),
            "index": MATCH,
        },
        "children",
    ),
    Input(
        {
            "type": (
                "emix-save-joint-display-row"
            ),
            "index": MATCH,
        },
        "n_clicks",
    ),
    State(
        {
            "type": (
                "emix-joint-display-comment"
            ),
            "index": MATCH,
        },
        "value",
    ),
    State(
        "emix-project-id",
        "data",
    ),
    State(
        "emix-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def save_emix_joint_display_row(
    n_clicks,
    integrated_comment,
    project_id,
    dataset_id,
):
    if not n_clicks:
        raise PreventUpdate

    triggered = ctx.triggered_id

    if not isinstance(
        triggered,
        dict,
    ):
        raise PreventUpdate

    link_id = triggered.get(
        "index"
    )

    if not link_id:
        raise PreventUpdate

    try:
        row = (
            _create_or_update_joint_display_row(
                project_id,
                dataset_id,
                link_id,
                integrated_comment,
            )
        )

    except Exception as exc:
        return dbc.Alert(
            f"Erreur : {exc}",
            color="danger",
            className="mb-0",
        )

    return dbc.Alert(
        (
            "Ligne Joint Display enregistrée "
            f"pour {row['source_link_id']}."
        ),
        color="success",
        className="mb-0",
    )


# ==========================================================
# Enregistrement des méta-inférences
# ==========================================================

@callback(
    Output(
        "emix-meta-action-status",
        "children",
    ),
    Input(
        "emix-save-meta-inference",
        "n_clicks",
    ),
    State(
        "emix-meta-statement",
        "value",
    ),
    State(
        "emix-meta-links",
        "value",
    ),
    State(
        "emix-meta-limitations",
        "value",
    ),
    State(
        "emix-meta-note",
        "value",
    ),
    State(
        "emix-meta-validated",
        "value",
    ),
    State(
        "emix-project-id",
        "data",
    ),
    State(
        "emix-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def save_emix_meta_inference(
    n_clicks,
    statement,
    link_ids,
    limitations_text,
    researcher_note,
    validated,
    project_id,
    dataset_id,
):
    if not n_clicks:
        raise PreventUpdate

    limitations = _parse_limitations(
        limitations_text
    )

    try:
        inference = _save_meta_inference(
            project_id,
            dataset_id,
            statement,
            link_ids,
            limitations,
            researcher_note,
            validated,
        )

    except Exception as exc:
        return dbc.Alert(
            f"Erreur : {exc}",
            color="danger",
            className="mb-0",
        )

    status = (
        "validée"
        if inference[
            "validated"
        ]
        else "enregistrée comme brouillon"
    )

    return dbc.Alert(
        (
            "Méta-inférence "
            f"{status}. "
            "Recliquez sur l'onglet "
            "Méta-inférences pour actualiser "
            "la liste."
        ),
        color=(
            "success"
            if inference[
                "validated"
            ]
            else "warning"
        ),
        className="mb-0",
    )


# ==========================================================
# Enregistrement de la synthèse EMIX
# ==========================================================

@callback(
    Output(
        "emix-summary-action-status",
        "children",
    ),
    Input(
        "emix-save-summary",
        "n_clicks",
    ),
    State(
        "emix-summary-validated",
        "value",
    ),
    State(
        "emix-summary-researcher-note",
        "value",
    ),
    State(
        "emix-project-id",
        "data",
    ),
    State(
        "emix-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def save_emix_summary(
    n_clicks,
    researcher_validated,
    researcher_note,
    project_id,
    dataset_id,
):
    if not n_clicks:
        raise PreventUpdate

    try:
        summary = _save_emix_summary(
            project_id,
            dataset_id,
            researcher_validated=(
                researcher_validated
            ),
            researcher_note=(
                researcher_note
            ),
        )

    except Exception as exc:

        return dbc.Alert(
            f"Erreur : {exc}",
            color="danger",
            className="mb-0",
        )

    validation = summary[
        "validation"
    ]

    if validation[
        "researcher_validated"
    ]:

        message = (
            "Synthèse EMIX enregistrée "
            "et explicitement validée "
            "par le chercheur."
        )

        color = "success"

    else:

        message = (
            "Synthèse EMIX enregistrée "
            "sans validation finale."
        )

        color = "warning"

    return dbc.Alert(
        message,
        color=color,
        className="mb-0",
    )
