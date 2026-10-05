from __future__ import annotations

import json

from dash import (
    Input,
    Output,
    State,
    callback,
    dcc,
    html,
    no_update,
)

import dash_bootstrap_components as dbc

from emidaf_core.reporting import (
    ReportEngine,
    ReportRenderer,
)

from emidaf_studio.pages.inspection.layout import (
    load_dataset,
)

from emidaf_studio.services.model_registry import (
    get_all_analyses,
)


def _stage_unavailable(stage_name):

    return {
        "status": "non_disponible",
        "message": (
            f"Les résultats de l'étape "
            f"« {stage_name} » ne sont pas "
            "persistés ou disponibles "
            "pour ce jeu de données."
        ),
    }



def _compact_etae_for_report(
    etae_context,
):
    """
    Prépare une version compacte et lisible
    des résultats ETAE pour le rapport.

    Les vecteurs documentaires, labels,
    indices et autres sorties volumineuses
    ne sont pas reproduits intégralement.
    """

    if not isinstance(
        etae_context,
        dict,
    ):
        return etae_context

    compact = {}

    # --------------------------------------------------
    # Corpus
    # --------------------------------------------------

    corpus = etae_context.get(
        "corpus"
    )

    if isinstance(corpus, dict):

        result = corpus.get(
            "result",
            {},
        )

        if isinstance(result, dict):
            compact["Corpus"] = {
                "Variable textuelle": (
                    result.get(
                        "text_column"
                    )
                    or corpus.get(
                        "text_column"
                    )
                ),
                "Documents": result.get(
                    "n_documents"
                ),
                "Documents valides": result.get(
                    "n_valid_documents"
                ),
                "Valeurs manquantes": result.get(
                    "n_missing"
                ),
                "Documents vides": result.get(
                    "n_empty"
                ),
                "Nombre total de mots": result.get(
                    "total_words"
                ),
                "Taille du vocabulaire": result.get(
                    "vocabulary_size"
                ),
                "Longueur moyenne en mots": result.get(
                    "mean_words"
                ),
                "Diversité lexicale": result.get(
                    "lexical_diversity"
                ),
            }

    # --------------------------------------------------
    # Lexique
    # --------------------------------------------------

    lexical = etae_context.get(
        "lexique"
    )

    if isinstance(lexical, dict):

        result = lexical.get(
            "result",
            {},
        )

        if isinstance(result, dict):
            compact["Lexique"] = {
                "Documents": result.get(
                    "n_documents"
                ),
                "Nombre total de tokens": result.get(
                    "total_tokens"
                ),
                "Taille du vocabulaire": result.get(
                    "vocabulary_size"
                ),
                "Termes les plus fréquents": (
                    result.get(
                        "items",
                        [],
                    )[:10]
                ),
            }

    # --------------------------------------------------
    # N-grams
    # --------------------------------------------------

    ngrams = etae_context.get(
        "ngrams"
    )

    if isinstance(ngrams, dict):

        result = ngrams.get(
            "result",
            {},
        )

        if isinstance(result, dict):
            compact["N-grams"] = {
                "Taille des n-grams": result.get(
                    "ngram_size"
                ),
                "Nombre total de n-grams": result.get(
                    "total_tokens"
                ),
                "Vocabulaire": result.get(
                    "vocabulary_size"
                ),
                "N-grams dominants": (
                    result.get(
                        "items",
                        [],
                    )[:10]
                ),
            }

    # --------------------------------------------------
    # TF-IDF
    # --------------------------------------------------

    tfidf = etae_context.get(
        "tfidf"
    )

    if isinstance(tfidf, dict):

        result = tfidf.get(
            "result",
            {},
        )

        if isinstance(result, dict):
            compact["TF-IDF"] = {
                "Documents": result.get(
                    "n_documents"
                ),
                "Nombre de caractéristiques": result.get(
                    "n_features"
                ),
                "Sparsité": result.get(
                    "sparsity"
                ),
                "Termes TF-IDF dominants": (
                    result.get(
                        "top_terms",
                        [],
                    )[:10]
                ),
            }

    # --------------------------------------------------
    # Sentiment
    # --------------------------------------------------

    sentiment = etae_context.get(
        "sentiment"
    )

    if isinstance(sentiment, dict):

        result = sentiment.get(
            "result",
            {},
        )

        if isinstance(result, dict):
            compact["Sentiment"] = {
                "Méthode": result.get(
                    "method"
                ),
                "Documents": result.get(
                    "n_documents"
                ),
                "Score moyen": result.get(
                    "mean_score"
                ),
                "Positifs": result.get(
                    "positive_count"
                ),
                "Neutres": result.get(
                    "neutral_count"
                ),
                "Négatifs": result.get(
                    "negative_count"
                ),
                "Couverture lexicale moyenne": (
                    result.get(
                        "mean_coverage"
                    )
                ),
            }

    # --------------------------------------------------
    # Topics
    # --------------------------------------------------

    topics = etae_context.get(
        "topics"
    )

    if isinstance(topics, dict):

        result = topics.get(
            "result",
            {},
        )

        if isinstance(result, dict):
            compact["Thèmes"] = {
                "Méthode": result.get(
                    "method"
                ),
                "Documents": result.get(
                    "n_documents"
                ),
                "Nombre de thèmes": result.get(
                    "n_topics"
                ),
                "Thèmes détectés": result.get(
                    "topics",
                    [],
                ),
            }

    # --------------------------------------------------
    # Clusters
    # --------------------------------------------------

    clusters = etae_context.get(
        "clusters"
    )

    if isinstance(clusters, dict):

        result = clusters.get(
            "result",
            {},
        )

        if isinstance(result, dict):
            compact["Clustering textuel"] = {
                "Documents": result.get(
                    "n_documents"
                ),
                "Nombre de clusters": result.get(
                    "n_clusters"
                ),
                "Silhouette": result.get(
                    "silhouette_score"
                ),
                "Davies-Bouldin": result.get(
                    "davies_bouldin_score"
                ),
                "Calinski-Harabasz": result.get(
                    "calinski_harabasz_score"
                ),
                "Clusters": result.get(
                    "clusters",
                    [],
                ),
            }

    # --------------------------------------------------
    # Associations
    # --------------------------------------------------

    associations = etae_context.get(
        "associations"
    )

    if isinstance(
        associations,
        dict,
    ):

        association_summary = {
            "Variable textuelle": (
                associations.get(
                    "text_column"
                )
            ),
            "Variable structurée": (
                associations.get(
                    "target"
                )
            ),
            "Type de variable": (
                associations.get(
                    "target_type"
                )
            ),
        }

        topic_result = associations.get(
            "topic_result"
        )

        if isinstance(
            topic_result,
            dict,
        ):
            inference = topic_result.get(
                "inference",
                {},
            )

            if isinstance(
                inference,
                dict,
            ):
                anova = inference.get(
                    "anova",
                    {},
                )

                kruskal = inference.get(
                    "kruskal",
                    {},
                )

                eta_squared = inference.get(
                    "eta_squared",
                    {},
                )

                if isinstance(anova, dict):
                    association_summary[
                        "ANOVA - p-value"
                    ] = anova.get(
                        "p_value"
                    )

                if isinstance(
                    kruskal,
                    dict,
                ):
                    association_summary[
                        "Kruskal-Wallis - p-value"
                    ] = kruskal.get(
                        "p_value"
                    )

                if isinstance(
                    eta_squared,
                    dict,
                ):
                    association_summary[
                        "Eta carré"
                    ] = eta_squared.get(
                        "value"
                    )

        sentiment_result = associations.get(
            "sentiment_result"
        )

        if isinstance(
            sentiment_result,
            dict,
        ):
            association_summary[
                "Sentiment - ANOVA p-value"
            ] = sentiment_result.get(
                "anova_p_value"
            )

            association_summary[
                "Sentiment - Kruskal p-value"
            ] = sentiment_result.get(
                "kruskal_p_value"
            )

        topic_interpretation = associations.get(
            "topic_interpretation"
        )

        if isinstance(
            topic_interpretation,
            dict,
        ):
            association_summary[
                "Interprétation thèmes"
            ] = topic_interpretation.get(
                "statements",
                [],
            )

        sentiment_interpretation = (
            associations.get(
                "sentiment_interpretation"
            )
            or associations.get(
                "interpretation"
            )
        )

        if isinstance(
            sentiment_interpretation,
            dict,
        ):
            association_summary[
                "Interprétation sentiment"
            ] = (
                sentiment_interpretation.get(
                    "statements",
                    [],
                )
            )

        compact[
            "Associations texte / données"
        ] = association_summary

    return compact


