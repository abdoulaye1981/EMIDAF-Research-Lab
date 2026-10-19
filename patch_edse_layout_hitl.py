from pathlib import Path


PATH = Path(
    "emidaf_studio/pages/edse/layout.py"
)

text = PATH.read_text(
    encoding="utf-8"
)


IMPORT = (
    "from emidaf_studio.pages.edse."
    "teacher_validation_components "
    "import teacher_validation_tab\n"
)


if IMPORT not in text:

    anchor = (
        "from emidaf_studio.services."
        "model_registry import get_eaie_run\n"
    )

    if anchor not in text:
        raise RuntimeError(
            "Import get_eaie_run introuvable."
        )

    text = text.replace(
        anchor,
        anchor + "\n" + IMPORT,
        1,
    )


label = 'label="Validation enseignant"'

label_position = text.find(
    label
)

if label_position < 0:
    raise RuntimeError(
        "Onglet Validation enseignant introuvable."
    )


start = text.rfind(
    "                            dbc.Tab(",
    0,
    label_position,
)

if start < 0:
    raise RuntimeError(
        "Début dbc.Tab introuvable."
    )


tab_id = (
    'tab_id="edse-tab-validation",'
)

tab_position = text.find(
    tab_id,
    label_position,
)

if tab_position < 0:
    raise RuntimeError(
        "tab_id validation introuvable."
    )


end_marker = (
    "                            ),"
)

end = text.find(
    end_marker,
    tab_position,
)

if end < 0:
    raise RuntimeError(
        "Fin de l'onglet introuvable."
    )

end += len(
    end_marker
)


replacement = (
    "                            "
    "teacher_validation_tab(),"
)


text = (
    text[:start]
    + replacement
    + text[end:]
)


PATH.write_text(
    text,
    encoding="utf-8",
)


print(
    "[OK] layout.py patché."
)
