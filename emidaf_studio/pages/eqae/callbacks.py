"""
=========================================================
EMIDAF Studio
EQAE - Callbacks
=========================================================
"""

from __future__ import annotations

from dash import (
    Input,
    Output,
    callback,
)

from .components import (
    eqae_intro_component,
)


_TAB_CONTENT = {
    "eqae-tab-corpus": (
        "Corpus qualitatif",
        (
            "Préparer et organiser les documents, "
            "segments et unités qualitatives qui seront "
            "analysés dans EQAE."
        ),
        (
            "ETAE peut contribuer à l'exploration "
            "textuelle du corpus, mais EQAE conserve "
            "une logique d'analyse qualitative distincte."
        ),
    ),

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
            "Les verbatims constituent les éléments "
            "textuels mobilisés pour étayer "
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
            "Les mémos assurent la traçabilité du "
            "raisonnement analytique."
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
)
def render_eqae_tab(
    active_tab,
):
    """
    Rend le contenu initial de l'onglet EQAE actif.
    """

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