def _compact_eqae_for_report(
    eqae_context,
):
    """
    Prépare une version compacte et lisible
    des résultats EQAE pour le rapport.

    Cette fonction organise uniquement les
    résultats persistés et validés dans EQAE.
    Elle ne produit pas d'interprétation
    qualitative automatique.
    """

    if not isinstance(
        eqae_context,
        dict,
    ):
        return eqae_context

    compact = {}

    # --------------------------------------------------
    # Corpus
    # --------------------------------------------------

    corpus = eqae_context.get(
        "corpus"
    )

    if isinstance(
        corpus,
        dict,
    ):
        compact["Corpus qualitatif"] = {
            "Variable qualitative": (
                corpus.get(
                    "text_column"
                )
            ),
            "Stratégie de segmentation": (
                corpus.get(
                    "segmentation_strategy"
                )
            ),
            "Documents valides": (
                corpus.get(
                    "n_valid_documents"
                )
            ),
            "Segments": (
                corpus.get(
                    "n_segments"
                )
            ),
            "Valeurs manquantes": (
                corpus.get(
                    "n_missing"
                )
            ),
            "Textes vides": (
                corpus.get(
                    "n_empty"
                )
            ),
        }

    # --------------------------------------------------
    # Codebook
    # --------------------------------------------------

    codebook = eqae_context.get(
        "codebook"
    )

    if isinstance(
        codebook,
        dict,
    ):
        codes = []

        for item in codebook.get(
            "codes",
            [],
        ):
            if not isinstance(
                item,
                dict,
            ):
                continue

            codes.append(
                {
                    "Nom": item.get(
                        "name"
                    ),
                    "Description": item.get(
                        "description"
                    ),
                    "Code parent": item.get(
                        "parent_code_id"
                    ),
                    "Actif": item.get(
                        "is_active"
                    ),
                }
            )

        compact["Codebook"] = {
            "Nom": codebook.get(
                "name"
            ),
            "Description": codebook.get(
                "description"
            ),
            "Nombre de codes": len(
                codes
            ),
            "Codes": codes,
        }

    # --------------------------------------------------
    # Codage
    # --------------------------------------------------

    coding = eqae_context.get(
        "coding"
    )

    if isinstance(
        coding,
        dict,
    ):
        assignments = coding.get(
            "assignments",
            [],
        )

        mode_counts = {}

        for item in assignments:
            if not isinstance(
                item,
                dict,
            ):
                continue

            mode = item.get(
                "mode",
                "unknown",
            )

            mode_counts[mode] = (
                mode_counts.get(
                    mode,
                    0,
                )
                + 1
            )

        compact["Codage qualitatif"] = {
            "Variable qualitative": (
                coding.get(
                    "text_column"
                )
            ),
            "Nombre d'affectations": len(
                assignments
            ),
            "Répartition par mode": (
                mode_counts
            ),
        }

    # --------------------------------------------------
    # Codage assisté
    # --------------------------------------------------

    assisted = eqae_context.get(
        "assisted"
    )

    if isinstance(
        assisted,
        dict,
    ):
        suggestions = assisted.get(
            "suggestions",
            [],
        )

        status_counts = {
            "pending": 0,
            "accepted": 0,
            "modified": 0,
            "rejected": 0,
        }

        for item in suggestions:
            if not isinstance(
                item,
                dict,
            ):
                continue

            status = item.get(
                "status"
            )

            if status in status_counts:
                status_counts[status] += 1

        compact["Codage assisté"] = {
            "Nombre de suggestions": len(
                suggestions
            ),
            "Statuts": status_counts,
            "Principe": (
                "Les suggestions assistées ne sont "
                "pas considérées comme des codages "
                "validés tant que le chercheur ne les "
                "a pas acceptées ou modifiées."
            ),
        }

    # --------------------------------------------------
    # Thèmes
    # --------------------------------------------------

    themes_payload = eqae_context.get(
        "themes"
    )

    if isinstance(
        themes_payload,
        dict,
    ):
        themes = []

        for item in themes_payload.get(
            "themes",
            [],
        ):
            if not isinstance(
                item,
                dict,
            ):
                continue

            themes.append(
                {
                    "Nom": item.get(
                        "name"
                    ),
                    "Description": item.get(
                        "description"
                    ),
                    "Thème parent": item.get(
                        "parent_theme_id"
                    ),
                    "Nombre de codes associés": len(
                        item.get(
                            "code_ids",
                            [],
                        )
                    ),
                }
            )

        compact["Structure thématique"] = {
            "Nombre de thèmes": len(
                themes
            ),
            "Thèmes": themes,
        }

    # --------------------------------------------------
    # Verbatims
    # --------------------------------------------------

    quotations = eqae_context.get(
        "quotations"
    )

    if isinstance(
        quotations,
        dict,
    ):
        items = quotations.get(
            "quotations",
            [],
        )

        compact["Verbatims"] = {
            "Nombre de verbatims": len(
                items
            ),
            "Extraits": [
                {
                    "Document": item.get(
                        "document_id"
                    ),
                    "Texte": item.get(
                        "text"
                    ),
                    "Note": item.get(
                        "note"
                    ),
                }
                for item in items[:20]
                if isinstance(
                    item,
                    dict,
                )
            ],
        }

    # --------------------------------------------------
    # Cooccurrences
    # --------------------------------------------------

    cooccurrence = eqae_context.get(
        "cooccurrence"
    )

    if isinstance(
        cooccurrence,
        dict,
    ):
        compact["Cooccurrences de codes"] = {
            "Niveau": cooccurrence.get(
                "level"
            ),
            "Nombre d'affectations": (
                cooccurrence.get(
                    "n_assignments"
                )
            ),
            "Paires": (
                cooccurrence.get(
                    "cooccurrences",
                    [],
                )
            ),
            "Précaution": (
                "Les cooccurrences sont descriptives "
                "et ne démontrent pas à elles seules "
                "une relation causale ou conceptuelle."
            ),
        }

    # --------------------------------------------------
    # Mémos
    # --------------------------------------------------

    memos = eqae_context.get(
        "memos"
    )

    if isinstance(
        memos,
        dict,
    ):
        memo_items = memos.get(
            "memos",
            [],
        )

        compact["Mémos analytiques"] = {
            "Nombre de mémos": len(
                memo_items
            ),
            "Mémos": [
                {
                    "Titre": item.get(
                        "title"
                    ),
                    "Type de cible": item.get(
                        "target_type"
                    ),
                    "Contenu": item.get(
                        "content"
                    ),
                    "Auteur": item.get(
                        "author"
                    ),
                }
                for item in memo_items[:20]
                if isinstance(
                    item,
                    dict,
                )
            ],
        }

    # --------------------------------------------------
    # Synthèse EQAE
    # --------------------------------------------------

    summary = eqae_context.get(
        "summary"
    )

    if isinstance(
        summary,
        dict,
    ):
        compact["Synthèse qualitative"] = {
            "Indicateurs globaux": (
                summary.get(
                    "global",
                    {},
                )
            ),
            "Synthèse par code": (
                summary.get(
                    "codes",
                    [],
                )
            ),
            "Synthèse par thème": (
                summary.get(
                    "themes",
                    [],
                )
            ),
            "Codage assisté": (
                summary.get(
                    "assisted_coding",
                    {},
                )
            ),
        }

    return compact


