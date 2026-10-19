from pathlib import Path


PATH = Path(
    "emidaf_studio/pages/edse/callbacks.py"
)

text = PATH.read_text(
    encoding="utf-8"
)


START = """# =========================================================
# VALIDATION ENSEIGNANT
# =========================================================
"""


END = """# =========================================================
# TABLEAU DE BORD D'ACCORD ENSEIGNANT - EMIDAF
# =========================================================
"""


start = text.find(
    START
)

end = text.find(
    END
)


if start < 0:

    print(
        "[INFO] Ancienne section VALIDATION ENSEIGNANT "
        "déjà retirée."
    )

else:

    if end < 0:

        raise RuntimeError(
            "Fin du bloc validation introuvable."
        )

    text = (
        text[:start]
        + END
        + text[
            end + len(
                END
            ):
        ]
    )

    print(
        "[OK] Ancienne section validation retirée."
    )


# ---------------------------------------------------------
# Le dashboard ne doit analyser que les validations complètes
# ---------------------------------------------------------

ANCHOR = """    latest_values = list(
        latest.values()
    )

    # -----------------------------------------------------
    # Statistiques de validation déclarée
"""


REPLACEMENT = """    latest_values = list(
        latest.values()
    )

    # Seules les validations finalisées participent
    # aux indicateurs d'accord humain-machine.
    latest_values = [
        value
        for value in latest_values
        if (
            getattr(
                value,
                "validation_status",
                "completed",
            )
            or "completed"
        ) == "completed"
    ]

    if not latest_values:

        return dbc.Alert(
            (
                "Des jugements indépendants peuvent déjà "
                "être verrouillés, mais aucune validation "
                "finalisée n'est encore disponible pour "
                "calculer l'accord humain-machine."
            ),
            color="secondary",
        )

    # -----------------------------------------------------
    # Statistiques de validation déclarée
"""


if ANCHOR in text:

    text = text.replace(
        ANCHOR,
        REPLACEMENT,
        1,
    )

    print(
        "[OK] Filtre validation_status=completed ajouté."
    )

elif (
    "Seules les validations finalisées participent"
    in text
):

    print(
        "[INFO] Filtre dashboard déjà présent."
    )

else:

    raise RuntimeError(
        "Ancre du dashboard d'accord introuvable."
    )


PATH.write_text(
    text,
    encoding="utf-8",
)


print(
    "[OK] callbacks.py patché."
)
