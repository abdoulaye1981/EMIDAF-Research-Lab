"""
=========================================================
EMIDAF Studio
EQAE - Callbacks
=========================================================
"""

from __future__ import annotations

import logging

import pandas as pd

from dash import (
    Input,
    Output,
    State,
    callback,
    ctx,
)

import dash_bootstrap_components as dbc

from emidaf_core.eqae import (
    CodingSuggestion,
    EQAEEngine,
    QualitativeSegment,
)

from emidaf_studio.pages.inspection.layout import (
    load_dataset,
)

from .components import (
    _eqae_codebook_options,
    eqae_assisted_component,
    eqae_assisted_table,
    eqae_themes_component,
    eqae_themes_table,
    eqae_quotations_component,
    eqae_quotations_table,
    eqae_cooccurrence_component,
    eqae_cooccurrence_pairs_table,
    eqae_cooccurrence_matrix_table,
    eqae_memos_component,
    eqae_memos_table,
    eqae_summary_component,
    eqae_summary_code_table,
    eqae_summary_theme_table,
    eqae_assignments_table,
    eqae_codebook_component,
    eqae_codebook_table,
    eqae_coding_component,
    eqae_corpus_component,
    eqae_intro_component,
)


logger = logging.getLogger(__name__)


def _load_eqae_dataframe(
    project_id,
    dataset_id,
) -> pd.DataFrame:
    """
    Recharge le dataset autorisé.

    Le DataFrame complet ne transite jamais
    par dcc.Store.
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
            "Le dataset EQAE est indisponible."
        )

    return result


def _persist_eqae_section(
    project_id,
    dataset_id,
    section,
    payload,
):
    """
    Persiste une sous-section EQAE dans
    le registre analytique générique EMIDAF.
    """

    from emidaf_studio.services.model_registry import (
        merge_analysis_section,
    )

    return merge_analysis_section(
        int(project_id),
        int(dataset_id),
        "eqae",
        section,
        payload,
    )


def _load_eqae_section(
    project_id,
    dataset_id,
    section,
    default=None,
):
    """
    Recharge une sous-section EQAE persistée.
    """

    from emidaf_studio.services.model_registry import (
        get_analysis,
    )

    result = get_analysis(
        int(project_id),
        int(dataset_id),
        "eqae",
        default={},
    )

    if not isinstance(result, dict):
        return default

    return result.get(
        section,
        default,
    )


def _restore_codebook(
    payload,
    *,
    name_override=None,
    description_override=None,
):
    """
    Reconstruit un Codebook EQAE depuis sa
    représentation persistée.

    Les identifiants originaux sont conservés.
    """

    payload = (
        payload
        if isinstance(payload, dict)
        else {}
    )

    name = (
        str(name_override).strip()
        if name_override is not None
        else str(
            payload.get(
                "name",
                "Codebook qualitatif",
            )
        ).strip()
    )

    description = (
        str(description_override).strip()
        if description_override is not None
        else str(
            payload.get(
                "description",
                "",
            )
        ).strip()
    )

    engine = EQAEEngine()

    codebook = engine.create_codebook(
        name,
        description=description,
    )

    pending = [
        dict(code)
        for code in payload.get(
            "codes",
            [],
        )
        if isinstance(code, dict)
    ]

    while pending:

        progressed = False

        for code in pending[:]:

            parent_id = code.get(
                "parent_code_id"
            )

            if (
                parent_id is not None
                and codebook.get_code(
                    parent_id
                ) is None
            ):
                continue

            codebook.add_code(
                code.get(
                    "name",
                    "",
                ),
                description=code.get(
                    "description",
                    "",
                ),
                parent_code_id=parent_id,
                color=code.get(
                    "color"
                ),
                code_id=code.get(
                    "code_id"
                ),
            )

            pending.remove(
                code
            )

            progressed = True

        if not progressed:
            raise ValueError(
                "Le codebook persisté contient "
                "une hiérarchie parent/enfant "
                "incohérente."
            )

    return codebook


def _restore_coder(
    codebook,
    segments,
    payload,
):
    """
    Reconstruit le QualitativeCoder EQAE
    depuis les affectations persistées.
    """

    engine = EQAEEngine()

    coder = engine.create_coder(
        codebook
    )

    segment_map = {
        segment.segment_id: segment
        for segment in segments
    }

    payload = (
        payload
        if isinstance(payload, dict)
        else {}
    )

    for item in payload.get(
        "assignments",
        [],
    ):

        if not isinstance(
            item,
            dict,
        ):
            continue

        segment_id = item.get(
            "segment_id"
        )

        segment = segment_map.get(
            segment_id
        )

        if segment is None:
            raise ValueError(
                "Une affectation persistée référence "
                "un segment absent du corpus : "
                f"{segment_id}"
            )

        coder.assign_code(
            segment=segment,
            code_id=item.get(
                "code_id",
                "",
            ),
            mode=item.get(
                "mode",
                "manual",
            ),
            memo=item.get(
                "memo",
                "",
            ),
            assignment_id=item.get(
                "assignment_id"
            ),
        )

    return coder


def _restore_assisted_manager(
    codebook,
    coder,
    segments,
    payload,
):
    """
    Restaure le gestionnaire de codage assisté
    sans rejouer les décisions déjà validées.
    """

    engine = EQAEEngine()

    manager = (
        engine.create_assisted_coding_manager(
            codebook=codebook,
            coder=coder,
        )
    )

    segment_map = {
        segment.segment_id: segment
        for segment in segments
    }

    payload = (
        payload
        if isinstance(payload, dict)
        else {}
    )

    for item in payload.get(
        "suggestions",
        [],
    ):

        if not isinstance(
            item,
            dict,
        ):
            continue

        segment = segment_map.get(
            item.get("segment_id")
        )

        if segment is None:
            raise ValueError(
                "Une suggestion persistée référence "
                "un segment absent du corpus."
            )

        suggestion = CodingSuggestion(
            suggestion_id=item.get(
                "suggestion_id",
                "",
            ),
            segment_id=item.get(
                "segment_id",
                "",
            ),
            document_id=item.get(
                "document_id",
                "",
            ),
            suggested_code_id=item.get(
                "suggested_code_id",
                "",
            ),
            confidence=item.get(
                "confidence"
            ),
            rationale=item.get(
                "rationale",
                "",
            ),
            source=item.get(
                "source",
                "assisted",
            ),
            status=item.get(
                "status",
                "pending",
            ),
            reviewed_code_id=item.get(
                "reviewed_code_id"
            ),
            reviewer_note=item.get(
                "reviewer_note",
                "",
            ),
        )

        manager.restore_suggestion(
            segment=segment,
            suggestion=suggestion,
        )

    return manager


def _restore_thematic_analysis(
    codebook,
    payload,
):
    """
    Reconstruit l'analyse thématique EQAE
    en conservant les identifiants persistés.
    """

    engine = EQAEEngine()

    analysis = (
        engine.create_thematic_analysis(
            codebook
        )
    )

    payload = (
        payload
        if isinstance(payload, dict)
        else {}
    )

    items = [
        item
        for item in payload.get(
            "themes",
            [],
        )
        if isinstance(item, dict)
    ]

    pending = list(items)

    while pending:

        progress = False
        remaining = []

        for item in pending:

            parent_id = item.get(
                "parent_theme_id"
            )

            if (
                parent_id is not None
                and analysis.get_theme(
                    parent_id
                )
                is None
            ):
                remaining.append(item)
                continue

            analysis.add_theme(
                name=item.get(
                    "name",
                    "",
                ),
                description=item.get(
                    "description",
                    "",
                ),
                parent_theme_id=(
                    parent_id
                ),
                theme_id=item.get(
                    "theme_id"
                ),
            )

            progress = True

        if not progress and remaining:
            raise ValueError(
                "Hiérarchie thématique "
                "persistée incohérente."
            )

        pending = remaining

    # Les liens code-thème sont restaurés
    # après la hiérarchie.
    for item in items:

        theme_id = item.get(
            "theme_id"
        )

        for code_id in item.get(
            "code_ids",
            [],
        ):
            analysis.link_code(
                theme_id=theme_id,
                code_id=code_id,
            )

    return analysis


def _restore_quotation_manager(
    *,
    coder,
    thematic_analysis,
    segments,
    payload,
):
    """
    Reconstruit le gestionnaire de verbatims EQAE
    en conservant les quotation_id persistés.
    """

    engine = EQAEEngine()

    manager = (
        engine.create_quotation_manager(
            coder=coder,
            thematic_analysis=(
                thematic_analysis
            ),
        )
    )

    segment_map = {
        segment.segment_id: segment
        for segment in segments
    }

    payload = (
        payload
        if isinstance(payload, dict)
        else {}
    )

    for item in payload.get(
        "quotations",
        [],
    ):

        if not isinstance(
            item,
            dict,
        ):
            continue

        segment_id = item.get(
            "segment_id"
        )

        segment = segment_map.get(
            segment_id
        )

        if segment is None:
            raise ValueError(
                "Un verbatim persisté référence "
                "un segment absent du corpus : "
                f"{segment_id}"
            )

        manager.add_quotation(
            segment=segment,
            note=item.get(
                "note",
                "",
            ),
            quotation_id=item.get(
                "quotation_id"
            ),
        )

    return manager


def _restore_memo_manager(
    payload,
):
    """
    Reconstruit le MemoManager EQAE
    en conservant identifiants et dates.
    """

    engine = EQAEEngine()

    manager = engine.create_memo_manager()

    payload = (
        payload
        if isinstance(payload, dict)
        else {}
    )

    for item in payload.get(
        "memos",
        [],
    ):

        if not isinstance(
            item,
            dict,
        ):
            continue

        manager.add_memo(
            title=item.get(
                "title",
                "",
            ),
            content=item.get(
                "content",
                "",
            ),
            target_type=item.get(
                "target_type",
                "analysis",
            ),
            target_id=item.get(
                "target_id"
            ),
            author=item.get(
                "author"
            ),
            memo_id=item.get(
                "memo_id"
            ),
            created_at=item.get(
                "created_at"
            ),
        )

    return manager


def _qualitative_columns(
    dataframe: pd.DataFrame,
) -> list[str]:
    """
    Colonnes susceptibles de contenir du texte qualitatif.

    Cette sélection reste volontairement permissive :
    le chercheur conserve la sélection finale.
    """

    columns = []

    for column in dataframe.columns:

        series = dataframe[column]

        if (
            pd.api.types.is_object_dtype(
                series.dtype
            )
            or pd.api.types.is_string_dtype(
                series.dtype
            )
            or isinstance(
                series.dtype,
                pd.CategoricalDtype,
            )
        ):
            columns.append(
                str(column)
            )

    return columns


def _build_initial_segments(
    dataframe: pd.DataFrame,
    *,
    column: str,
) -> tuple[
    list[QualitativeSegment],
    int,
    int,
]:
    """
    Stratégie initiale :
    1 valeur textuelle valide = 1 document = 1 segment.

    Les identifiants sont déterministes par position
    afin de rester stables entre deux callbacks
    sur un dataset inchangé.
    """

    if column not in dataframe.columns:
        raise ValueError(
            f"Variable introuvable : {column}"
        )

    series = dataframe[column]

    n_missing = int(
        series.isna().sum()
    )

    segments = []
    n_empty = 0

    for position, value in enumerate(
        series.tolist()
    ):

        if pd.isna(value):
            continue

        text = str(
            value
        ).strip()

        if not text:
            n_empty += 1
            continue

        document_id = (
            f"row-{position}"
        )

        segment_id = (
            f"{column}:row-{position}:segment-0"
        )

        segment = QualitativeSegment.create(
            document_id=document_id,
            segment_id=segment_id,
            text=text,
            start=0,
            end=len(text),
            metadata={
                "row_position": position,
                "source_column": column,
                "segmentation_strategy": (
                    "document_entier"
                ),
            },
        )

        segments.append(
            segment
        )

    return (
        segments,
        n_missing,
        n_empty,
    )


@callback(
    Output(
        "eqae-text-column",
        "options",
    ),
    Output(
        "eqae-text-column",
        "value",
    ),
    Output(
        "eqae-text-column-status",
        "children",
    ),
    Input(
        "eqae-project-id",
        "data",
    ),
    Input(
        "eqae-dataset-id",
        "data",
    ),
)
def initialize_eqae_columns(
    project_id,
    dataset_id,
):
    """
    Initialise les colonnes qualitatives disponibles.
    """

    if (
        project_id is None
        or dataset_id is None
    ):
        return (
            [],
            None,
            dbc.Alert(
                (
                    "Projet ou jeu de données "
                    "indisponible."
                ),
                color="warning",
                className="py-2 mb-0",
            ),
        )

    try:
        dataframe = _load_eqae_dataframe(
            project_id,
            dataset_id,
        )

        columns = _qualitative_columns(
            dataframe
        )

        options = [
            {
                "label": column,
                "value": column,
            }
            for column in columns
        ]

        selected = (
            columns[0]
            if columns
            else None
        )

        if columns:
            message = (
                f"{len(columns)} variable(s) "
                "qualitative(s) candidate(s) "
                "disponible(s). La sélection "
                "reste sous le contrôle du chercheur."
            )
            color = "success"
        else:
            message = (
                "Aucune colonne textuelle ou "
                "catégorielle candidate n'a été "
                "identifiée dans ce dataset."
            )
            color = "warning"

        return (
            options,
            selected,
            dbc.Alert(
                message,
                color=color,
                className="py-2 mb-0",
            ),
        )

    except Exception as exc:
        logger.exception(
            "Erreur initialisation corpus EQAE"
        )

        return (
            [],
            None,
            dbc.Alert(
                str(exc),
                color="danger",
                className="py-2 mb-0",
            ),
        )


_TAB_CONTENT = {
    "eqae-tab-codebook": (
        "Codebook",
        (
            "Créer, documenter et organiser les codes "
            "qualitatifs utilisés par le chercheur."
        ),
        (
            "Chaque code doit conserver une définition "
            "explicite afin de renforcer la traçabilité "
            "du processus de codage."
        ),
    ),

    "eqae-tab-coding": (
        "Codage qualitatif",
        (
            "Affecter manuellement un ou plusieurs codes "
            "aux segments et verbatims du corpus."
        ),
        (
            "Le codage manuel constitue un résultat "
            "validé directement par le chercheur."
        ),
    ),

    "eqae-tab-assisted": (
        "Codage assisté",
        (
            "Examiner les suggestions de codage produites "
            "par les mécanismes d'assistance."
        ),
        (
            "Une suggestion reste en attente tant qu'elle "
            "n'a pas été acceptée, modifiée ou rejetée "
            "par le chercheur."
        ),
    ),

    "eqae-tab-themes": (
        "Thèmes et sous-thèmes",
        (
            "Structurer les codes en thèmes et sous-thèmes "
            "issus de l'interprétation qualitative."
        ),
        (
            "Un thème EQAE est une construction analytique "
            "validée par le chercheur ; il ne doit pas être "
            "confondu avec un topic algorithmique ETAE."
        ),
    ),

    "eqae-tab-quotations": (
        "Verbatims",
        (
            "Sélectionner les extraits textuels qui "
            "illustrent et documentent les codes et thèmes."
        ),
        (
            "Les verbatims servent à étayer "
            "l'interprétation qualitative."
        ),
    ),

    "eqae-tab-cooccurrence": (
        "Cooccurrences de codes",
        (
            "Étudier les codes apparaissant conjointement "
            "dans les mêmes segments ou documents."
        ),
        (
            "La fréquence de cooccurrence est descriptive "
            "et ne constitue pas, à elle seule, une "
            "interprétation qualitative."
        ),
    ),

    "eqae-tab-memos": (
        "Mémos analytiques",
        (
            "Consigner les réflexions, décisions, "
            "hypothèses et pistes interprétatives "
            "du chercheur."
        ),
        (
            "Les mémos assurent la traçabilité "
            "du raisonnement analytique."
        ),
    ),

    "eqae-tab-summary": (
        "Synthèse qualitative",
        (
            "Regrouper les principaux indicateurs EQAE, "
            "codes, thèmes, verbatims et décisions "
            "de codage."
        ),
        (
            "La synthèse descriptive organise les "
            "résultats ; elle ne remplace pas "
            "l'interprétation scientifique."
        ),
    ),
}


@callback(
    Output(
        "eqae-tab-content",
        "children",
    ),
    Input(
        "eqae-tabs",
        "active_tab",
    ),
    Input(
        "eqae-project-id",
        "data",
    ),
    Input(
        "eqae-dataset-id",
        "data",
    ),
    Input(
        "eqae-text-column",
        "value",
    ),
    Input(
        "eqae-segmentation-strategy",
        "value",
    ),
)
def render_eqae_tab(
    active_tab,
    project_id,
    dataset_id,
    text_column,
    segmentation_strategy,
):
    """
    Rend le contenu de l'onglet EQAE actif.
    """

    if active_tab == "eqae-tab-corpus":

        if not text_column:
            return dbc.Alert(
                (
                    "Sélectionnez une variable "
                    "qualitative pour construire "
                    "le corpus."
                ),
                color="warning",
            )

        if (
            segmentation_strategy
            != "document_entier"
        ):
            return dbc.Alert(
                (
                    "La stratégie de segmentation "
                    "sélectionnée n'est pas encore "
                    "disponible."
                ),
                color="warning",
            )

        try:
            dataframe = (
                _load_eqae_dataframe(
                    project_id,
                    dataset_id,
                )
            )

            (
                segments,
                n_missing,
                n_empty,
            ) = _build_initial_segments(
                dataframe,
                column=text_column,
            )

            preview_rows = []

            for segment in segments[:10]:
                preview_rows.append(
                    {
                        "Document": (
                            segment.document_id
                        ),
                        "Segment": (
                            segment.segment_id
                        ),
                        "Texte": (
                            segment.text[:250]
                            + (
                                "…"
                                if len(segment.text)
                                > 250
                                else ""
                            )
                        ),
                    }
                )

            preview = pd.DataFrame(
                preview_rows,
                columns=[
                    "Document",
                    "Segment",
                    "Texte",
                ],
            )

            _persist_eqae_section(
                project_id,
                dataset_id,
                "corpus",
                {
                    "schema_version": 1,
                    "text_column": text_column,
                    "segmentation_strategy": (
                        "document_entier"
                    ),
                    "n_rows": int(
                        len(dataframe)
                    ),
                    "n_valid_documents": int(
                        len(segments)
                    ),
                    "n_missing": int(
                        n_missing
                    ),
                    "n_empty": int(
                        n_empty
                    ),
                    "n_segments": int(
                        len(segments)
                    ),
                    "preview": [
                        dict(row)
                        for row in preview_rows
                    ],
                    "reproducibility": {
                        "document_id_strategy": (
                            "row-position"
                        ),
                        "segment_id_strategy": (
                            "column:row-position:"
                            "segment-index"
                        ),
                        "segment_start": 0,
                        "source": "dataset",
                    },
                },
            )

            return eqae_corpus_component(
                n_rows=len(dataframe),
                n_valid_documents=(
                    len(segments)
                ),
                n_missing=n_missing,
                n_empty=n_empty,
                n_segments=len(segments),
                preview=preview,
                column=text_column,
            )

        except Exception as exc:
            logger.exception(
                "Erreur construction corpus EQAE"
            )

            return dbc.Alert(
                str(exc),
                color="danger",
            )

    if active_tab == "eqae-tab-summary":

        try:
            summary_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "summary",
                    default={},
                )
            )

            memos_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "memos",
                    default={},
                )
            )

            n_memos = len(
                memos_payload.get(
                    "memos",
                    [],
                )
                if isinstance(
                    memos_payload,
                    dict,
                )
                else []
            )

            return eqae_summary_component(
                summary_payload=(
                    summary_payload
                ),
                n_memos=n_memos,
            )

        except Exception as exc:
            logger.exception(
                "Erreur chargement synthèse EQAE"
            )

            return dbc.Alert(
                str(exc),
                color="danger",
            )

    if active_tab == "eqae-tab-memos":

        try:
            dataframe = _load_eqae_dataframe(
                project_id,
                dataset_id,
            )

            segments, _, _ = (
                _build_initial_segments(
                    dataframe,
                    column=text_column,
                )
            )

            codebook_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "codebook",
                    default={},
                )
            )

            themes_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "themes",
                    default={},
                )
            )

            quotations_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "quotations",
                    default={},
                )
            )

            memos_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "memos",
                    default={},
                )
            )

            return eqae_memos_component(
                memos_payload=memos_payload,
                codebook_payload=(
                    codebook_payload
                ),
                themes_payload=(
                    themes_payload
                ),
                quotations_payload=(
                    quotations_payload
                ),
                segments=segments,
            )

        except Exception as exc:
            logger.exception(
                "Erreur chargement mémos EQAE"
            )

            return dbc.Alert(
                str(exc),
                color="danger",
            )

    if active_tab == "eqae-tab-cooccurrence":

        try:
            codebook_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "codebook",
                    default=None,
                )
            )

            if not codebook_payload:
                raise ValueError(
                    "Créez d'abord un Codebook."
                )

            payload = _load_eqae_section(
                project_id,
                dataset_id,
                "cooccurrence",
                default={},
            )

            return eqae_cooccurrence_component(
                payload=payload,
                codebook_payload=(
                    codebook_payload
                ),
            )

        except Exception as exc:
            logger.exception(
                "Erreur chargement cooccurrences EQAE"
            )

            return dbc.Alert(
                str(exc),
                color="danger",
            )

    if active_tab == "eqae-tab-quotations":

        try:
            if not text_column:
                raise ValueError(
                    "Sélectionnez d'abord "
                    "la variable qualitative."
                )

            dataframe = _load_eqae_dataframe(
                project_id,
                dataset_id,
            )

            segments, _, _ = (
                _build_initial_segments(
                    dataframe,
                    column=text_column,
                )
            )

            codebook_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "codebook",
                    default=None,
                )
            )

            if not codebook_payload:
                raise ValueError(
                    "Créez d'abord un Codebook."
                )

            themes_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "themes",
                    default={},
                )
            )

            quotations_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "quotations",
                    default={},
                )
            )

            return eqae_quotations_component(
                segments=segments,
                quotations_payload=(
                    quotations_payload
                ),
                codebook_payload=(
                    codebook_payload
                ),
                themes_payload=(
                    themes_payload
                ),
            )

        except Exception as exc:
            logger.exception(
                "Erreur chargement verbatims EQAE"
            )

            return dbc.Alert(
                str(exc),
                color="danger",
            )

    if active_tab == "eqae-tab-themes":

        try:
            codebook_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "codebook",
                    default=None,
                )
            )

            if not codebook_payload:
                raise ValueError(
                    "Créez d'abord un Codebook."
                )

            themes_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "themes",
                    default={},
                )
            )

            return eqae_themes_component(
                themes_payload=(
                    themes_payload
                ),
                codebook_payload=(
                    codebook_payload
                ),
            )

        except Exception as exc:
            logger.exception(
                "Erreur chargement thèmes EQAE"
            )

            return dbc.Alert(
                str(exc),
                color="danger",
            )

    if active_tab == "eqae-tab-assisted":

        try:
            if not text_column:
                raise ValueError(
                    "Sélectionnez d'abord la variable "
                    "qualitative."
                )

            dataframe = _load_eqae_dataframe(
                project_id,
                dataset_id,
            )

            segments, _, _ = (
                _build_initial_segments(
                    dataframe,
                    column=text_column,
                )
            )

            codebook_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "codebook",
                    default=None,
                )
            )

            if not codebook_payload:
                raise ValueError(
                    "Créez d'abord un Codebook."
                )

            assisted_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "assisted",
                    default={},
                )
            )

            return eqae_assisted_component(
                segments=segments,
                codebook_payload=(
                    codebook_payload
                ),
                assisted_payload=(
                    assisted_payload
                ),
            )

        except Exception as exc:
            logger.exception(
                "Erreur chargement codage assisté EQAE"
            )

            return dbc.Alert(
                str(exc),
                color="danger",
            )

    if active_tab == "eqae-tab-coding":

        try:
            if not text_column:
                raise ValueError(
                    "Sélectionnez d'abord la variable "
                    "qualitative du corpus."
                )

            dataframe = _load_eqae_dataframe(
                project_id,
                dataset_id,
            )

            (
                segments,
                _,
                _,
            ) = _build_initial_segments(
                dataframe,
                column=text_column,
            )

            codebook_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "codebook",
                    default=None,
                )
            )

            if not codebook_payload:
                raise ValueError(
                    "Créez d'abord un Codebook "
                    "avant de commencer le codage."
                )

            coding_payload = (
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "coding",
                    default={},
                )
            )

            return eqae_coding_component(
                segments=segments,
                codebook_payload=(
                    codebook_payload
                ),
                coding_payload=(
                    coding_payload
                ),
            )

        except Exception as exc:
            logger.exception(
                "Erreur chargement codage EQAE"
            )

            return dbc.Alert(
                str(exc),
                color="danger",
            )

    if active_tab == "eqae-tab-codebook":

        try:
            payload = _load_eqae_section(
                project_id,
                dataset_id,
                "codebook",
                default=None,
            )

            return eqae_codebook_component(
                payload
            )

        except Exception as exc:
            logger.exception(
                "Erreur chargement codebook EQAE"
            )

            return dbc.Alert(
                str(exc),
                color="danger",
            )

    content = _TAB_CONTENT.get(
        active_tab
    )

    if content is None:
        return eqae_intro_component(
            "EQAE",
            (
                "Sélectionnez un onglet pour "
                "commencer l'analyse qualitative."
            ),
        )

    title, description, note = content

    return eqae_intro_component(
        title,
        description,
        note=note,
    )


@callback(
    Output(
        "eqae-codebook-feedback",
        "children",
    ),
    Output(
        "eqae-codebook-table",
        "children",
    ),
    Output(
        "eqae-code-parent",
        "options",
    ),
    Output(
        "eqae-code-parent",
        "value",
    ),
    Output(
        "eqae-delete-code-id",
        "options",
    ),
    Output(
        "eqae-delete-code-id",
        "value",
    ),
    Output(
        "eqae-code-name",
        "value",
    ),
    Output(
        "eqae-code-description",
        "value",
    ),
    Input(
        "eqae-add-code",
        "n_clicks",
    ),
    Input(
        "eqae-delete-code",
        "n_clicks",
    ),
    State(
        "eqae-project-id",
        "data",
    ),
    State(
        "eqae-dataset-id",
        "data",
    ),
    State(
        "eqae-codebook-name",
        "value",
    ),
    State(
        "eqae-codebook-description",
        "value",
    ),
    State(
        "eqae-code-name",
        "value",
    ),
    State(
        "eqae-code-description",
        "value",
    ),
    State(
        "eqae-code-parent",
        "value",
    ),
    State(
        "eqae-code-color",
        "value",
    ),
    State(
        "eqae-delete-code-id",
        "value",
    ),
    prevent_initial_call=True,
)
def manage_eqae_codebook(
    add_clicks,
    delete_clicks,
    project_id,
    dataset_id,
    codebook_name,
    codebook_description,
    code_name,
    code_description,
    parent_code_id,
    color,
    delete_code_id,
):
    """
    Création et suppression contrôlées
    des codes EQAE.
    """

    try:
        payload = _load_eqae_section(
            project_id,
            dataset_id,
            "codebook",
            default=None,
        )

        codebook = _restore_codebook(
            payload,
            name_override=codebook_name,
            description_override=(
                codebook_description
            ),
        )

        triggered = ctx.triggered_id

        if triggered == "eqae-add-code":

            codebook.add_code(
                code_name,
                description=(
                    code_description
                    or ""
                ),
                parent_code_id=(
                    parent_code_id
                    or None
                ),
                color=(
                    color
                    or None
                ),
            )

            feedback = dbc.Alert(
                (
                    f"Code « {str(code_name).strip()} » "
                    "ajouté au codebook."
                ),
                color="success",
                className="py-2",
            )

        elif triggered == "eqae-delete-code":

            if not delete_code_id:
                raise ValueError(
                    "Sélectionnez un code "
                    "à supprimer."
                )

            coding_payload = _load_eqae_section(
                project_id,
                dataset_id,
                "coding",
                default={},
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

            if any(
                assignment.get("code_id")
                == delete_code_id
                for assignment in assignments
                if isinstance(
                    assignment,
                    dict,
                )
            ):
                raise ValueError(
                    "Impossible de supprimer ce code : "
                    "il est déjà utilisé dans le codage "
                    "qualitatif."
                )

            themes_payload = _load_eqae_section(
                project_id,
                dataset_id,
                "themes",
                default={},
            )

            themes = (
                themes_payload.get(
                    "themes",
                    [],
                )
                if isinstance(
                    themes_payload,
                    dict,
                )
                else []
            )

            if any(
                delete_code_id
                in theme.get(
                    "code_ids",
                    [],
                )
                for theme in themes
                if isinstance(
                    theme,
                    dict,
                )
            ):
                raise ValueError(
                    "Impossible de supprimer ce code : "
                    "il est associé à un thème qualitatif."
                )

            removed = codebook.remove_code(
                delete_code_id
            )

            feedback = dbc.Alert(
                (
                    f"Code « {removed.name} » "
                    "supprimé du codebook."
                ),
                color="success",
                className="py-2",
            )

        else:
            raise ValueError(
                "Action Codebook inconnue."
            )

        serialized = codebook.to_dict()

        _persist_eqae_section(
            project_id,
            dataset_id,
            "codebook",
            {
                "schema_version": 1,
                **serialized,
            },
        )

        options = _eqae_codebook_options(
            serialized
        )

        return (
            feedback,
            eqae_codebook_table(
                serialized
            ),
            options,
            None,
            options,
            None,
            "",
            "",
        )

    except Exception as exc:
        logger.exception(
            "Erreur modification codebook EQAE"
        )

        current = _load_eqae_section(
            project_id,
            dataset_id,
            "codebook",
            default={},
        )

        options = _eqae_codebook_options(
            current
        )

        return (
            dbc.Alert(
                str(exc),
                color="danger",
                className="py-2",
            ),
            eqae_codebook_table(
                current
            ),
            options,
            parent_code_id,
            options,
            delete_code_id,
            code_name or "",
            code_description or "",
        )


@callback(
    Output(
        "eqae-coding-feedback",
        "children",
    ),
    Output(
        "eqae-coding-assignments-table",
        "children",
    ),
    Output(
        "eqae-delete-assignment-id",
        "options",
    ),
    Output(
        "eqae-delete-assignment-id",
        "value",
    ),
    Output(
        "eqae-coding-segment",
        "value",
    ),
    Output(
        "eqae-coding-code",
        "value",
    ),
    Output(
        "eqae-coding-memo",
        "value",
    ),
    Input(
        "eqae-assign-code",
        "n_clicks",
    ),
    Input(
        "eqae-delete-assignment",
        "n_clicks",
    ),
    State(
        "eqae-project-id",
        "data",
    ),
    State(
        "eqae-dataset-id",
        "data",
    ),
    State(
        "eqae-text-column",
        "value",
    ),
    State(
        "eqae-coding-segment",
        "value",
    ),
    State(
        "eqae-coding-code",
        "value",
    ),
    State(
        "eqae-coding-memo",
        "value",
    ),
    State(
        "eqae-delete-assignment-id",
        "value",
    ),
    prevent_initial_call=True,
)
def manage_eqae_manual_coding(
    assign_clicks,
    delete_clicks,
    project_id,
    dataset_id,
    text_column,
    segment_id,
    code_id,
    memo,
    delete_assignment_id,
):
    """
    Gestion du codage qualitatif manuel.
    """

    try:
        dataframe = _load_eqae_dataframe(
            project_id,
            dataset_id,
        )

        (
            segments,
            _,
            _,
        ) = _build_initial_segments(
            dataframe,
            column=text_column,
        )

        segment_map = {
            segment.segment_id: segment
            for segment in segments
        }

        codebook_payload = (
            _load_eqae_section(
                project_id,
                dataset_id,
                "codebook",
                default=None,
            )
        )

        if not codebook_payload:
            raise ValueError(
                "Le Codebook EQAE est indisponible."
            )

        codebook = _restore_codebook(
            codebook_payload
        )

        coding_payload = (
            _load_eqae_section(
                project_id,
                dataset_id,
                "coding",
                default={},
            )
        )

        coder = _restore_coder(
            codebook,
            segments,
            coding_payload,
        )

        triggered = ctx.triggered_id

        if triggered == "eqae-assign-code":

            if not segment_id:
                raise ValueError(
                    "Sélectionnez un segment."
                )

            if not code_id:
                raise ValueError(
                    "Sélectionnez un code."
                )

            segment = segment_map.get(
                segment_id
            )

            if segment is None:
                raise ValueError(
                    "Segment introuvable."
                )

            assignment = coder.assign_code(
                segment=segment,
                code_id=code_id,
                mode="manual",
                memo=memo or "",
            )

            feedback = dbc.Alert(
                (
                    "Code affecté au segment "
                    f"« {assignment.segment_id} »."
                ),
                color="success",
                className="py-2",
            )

        elif (
            triggered
            == "eqae-delete-assignment"
        ):

            if not delete_assignment_id:
                raise ValueError(
                    "Sélectionnez une affectation "
                    "à supprimer."
                )

            coder.remove_assignment(
                delete_assignment_id
            )

            feedback = dbc.Alert(
                "Affectation supprimée.",
                color="success",
                className="py-2",
            )

        else:
            raise ValueError(
                "Action de codage inconnue."
            )

        serialized = coder.to_dict()

        _persist_eqae_section(
            project_id,
            dataset_id,
            "coding",
            {
                "schema_version": 1,
                "text_column": text_column,
                **serialized,
            },
        )

        assignments = serialized.get(
            "assignments",
            [],
        )

        delete_options = [
            {
                "label": (
                    f"{item.get('document_id', '')} — "
                    f"{item.get('assignment_id', '')[:8]}"
                ),
                "value": item.get(
                    "assignment_id"
                ),
            }
            for item in assignments
        ]

        return (
            feedback,
            eqae_assignments_table(
                serialized,
                codebook_payload,
            ),
            delete_options,
            None,
            None,
            None,
            "",
        )

    except Exception as exc:
        logger.exception(
            "Erreur codage manuel EQAE"
        )

        current = _load_eqae_section(
            project_id,
            dataset_id,
            "coding",
            default={},
        )

        codebook_payload = (
            _load_eqae_section(
                project_id,
                dataset_id,
                "codebook",
                default={},
            )
        )

        assignments = (
            current.get(
                "assignments",
                [],
            )
            if isinstance(
                current,
                dict,
            )
            else []
        )

        delete_options = [
            {
                "label": (
                    f"{item.get('document_id', '')} — "
                    f"{item.get('assignment_id', '')[:8]}"
                ),
                "value": item.get(
                    "assignment_id"
                ),
            }
            for item in assignments
        ]

        return (
            dbc.Alert(
                str(exc),
                color="danger",
                className="py-2",
            ),
            eqae_assignments_table(
                current,
                codebook_payload,
            ),
            delete_options,
            delete_assignment_id,
            segment_id,
            code_id,
            memo or "",
        )


@callback(
    Output(
        "eqae-assisted-feedback",
        "children",
        allow_duplicate=True,
    ),
    Output(
        "eqae-assisted-suggestions-table",
        "children",
        allow_duplicate=True,
    ),
    Output(
        "eqae-assisted-suggestion-id",
        "options",
        allow_duplicate=True,
    ),
    Output(
        "eqae-assisted-suggestion-id",
        "value",
        allow_duplicate=True,
    ),
    Input(
        "eqae-create-suggestion",
        "n_clicks",
    ),
    State(
        "eqae-project-id",
        "data",
    ),
    State(
        "eqae-dataset-id",
        "data",
    ),
    State(
        "eqae-text-column",
        "value",
    ),
    State(
        "eqae-assisted-segment",
        "value",
    ),
    State(
        "eqae-assisted-code",
        "value",
    ),
    State(
        "eqae-assisted-confidence",
        "value",
    ),
    State(
        "eqae-assisted-rationale",
        "value",
    ),
    State(
        "eqae-assisted-source",
        "value",
    ),
    prevent_initial_call=True,
)
def create_eqae_assisted_suggestion(
    n_clicks,
    project_id,
    dataset_id,
    text_column,
    segment_id,
    code_id,
    confidence,
    rationale,
    source,
):

    print(
        "[EQAE ASSISTED CREATE]",
        "clicks=",
        n_clicks,
        "project=",
        project_id,
        "dataset=",
        dataset_id,
        "column=",
        text_column,
        "segment=",
        segment_id,
        "code=",
        code_id,
        "confidence=",
        confidence,
        "source=",
        source,
        flush=True,
    )

    try:
        if not segment_id:
            raise ValueError(
                "Sélectionnez un segment."
            )

        if not code_id:
            raise ValueError(
                "Sélectionnez un code suggéré."
            )

        dataframe = _load_eqae_dataframe(
            project_id,
            dataset_id,
        )

        segments, _, _ = _build_initial_segments(
            dataframe,
            column=text_column,
        )

        segment_map = {
            segment.segment_id: segment
            for segment in segments
        }

        segment = segment_map.get(
            segment_id
        )

        if segment is None:
            raise ValueError(
                "Segment introuvable."
            )

        codebook_payload = _load_eqae_section(
            project_id,
            dataset_id,
            "codebook",
            default=None,
        )

        codebook = _restore_codebook(
            codebook_payload
        )

        coding_payload = _load_eqae_section(
            project_id,
            dataset_id,
            "coding",
            default={},
        )

        coder = _restore_coder(
            codebook,
            segments,
            coding_payload,
        )

        assisted_payload = _load_eqae_section(
            project_id,
            dataset_id,
            "assisted",
            default={},
        )

        manager = _restore_assisted_manager(
            codebook,
            coder,
            segments,
            assisted_payload,
        )

        manager.suggest_code(
            segment=segment,
            code_id=code_id,
            confidence=confidence,
            rationale=rationale or "",
            source=source or "assisted",
        )

        serialized = manager.to_dict()

        _persist_eqae_section(
            project_id,
            dataset_id,
            "assisted",
            {
                "schema_version": 1,
                **serialized,
            },
        )

        pending = [
            item
            for item in serialized.get(
                "suggestions",
                [],
            )
            if item.get("status") == "pending"
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
        ]

        new_suggestion_id = (
            pending[-1].get("suggestion_id")
            if pending
            else None
        )

        return (
            dbc.Alert(
                (
                    "Suggestion créée en statut "
                    "« pending ». Aucun codage "
                    "n'a encore été validé."
                ),
                color="success",
                className="py-2",
            ),
            eqae_assisted_table(
                serialized,
                codebook_payload,
            ),
            pending_options,
            new_suggestion_id,
        )

    except Exception as exc:
        logger.exception(
            "Erreur création suggestion EQAE"
        )

        assisted_payload = _load_eqae_section(
            project_id,
            dataset_id,
            "assisted",
            default={},
        )

        codebook_payload = _load_eqae_section(
            project_id,
            dataset_id,
            "codebook",
            default={},
        )

        pending = [
            item
            for item in assisted_payload.get(
                "suggestions",
                [],
            )
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
        ]

        return (
            dbc.Alert(
                str(exc),
                color="danger",
                className="py-2",
            ),
            eqae_assisted_table(
                assisted_payload,
                codebook_payload,
            ),
            pending_options,
            None,
        )


@callback(
    Output(
        "eqae-assisted-feedback",
        "children",
        allow_duplicate=True,
    ),
    Output(
        "eqae-assisted-suggestions-table",
        "children",
        allow_duplicate=True,
    ),
    Output(
        "eqae-assisted-suggestion-id",
        "options",
        allow_duplicate=True,
    ),
    Output(
        "eqae-assisted-suggestion-id",
        "value",
        allow_duplicate=True,
    ),
    Input(
        "eqae-accept-suggestion",
        "n_clicks",
    ),
    Input(
        "eqae-modify-suggestion",
        "n_clicks",
    ),
    Input(
        "eqae-reject-suggestion",
        "n_clicks",
    ),
    State(
        "eqae-project-id",
        "data",
    ),
    State(
        "eqae-dataset-id",
        "data",
    ),
    State(
        "eqae-text-column",
        "value",
    ),
    State(
        "eqae-assisted-suggestion-id",
        "value",
    ),
    State(
        "eqae-assisted-replacement-code",
        "value",
    ),
    State(
        "eqae-assisted-reviewer-note",
        "value",
    ),
    prevent_initial_call=True,
)
def review_eqae_assisted_suggestion(
    accept_clicks,
    modify_clicks,
    reject_clicks,
    project_id,
    dataset_id,
    text_column,
    suggestion_id,
    replacement_code_id,
    reviewer_note,
):

    print(
        "[EQAE ASSISTED REVIEW]",
        "trigger=",
        ctx.triggered_id,
        "accept=",
        accept_clicks,
        "modify=",
        modify_clicks,
        "reject=",
        reject_clicks,
        "suggestion=",
        suggestion_id,
        "replacement=",
        replacement_code_id,
        "note=",
        reviewer_note,
        flush=True,
    )

    try:
        if not suggestion_id:
            raise ValueError(
                "Sélectionnez une suggestion pending."
            )

        dataframe = _load_eqae_dataframe(
            project_id,
            dataset_id,
        )

        segments, _, _ = _build_initial_segments(
            dataframe,
            column=text_column,
        )

        codebook_payload = _load_eqae_section(
            project_id,
            dataset_id,
            "codebook",
            default=None,
        )

        codebook = _restore_codebook(
            codebook_payload
        )

        coding_payload = _load_eqae_section(
            project_id,
            dataset_id,
            "coding",
            default={},
        )

        coder = _restore_coder(
            codebook,
            segments,
            coding_payload,
        )

        assisted_payload = _load_eqae_section(
            project_id,
            dataset_id,
            "assisted",
            default={},
        )

        manager = _restore_assisted_manager(
            codebook,
            coder,
            segments,
            assisted_payload,
        )

        triggered = ctx.triggered_id

        if triggered == "eqae-accept-suggestion":

            reviewed = manager.accept(
                suggestion_id,
                reviewer_note=(
                    reviewer_note or ""
                ),
            )

            message = (
                "Suggestion acceptée et codage "
                "assisté validé."
            )

        elif triggered == "eqae-modify-suggestion":

            if not replacement_code_id:
                raise ValueError(
                    "Sélectionnez le code de "
                    "remplacement."
                )

            reviewed = manager.modify(
                suggestion_id,
                code_id=replacement_code_id,
                reviewer_note=(
                    reviewer_note or ""
                ),
            )

            message = (
                "Suggestion modifiée puis "
                "validée par le chercheur."
            )

        elif triggered == "eqae-reject-suggestion":

            reviewed = manager.reject(
                suggestion_id,
                reviewer_note=(
                    reviewer_note or ""
                ),
            )

            message = (
                "Suggestion rejetée. "
                "Aucun nouveau codage créé."
            )

        else:
            raise ValueError(
                "Décision assistée inconnue."
            )

        assisted_serialized = (
            manager.to_dict()
        )

        coding_serialized = (
            coder.to_dict()
        )

        _persist_eqae_section(
            project_id,
            dataset_id,
            "assisted",
            {
                "schema_version": 1,
                **assisted_serialized,
            },
        )

        # Important :
        # accept/modify modifient coder ;
        # reject laisse coder inchangé.
        _persist_eqae_section(
            project_id,
            dataset_id,
            "coding",
            {
                "schema_version": 1,
                "text_column": text_column,
                **coding_serialized,
            },
        )

        pending = [
            item
            for item in assisted_serialized.get(
                "suggestions",
                [],
            )
            if item.get("status") == "pending"
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
        ]

        return (
            dbc.Alert(
                (
                    f"{message} "
                    f"Statut : {reviewed.status}."
                ),
                color="success",
                className="py-2",
            ),
            eqae_assisted_table(
                assisted_serialized,
                codebook_payload,
            ),
            pending_options,
            None,
        )

    except Exception as exc:
        logger.exception(
            "Erreur validation suggestion EQAE"
        )

        current_assisted = _load_eqae_section(
            project_id,
            dataset_id,
            "assisted",
            default={},
        )

        current_codebook = _load_eqae_section(
            project_id,
            dataset_id,
            "codebook",
            default={},
        )

        pending = [
            item
            for item in current_assisted.get(
                "suggestions",
                [],
            )
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
        ]

        return (
            dbc.Alert(
                str(exc),
                color="danger",
                className="py-2",
            ),
            eqae_assisted_table(
                current_assisted,
                current_codebook,
            ),
            pending_options,
            suggestion_id,
        )


@callback(
    Output(
        "eqae-theme-feedback",
        "children",
    ),
    Output(
        "eqae-themes-table",
        "children",
    ),
    Output(
        "eqae-theme-parent",
        "options",
    ),
    Output(
        "eqae-theme-parent",
        "value",
    ),
    Output(
        "eqae-theme-link-id",
        "options",
    ),
    Output(
        "eqae-theme-link-id",
        "value",
    ),
    Output(
        "eqae-delete-theme-id",
        "options",
    ),
    Output(
        "eqae-delete-theme-id",
        "value",
    ),
    Output(
        "eqae-theme-name",
        "value",
    ),
    Output(
        "eqae-theme-description",
        "value",
    ),
    Input(
        "eqae-add-theme",
        "n_clicks",
    ),
    Input(
        "eqae-link-theme-code",
        "n_clicks",
    ),
    Input(
        "eqae-unlink-theme-code",
        "n_clicks",
    ),
    Input(
        "eqae-delete-theme",
        "n_clicks",
    ),
    State(
        "eqae-project-id",
        "data",
    ),
    State(
        "eqae-dataset-id",
        "data",
    ),
    State(
        "eqae-theme-name",
        "value",
    ),
    State(
        "eqae-theme-description",
        "value",
    ),
    State(
        "eqae-theme-parent",
        "value",
    ),
    State(
        "eqae-theme-link-id",
        "value",
    ),
    State(
        "eqae-theme-code-id",
        "value",
    ),
    State(
        "eqae-delete-theme-id",
        "value",
    ),
    prevent_initial_call=True,
)
def manage_eqae_themes(
    add_clicks,
    link_clicks,
    unlink_clicks,
    delete_clicks,
    project_id,
    dataset_id,
    theme_name,
    theme_description,
    parent_theme_id,
    link_theme_id,
    code_id,
    delete_theme_id,
):
    """
    Gestion des thèmes, sous-thèmes
    et liens thème-code.
    """

    try:
        codebook_payload = (
            _load_eqae_section(
                project_id,
                dataset_id,
                "codebook",
                default=None,
            )
        )

        if not codebook_payload:
            raise ValueError(
                "Le Codebook EQAE est indisponible."
            )

        codebook = _restore_codebook(
            codebook_payload
        )

        themes_payload = (
            _load_eqae_section(
                project_id,
                dataset_id,
                "themes",
                default={},
            )
        )

        analysis = (
            _restore_thematic_analysis(
                codebook,
                themes_payload,
            )
        )

        triggered = ctx.triggered_id

        if triggered == "eqae-add-theme":

            if not str(
                theme_name or ""
            ).strip():
                raise ValueError(
                    "Saisissez le nom du thème."
                )

            created = analysis.add_theme(
                name=theme_name,
                description=(
                    theme_description or ""
                ),
                parent_theme_id=(
                    parent_theme_id
                ),
            )

            feedback = dbc.Alert(
                (
                    f"Thème « {created.name} » "
                    "créé."
                ),
                color="success",
                className="py-2",
            )

        elif (
            triggered
            == "eqae-link-theme-code"
        ):

            if not link_theme_id:
                raise ValueError(
                    "Sélectionnez un thème."
                )

            if not code_id:
                raise ValueError(
                    "Sélectionnez un code."
                )

            analysis.link_code(
                theme_id=link_theme_id,
                code_id=code_id,
            )

            feedback = dbc.Alert(
                "Code associé au thème.",
                color="success",
                className="py-2",
            )

        elif (
            triggered
            == "eqae-unlink-theme-code"
        ):

            if not link_theme_id:
                raise ValueError(
                    "Sélectionnez un thème."
                )

            if not code_id:
                raise ValueError(
                    "Sélectionnez un code."
                )

            analysis.unlink_code(
                theme_id=link_theme_id,
                code_id=code_id,
            )

            feedback = dbc.Alert(
                "Code retiré du thème.",
                color="success",
                className="py-2",
            )

        elif (
            triggered
            == "eqae-delete-theme"
        ):

            if not delete_theme_id:
                raise ValueError(
                    "Sélectionnez un thème "
                    "à supprimer."
                )

            removed = analysis.remove_theme(
                delete_theme_id
            )

            feedback = dbc.Alert(
                (
                    f"Thème « {removed.name} » "
                    "supprimé."
                ),
                color="success",
                className="py-2",
            )

        else:
            raise ValueError(
                "Action thématique inconnue."
            )

        serialized = analysis.to_dict()

        _persist_eqae_section(
            project_id,
            dataset_id,
            "themes",
            {
                "schema_version": 1,
                **serialized,
            },
        )

        options = [
            {
                "label": item.get(
                    "name",
                    item.get(
                        "theme_id",
                        "",
                    ),
                ),
                "value": item.get(
                    "theme_id"
                ),
            }
            for item in serialized.get(
                "themes",
                [],
            )
        ]

        return (
            feedback,
            eqae_themes_table(
                serialized,
                codebook_payload,
            ),
            options,
            None,
            options,
            None,
            options,
            None,
            "",
            "",
        )

    except Exception as exc:
        logger.exception(
            "Erreur gestion thèmes EQAE"
        )

        current = _load_eqae_section(
            project_id,
            dataset_id,
            "themes",
            default={},
        )

        codebook_payload = (
            _load_eqae_section(
                project_id,
                dataset_id,
                "codebook",
                default={},
            )
        )

        options = [
            {
                "label": item.get(
                    "name",
                    item.get(
                        "theme_id",
                        "",
                    ),
                ),
                "value": item.get(
                    "theme_id"
                ),
            }
            for item in current.get(
                "themes",
                [],
            )
            if isinstance(item, dict)
        ]

        return (
            dbc.Alert(
                str(exc),
                color="danger",
                className="py-2",
            ),
            eqae_themes_table(
                current,
                codebook_payload,
            ),
            options,
            parent_theme_id,
            options,
            link_theme_id,
            options,
            delete_theme_id,
            theme_name or "",
            theme_description or "",
        )


@callback(
    Output(
        "eqae-quotation-feedback",
        "children",
        allow_duplicate=True,
    ),
    Output(
        "eqae-quotations-table",
        "children",
        allow_duplicate=True,
    ),
    Output(
        "eqae-delete-quotation-id",
        "options",
        allow_duplicate=True,
    ),
    Output(
        "eqae-delete-quotation-id",
        "value",
        allow_duplicate=True,
    ),
    Input(
        "eqae-add-quotation",
        "n_clicks",
    ),
    Input(
        "eqae-delete-quotation",
        "n_clicks",
    ),
    State(
        "eqae-project-id",
        "data",
    ),
    State(
        "eqae-dataset-id",
        "data",
    ),
    State(
        "eqae-text-column",
        "value",
    ),
    State(
        "eqae-quotation-segment",
        "value",
    ),
    State(
        "eqae-quotation-note",
        "value",
    ),
    State(
        "eqae-delete-quotation-id",
        "value",
    ),
    prevent_initial_call=True,
)
def manage_eqae_quotations(
    add_clicks,
    delete_clicks,
    project_id,
    dataset_id,
    text_column,
    segment_id,
    note,
    delete_quotation_id,
):
    """
    Gestion des verbatims EQAE.
    """

    try:
        dataframe = _load_eqae_dataframe(
            project_id,
            dataset_id,
        )

        segments, _, _ = _build_initial_segments(
            dataframe,
            column=text_column,
        )

        segment_map = {
            segment.segment_id: segment
            for segment in segments
        }

        codebook_payload = _load_eqae_section(
            project_id,
            dataset_id,
            "codebook",
            default=None,
        )

        if not codebook_payload:
            raise ValueError(
                "Le Codebook EQAE est indisponible."
            )

        codebook = _restore_codebook(
            codebook_payload
        )

        coding_payload = _load_eqae_section(
            project_id,
            dataset_id,
            "coding",
            default={},
        )

        coder = _restore_coder(
            codebook,
            segments,
            coding_payload,
        )

        themes_payload = _load_eqae_section(
            project_id,
            dataset_id,
            "themes",
            default={},
        )

        thematic = _restore_thematic_analysis(
            codebook,
            themes_payload,
        )

        quotations_payload = (
            _load_eqae_section(
                project_id,
                dataset_id,
                "quotations",
                default={},
            )
        )

        manager = _restore_quotation_manager(
            coder=coder,
            thematic_analysis=thematic,
            segments=segments,
            payload=quotations_payload,
        )

        triggered = ctx.triggered_id

        if triggered == "eqae-add-quotation":

            if not segment_id:
                raise ValueError(
                    "Sélectionnez un segment."
                )

            segment = segment_map.get(
                segment_id
            )

            if segment is None:
                raise ValueError(
                    "Segment introuvable."
                )

            quotation = (
                manager.add_quotation(
                    segment=segment,
                    note=note or "",
                )
            )

            feedback = dbc.Alert(
                (
                    "Verbatim enregistré : "
                    f"{quotation.quotation_id[:8]}"
                ),
                color="success",
                className="py-2",
            )

        elif (
            triggered
            == "eqae-delete-quotation"
        ):

            if not delete_quotation_id:
                raise ValueError(
                    "Sélectionnez un verbatim "
                    "à supprimer."
                )

            manager.remove_quotation(
                delete_quotation_id
            )

            feedback = dbc.Alert(
                "Verbatim supprimé.",
                color="success",
                className="py-2",
            )

        else:
            raise ValueError(
                "Action verbatim inconnue."
            )

        serialized = manager.to_dict()

        _persist_eqae_section(
            project_id,
            dataset_id,
            "quotations",
            {
                "schema_version": 1,
                **serialized,
            },
        )

        delete_options = [
            {
                "label": (
                    f"{item.get('document_id', '')} — "
                    f"{item.get('quotation_id', '')[:8]}"
                ),
                "value": item.get(
                    "quotation_id"
                ),
            }
            for item in serialized.get(
                "quotations",
                [],
            )
        ]

        return (
            feedback,
            eqae_quotations_table(
                serialized
            ),
            delete_options,
            None,
        )

    except Exception as exc:
        logger.exception(
            "Erreur gestion verbatims EQAE"
        )

        current = _load_eqae_section(
            project_id,
            dataset_id,
            "quotations",
            default={},
        )

        delete_options = [
            {
                "label": (
                    f"{item.get('document_id', '')} — "
                    f"{item.get('quotation_id', '')[:8]}"
                ),
                "value": item.get(
                    "quotation_id"
                ),
            }
            for item in current.get(
                "quotations",
                [],
            )
            if isinstance(item, dict)
        ]

        return (
            dbc.Alert(
                str(exc),
                color="danger",
                className="py-2",
            ),
            eqae_quotations_table(
                current
            ),
            delete_options,
            delete_quotation_id,
        )


@callback(
    Output(
        "eqae-quotations-table",
        "children",
        allow_duplicate=True,
    ),
    Input(
        "eqae-quotation-filter-code",
        "value",
    ),
    Input(
        "eqae-quotation-filter-theme",
        "value",
    ),
    Input(
        "eqae-quotation-filter-document",
        "value",
    ),
    State(
        "eqae-project-id",
        "data",
    ),
    State(
        "eqae-dataset-id",
        "data",
    ),
    State(
        "eqae-text-column",
        "value",
    ),
    prevent_initial_call=True,
)
def filter_eqae_quotations(
    code_id,
    theme_id,
    document_id,
    project_id,
    dataset_id,
    text_column,
):
    """
    Filtrage analytique des verbatims.
    """

    try:
        dataframe = _load_eqae_dataframe(
            project_id,
            dataset_id,
        )

        segments, _, _ = _build_initial_segments(
            dataframe,
            column=text_column,
        )

        codebook_payload = _load_eqae_section(
            project_id,
            dataset_id,
            "codebook",
            default={},
        )

        codebook = _restore_codebook(
            codebook_payload
        )

        coder = _restore_coder(
            codebook,
            segments,
            _load_eqae_section(
                project_id,
                dataset_id,
                "coding",
                default={},
            ),
        )

        thematic = _restore_thematic_analysis(
            codebook,
            _load_eqae_section(
                project_id,
                dataset_id,
                "themes",
                default={},
            ),
        )

        manager = _restore_quotation_manager(
            coder=coder,
            thematic_analysis=thematic,
            segments=segments,
            payload=_load_eqae_section(
                project_id,
                dataset_id,
                "quotations",
                default={},
            ),
        )

        if code_id:
            selected = (
                manager.quotations_for_code(
                    code_id
                )
            )

        elif theme_id:
            selected = (
                manager.quotations_for_theme(
                    theme_id
                )
            )

        elif document_id:
            selected = (
                manager.quotations_for_document(
                    document_id
                )
            )

        else:
            selected = manager.quotations

        return eqae_quotations_table(
            {
                "quotations": [
                    item.to_dict()
                    for item in selected
                ]
            }
        )

    except Exception as exc:
        logger.exception(
            "Erreur filtrage verbatims EQAE"
        )

        return dbc.Alert(
            str(exc),
            color="danger",
        )


@callback(
    Output(
        "eqae-cooccurrence-feedback",
        "children",
    ),
    Output(
        "eqae-cooccurrence-pairs-table",
        "children",
    ),
    Output(
        "eqae-cooccurrence-matrix-table",
        "children",
    ),
    Input(
        "eqae-run-cooccurrence",
        "n_clicks",
    ),
    State(
        "eqae-project-id",
        "data",
    ),
    State(
        "eqae-dataset-id",
        "data",
    ),
    State(
        "eqae-text-column",
        "value",
    ),
    State(
        "eqae-cooccurrence-level",
        "value",
    ),
    prevent_initial_call=True,
)
def run_eqae_cooccurrence(
    n_clicks,
    project_id,
    dataset_id,
    text_column,
    level,
):
    """
    Calcule les cooccurrences de codes EQAE.
    """

    try:
        if level not in {
            "segment",
            "document",
        }:
            raise ValueError(
                "Niveau de cooccurrence invalide."
            )

        dataframe = _load_eqae_dataframe(
            project_id,
            dataset_id,
        )

        segments, _, _ = (
            _build_initial_segments(
                dataframe,
                column=text_column,
            )
        )

        codebook_payload = (
            _load_eqae_section(
                project_id,
                dataset_id,
                "codebook",
                default=None,
            )
        )

        if not codebook_payload:
            raise ValueError(
                "Le Codebook EQAE est indisponible."
            )

        codebook = _restore_codebook(
            codebook_payload
        )

        coding_payload = (
            _load_eqae_section(
                project_id,
                dataset_id,
                "coding",
                default={},
            )
        )

        coder = _restore_coder(
            codebook,
            segments,
            coding_payload,
        )

        engine = EQAEEngine()

        analyzer = (
            engine.create_cooccurrence_analyzer(
                coder
            )
        )

        result = analyzer.to_dict(
            level=level
        )

        payload = {
            "schema_version": 1,
            "text_column": text_column,
            "n_assignments": len(
                coder.assignments
            ),
            **result,
        }

        _persist_eqae_section(
            project_id,
            dataset_id,
            "cooccurrence",
            payload,
        )

        n_pairs = len(
            result.get(
                "cooccurrences",
                [],
            )
        )

        level_label = (
            "segment"
            if level == "segment"
            else "document"
        )

        feedback = dbc.Alert(
            (
                f"Analyse terminée au niveau "
                f"« {level_label} » : "
                f"{n_pairs} paire(s) de codes "
                "en cooccurrence."
            ),
            color="success",
            className="py-2",
        )

        return (
            feedback,
            eqae_cooccurrence_pairs_table(
                result,
                codebook_payload,
            ),
            eqae_cooccurrence_matrix_table(
                result,
                codebook_payload,
            ),
        )

    except Exception as exc:
        logger.exception(
            "Erreur analyse cooccurrences EQAE"
        )

        return (
            dbc.Alert(
                str(exc),
                color="danger",
                className="py-2",
            ),
            dbc.Alert(
                "Analyse indisponible.",
                color="light",
            ),
            dbc.Alert(
                "Matrice indisponible.",
                color="light",
            ),
        )


@callback(
    Output(
        "eqae-memo-target-id",
        "options",
    ),
    Output(
        "eqae-memo-target-id",
        "value",
    ),
    Output(
        "eqae-memo-target-id",
        "disabled",
    ),
    Input(
        "eqae-memo-target-type",
        "value",
    ),
    State(
        "eqae-memo-code-options",
        "data",
    ),
    State(
        "eqae-memo-theme-options",
        "data",
    ),
    State(
        "eqae-memo-quotation-options",
        "data",
    ),
    State(
        "eqae-memo-segment-options",
        "data",
    ),
    State(
        "eqae-memo-document-options",
        "data",
    ),
)
def update_eqae_memo_target_options(
    target_type,
    code_options,
    theme_options,
    quotation_options,
    segment_options,
    document_options,
):
    """
    Adapte la liste des cibles au type de mémo.
    """

    mapping = {
        "code": code_options or [],
        "theme": theme_options or [],
        "quotation": (
            quotation_options or []
        ),
        "segment": segment_options or [],
        "document": document_options or [],
    }

    if target_type == "analysis":
        return (
            [],
            None,
            True,
        )

    return (
        mapping.get(
            target_type,
            [],
        ),
        None,
        False,
    )


@callback(
    Output(
        "eqae-memo-feedback",
        "children",
    ),
    Output(
        "eqae-memos-table",
        "children",
    ),
    Output(
        "eqae-delete-memo-id",
        "options",
    ),
    Output(
        "eqae-delete-memo-id",
        "value",
    ),
    Output(
        "eqae-memo-title",
        "value",
    ),
    Output(
        "eqae-memo-content",
        "value",
    ),
    Input(
        "eqae-add-memo",
        "n_clicks",
    ),
    Input(
        "eqae-delete-memo",
        "n_clicks",
    ),
    State(
        "eqae-project-id",
        "data",
    ),
    State(
        "eqae-dataset-id",
        "data",
    ),
    State(
        "eqae-memo-title",
        "value",
    ),
    State(
        "eqae-memo-content",
        "value",
    ),
    State(
        "eqae-memo-target-type",
        "value",
    ),
    State(
        "eqae-memo-target-id",
        "value",
    ),
    State(
        "eqae-memo-author",
        "value",
    ),
    State(
        "eqae-delete-memo-id",
        "value",
    ),
    prevent_initial_call=True,
)
def manage_eqae_memos(
    add_clicks,
    delete_clicks,
    project_id,
    dataset_id,
    title,
    content,
    target_type,
    target_id,
    author,
    delete_memo_id,
):
    """
    Gestion des mémos analytiques EQAE.
    """

    try:
        payload = _load_eqae_section(
            project_id,
            dataset_id,
            "memos",
            default={},
        )

        manager = _restore_memo_manager(
            payload
        )

        triggered = ctx.triggered_id

        if triggered == "eqae-add-memo":

            memo = manager.add_memo(
                title=title or "",
                content=content or "",
                target_type=(
                    target_type
                    or "analysis"
                ),
                target_id=(
                    None
                    if target_type
                    == "analysis"
                    else target_id
                ),
                author=author or None,
            )

            feedback = dbc.Alert(
                (
                    "Mémo enregistré : "
                    f"{memo.memo_id[:8]}"
                ),
                color="success",
                className="py-2",
            )

        elif (
            triggered
            == "eqae-delete-memo"
        ):

            if not delete_memo_id:
                raise ValueError(
                    "Sélectionnez un mémo "
                    "à supprimer."
                )

            manager.remove_memo(
                delete_memo_id
            )

            feedback = dbc.Alert(
                "Mémo supprimé.",
                color="success",
                className="py-2",
            )

        else:
            raise ValueError(
                "Action mémo inconnue."
            )

        serialized = manager.to_dict()

        _persist_eqae_section(
            project_id,
            dataset_id,
            "memos",
            {
                "schema_version": 1,
                **serialized,
            },
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
            for item in serialized.get(
                "memos",
                [],
            )
        ]

        return (
            feedback,
            eqae_memos_table(
                serialized
            ),
            delete_options,
            None,
            "",
            "",
        )

    except Exception as exc:
        logger.exception(
            "Erreur gestion mémos EQAE"
        )

        current = _load_eqae_section(
            project_id,
            dataset_id,
            "memos",
            default={},
        )

        options = [
            {
                "label": (
                    f"{item.get('title', '')} — "
                    f"{item.get('memo_id', '')[:8]}"
                ),
                "value": item.get(
                    "memo_id"
                ),
            }
            for item in current.get(
                "memos",
                [],
            )
            if isinstance(item, dict)
        ]

        return (
            dbc.Alert(
                str(exc),
                color="danger",
                className="py-2",
            ),
            eqae_memos_table(
                current
            ),
            options,
            delete_memo_id,
            title or "",
            content or "",
        )


@callback(
    Output(
        "eqae-summary-feedback",
        "children",
    ),
    Output(
        "eqae-summary-code-table",
        "children",
    ),
    Output(
        "eqae-summary-theme-table",
        "children",
    ),
    Output(
        "eqae-summary-n-codes",
        "children",
    ),
    Output(
        "eqae-summary-n-themes",
        "children",
    ),
    Output(
        "eqae-summary-n-assignments",
        "children",
    ),
    Output(
        "eqae-summary-n-documents",
        "children",
    ),
    Output(
        "eqae-summary-n-segments",
        "children",
    ),
    Output(
        "eqae-summary-n-quotations",
        "children",
    ),
    Output(
        "eqae-summary-n-suggestions",
        "children",
    ),
    Output(
        "eqae-summary-pending",
        "children",
    ),
    Output(
        "eqae-summary-accepted",
        "children",
    ),
    Output(
        "eqae-summary-modified",
        "children",
    ),
    Output(
        "eqae-summary-rejected",
        "children",
    ),
    Input(
        "eqae-run-summary",
        "n_clicks",
    ),
    State(
        "eqae-project-id",
        "data",
    ),
    State(
        "eqae-dataset-id",
        "data",
    ),
    State(
        "eqae-text-column",
        "value",
    ),
    prevent_initial_call=True,
)
def run_eqae_summary(
    n_clicks,
    project_id,
    dataset_id,
    text_column,
):
    """
    Construit et persiste la synthèse descriptive EQAE.
    """

    print(
        "[EQAE SUMMARY RUN]",
        "clicks=",
        n_clicks,
        "project=",
        project_id,
        "dataset=",
        dataset_id,
        "column=",
        text_column,
        flush=True,
    )

    try:
        dataframe = _load_eqae_dataframe(
            project_id,
            dataset_id,
        )

        segments, _, _ = (
            _build_initial_segments(
                dataframe,
                column=text_column,
            )
        )

        codebook_payload = (
            _load_eqae_section(
                project_id,
                dataset_id,
                "codebook",
                default=None,
            )
        )

        if not codebook_payload:
            raise ValueError(
                "Le Codebook EQAE est indisponible."
            )

        codebook = _restore_codebook(
            codebook_payload
        )

        coder = _restore_coder(
            codebook,
            segments,
            _load_eqae_section(
                project_id,
                dataset_id,
                "coding",
                default={},
            ),
        )

        thematic = (
            _restore_thematic_analysis(
                codebook,
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "themes",
                    default={},
                ),
            )
        )

        quotation_manager = (
            _restore_quotation_manager(
                coder=coder,
                thematic_analysis=thematic,
                segments=segments,
                payload=_load_eqae_section(
                    project_id,
                    dataset_id,
                    "quotations",
                    default={},
                ),
            )
        )

        assisted_manager = (
            _restore_assisted_manager(
                codebook,
                coder,
                segments,
                _load_eqae_section(
                    project_id,
                    dataset_id,
                    "assisted",
                    default={},
                ),
            )
        )

        engine = EQAEEngine()

        builder = (
            engine.create_summary_builder(
                coder=coder,
                thematic_analysis=thematic,
                quotation_manager=(
                    quotation_manager
                ),
                assisted_coding=(
                    assisted_manager
                ),
            )
        )

        result = builder.to_dict()

        payload = {
            "schema_version": 1,
            "text_column": text_column,
            **result,
        }

        _persist_eqae_section(
            project_id,
            dataset_id,
            "summary",
            payload,
        )

        global_data = result.get(
            "global",
            {},
        )

        assisted_data = result.get(
            "assisted_coding",
            {},
        )

        feedback = dbc.Alert(
            (
                "Synthèse EQAE actualisée : "
                f"{global_data.get('n_codes', 0)} code(s), "
                f"{global_data.get('n_themes', 0)} thème(s), "
                f"{global_data.get('n_assignments', 0)} "
                "affectation(s)."
            ),
            color="success",
            className="py-2",
        )

        return (
            feedback,
            eqae_summary_code_table(
                result
            ),
            eqae_summary_theme_table(
                result
            ),
            global_data.get(
                "n_codes",
                0,
            ),
            global_data.get(
                "n_themes",
                0,
            ),
            global_data.get(
                "n_assignments",
                0,
            ),
            global_data.get(
                "n_documents_coded",
                0,
            ),
            global_data.get(
                "n_segments_coded",
                0,
            ),
            global_data.get(
                "n_quotations",
                0,
            ),
            global_data.get(
                "n_assisted_suggestions",
                0,
            ),
            assisted_data.get(
                "pending",
                0,
            ),
            assisted_data.get(
                "accepted",
                0,
            ),
            assisted_data.get(
                "modified",
                0,
            ),
            assisted_data.get(
                "rejected",
                0,
            ),
        )

    except Exception as exc:
        logger.exception(
            "Erreur synthèse qualitative EQAE"
        )

        current = _load_eqae_section(
            project_id,
            dataset_id,
            "summary",
            default={},
        )

        global_data = (
            current.get(
                "global",
                {},
            )
            if isinstance(
                current,
                dict,
            )
            else {}
        )

        assisted_data = (
            current.get(
                "assisted_coding",
                {},
            )
            if isinstance(
                current,
                dict,
            )
            else {}
        )

        return (
            dbc.Alert(
                str(exc),
                color="danger",
                className="py-2",
            ),
            eqae_summary_code_table(
                current
            ),
            eqae_summary_theme_table(
                current
            ),
            global_data.get(
                "n_codes",
                0,
            ),
            global_data.get(
                "n_themes",
                0,
            ),
            global_data.get(
                "n_assignments",
                0,
            ),
            global_data.get(
                "n_documents_coded",
                0,
            ),
            global_data.get(
                "n_segments_coded",
                0,
            ),
            global_data.get(
                "n_quotations",
                0,
            ),
            global_data.get(
                "n_assisted_suggestions",
                0,
            ),
            assisted_data.get(
                "pending",
                0,
            ),
            assisted_data.get(
                "accepted",
                0,
            ),
            assisted_data.get(
                "modified",
                0,
            ),
            assisted_data.get(
                "rejected",
                0,
            ),
        )