def _compact_ekde_for_report(
    ekde_context,
):
    """
    Prépare une version compacte et lisible des résultats EKDE
    pour les rapports.

    Les résultats persistés en base restent inchangés.
    """

    if not isinstance(
        ekde_context,
        dict,
    ):
        return ekde_context

    compact = {}

    for section, payload in ekde_context.items():

        if not isinstance(
            payload,
            dict,
        ):
            compact[section] = payload
            continue

        section_data = dict(payload)

        if section == "kmeans":

            section_data.pop(
                "labels",
                None,
            )

            section_data.pop(
                "cluster_centers",
                None,
            )

        elif section in {
            "dbscan",
            "agglomerative",
        }:

            section_data.pop(
                "labels",
                None,
            )

        elif section == "selection":

            result = section_data.get(
                "result"
            )

            if isinstance(
                result,
                list,
            ):

                cleaned_rows = []

                for row in result:

                    if not isinstance(
                        row,
                        dict,
                    ):
                        continue

                    cleaned_row = {}

                    for key, value in row.items():

                        if (
                            key == "Résultat"
                            and isinstance(
                                value,
                                str,
                            )
                            and (
                                "VarianceThreshold(" in value
                                or "SelectKBest(" in value
                                or "object at 0x" in value
                            )
                        ):
                            continue

                        cleaned_row[key] = value

                    if cleaned_row:
                        cleaned_rows.append(
                            cleaned_row
                        )

                if cleaned_rows:

                    section_data[
                        "result"
                    ] = cleaned_rows

                else:

                    section_data.pop(
                        "result",
                        None,
                    )

        compact[
            section
        ] = section_data

    return compact


