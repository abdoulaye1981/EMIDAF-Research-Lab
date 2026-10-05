"""
=========================================================
EMIDAF
Libellés d'affichage ELAE
=========================================================

Les fonctions de ce module ne modifient jamais
les noms de variables ni les valeurs du dataset.
Elles servent uniquement à l'affichage.
=========================================================
"""

from __future__ import annotations


VARIABLE_LABELS = {
    "cycle": "Cycle scolaire",
    "niveau": "Niveau scolaire",
    "niveau_etude": "Niveau d'étude",
    "poste": "Poste",
    "genre": "Genre",
    "type_ecole": "Type d'école",

    "note_maths": "Note de mathématiques",
    "interet_maths": "Intérêt pour les mathématiques",
    "stress": "Stress",
    "motivation": "Motivation",
    "exercices_semaine": "Exercices par semaine",
    "implication": "Implication",
    "temps_aide_hebdo": "Temps d'aide hebdomadaire",
    "pratiques_pedagogiques": "Pratiques pédagogiques",
    "heures_par_semaine": "Heures par semaine",
    "feedback_prof": "Feedback enseignant",
    "experience_annees": "Expérience",
    "budget_annuel": "Budget annuel",
    "effectif_total_eleves": "Effectif total des élèves",
}


LEVEL_LABELS = {
    "6e": "6e",
    "5e": "5e",
    "4e": "4e",
    "3e": "3e",
    "2nde": "Seconde",
    "2ème": "Seconde",
    "2e": "Seconde",
    "1ere": "Première",
    "1ère": "Première",
    "Terminale": "Terminale",
}


def variable_label(name):
    """
    Libellé lisible d'une variable.
    """

    if name is None:
        return ""

    return VARIABLE_LABELS.get(
        str(name),
        str(name).replace(
            "_",
            " ",
        ),
    )


def category_label(
    variable,
    value,
):
    """
    Libellé lisible d'une modalité.

    Les niveaux scolaires bénéficient
    d'un mapping explicite.
    """

    if value is None:
        return "Valeur manquante"

    text = str(value)

    if variable in {
        "niveau",
        "niveau_etude",
    }:
        return LEVEL_LABELS.get(
            text,
            text,
        )

    return text