def _compact_emix_for_report(
    emix_context,
):
    """
    Prépare une version compacte et lisible
    des résultats EMIX pour le reporting.

    Aucun nouveau lien, aucune convergence et
    aucune conclusion scientifique ne sont générés.
    """

    if not isinstance(
        emix_context,
        dict,
    ):
        return emix_context

    sources = emix_context.get(
        "sources",
        {},
    )

    candidates = emix_context.get(
        "candidates",
        {},
    )

    integration = emix_context.get(
        "integration",
        {},
    )

    joint_display = emix_context.get(
        "joint_display",
        {},
    )

    meta_inferences = emix_context.get(
        "meta_inferences",
        {},
    )

    summary = emix_context.get(
        "summary",
        {},
    )

    selected_sources = (
        sources.get(
            "selected_stages",
            [],
        )
        if isinstance(
            sources,
            dict,
        )
        else []
    )

    candidate_items = (
        candidates.get(
            "items",
            [],
        )
        if isinstance(
            candidates,
            dict,
        )
        else []
    )

    links = (
        integration.get(
            "links",
            [],
        )
        if isinstance(
            integration,
            dict,
        )
        else []
    )

    joint_rows = (
        joint_display.get(
            "rows",
            [],
        )
        if isinstance(
            joint_display,
            dict,
        )
        else []
    )

    inference_items = (
        meta_inferences.get(
            "items",
            [],
        )
        if isinstance(
            meta_inferences,
            dict,
        )
        else []
    )

    candidate_statuses = {
        "pending": 0,
        "accepted": 0,
        "rejected": 0,
    }

    for candidate in candidate_items:
        if not isinstance(
            candidate,
            dict,
        ):
            continue

        status = candidate.get(
            "status",
            "pending",
        )

        if status in candidate_statuses:
            candidate_statuses[
                status
            ] += 1

    relations = {
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

        relation = link.get(
            "relation_type",
            "undetermined",
        )

        if relation in relations:
            relations[
                relation
            ] += 1

    link_by_id = {
        link.get("link_id"): link
        for link in links
        if (
            isinstance(link, dict)
            and link.get("link_id")
        )
    }

    source_labels = {
        "eaie-source": "EAIE",
        "etae-source": "ETAE",
        "eqae-source": "EQAE",
        "elae-source": "ELAE",
        "ekde-source": "EKDE",
        "edse-source": "EDSE",
    }

    source_types = {
        "eaie-source": "Résultat quantitatif",
        "etae-source": (
            "Résultat textuel computationnel"
        ),
        "eqae-source": "Résultat qualitatif",
        "elae-source": (
            "Résultat quantitatif exploratoire"
        ),
        "ekde-source": (
            "Résultat quantitatif non supervisé"
        ),
        "edse-source": (
            "Résultat d'aide à la décision"
        ),
    }

    compact_joint_rows = []

    for row in joint_rows:
        if not isinstance(
            row,
            dict,
        ):
            continue

        source_link_id = row.get(
            "source_link_id",
            "",
        )

        link = link_by_id.get(
            source_link_id,
            {},
        )

        source_id_1 = row.get(
            "source_id_1",
            link.get(
                "source_id_1",
                "",
            ),
        )

        source_id_2 = row.get(
            "source_id_2",
            link.get(
                "source_id_2",
                "",
            ),
        )

        compact_joint_rows.append(
            {
                "source_1": {
                    "label": (
                        row.get(
                            "source_label_1",
                            "",
                        )
                        or source_labels.get(
                            source_id_1,
                            "",
                        )
                    ),
                    "type": (
                        row.get(
                            "result_type_label_1",
                            "",
                        )
                        or source_types.get(
                            source_id_1,
                            "",
                        )
                    ),
                    "result": row.get(
                        "result_1",
                        row.get(
                            "quantitative_result",
                            "",
                        ),
                    ),
                },
                "source_2": {
                    "label": (
                        row.get(
                            "source_label_2",
                            "",
                        )
                        or source_labels.get(
                            source_id_2,
                            "",
                        )
                    ),
                    "type": (
                        row.get(
                            "result_type_label_2",
                            "",
                        )
                        or source_types.get(
                            source_id_2,
                            "",
                        )
                    ),
                    "result": row.get(
                        "result_2",
                        row.get(
                            "qualitative_result",
                            "",
                        ),
                    ),
                },
                "relation_type": row.get(
                    "relation_type",
                    "undetermined",
                ),
                "integrated_comment": row.get(
                    "integrated_comment",
                    "",
                ),
                "source_link_id": row.get(
                    "source_link_id",
                    "",
                ),
            }
        )

    compact_inferences = []

    for inference in inference_items:
        if not isinstance(
            inference,
            dict,
        ):
            continue

        compact_inferences.append(
            {
                "statement": inference.get(
                    "statement",
                    "",
                ),
                "link_ids": inference.get(
                    "link_ids",
                    [],
                ),
                "limitations": inference.get(
                    "limitations",
                    [],
                ),
                "researcher_note": inference.get(
                    "researcher_note",
                    "",
                ),
                "validated": bool(
                    inference.get(
                        "validated",
                        False,
                    )
                ),
            }
        )

    validation = {}

    if isinstance(
        summary,
        dict,
    ):
        validation = summary.get(
            "validation",
            {},
        )

    if not isinstance(
        validation,
        dict,
    ):
        validation = {}

    return {
        "sources": {
            "selected_stages": list(
                selected_sources
            ),
            "count": len(
                selected_sources
            ),
        },
        "candidate_statuses": (
            candidate_statuses
        ),
        "relations": relations,
        "joint_display": (
            compact_joint_rows
        ),
        "meta_inferences": (
            compact_inferences
        ),
        "validation": {
            "researcher_validated": bool(
                validation.get(
                    "researcher_validated",
                    False,
                )
            ),
            "researcher_note": validation.get(
                "researcher_note",
                "",
            ),
            "validated_links": validation.get(
                "validated_links",
                0,
            ),
            "validated_meta_inferences": (
                validation.get(
                    "validated_meta_inferences",
                    0,
                )
            ),
            "undetermined_links": (
                validation.get(
                    "undetermined_links",
                    0,
                )
            ),
            "principle": validation.get(
                "principle",
                (
                    "EMIX structure l'intégration "
                    "des résultats sans transformer "
                    "automatiquement les associations "
                    "ou rapprochements en conclusions "
                    "scientifiques ou causales."
                ),
            ),
        },
        "summary": {
            "global": (
                summary.get(
                    "global",
                    {},
                )
                if isinstance(
                    summary,
                    dict,
                )
                else {}
            ),
        },
    }


@callback(
    Output(
        "reports-status",
        "children",
    ),
    Output(
        "reports-preview",
        "children",
    ),
    Output(
        "reports-generated-content",
        "data",
    ),
    Output(
        "reports-generated-filename",
        "data",
    ),
    Output(
        "reports-download-button",
        "disabled",
    ),
    Input(
        "reports-generate",
        "n_clicks",
    ),
    State(
        "reports-title",
        "value",
    ),
    State(
        "reports-sections",
        "value",
    ),
    State(
        "reports-format",
        "value",
    ),
    State(
        "reports-project-id",
        "data",
    ),
    State(
        "reports-dataset-id",
        "data",
    ),
    prevent_initial_call=True,
)
def generate_report(
    n_clicks,
    title,
    selected_sections,
    export_format,
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

    if not selected_sections:
        return (
            dbc.Alert(
                (
                    "Sélectionnez au moins "
                    "une section."
                ),
                color="warning",
            ),
            "",
            None,
            None,
            True,
        )

    project, dataset, dataframe = load_dataset(
        project_id,
        dataset_id,
    )

    if isinstance(dataframe, str):
        return (
            dbc.Alert(
                dataframe,
                color="danger",
            ),
            "",
            None,
            None,
            True,
        )

    analyses = get_all_analyses(
        project_id,
        dataset_id,
    )

    eidpp_context = analyses.get("eidpp")
    elae_context = analyses.get("elae")
    etae_context = analyses.get("etae")
    eqae_context = analyses.get("eqae")
    ekde_context = analyses.get("ekde")
    eaie_context = analyses.get("eaie")
    exaie_context = analyses.get("exaie")
    edse_context = analyses.get("edse")
    emix_context = analyses.get("emix")

    report_title = (
        title.strip()
        if title and title.strip()
        else "Rapport d'analyse EMIDAF"
    )

    engine = ReportEngine(
        title=report_title,
        subtitle=(
            f"Projet : {project.name} — "
            f"Jeu de données : {dataset.name}"
        ),
        summary=(
            "Rapport consolidé des résultats "
            "disponibles dans le pipeline EMIDAF."
        ),
    )

    # ======================================================
    # Projet
    # ======================================================

    if "project" in selected_sections:

        engine.add_stage(
            "project",
            {
                "project_id": project_id,
                "project_name": project.name,
                "dataset_id": dataset_id,
                "dataset_name": dataset.name,
                "observations": len(dataframe),
                "variables": len(
                    dataframe.columns
                ),
                "columns": list(
                    dataframe.columns
                ),
            },
            interpretation=(
                "Cette section décrit le contexte "
                "du projet et le jeu de données "
                "utilisé dans l'analyse."
            ),
        )

    # ======================================================
    # Inspection
    # ======================================================

    if "inspection" in selected_sections:

        missing_total = int(
            dataframe.isna().sum().sum()
        )

        duplicate_rows = int(
            dataframe.duplicated().sum()
        )

        engine.add_stage(
            "inspection",
            {
                "shape": {
                    "rows": len(dataframe),
                    "columns": len(
                        dataframe.columns
                    ),
                },
                "missing_values_total": (
                    missing_total
                ),
                "duplicate_rows": (
                    duplicate_rows
                ),
                "data_types": {
                    column: str(dtype)
                    for column, dtype
                    in dataframe.dtypes.items()
                },
            },
            interpretation=(
                "Synthèse structurelle du jeu "
                "de données chargé dans EMIDAF."
            ),
            limitations=[
                (
                    "Cette synthèse reprend uniquement "
                    "des indicateurs structurels simples. "
                    "Elle ne remplace pas le diagnostic "
                    "complet du module Inspection."
                )
            ],
        )

    # ======================================================
    # Prétraitement
    # ======================================================

    if "preprocessing" in selected_sections:

        if eidpp_context is None:

            engine.add_stage(
                "preprocessing",
                _stage_unavailable(
                    "Prétraitement des données"
                ),
                limitations=[
                    (
                        "Aucun résultat EIDPP "
                        "persisté n'est disponible "
                        "pour ce jeu de données."
                    )
                ],
            )

        else:

            before = eidpp_context.get(
                "before_metrics",
                {},
            )

            after = eidpp_context.get(
                "after_metrics",
                {},
            )

            comparison = [
                {
                    "Indicateur": "Observations",
                    "Avant": before.get(
                        "rows"
                    ),
                    "Après": after.get(
                        "rows"
                    ),
                },
                {
                    "Indicateur": "Variables",
                    "Avant": before.get(
                        "columns"
                    ),
                    "Après": after.get(
                        "columns"
                    ),
                },
                {
                    "Indicateur": "Cellules",
                    "Avant": before.get(
                        "cells"
                    ),
                    "Après": after.get(
                        "cells"
                    ),
                },
                {
                    "Indicateur": (
                        "Valeurs manquantes"
                    ),
                    "Avant": before.get(
                        "missing"
                    ),
                    "Après": after.get(
                        "missing"
                    ),
                },
                {
                    "Indicateur": "Doublons",
                    "Avant": before.get(
                        "duplicates"
                    ),
                    "Après": after.get(
                        "duplicates"
                    ),
                },
            ]

            operations = (
                eidpp_context.get(
                    "operations",
                    {},
                )
                or {}
            )

            transformations = {}

            imputation = operations.get(
                "imputation"
            )

            if imputation not in (
                None,
                "",
                "none",
            ):
                transformations[
                    "Imputation"
                ] = imputation

            duplicates = operations.get(
                "duplicates"
            )

            if duplicates:

                if (
                    isinstance(
                        duplicates,
                        list,
                    )
                    and "remove"
                    in duplicates
                ):
                    transformations[
                        "Doublons"
                    ] = (
                        "Suppression des "
                        "lignes dupliquées"
                    )

                elif duplicates not in (
                    None,
                    "",
                    "none",
                    [],
                ):
                    transformations[
                        "Doublons"
                    ] = duplicates

            outliers = operations.get(
                "outliers"
            )

            if outliers not in (
                None,
                "",
                "none",
            ):
                transformations[
                    "Valeurs aberrantes"
                ] = outliers

            encoding = operations.get(
                "encoding"
            )

            if encoding not in (
                None,
                "",
                "none",
            ):
                transformations[
                    "Encodage"
                ] = encoding

            scaling = operations.get(
                "scaling"
            )

            if scaling not in (
                None,
                "",
                "none",
            ):
                transformations[
                    "Mise à l'échelle"
                ] = scaling

            converted_columns = (
                eidpp_context.get(
                    "converted_columns",
                    [],
                )
                or []
            )

            data = {
                "comparison": comparison,
            }

            if transformations:

                data[
                    "transformations"
                ] = transformations

            else:

                data[
                    "synthese_traitement"
                ] = (
                    "Aucune transformation "
                    "substantielle n'a été "
                    "nécessaire lors de cette "
                    "exécution du prétraitement."
                )

            if converted_columns:

                data[
                    "converted_columns"
                ] = converted_columns

            engine.add_stage(
                "preprocessing",
                data,
                interpretation=(
                    "Le tableau compare l'état du "
                    "jeu de données avant et après "
                    "les traitements réellement "
                    "appliqués par EIDPP. "
                    "Le jeu de données source "
                    "reste inchangé."
                ),
                limitations=[
                    (
                        "Les transformations appliquées "
                        "doivent être interprétées au "
                        "regard de l'objectif analytique "
                        "et de la nature des variables."
                    )
                ],
            )

    # ======================================================
    # ELAE
    # ======================================================

    if "elae" in selected_sections:

        if elae_context is None:

            engine.add_stage(
                "elae",
                _stage_unavailable(
                    "Analyse exploratoire"
                ),
            )

        else:

            engine.add_stage(
                "elae",
                elae_context,
                interpretation=(
                    "Résultats de l'analyse "
                    "exploratoire produits par ELAE."
                ),
            )

    # ======================================================
    # ETAE
    # ======================================================

    if "etae" in selected_sections:

        if etae_context is None:

            engine.add_stage(
                "etae",
                _stage_unavailable(
                    "Analyse textuelle"
                ),
                limitations=[
                    (
                        "Aucune analyse textuelle ETAE "
                        "persistée n'est disponible "
                        "pour ce jeu de données."
                    )
                ],
            )

        else:

            etae_report_data = (
                _compact_etae_for_report(
                    etae_context
                )
            )

            engine.add_stage(
                "etae",
                etae_report_data,
                interpretation=(
                    "Résultats de l'analyse textuelle "
                    "produits par ETAE : profil du corpus, "
                    "fréquences lexicales, n-grammes, "
                    "TF-IDF, sentiment, thèmes, clustering "
                    "textuel et associations avec les "
                    "variables structurées lorsque ces "
                    "analyses sont disponibles."
                ),
                limitations=[
                    (
                        "Les résultats textuels doivent être "
                        "interprétés en tenant compte de la "
                        "diversité réelle du corpus et du "
                        "nombre de textes distincts."
                    )
                ],
            )


    # ======================================================
    # EQAE
    # ======================================================

    if "eqae" in selected_sections:

        if eqae_context is None:

            engine.add_stage(
                "eqae",
                _stage_unavailable(
                    "Analyse qualitative"
                ),
                limitations=[
                    (
                        "Aucune analyse qualitative EQAE "
                        "persistée n'est disponible "
                        "pour ce jeu de données."
                    )
                ],
            )

        else:

            eqae_report_data = (
                _compact_eqae_for_report(
                    eqae_context
                )
            )

            engine.add_stage(
                "eqae",
                eqae_report_data,
                interpretation=(
                    "Synthèse descriptive des éléments "
                    "d'analyse qualitative produits dans "
                    "EQAE : codebook, affectations de codes, "
                    "codage assisté validé par le chercheur, "
                    "structure thématique, verbatims, "
                    "cooccurrences, mémos et synthèse "
                    "qualitative lorsque ces éléments sont "
                    "disponibles."
                ),
                limitations=[
                    (
                        "Les thèmes et interprétations "
                        "qualitatives relèvent de la validation "
                        "du chercheur et ne doivent pas être "
                        "assimilés automatiquement aux thèmes "
                        "algorithmiques produits par ETAE."
                    ),
                    (
                        "Les fréquences, cooccurrences et "
                        "suggestions assistées sont des aides "
                        "descriptives ; elles ne constituent "
                        "pas, à elles seules, une preuve "
                        "d'interprétation qualitative."
                    ),
                ],
            )

    # ======================================================
    # EKDE
    # ======================================================

    if "ekde" in selected_sections:

        if ekde_context is None:

            engine.add_stage(
                "ekde",
                _stage_unavailable(
                    "Découverte de connaissances"
                ),
            )

        else:

            ekde_report_data = (
                _compact_ekde_for_report(
                    ekde_context
                )
            )

            engine.add_stage(
                "ekde",
                ekde_report_data,
                interpretation=(
                    "Synthèse des résultats de découverte "
                    "de connaissances produits par EKDE. "
                    "Les données techniques volumineuses "
                    "sans intérêt direct pour "
                    "l'interprétation sont omises du rapport."
                ),
            )

    # ======================================================
    # EAIE
    # ======================================================

    if "eaie" in selected_sections:

        if eaie_context is None:

            engine.add_stage(
                "eaie",
                _stage_unavailable(
                    "Modélisation prédictive"
                ),
                limitations=[
                    (
                        "Aucune exécution EAIE "
                        "persistée n'est disponible "
                        "pour ce jeu de données."
                    )
                ],
            )

        else:

            cv_mean = eaie_context.get(
                "cv_mean"
            )

            test_score = eaie_context.get(
                "test_score"
            )

            baseline_cv_mean = (
                eaie_context.get(
                    "baseline_cv_mean"
                )
            )

            better_than_baseline = (
                eaie_context.get(
                    "better_than_baseline"
                )
            )

            limitations = []

            if (
                eaie_context.get("task")
                == "regression"
                and (
                    (
                        cv_mean is not None
                        and cv_mean <= 0
                    )
                    or (
                        test_score is not None
                        and test_score <= 0
                    )
                )
            ):
                limitations.append(
                    (
                        "La capacité prédictive "
                        "du modèle n'est pas "
                        "convaincante au regard "
                        "des scores observés."
                    )
                )

            if better_than_baseline is False:
                limitations.append(
                    (
                        "Le modèle sélectionné ne "
                        "dépasse pas la référence "
                        "naïve en validation croisée."
                    )
                )

            engine.add_stage(
                "eaie",
                {
                    "model": (
                        eaie_context.get(
                            "model_name"
                        )
                    ),
                    "task": (
                        eaie_context.get(
                            "task"
                        )
                    ),
                    "target": (
                        eaie_context.get(
                            "target"
                        )
                    ),
                    "features": (
                        eaie_context.get(
                            "features",
                            [],
                        )
                    ),
                    "cv_mean": cv_mean,
                    "cv_std": (
                        eaie_context.get(
                            "cv_std"
                        )
                    ),
                    "test_score": test_score,
                    "baseline_cv_mean": (
                        baseline_cv_mean
                    ),
                    "better_than_baseline": (
                        better_than_baseline
                    ),
                },
                interpretation=(
                    "Résultats issus du modèle "
                    "sélectionné par EAIE sur la "
                    "validation croisée. La comparaison "
                    "à la référence naïve est conservée "
                    "lorsqu'elle est disponible."
                ),
                limitations=limitations,
            )

    # ======================================================
    # EXAIE
    # ======================================================

    if "exaie" in selected_sections:

        if exaie_context is None:

            engine.add_stage(
                "exaie",
                _stage_unavailable(
                    "Explicabilité des modèles"
                ),
                limitations=[
                    (
                        "Aucune analyse EXAIE "
                        "persistée n'est disponible."
                    )
                ],
            )

        else:

            summary = (
                exaie_context.get(
                    "summary",
                    {},
                )
                or {}
            )

            cv_mean = exaie_context.get(
                "cv_mean"
            )

            cv_std = exaie_context.get(
                "cv_std"
            )

            test_score = exaie_context.get(
                "test_score"
            )

            performance = {
                "Score moyen en validation croisée": (
                    round(
                        float(cv_mean),
                        4,
                    )
                    if cv_mean is not None
                    else None
                ),
                "Écart-type en validation croisée": (
                    round(
                        float(cv_std),
                        4,
                    )
                    if cv_std is not None
                    else None
                ),
                "Score sur le jeu de test": (
                    round(
                        float(test_score),
                        4,
                    )
                    if test_score is not None
                    else None
                ),
            }

            exaie_data = {
                "model": (
                    exaie_context.get(
                        "model_name"
                    )
                ),
                "task": (
                    exaie_context.get(
                        "task"
                    )
                ),
                "target": (
                    exaie_context.get(
                        "target"
                    )
                ),
                "performance": performance,
            }

            native_importance = (
                exaie_context.get(
                    "native_importance"
                )
            )

            if native_importance is not None:
                exaie_data[
                    "importance_native"
                ] = {
                    "results": native_importance,
                    "interpretation": (
                        summary.get(
                            "native_interpretation"
                        )
                    ),
                }

            permutation_importance = (
                exaie_context.get(
                    "permutation_importance"
                )
            )

            if permutation_importance is not None:
                exaie_data[
                    "importance_permutation"
                ] = {
                    "results": (
                        permutation_importance
                    ),
                    "interpretation": (
                        summary.get(
                            "permutation_interpretation"
                        )
                    ),
                }

            local_explanation = (
                exaie_context.get(
                    "local_explanation"
                )
            )

            if local_explanation is not None:
                exaie_data[
                    "local_explanation"
                ] = local_explanation

            shap_context = (
                exaie_context.get(
                    "shap"
                )
            )

            if shap_context is not None:
                exaie_data[
                    "shap"
                ] = shap_context

            predictive_warning = (
                exaie_context.get(
                    "predictive_warning"
                )
            )

            if predictive_warning:
                exaie_data[
                    "predictive_warning"
                ] = predictive_warning

            engine.add_stage(
                "exaie",
                exaie_data,
                interpretation=(
                    "EXAIE explique le comportement "
                    "du modèle sélectionné par EAIE. "
                    "Le rapport reprend les résultats "
                    "globaux, par permutation, locaux "
                    "et SHAP réellement persistés "
                    "lorsqu'ils sont disponibles."
                ),
                limitations=(
                    exaie_context.get(
                        "limitations",
                        [
                            (
                                "Les importances et "
                                "explications prédictives "
                                "décrivent le comportement "
                                "du modèle et ne constituent "
                                "pas une preuve de causalité."
                            )
                        ],
                    )
                ),
            )

    # ======================================================
    # EDSE
    # ======================================================

    if "edse" in selected_sections:

        if edse_context is None:

            engine.add_stage(
                "edse",
                _stage_unavailable(
                    "Aide à la décision"
                ),
                limitations=[
                    (
                        "Aucune analyse EDSE "
                        "persistée n'est disponible."
                    )
                ],
            )

        else:

            engine.add_stage(
                "edse",
                {
                    "model": (
                        edse_context.get(
                            "model_name"
                        )
                    ),
                    "task": (
                        edse_context.get(
                            "task"
                        )
                    ),
                    "target": (
                        edse_context.get(
                            "target"
                        )
                    ),
                    "threshold": (
                        edse_context.get(
                            "threshold"
                        )
                    ),
                    "direction": (
                        edse_context.get(
                            "direction"
                        )
                    ),
                    "summary": (
                        edse_context.get(
                            "summary"
                        )
                    ),
                    "scenario": (
                        edse_context.get(
                            "scenario"
                        )
                    ),
                    "profiles": (
                        edse_context.get(
                            "profiles"
                        )
                    ),
                },
                interpretation=(
                    "Les résultats EDSE fournissent "
                    "une aide structurée à l'analyse "
                    "de scénarios. Le rapport reprend "
                    "le scénario et les profils "
                    "persistés sans recalculer le modèle "
                    "et sans prendre la décision à la "
                    "place de l'utilisateur."
                ),
                limitations=[
                    (
                        "Les seuils décisionnels "
                        "doivent être définis et "
                        "justifiés selon le contexte "
                        "d'utilisation."
                    ),
                    (
                        "Les résultats prédictifs "
                        "doivent être considérés avec "
                        "les performances et limites "
                        "du modèle EAIE."
                    ),
                    (
                        "Les profils et observations "
                        "présentés ne constituent pas "
                        "une priorisation normative."
                    ),
                ],
            )

    # ======================================================
    # EMIX
    # ======================================================

    if "emix" in selected_sections:

        if emix_context is None:

            engine.add_stage(
                "emix",
                _stage_unavailable(
                    "Intégration des méthodes mixtes"
                ),
                limitations=[
                    (
                        "Aucune analyse EMIX persistée "
                        "n'est disponible pour ce jeu "
                        "de données."
                    )
                ],
            )

        else:

            emix_report_data = (
                _compact_emix_for_report(
                    emix_context
                )
            )

            engine.add_stage(
                "emix",
                emix_report_data,
                interpretation=(
                    "Synthèse de l'intégration des "
                    "résultats réalisée dans EMIX : "
                    "sources retenues, candidats, "
                    "liens validés, Joint Display, "
                    "méta-inférences et état de "
                    "validation du chercheur."
                ),
                limitations=[
                    (
                        "EMIX structure les "
                        "rapprochements entre résultats "
                        "issus de différentes composantes "
                        "analytiques sans produire "
                        "automatiquement de conclusion "
                        "scientifique ou causale."
                    ),
                    (
                        "Les thèmes computationnels ETAE "
                        "ne doivent pas être assimilés "
                        "automatiquement aux thèmes "
                        "qualitatifs construits dans EQAE."
                    ),
                    (
                        "Les relations de convergence, "
                        "complémentarité, divergence ou "
                        "indétermination résultent d'une "
                        "qualification explicite du "
                        "chercheur."
                    ),
                ],
            )


    report = engine.build()

    if export_format == "markdown":

        content = ReportRenderer.markdown(
            report
        )

        extension = "md"

    elif export_format == "json":

        content = ReportRenderer.json(
            report
        )

        extension = "json"

    else:

        content = ReportRenderer.html(
            report
        )

        extension = "html"

    filename = (
        "rapport_emidaf_"
        f"projet_{project_id}_"
        f"dataset_{dataset_id}."
        f"{extension}"
    )

    sections = report.metadata.get(
        "structured_sections",
        [],
    )

    def _preview_scalar(value):

        if value is None:
            return "—"

        if isinstance(value, bool):
            return "Oui" if value else "Non"

        if isinstance(value, float):
            return f"{value:.4f}"

        if isinstance(value, list):
            return ", ".join(
                str(item)
                for item in value
            )

        return str(value)


    def _preview_table(data):

        if not isinstance(data, dict):
            return html.Pre(
                json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=2,
                    default=str,
                ),
                className="mb-0",
            )

        rows = []

        simple_values = {}

        for key, value in data.items():

            if isinstance(
                value,
                (
                    dict,
                    list,
                    tuple,
                ),
            ):
                continue

            simple_values[key] = value

        if simple_values:

            for key, value in simple_values.items():

                label = (
                    str(key)
                    .replace("_", " ")
                    .capitalize()
                )

                rows.append(
                    html.Tr(
                        [
                            html.Th(
                                label,
                                style={
                                    "width": "45%",
                                    "fontWeight": "600",
                                },
                            ),
                            html.Td(
                                _preview_scalar(
                                    value
                                )
                            ),
                        ]
                    )
                )

        components = []

        if rows:

            components.append(
                dbc.Table(
                    [
                        html.Tbody(rows)
                    ],
                    bordered=False,
                    hover=True,
                    responsive=True,
                    size="sm",
                    className="mb-3",
                )
            )

        for key, value in data.items():

            if not isinstance(
                value,
                (
                    dict,
                    list,
                    tuple,
                ),
            ):
                continue

            label = (
                str(key)
                .replace("_", " ")
                .capitalize()
            )

            components.append(
                html.H6(
                    label,
                    className=(
                        "fw-semibold "
                        "text-primary mt-3"
                    ),
                )
            )

            if isinstance(value, dict):

                nested_rows = []

                for nested_key, nested_value in value.items():

                    nested_rows.append(
                        html.Tr(
                            [
                                html.Th(
                                    str(
                                        nested_key
                                    )
                                    .replace(
                                        "_",
                                        " ",
                                    )
                                    .capitalize(),
                                    style={
                                        "width": "45%",
                                    },
                                ),
                                html.Td(
                                    _preview_scalar(
                                        nested_value
                                    )
                                ),
                            ]
                        )
                    )

                components.append(
                    dbc.Table(
                        [
                            html.Tbody(
                                nested_rows
                            )
                        ],
                        bordered=False,
                        hover=True,
                        responsive=True,
                        size="sm",
                    )
                )

            else:

                components.append(
                    html.Ul(
                        [
                            html.Li(
                                _preview_scalar(
                                    item
                                )
                            )
                            for item in value
                        ]
                    )
                )

        if not components:

            return dbc.Alert(
                "Aucun résultat détaillé.",
                color="secondary",
            )

        return html.Div(
            components
        )


    preview_items = []

    for index, section in enumerate(
        sections,
        start=1,
    ):

        interpretation = section.get(
            "interpretation",
            "",
        )

        limitations = section.get(
            "limitations",
            [],
        )

        card_content = [

            html.Div(
                [
                    html.Span(
                        f"{index:02d}",
                        className=(
                            "badge bg-primary "
                            "rounded-pill me-2"
                        ),
                    ),

                    html.Span(
                        section["title"],
                        className="fw-semibold",
                    ),
                ],
                className="mb-3",
            ),

            _preview_table(
                section.get(
                    "data"
                )
            ),
        ]

        if interpretation:

            card_content.append(
                dbc.Alert(
                    [
                        html.Strong(
                            "Interprétation"
                        ),
                        html.Br(),
                        interpretation,
                    ],
                    color="info",
                    className="mt-3 mb-2",
                )
            )

        if limitations:

            card_content.append(
                dbc.Alert(
                    [
                        html.Strong(
                            "Limites méthodologiques"
                        ),
                        html.Ul(
                            [
                                html.Li(
                                    limitation
                                )
                                for limitation
                                in limitations
                            ],
                            className="mb-0 mt-2",
                        ),
                    ],
                    color="warning",
                    className="mt-2 mb-0",
                )
            )

        preview_items.append(
            dbc.Card(
                dbc.CardBody(
                    card_content
                ),
                className=(
                    "mb-4 shadow-sm "
                    "border-0"
                ),
                style={
                    "borderRadius": "12px",
                },
            )
        )
    return (
        dbc.Alert(
            (
                "Rapport généré avec succès. "
                f"{len(sections)} section(s) "
                "ont été intégrées."
            ),
            color="success",
        ),
        preview_items,
        content,
        filename,
        False,
    )


@callback(
    Output(
        "reports-download",
        "data",
    ),
    Input(
        "reports-download-button",
        "n_clicks",
    ),
    State(
        "reports-generated-content",
        "data",
    ),
    State(
        "reports-generated-filename",
        "data",
    ),
    prevent_initial_call=True,
)
def download_report(
    n_clicks,
    content,
    filename,
):

    if (
        not n_clicks
        or not content
        or not filename
    ):
        return no_update

    content_type = "text/plain"

    if filename.endswith(".html"):
        content_type = "text/html; charset=utf-8"

    elif filename.endswith(".json"):
        content_type = "application/json"

    elif filename.endswith(".md"):
        content_type = "text/markdown; charset=utf-8"

    return dcc.send_string(
        content,
        filename,
        type=content_type,
    )
